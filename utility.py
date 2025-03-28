from time import sleep
from datetime import datetime
import random

from constants import MAX_DELAY, MIN_DELAY

def update_status(msg: str):
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")

    print(str(current_time) + " - " + str(msg))
    
def get_random_sec():
    randomTime = random.randint(MIN_DELAY, MAX_DELAY)
    return randomTime
    
def sleep_like_human(sec: int = get_random_sec()):
    update_status(f"delay for {sec} seconds")
    sleep(sec)
    