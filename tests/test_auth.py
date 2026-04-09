"""Authentication tests"""
import logging

from pyats import aetest

from utils.api_client import APIClient
from data.config import Config

log: logging.Logger = logging.getLogger(__name__)

#pylint: disable=too-few-public-methods
class TestAuth(aetest.Testcase):
    """Test case for authentication."""

    @aetest.subsection
    def authenticate(self):
        """Authenticate and store access token globally."""

        try:
            token = APIClient.authenticate(
                base_url=Config.BASE_API_URL,
                email=Config.USER_EMAIL,
                password=Config.USER_PASSWORD,
                logger=log
            )

            self.parent.parameters["access_token"] = token

            log.info("Access token stored globally")

        except RuntimeError as e:
            log.error("Authentication failed: %s", e)
            self.parent.terminate(reason="Auth failed")
