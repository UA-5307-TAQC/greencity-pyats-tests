import logging
import requests
from pyats import aetest
from utils.api_client import get_auth_token
from utils.schema_validator import validate_user_profile

from tests.base_test import BaseSetup, BaseCleanup

log = logging.getLogger(__name__)

# SETUP: Authenticate and prepare headers
class CommonSetup(BaseSetup):
    pass

# TESTCASE: Validate /user/profile API Contract
class TestProfileContract(aetest.Testcase):
    
    @aetest.test
    def test_profile_schema_and_business_logic(self):
        log.info("Task 3: Validating User Profile API Contract...")
        
        user_url = self.parent.parameters['user_api_url']
        headers = self.parent.parameters['headers']
        user_id = self.parent.parameters['user_id']
        
        endpoint_url = f"{user_url}/user/{user_id}/profile/"
        log.info(f"Sending GET request to: {endpoint_url}")
        
        try:
            response = requests.get(endpoint_url, headers=headers, timeout=10)
            
            if response.status_code != 200:
                self.failed(f"Expected 200 OK, got {response.status_code}. Details: {response.text}")
                
            profile_data = response.json()
            log.info(f"Received Profile Data: {profile_data}")
            
            # Requirement 1: Schema Validation (Field types and patterns)
            log.info("Executing Schema Validation...")
            try:
                validate_user_profile(profile_data)
            except Exception as e:
                self.failed(f"Schema Validation Error: {e}")
                
            # Requirement 2: Business Logic (Mandatory fields are not null)
            log.info("Executing Business Logic Validation...")
            name = profile_data.get('name')
            rating = profile_data.get('rating')
            
            if name is None or rating is None:
                self.failed(f"Business Logic Error: 'name' ({name}) or 'rating' ({rating}) must not be null!")
            else:
                log.info(f"Business Logic passed. Name: {name}, Rating: {rating}")
                
            self.passed("API Contract Validation completed successfully!")
            
        except requests.exceptions.RequestException as e:
            self.failed(f"Connection error: {e}")

# CLEANUP
class CommonCleanup(BaseCleanup):
    pass

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    aetest.main()