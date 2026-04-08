import logging
import requests
from pyats import aetest

from tests.base_test import BaseSetup, BaseCleanup

log = logging.getLogger(__name__)

class CommonSetup(BaseSetup):
    pass

# TESTCASE: Role-Based Access Control (RBAC) Testing (403 Forbidden)
class TestRoleBasedAccessControl(aetest.Testcase):

    @aetest.test
    def test_admin_user_management_access(self):
        log.info("Task 8.1: Attempting to access Admin User Management endpoint...")
        
        # Управління користувачами живе на User API
        user_url = self.parent.parameters['user_api_url']
        headers = self.parent.parameters['headers']
        
        endpoint = f"{user_url}/management/users"
        log.info(f"Sending GET request to {endpoint} with standard user token...")
        
        res = requests.get(endpoint, headers=headers, timeout=10)
        
        if res.status_code != 403:
            self.failed(f"Security Alert! Expected 403 Forbidden, but got {res.status_code}. Response: {res.text}")
            
        log.info("Successfully rejected with 403 Forbidden. Regular user cannot view all users.")

    @aetest.test
    def test_admin_econews_management_access(self):
        log.info("Task 8.2: Attempting to access Admin Eco-News Management endpoint...")
        
        main_url = self.parent.parameters['main_api_url']
        headers = self.parent.parameters['headers']
        
        endpoint = f"{main_url}/management/eco-news/1"
        log.info(f"Sending DELETE request to {endpoint} with standard user token...")
        
        res = requests.delete(endpoint, headers=headers, timeout=10)
        
        if res.status_code != 403:
            self.failed(f"Security Alert! Expected 403 Forbidden, but got {res.status_code}. Response: {res.text}")
            
        log.info("Successfully rejected with 403 Forbidden. Regular user cannot delete eco-news.")

class CommonCleanup(BaseCleanup):
    pass

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    aetest.main()