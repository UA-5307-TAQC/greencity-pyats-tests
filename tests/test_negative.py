import logging
import requests
from pyats import aetest

from tests.base_test import BaseSetup, BaseCleanup

log = logging.getLogger(__name__)

class CommonSetup(BaseSetup):
    pass

# TESTCASE: Negative Testing (Error Handling)
class TestErrorHandling(aetest.Testcase):

    @aetest.test
    def test_empty_json_body(self):
        log.info("Task 6.1: Sending empty JSON body {} to POST endpoint...")
        user_url = self.parent.parameters['user_api_url']
        
        endpoint = f"{user_url}/ownSecurity/signIn"
        log.info(f"Sending POST request to {endpoint} with empty payload {{}}")
        
        res = requests.post(endpoint, json={}, timeout=10)
        
        # Перевіряємо статус 400
        if res.status_code != 400:
            self.failed(f"Expected 400 Bad Request, got {res.status_code}")
            
        error_data = res.json()
        log.info(f"Received Error Response: {error_data}")
        
        if not error_data:
            self.failed("Error body is empty! API did not provide a descriptive message.")
            
        self.passed("Handled empty JSON body gracefully with a descriptive error.")

    @aetest.test
    def test_invalid_email_format(self):
        log.info("Task 6.2: Submitting an invalid email format...")
        user_url = self.parent.parameters['user_api_url']
        
        endpoint = f"{user_url}/ownSecurity/signIn"
        invalid_payload = {
            "email": "user_at_domain.com",
            "password": "SomeValidPassword123!"
        }
        
        res = requests.post(endpoint, json=invalid_payload, timeout=10)
        
        if res.status_code != 400:
            self.failed(f"Expected 400 Bad Request, got {res.status_code}")
            
        error_data = res.json()
        log.info(f"Received Error Response: {error_data}")
        
        if not error_data:
            self.failed("API did not provide a descriptive message for invalid email.")
            
        self.passed("Handled invalid email format gracefully.")

    @aetest.test
    def test_out_of_range_id(self):
        log.info("Task 6.3: Passing out-of-range values for IDs...")
        main_url = self.parent.parameters['main_api_url']
        headers = self.parent.parameters['headers']
        
        invalid_id = -1
        endpoint = f"{main_url}/habit/assign/{invalid_id}"
        
        log.info(f"Sending POST request to {endpoint} (expecting validation error)")
        res = requests.post(endpoint, headers=headers, timeout=10)
        

        if res.status_code not in [400, 404]:
            log.warning(f"Raw server response: {res.text}")
            self.failed(f"Expected 400 Bad Request, but got {res.status_code}")
            
        error_data = res.json()
        log.info(f"Received Error Response: {error_data}")
        
        if not error_data:
            self.failed("API did not provide a descriptive message for out-of-range ID.")
            
        self.passed("Handled out-of-range ID gracefully.")

class CommonCleanup(BaseCleanup):
    pass

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    aetest.main()