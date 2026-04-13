"""Configuration module to load environment variables."""

import os
from pathlib import Path

from dotenv import load_dotenv

ENV_PATH = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)


class Config: # pylint: disable=too-few-public-methods
    """Configuration class to hold environment variables."""

    BROWSER_LANG = os.getenv("BROWSER_LANG", "uk-UA")
    USER_EMAIL = os.getenv("USER_EMAIL")
    USER_PASSWORD = os.getenv("USER_PASSWORD")
