import logging
from pyats import aetest
from utils.api_client import get_auth_token

log = logging.getLogger(__name__)

class BaseSetup(aetest.CommonSetup):
    @aetest.subsection
    def setup_api_client(self):
        log.info("GLOBAL SETUP: Authenticating and preparing headers...")
        
        user_api_url = "https://greencity-user.greencity.cx.ua"
        self.parent.parameters['user_api_url'] = user_api_url
        self.parent.parameters['main_api_url'] = "https://greencity.greencity.cx.ua"
        
        try:
            auth_data = get_auth_token(user_api_url)
            self.parent.parameters['user_id'] = auth_data["user_id"]
            self.parent.parameters['headers'] = {
                "Authorization": f"Bearer {auth_data['token']}",
                "Content-Type": "application/json"
            }
            log.info("GLOBAL SETUP: Token and User ID prepared for all tests!")
        except Exception as e:
            self.failed(f"Global Setup failed due to auth error: {e}")

class BaseCleanup(aetest.CommonCleanup):
    @aetest.subsection
    def clean_up(self):
        log.info("GLOBAL CLEANUP: All tests finished.")