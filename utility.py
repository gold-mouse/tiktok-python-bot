from halo import Halo # type: ignore
from time import sleep
from datetime import datetime
import random

from constants import MAX_DELAY, MIN_DELAY

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
    
    return True
