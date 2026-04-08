import logging
import requests
from pyats import aetest

from tests.base_test import BaseSetup, BaseCleanup

log = logging.getLogger(__name__)

class CommonSetup(BaseSetup):
    pass

# TESTCASE: Unauthorized Access Testing (401)
class TestUnauthorizedAccess(aetest.Testcase):

    SCENARIOS = {
        'missing_token': {
            'auth_header': None,
            'desc': 'No Authorization header at all'
        },
        'invalid_token': {
            'auth_header': 'Bearer invalid_and_fake_jwt_token_12345',
            'desc': 'Malformed or expired JWT token'
        }
    }

    @aetest.test.loop(scenario_name=SCENARIOS.keys())
    def test_401_unauthorized(self, scenario_name):
        test_data = self.SCENARIOS[scenario_name]
        log.info(f"Task 7: Testing scenario -> {test_data['desc']}")
        
        user_url = self.parent.parameters['user_api_url']
        endpoint = f"{user_url}/user"
        
        headers = {"Content-Type": "application/json"}
        if test_data['auth_header']:
            headers["Authorization"] = test_data['auth_header']
            
        log.info(f"Sending GET request to {endpoint} with headers: {headers}")
        res = requests.get(endpoint, headers=headers, timeout=10)
        
        if res.status_code != 401:
            self.failed(f"Security Alert! Expected 401 Unauthorized, but got {res.status_code}. Response: {res.text}")
            
        log.info(f"Successfully rejected with 401. Server response: {res.text}")
        self.passed(f"Scenario '{scenario_name}' handled securely.")

class CommonCleanup(BaseCleanup):
    pass

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    aetest.main()