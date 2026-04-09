"""API client for handling authentication and API requests."""
import logging
from multiprocessing import AuthenticationError

import requests

from data.config import Config

log: logging.Logger = logging.getLogger(__name__)
# pylint: disable=too-few-public-methods
class APIClient:
    """API client for handling authentication and API requests."""

    DEFAULT_TIMEOUT = 5

    @staticmethod
    def authenticate(base_url = Config.BASE_USER_API_URL,
                     email = Config.USER_EMAIL ,
                     password = Config.USER_PASSWORD,
                     logger = log,
                     testbed=None):
        """
        Perform login and return access token
        """

        if not email or not password:
            if testbed:
                email = testbed.custom.get("email")
                password = testbed.custom.get("password")

        if not email or not password:
            raise ValueError("Missing credentials (env or testbed)")

        url = f"{base_url}/ownSecurity/signIn"

        payload = {
            "email": email,
            "password": password,
            "projectName" : "GREENCITY"
        }

        logger.info("Authenticating user...")

        response = requests.post(url, json=payload, timeout=5)

        if response.status_code != 200:
            raise RuntimeError(
                f"Auth failed: {response.status_code} - {response.text}"
            )

        data = response.json()

        access_token = data.get("accessToken")

        if not access_token:
            raise RuntimeError("No accessToken in response")

        logger.info("Authentication successful")

        return access_token

    @staticmethod
    def authenticate_user(base_url, credentials):
        """Authenticate with provided credentials and return access token."""
        url = f"{base_url}/ownSecurity/signIn"

        response = requests.post(
            url,
            json=credentials,
            timeout=5
        )

        if response.status_code != 200:
            raise AuthenticationError(
                f"Auth failed: {response.status_code}"
            )

        token = response.json().get("accessToken")

        if not token:
            raise AuthenticationError("Missing accessToken")

        return token

    @staticmethod
    def get(url, testbed=None, **kwargs):
        """Make a GET request with optional timeout from testbed."""
        timeout = 5

        if testbed:
            timeout = testbed.custom.get("request_timeout", 5)

        return requests.get(url, timeout=timeout, **kwargs)

    @staticmethod
    def post(url, testbed=None, **kwargs):
        """Make a POST request with optional timeout from testbed."""
        timeout = 5

        if testbed:
            timeout = testbed.custom.get("request_timeout", 5)

        return requests.post(url, timeout=timeout, **kwargs)

    @staticmethod
    def put(url, **kwargs):
        """Make a PUT request with default timeout."""
        return requests.put(url, timeout=5, **kwargs)

    @staticmethod
    def delete(url, **kwargs):
        """Make a DELETE request with default timeout."""
        return requests.delete(url, timeout=5, **kwargs)
