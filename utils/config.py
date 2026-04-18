import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BASE_URL = os.getenv("BASE_URL", "https://greencity.greencity.cx.ua")
    USER_API_URL = os.getenv("USER_API_URL", "https://greencity-user.greencity.cx.ua")
    USER_EMAIL = os.getenv("USER_EMAIL", "")
    USER_PASSWORD = os.getenv("USER_PASSWORD", "")
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "15"))
