"""File to ensure the SUT (System Under Test) is reachable before executing the suite"""

import logging
import requests
from pyats import aetest
from utils.api_client import get_auth_token

log = logging.getLogger(__name__)

# SETUP: Task 1 - Ensure the SUT is reachable
class CommonSetup(aetest.CommonSetup):
    """Class for setup."""
    
    @aetest.subsection
    def check_environment_reachability(self):
        log.info("Task 1: Checking SUT (System Under Test) reachability...")
        
        swagger_url = "https://greencity.greencity.cx.ua/swagger-ui/index.html"
        
        self.parent.parameters['base_url'] = "https://www.greencity.cx.ua/#/greenCity"
        self.parent.parameters['user_api_url'] = "https://greencity-user.greencity.cx.ua"
        
        try:
            log.info(f"Sending GET request (Handshake) to: {swagger_url}")
            response = requests.get(swagger_url, timeout=10)
            
            latency = response.elapsed.total_seconds()
            log.info(f"Response latency: {latency} seconds")
            
            if response.status_code != 200:
                error_msg = f"SUT is unreachable! Received status code: {response.status_code}"
                log.error(error_msg)
                self.parent.terminate(reason=error_msg)
            else:
                log.info("SUT (GreenCity API) is reachable! Ready to start testing.")
                
        except requests.exceptions.RequestException as e:
            error_msg = f"Critical connection error: {e}"
            log.error(error_msg)
            self.parent.terminate(reason=error_msg)


# TESTCASES: Authentication and Token Extraction
class TestAuthentication(aetest.Testcase):
    
    @aetest.test
    def test_login_and_store_token(self):
        """Test to verify secure login flow and global token storage."""
        log.info("Task 2: Executing reusable auth mechanism test.")
        
        user_api_url = self.parent.parameters.get('user_api_url')
        
        try:
            token = get_auth_token(user_api_url)
            
            self.parent.parameters['access_token'] = token
            log.info("Token successfully stored in self.parent.parameters['access_token'] for future TestClasses.")
            
            self.passed("Authentication test passed. System is ready for protected API calls.")
            
        except Exception as e:
            self.failed(f"Authentication test failed due to an error: {e}")


# CLEANUP
class CommonCleanup(aetest.CommonCleanup):
    """Class for cleanup."""
    @aetest.subsection
    def clean_up(self):
        log.info("Cleaning up and finishing script execution.")

# Entry point
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    aetest.main()