import os

from dotenv import load_dotenv
load_dotenv() 

MAX_DELAY: int = int(os.getenv('MAX_DELAY', 0))
MIN_DELAY: int = int(os.getenv('MIN_DELAY', 0))
RETRYABLE_COUNT: int = int(os.getenv('RETRYABLE_COUNT', 0))
PORT: int = int(os.getenv("PORT", 5000))
