from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

from selenium.webdriver.common.by import By
from typing import Dict, Any, List

from driver_model import driver_model
from utility import sleep_like_human, update_status

from constants import RETRYABLE_COUNT

def wait_and_click(driver: Any, xpath: str, retry: int = RETRYABLE_COUNT) -> None:
    for i in range(retry): # type: ignore
        try:
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
            break
        except Exception as e: # type: ignore
            update_status("retrying...")
            sleep_like_human()
            driver.refresh()

def wait_and_send_keys(driver: Any, xpath: str, keys: str, retry: int = RETRYABLE_COUNT) -> None:
    for i in range(retry): # type: ignore
        try:
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, xpath))).send_keys(keys)
            break
        except Exception as e: # type: ignore
            update_status("retrying...")
            sleep_like_human()
            driver.refresh()

def launch_driver(profile: str):
    try:
        options = Options()
        options.add_argument("start-maximized") # type: ignore
        options.add_argument("--log-level=3") # type: ignore
        options.add_experimental_option("useAutomationExtension", False) # type: ignore
        options.add_experimental_option("excludeSwitches", ["enable-automation"]) # type: ignore
        # adding argument to disable the AutomationControlled flag 
        options.add_argument("--disable-blink-features=AutomationControlled") # type: ignore
        # exclude the collection of enable-automation switches 
        options.add_experimental_option("excludeSwitches", ["enable-automation"]) # type: ignore
        # turn-off userAutomationExtension 
        options.add_experimental_option("useAutomationExtension", False) # type: ignore
        options.add_experimental_option("excludeSwitches", ["enable-automation"]) # type: ignore
        options.add_argument(f"user-data-dir=" + os.path.join(os.path.dirname(os.path.abspath(__file__)), f"chrome_profiles/{profile}")) # type: ignore
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options, keep_alive=True)

        # changing the property of the navigator value for webdriver to undefined 
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") # type: ignore

        return driver
    except Exception as e:
        print(e)
        return None

def login(username: str, password: str) -> Dict[str, Any] | None:
    driver = driver_model.get_driver(username)
    
    if driver == None:
        return None
    
    driver.get("https://www.tiktok.com/login/phone-or-email/email")
    
    wait_and_send_keys(driver=driver, xpath="//form//input[@name='username']", keys=username)
    wait_and_send_keys(driver=driver, xpath="//form//input[@type='password']", keys=password)

    sleep_like_human()

    wait_and_click(driver=driver, xpath="//form//button[@type='submit']")

    driver_model.set_driver(username, driver)

    return { "status": True, "message": "success" }

def search(username: str, keyword: str) -> Dict[str, Any] | None:
    driver = driver_model.get_driver(username)

    if driver == None:
        print(username, keyword)
        return None

    driver.get(f"https://www.tiktok.com/explore?lang=en&q={keyword}")

    searched_links = driver.find_elements(By.XPATH, "//div[@data-e2e='explore-item']//a")
    searched_imgs = driver.find_elements(By.XPATH, "//div[@data-e2e='explore-item']//img")

    searched_videos: List[Dict[str, Any]] = [] # type: ignore

    print(len(searched_links), "------>>>shit")
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

    driver.get(link)

    sleep_like_human()

    wait_and_click(driver=driver, xpath="//article/div/section[2]/button[2]")

    return { "status": True, "message": "success" }

def favorite(username: str, link: str) -> Dict[str, Any] | None:
    driver = driver_model.get_driver(username)

    if driver == None:
        return None

    driver.get(link)

    sleep_like_human()

    wait_and_click(driver=driver, xpath="//article/div/section[2]/div[4]")

    return { "status": True, "message": "success" }

def leaveComment(username: str, link: str, comment: str = "Wonderful, I like it") -> Dict[str, Any] | None:
    driver = driver_model.get_driver(username)

    if driver == None:
        return None

    driver.get(link)

    sleep_like_human()

    wait_and_click(driver=driver, xpath="//div[@id='comments']")

    wait_and_click(driver=driver, xpath="//button[@id='comments']")

    wait_and_send_keys(driver=driver, xpath="//div[@class='DraftEditor-editorContainer']/div[@class='notranslate public-DraftEditor-content' and starts-with(@aria-describedby, 'placeholder')]", keys=comment)

    sleep_like_human(3)

    wait_and_click(driver=driver, xpath="//div[@data-e2e='comment-post']")

    return { "status": True, "message": "success" }
