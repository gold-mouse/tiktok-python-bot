import pyautogui
from typing import Any
from halo import Halo # type: ignore
from time import sleep
from datetime import datetime
import random
from pywinauto import Application # type: ignore

from constants import MAX_DELAY, MIN_DELAY
from model import driver_model

def update_status(msg: str):
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")

    print(str(current_time) + " - " + str(msg))
    
def get_random_sec(a: int, b: int):
    if 0 < b < a:
        return random.randint(MIN_DELAY, MAX_DELAY)
    return random.randint(a if a > 0 else MIN_DELAY, b if b > 0 else MAX_DELAY)
    
def sleep_like_human(a: int = 0, b: int = 0):
    sec = get_random_sec(a, b)
    update_status(f"delay for {sec} seconds")
    for remaining in range(sec, 0, -1):
        with Halo(text=f"{remaining} seconds remaining...", spinner="dots"):
            sleep(0.9)
        print("\r", end="") 

def click_element(element: Any, username: str):
    try:

        # bring_chrome_to_front(username)
        location = element.location
        size = element.size

        offset = driver_model.get_browser_offset(username)
        
        # Calculate the center of the element
        x = location['x'] + size['width'] // 2
        y = location['y'] + offset + size['height'] // 2

        update_status(f"The element is located at ({x}, {y})")
        
        pyautogui.moveTo(x, y, duration=0.5)  # Smooth movement
        pyautogui.click()

        return True

    except Exception as e: # type: ignore
        return False
    
def bring_chrome_to_front(username: str):
    """ Bring the correct Chrome window to the front """
    pid = driver_model.get_chrome_pid(username)
    app: Any = Application().connect(process=pid)  # type: ignore
    window = app.top_window()
    window.set_focus()
    sleep(0.5)
    window.bring_to_front()
