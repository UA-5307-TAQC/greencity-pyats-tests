"""implement """
import os

class Config: # pylint: disable=too-few-public-methods
    """Configuration class to hold environment variables."""
    USER_EMAIL = os.getenv("USER_EMAIL")
    USER_PASSWORD = os.getenv("USER_PASSWORD")
    BASE_API_URL_LOGIN = os.getenv("BASE_API_URL_LOGIN")
