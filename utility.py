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

# def interceptor(request):

#     # add the missing headers
#     request.headers["Accept-Language"] = "en-US,en;q=0.9"
#     request.headers["Referer"] = "https://www.google.com/"

#     # delete the existing misconfigured default headers values
#     del request.headers["User-Agent"]
#     del request.headers["Sec-Ch-Ua"]
#     del request.headers["Sec-Fetch-Site"]
#     del request.headers["Accept-Encoding"]
#     del request.headers["x-client-data"]
    
#     # replace the deleted headers with edited values
#     request.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
#     request.headers["Sec-Ch-Ua"] = "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Google Chrome\";v=\"122\""
#     request.headers["Sec-Fetch-Site"] = "cross-site"
#     request.headers["Accept-Encoding"] = "gzip, deflate, br, zstd"
