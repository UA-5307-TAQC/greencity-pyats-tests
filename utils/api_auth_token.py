"""get auth token"""
import logging
import requests

from data.config import Config

log = logging.getLogger(__name__)


def get_auth_token(base_url=Config.BASE_API_URL_LOGIN):
    """get auth token"""
    log.info("Attempting to authenticate and fetch access token...")

    email = Config.USER_EMAIL
    password = Config.USER_PASSWORD

    if not email or not password:
        raise ValueError(
            "Security Error: Credentials not found! Please set GREENCITY_EMAIL "
            "and GREENCITY_PASSWORD environment variables.")

    login_url = f"{base_url}/ownSecurity/signIn"

    payload = {
        "email": email,
        "password": password,
        "projectName": "GREENCITY"
    }

    try:
        response = requests.post(login_url, json=payload, timeout=10)
        response.raise_for_status()

        response_data = response.json()

        access_token = response_data.get('accessToken')
        user_id = response_data.get('userId')

        if not access_token:
            raise KeyError("Validation Error: 'accessToken' not found in the response payload.")

        log.info("Successfully extracted accessToken and userId: %s", user_id)
        return {"token": access_token, "user_id": user_id}

    except requests.exceptions.RequestException as e:
        log.error("Failed to authenticate. Error: %s", e)
        raise
