from tiktok_captcha_solver import SeleniumSolver # type: ignore
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth # type: ignore

import os
from time import sleep, time
import random
from halo import Halo # type: ignore

from selenium.webdriver.common.by import By
from typing import Dict, Any, List, Union, Callable

from model import driver_model
from utility import sleep_like_human, update_status

from constants import RETRYABLE_COUNT, BYPASSING_BOT_API_KEY, ELEMENT_CSS

def bypass_robot(driver: Any):
    update_status("Solving Captcha if present...", "info")
    sadcaptcha = SeleniumSolver( # type: ignore
        driver,
        BYPASSING_BOT_API_KEY,
        mouse_step_size=1,
        mouse_step_delay_ms=10
    )

    sadcaptcha.solve_captcha_if_present() # type: ignore

    sleep_like_human(1, 3)

def navigate(driver: Any, link: str) -> Any:
    driver.get(link)
    sleep_like_human(1, 3)
    bypass_robot(driver)
    return driver

def refresh(driver: Any) -> None:
    driver.refresh()
    sleep_like_human(1, 3)
    bypass_robot(driver)

def smooth_scroll_for_duration(driver: uc.Chrome, duration: int = 20, scroll_increment: int = 100):
    
    spinner = Halo(text=f'Scrolling to fetch data for {duration} seconds...', spinner='dots') # type: ignore
    spinner.start() # type: ignore
    start_time = time()
    
    while True:
        driver.execute_script(f"window.scrollBy(0, {scroll_increment});") # type: ignore
        
        sleep(random.uniform(*(0.1, 0.3)))

        elapsed_time = time() - start_time
        
        if elapsed_time >= duration:
            break

    spinner.stop() # type: ignore
    update_status("Scrolling finished!", "info")

def human_typing(element: Any, text: str, delay_range: tuple[float, float]=(0.05, 0.2)):
    for char in text:
        element.send_keys(char)
        sleep(random.uniform(*delay_range))

def retry_action(driver: Any, selectorStr: Union[str, List[str]], by: str, logStr: str, action: Callable[[str], bool], retry: int) -> bool:
    update_status(logStr)
    
    def try_selectors(selectors: List[str]) -> bool:
        for sel in selectors:
            if action(sel):
                return True
        return False

    selectors = selectorStr if isinstance(selectorStr, list) else [selectorStr]

    for i in range(retry): # type: ignore
        if try_selectors(selectors):
            return True
        update_status(f"Failed to process element: {selectorStr}", "error")
        if retry == 1:
            return False
        update_status("retrying...")
        refresh(driver)

    return False

def wait_and_get_element(driver: Any, selectorStr: Union[str, List[str]], by: str, logStr: str, retry: int = RETRYABLE_COUNT, waitTime: int = 10) -> Any:
    def action(selector: str):
        try:
            update_status("Getting Element...")
            return WebDriverWait(driver, waitTime).until(EC.presence_of_element_located((by, selector)))
        except Exception:  # type: ignore
            return None

    result = [None]
    def wrapped_action(sel: str) -> bool:
        res = action(sel)
        if res:
            result[0] = res # type: ignore
            return True
        return False

    return result[0] if retry_action(driver, selectorStr, by, logStr, wrapped_action, retry) else None

def wait_and_click(driver: Any, selectorStr: Union[str, List[str]], by: str, logStr: str, retry: int = RETRYABLE_COUNT, waitTime: int = 10) -> bool:
    def action(selector: str) -> bool:
        try:
            update_status("Getting Element...")
            WebDriverWait(driver, waitTime).until(EC.element_to_be_clickable((by, selector))).click()
            sleep_like_human()
            return True
        except Exception:  # type: ignore
            return False

    return retry_action(driver, selectorStr, by, logStr, action, retry)

def wait_and_send_keys(driver: Any, selectorStr: Union[str, List[str]], by: str, logStr: str, keys: str, retry: int = RETRYABLE_COUNT, waitTime: int = 10) -> bool:
    def action(selector: str) -> bool:
        try:
            update_status("Getting Element...")
            element = WebDriverWait(driver, waitTime).until(EC.element_to_be_clickable((by, selector)))
            human_typing(element, keys)
            sleep_like_human()
            return True
        except Exception:  # type: ignore
            return False

    return retry_action(driver, selectorStr, by, logStr, action, retry)

def launch_driver(profile: str):
    try:
        user_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"chrome_profiles/{profile}")
        options = uc.ChromeOptions()
        options.add_argument("--start-maximized") # type: ignore
        options.add_argument("--disable-blink-features=AutomationControlled") # type: ignore
        driver = uc.Chrome(user_data_dir=user_data_dir, options=options)
        
        stealth(
            driver,
            languages=["en-US", "en"],            # Mimic browser language preferences
            vendor="Google Inc.",                 # Set vendor string
            platform="Win64",                     # Define OS platform
            webgl_vendor="Intel Inc.",            # Mask WebGL vendor details
            renderer="Intel Iris OpenGL Engine",  # Mask WebGL renderer details
            fix_hairline=True                     # Prevent detection via hairline rendering
        )
        
        return driver
    except Exception as e:
        print(e)
        return None

