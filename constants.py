import os

from dotenv import load_dotenv
load_dotenv() 

MAX_DELAY: int = int(os.getenv('MAX_DELAY', 0))
MIN_DELAY: int = int(os.getenv('MIN_DELAY', 0))
RETRYABLE_COUNT: int = int(os.getenv('RETRYABLE_COUNT', 0))
PORT: int = int(os.getenv("PORT", 5000))
BYPASSING_BOT_API_KEY = os.getenv('BYPASSING_BOT_API_KEY', "")

ELEMENT_PATHS = {
    "heart": [
        "//article/div/section[2]/button[2]",
        "//div[@id='main-content-video_detail']/div/div[2]/div/div/div/div[5]/div[2]/button"
    ],
    "favorite": [
        "//article/div/section[2]/div[4]",
        "//div[@id='main-content-video_detail']/div/div[2]/div/div/div/div[5]/div[2]/div[3]/button"
    ]
}
