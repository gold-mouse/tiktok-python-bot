import os

from dotenv import load_dotenv
load_dotenv() 

MAX_DELAY: int = int(os.getenv('MAX_DELAY', 0))
MIN_DELAY: int = int(os.getenv('MIN_DELAY', 0))
RETRYABLE_COUNT: int = int(os.getenv('RETRYABLE_COUNT', 0))
PORT: int = int(os.getenv("PORT", 5000))
BYPASSING_BOT_API_KEY = os.getenv('BYPASSING_BOT_API_KEY', "")

ELEMENT_CSS = {
    "heart": [
        "#main-content-video_detail > div > div:nth-child(2) > div > div > div > div:nth-child(5) > div:nth-child(2) > button",
        "article > div > section:nth-child(2) > button:nth-child(2)"
    ],
    "favorite": [
        "#main-content-video_detail > div > div:nth-child(2) > div > div > div > div:nth-child(5) > div:nth-child(2) > div:nth-child(3) > button",
        "article > div > section:nth-child(2) > div:nth-child(4)",
    ],
    "comment-input-field": [
        "div.DraftEditor-editorContainer > div.notranslate.public-DraftEditor-content[aria-describedby^='placeholder']",
    ],
    "open-comment": [
        "#comments > button"
    ],
    "post-button": [
        "div[data-e2e='comment-post']"
    ]
}