def login(username: str, password: str) -> Dict[str, Any] | None:
    driver = driver_model.get_driver(username)
    
    if driver == None:
        return { "status": False, "message": "Can't find profile settings (Open chrome first)" }
    
    driver = navigate(driver, "https://www.tiktok.com/login/phone-or-email/email")
    
    isLoggedIn = wait_and_get_element(driver=driver, selectorStr="//form//input[@name='username']", by=By.XPATH, logStr="Checking if logged in...", retry=1)

    if isLoggedIn == None:
        return { "status": True, "message": "Already logged in" }
    
    wait_and_send_keys(driver=driver, selectorStr="//form//input[@name='username']", keys=username, retry=1, by=By.XPATH, logStr="Sending username...")
    wait_and_send_keys(driver=driver, selectorStr="//form//input[@type='password']", keys=password, retry=1, by=By.XPATH, logStr="Sending password...")

    wait_and_click(driver=driver, selectorStr="//form//button[@type='submit']", retry=1, by=By.XPATH, logStr="Logging in...")

    sleep(2)
    
    isSuccess = wait_and_get_element(driver=driver, selectorStr="button[role='searchbox']", by=By.CSS_SELECTOR, logStr="Checking if logged in...", waitTime=30, retry=1)

    if isSuccess == None:
        return { "status": False, "message": "Login failed" }
    
    bypass_robot(driver)

    driver_model.set_driver(username, driver)

    return { "status": True, "message": "success" }

def search(username: str, keyword: str, comment: str) -> Dict[str, Any] | None:
    driver = driver_model.get_driver(username)

    if driver == None:
        print(username, keyword)
        return { "status": False, "message": "Can't find profile settings (Open chrome first)" }

    driver = navigate(driver, f"https://www.tiktok.com/search?q={keyword}")

    smooth_scroll_for_duration(driver)

    searched_links = driver.find_elements(By.CSS_SELECTOR, "#tabs-0-panel-search_top div[mode='search-video-list'] > div > div:nth-child(1) > div > div a")
    searched_imgs = driver.find_elements(By.CSS_SELECTOR, "#tabs-0-panel-search_top div[mode='search-video-list'] > div > div:nth-child(1) > div > div img")

    searched_videos: List[Dict[str, Any]] = [] # type: ignore

    for i in range(len(searched_links)):
        src = searched_imgs[i].get_attribute("src")
        href = searched_links[i].get_attribute("href")
        if src.startswith("data:"):
            continue
        searched_videos.append({
            "link": href,
            "img": src,
            "id": i,
        })

    update_status(f"Found {len(searched_videos)} videos")
    update_status("Processing video...")

    if len(searched_videos) > 0:
        searched_videos = searched_videos[:3] # splice first 3 for testing porses
        update_status("Only processing first 3 videos for testing purposes", "info")


    return {
        "status": True,
        "message": "success",
        "data": [
            {
                "id": videoInfo["id"],
                "link": videoInfo["link"],
                "img": videoInfo["img"],
                "result": main_action(username, videoInfo["link"], comment)
            } for videoInfo in searched_videos
        ]
    }

def main_action(username: str, link: str, comment: str) -> Dict[str, Any] | None:

    driver = driver_model.get_driver(username)

    driver.get(link)
    sleep_like_human(2, 4)

    videoEl = None
    for i in range(RETRYABLE_COUNT): # type: ignore
        try:
            videoEl = wait_and_get_element(driver=driver, selectorStr="video", by=By.CSS_SELECTOR, logStr="Getting video element...")
            break
        except Exception as e: # type: ignore
            update_status("Not found video element", "error")
            bypass_robot(driver)

    if (videoEl == None):
        return { "success": False, "message": "Video not found" }

    driver.execute_script("arguments[0].pause()", videoEl) # once video is finished, necessary elements are disappeared. so it must be paused first

    sleep_like_human(2, 4)

    heart_res = wait_and_click(driver=driver, selectorStr=ELEMENT_CSS.get("heart", []), logStr="Clicking heart...", by=By.CSS_SELECTOR)

    favorite_res = wait_and_click(driver=driver, selectorStr=ELEMENT_CSS.get("favorite", []), logStr="Clicking favorite...", by=By.CSS_SELECTOR)

    comment_res = leaveComment(driver=driver, comment=comment)

    update_status("Done", "info")
    update_status(f"Link: {link}")

    sleep_like_human()
    return {
        "success": heart_res and favorite_res and comment_res,
        "data": {
            "heart": heart_res,
            "favorite": favorite_res,
            "comment": comment_res
        }
    }

def leaveComment(driver: str, comment: str = "Wonderful, I like it") -> bool:
    for i in range(2): # check if comment button is opened. If not, open it on second trying
        sendKey_res = wait_and_send_keys(
            driver=driver,
            selectorStr=ELEMENT_CSS.get("comment-input-field", []),
            keys=comment, logStr="Sending comment...",
            by=By.CSS_SELECTOR,
            retry=1
        )
        if not sendKey_res:
            print("Failed to send comment", "error")
            if i == 0:
                wait_and_click(driver=driver, selectorStr=ELEMENT_CSS.get("open-comment", []), logStr="Opening comments...", by=By.CSS_SELECTOR, retry=1)
                continue
            return False
        
        try:
            update_status("Posting comment...")
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-e2e='comment-post']"))) # type: ignore
            driver.execute_script("arguments[0].click();", element) # type: ignore
            return True
        except Exception as e: # type: ignore
            print("Failed to post comment", "error")
            return False

    return True
