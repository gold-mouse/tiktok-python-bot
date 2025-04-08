from tiktok_captcha_solver import SeleniumSolver # type: ignore
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth # type: ignore

import os
from time import sleep
import random

from selenium.webdriver.common.by import By
from typing import Dict, Any, List

from model import driver_model
from utility import sleep_like_human, update_status

from constants import RETRYABLE_COUNT, BYPASSING_BOT_API_KEY, ELEMENT_PATHS

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

    sleep_like_human(3, 5)

def navigate(driver: Any, link: str) -> Any:
    driver.get(link)
    sleep_like_human()
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    bypass_robot(driver)
    return driver

def refresh(driver: Any) -> None:
    driver.refresh()
    sleep_like_human(3, 5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    bypass_robot(driver)

def human_type(element: Any, text: str, delay_range: tuple[float, float]=(0.05, 0.2)):
    for char in text:
        element.send_keys(char)
        sleep(random.uniform(*delay_range))

def wait_and_get_element(driver: Any, selectorStr: str, retry: int = RETRYABLE_COUNT, by: str = By.XPATH) -> Any:
    def click_el(selector: str):
        for i in range(retry): # type: ignore
            try:
                update_status("Getting Element...")
                return WebDriverWait(driver, 20).until(EC.presence_of_element_located((by, selector)))
            except Exception as e: # type: ignore
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

def wait_and_click(driver: Any, selectorStr: str | List[str], retry: int = RETRYABLE_COUNT, by: str = By.XPATH) -> bool:
    def click_el(selector: str) -> bool:
        for i in range(retry): # type: ignore
            try:
                update_status("Getting Element...")
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((by, selector))).click()
                sleep_like_human()
                return True
            except Exception as e: # type: ignore
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

def wait_and_send_keys(driver: Any, selectorStr: str, keys: str, retry: int = RETRYABLE_COUNT, by: str = By.XPATH) -> bool:
    def click_el(selector: str):
        for i in range(retry): # type: ignore
            try:
                update_status("Getting Element...")
                element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((by, selector)))
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                human_type(element, keys)
                sleep_like_human()
                return True
            except Exception as e: # type: ignore
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
            languages=["en-US", "en"],           # Mimic browser language preferences
            vendor="Google Inc.",               # Set vendor string
            platform="Win64",                   # Define OS platform
            webgl_vendor="Intel Inc.",          # Mask WebGL vendor details
            renderer="Intel Iris OpenGL Engine",  # Mask WebGL renderer details
            fix_hairline=True                   # Prevent detection via hairline rendering
        )
        
        return driver
    except Exception as e:
        print(e)
        return None

def login(username: str, password: str) -> Dict[str, Any] | None:
    driver = driver_model.get_driver(username)
    
    if driver == None:
        return None
    
    driver = navigate(driver, "https://www.tiktok.com/login/phone-or-email/email")
    
    wait_and_send_keys(driver=driver, selectorStr="//form//input[@name='username']", keys=username, retry=1)
    wait_and_send_keys(driver=driver, selectorStr="//form//input[@type='password']", keys=password, retry=1)

    sleep_like_human()

    wait_and_click(driver=driver, selectorStr="//form//button[@type='submit']", retry=1)

    driver_model.set_driver(username, driver)

    return { "status": True, "message": "success" }

def search(username: str, keyword: str) -> Dict[str, Any] | None:
    driver = driver_model.get_driver(username)

    if driver == None:
        print(username, keyword)
        return None

    driver = navigate(driver, f"https://www.tiktok.com/explore?lang=en&q={keyword}")

    searched_links = driver.find_elements(By.XPATH, "//div[@data-e2e='explore-item']//a")
    searched_imgs = driver.find_elements(By.XPATH, "//div[@data-e2e='explore-item']//img")

    searched_videos: List[Dict[str, Any]] = [] # type: ignore

    for i in range(len(searched_links)):
        searched_videos.append({
            "link": searched_links[i].get_attribute("href"),
            "img": searched_imgs[i].get_attribute("src"),
            "id": i
        })
    return { "status": True, "message": "success", "data": searched_videos }

def follow(username: str, link: str) -> Dict[str, Any] | None:
    driver = driver_model.get_driver(username)

    if driver == None:
        return None

    driver = navigate(driver=driver, link=link)

    videoEl = wait_and_get_element(driver=driver, selectorStr="//video")

    if (videoEl == None):
        return { "status": False, "message": "Video not found" }

    driver.execute_script("arguments[0].pause()", videoEl)

    res = wait_and_click(driver=driver, selectorStr=ELEMENT_PATHS.get("heart", []))

    if res == False:
        return { "status": False, "message": "Failed to follow video" }

    return { "status": True, "message": "success" }

def favorite(username: str, link: str) -> Dict[str, Any] | None:
    driver = driver_model.get_driver(username)

    if driver == None:
        return None

    driver = navigate(driver=driver, link=link)

    res = wait_and_click(driver=driver, selectorStr=ELEMENT_PATHS.get("favorite", []))

    if res == False:
        return { "status": False, "message": "Failed to favorite video" }

    return { "status": True, "message": "success" }

def leaveComment(username: str, link: str, comment: str = "Wonderful, I like it") -> Dict[str, Any] | None:
    driver = driver_model.get_driver(username)

    if driver == None:
        return None

    driver = navigate(driver=driver, link=link)

    sleep_like_human()

    wait_and_click(driver=driver, selectorStr="//div[@id='comments']")
    wait_and_click(driver=driver, selectorStr="//button[@id='comments']")
    wait_and_send_keys(driver=driver, selectorStr="//div[@class='DraftEditor-editorContainer']/div[@class='notranslate public-DraftEditor-content' and starts-with(@aria-describedby, 'placeholder')]", keys=comment)

    sleep_like_human(3)

    wait_and_click(driver=driver, selectorStr="//div[@data-e2e='comment-post']")

    return { "status": True, "message": "success" }
