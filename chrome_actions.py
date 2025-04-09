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
from typing import Dict, Any, List

from model import driver_model
from utility import sleep_like_human, update_status

from constants import RETRYABLE_COUNT, BYPASSING_BOT_API_KEY, ELEMENT_CSS

def bypass_robot(driver: Any):
    update_status("Solving Captcha if present...")
    sadcaptcha = SeleniumSolver( # type: ignore
        driver,
        BYPASSING_BOT_API_KEY,
        mouse_step_size=1, # Adjust to change mouse speed
        mouse_step_delay_ms=10 # Adjust to change mouse speed
    )

    # Selenium code that causes a TikTok or Douyin captcha...

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
    start_time = time()  # Record the start time
    
    while True:
        driver.execute_script(f"window.scrollBy(0, {scroll_increment});") # type: ignore
        
        # Wait for the scroll to finish
        sleep(random.uniform(*(0.1, 0.3)))

        # Check how much time has passed
        elapsed_time = time() - start_time
        
        # Stop scrolling after the specified duration
        if elapsed_time >= duration:
            break

    spinner.stop() # type: ignore
    update_status("Scrolling finished!")

def human_typing(element: Any, text: str, delay_range: tuple[float, float]=(0.05, 0.2)):
    for char in text:
        element.send_keys(char)
        sleep(random.uniform(*delay_range))

def wait_and_get_element(driver: Any, selectorStr: str, by: str, logStr: str, retry: int = RETRYABLE_COUNT) -> Any:
    update_status(logStr)
    def click_el(selector: str):
        for i in range(retry): # type: ignore
            try:
                update_status("Getting Element...")
                return WebDriverWait(driver, 10).until(EC.presence_of_element_located((by, selector)))
            except Exception as e: # type: ignore
                print(e)
                if retry == 1:
                    return None
                update_status("retrying...")
                refresh(driver)
        return None
    
    if isinstance(selectorStr, list):
        for sel in selectorStr:
            if click_el(sel):
                return True
        return False
    else:
        return click_el(selectorStr)

def wait_and_click(driver: Any, selectorStr: str | List[str], by: str, logStr: str, retry: int = RETRYABLE_COUNT) -> bool:
    update_status(logStr)
    def click_el(selector: str) -> bool:
        for i in range(retry): # type: ignore
            try:
                update_status("Getting Element...")
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((by, selector))).click()
                sleep_like_human()
                return True
            except Exception as e: # type: ignore
                print(selector)
                print(e)
                if retry == 1:
                    return False
                update_status("retrying...")
                refresh(driver)

        return False
    
    if isinstance(selectorStr, list):
        for sel in selectorStr:
            if click_el(sel):
                return True
        return False
    else:
        return click_el(selectorStr)

def wait_and_send_keys(driver: Any, selectorStr: str | List[str], by: str, logStr: str, keys: str, retry: int = RETRYABLE_COUNT) -> bool:
    update_status(logStr)
    def click_el(selector: str):
        for i in range(retry): # type: ignore
            try:
                update_status("Getting Element...")
                element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((by, selector)))
                human_typing(element, keys)
                sleep_like_human()
                return True
            except Exception as e: # type: ignore
                print(e)
                if retry == 1:
                    return False
                update_status("retrying...")
                refresh(driver)
            
        return False
    
    if isinstance(selectorStr, list):
        for sel in selectorStr:
            if click_el(sel):
                return True
        return False
    else:
        return click_el(selectorStr)

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

    driver_model.set_driver(username, driver)

    return { "status": True, "message": "success" }

def search(username: str, keyword: str) -> Dict[str, Any] | None:
    driver = driver_model.get_driver(username)

    if driver == None:
        print(username, keyword)
        return { "status": False, "message": "Can't find profile settings (Open chrome first)" }

    driver = navigate(driver, f"https://www.tiktok.com/search?q={keyword}")

    smooth_scroll_for_duration(driver)

# "#tabs-0-panel-search_top div[mode='search-video-list'] > div"
    searched_links = driver.find_elements(By.CSS_SELECTOR, "#tabs-0-panel-search_top div[mode='search-video-list'] > div > div:nth-child(1) > div > div a")
    searched_imgs = driver.find_elements(By.CSS_SELECTOR, "#tabs-0-panel-search_top div[mode='search-video-list'] > div > div:nth-child(1) > div > div img")

    searched_videos: List[Dict[str, Any]] = [] # type: ignore

    for i in range(len(searched_links)):
        src = searched_imgs[i].get_attribute("src")
        if src.startswith("data:"):
            continue
        searched_videos.append({
            "link": searched_links[i].get_attribute("href"),
            "img": src,
            "id": i
        })
    return { "status": True, "message": "success", "data": searched_videos }

def main_action(username: str, link: str) -> Dict[str, Any] | None:
    driver = driver_model.get_driver(username)

    if driver == None:
        return { "status": False, "message": "Can't find profile settings (Open chrome first)"}

    driver = navigate(driver=driver, link=link)

    videoEl = wait_and_get_element(driver=driver, selectorStr="video", by=By.CSS_SELECTOR, logStr="Getting video element...")

    if (videoEl == None):
        return { "status": False, "message": "Video not found" }

    driver.execute_script("arguments[0].pause()", videoEl) # once video is finished, necessary elements are disappeared. so it must be paused first

    heart_res = wait_and_click(driver=driver, selectorStr=ELEMENT_CSS.get("heart", []), logStr="Clicking heart...", by=By.CSS_SELECTOR)

    favorite_res = wait_and_click(driver=driver, selectorStr=ELEMENT_CSS.get("favorite", []), logStr="Clicking favorite...", by=By.CSS_SELECTOR)

    comment_res = leaveComment(driver=driver)

    return { "status": heart_res and favorite_res and comment_res, "message": f"Heart: {heart_res}, Favorite: {favorite_res}, Comment: {comment_res}" }

def leaveComment(driver: str, comment: str = "Wonderful, I like it") -> bool:

    wait_and_click(driver=driver, selectorStr=ELEMENT_CSS.get("open-comment", []), logStr="Opening comments...", by=By.CSS_SELECTOR, retry=1)
    sendKey_res = wait_and_send_keys(
        driver=driver,
        selectorStr=ELEMENT_CSS.get("comment-input-field", []),
        keys=comment, logStr="Sending comment...",
        by=By.CSS_SELECTOR,
        retry=1
    )

    sleep_like_human()

    if not sendKey_res:
        print("Failed to send comment")
        return False
    
    postComment = wait_and_click(driver=driver, selectorStr=ELEMENT_CSS.get("post-button", []), logStr="Posting comment...", by=By.CSS_SELECTOR, retry=1)

    if not postComment:
        print("Failed to post comment")
        return False

    return True
