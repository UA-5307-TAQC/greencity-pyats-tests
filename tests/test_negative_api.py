import logging
from pyats import aetest

from utils.shared_setup import AuthorizationSetup

log = logging.getLogger(__name__)

class CommonSetup(AuthorizationSetup):
    pass


class NegativeAPITests(aetest.Testcase):

    @aetest.setup
    def setup(self):
        log.info("Preparing test data for negative API tests")
        self.client = self.parent.parameters.get('api_client')
        self.authorized_client = self.parent.parameters.get('authorized_client')


    @aetest.test
    def test_empty_json_body(self):
        log.info("Sending empty JSON body")

        response = self.client.request(
            method="POST",
            endpoint="/ownSecurity/signIn",
            json={}
        )

        if response.status_code != 400:
            self.failed(f"Expected 400 but got {response.status_code}")

        error_msg = response.json().get('message', '').lower()
        if not error_msg:
             self.failed("Response body missing error message")
        if "empty" not in error_msg:
            self.failed(f"API didn't identify empty body")


    @aetest.test
    def test_invalid_email_format(self):
        log.info("Sending an invalid email format")

        payload = {
            "email": "user_at_domain.com",
            "password": "Abc123!@#",
            "projectName": "GREENCITY"
        }
        response = self.client.request(
            method="POST",
            endpoint="/ownSecurity/signIn",
            json=payload
        )

        if response.status_code != 400:
            self.failed(f"Expected 400 but got {response.status_code}")

        error_msg = response.json().get('message', '').lower()
        if not error_msg:
             self.failed("Response body missing error message")
        if "email" not in error_msg:
            self.failed("API didn't identify invalid email format")


    @aetest.test
    def test_out_of_range_id(self):
        log.info("Sending out-of-range value for habitId")
        
        out_of_range_id = -1
        response = self.authorized_client.request(
            method="POST",
            endpoint=f"/habit/assign/{out_of_range_id}"
        )

        if response.status_code != 400:
            self.failed(f"Expected 400 but got {response.status_code}")

        error_msg = response.json().get('message', '').lower()
        if not error_msg:
             self.failed("Response body missing error message")

        keywords = ["range", "limit"]
        if not any(word in error_msg for word in keywords):
            self.failed("API didn't identify out-of-range ID")
