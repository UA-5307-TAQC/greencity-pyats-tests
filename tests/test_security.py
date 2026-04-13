import logging
from pyats import aetest

from utils.api_client import APIClient
from utils.shared_setup import AuthorizationSetup

log = logging.getLogger(__name__)

SCENARIOS = [
    {
        "name": "missing_token",
        "token": None,
    },
    {
        "name": "invalid_token",
        "token": "invalid_token_123"
    }
]

class CommonSetup(AuthorizationSetup):
    pass


class SecurityAccessTest(aetest.Testcase):

    @aetest.setup
    def setup(self):
        log.info("Preparing test data for user profile unauthorized access")
        self.user_id = self.parent.parameters.get('user_id')
        self.base_url = self.parent.parameters.get('base_url')

    @aetest.test.loop(scenario=SCENARIOS)
    def verify_unauthorized_access(self, scenario):
        log.info(f"Testing scenario: {scenario['name']}")

        access_token = scenario['token']
        client = APIClient(self.base_url, access_token)

        response = client.request(
            method="POST",
            endpoint=f"/user/{self.user_id}/profile"
        )

        if response.status_code != 401:
            self.failed(
                f"Vulnerability! /user/{self.user_id}/profile returned {response.status_code} "
                f"with {scenario['name']} credentials."
            )
