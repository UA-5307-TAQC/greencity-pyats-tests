"""Common setup for all tests, including SUT availability and latency check."""
import time
import logging
from pyats import aetest
import requests

from data.config import Config
from utils.api_client import APIClient

log: logging.Logger = logging.getLogger(__name__)

#pylint: disable=too-few-public-methods
class CommonSetup(aetest.CommonSetup):
    """Common setup for all test cases in the suite."""

    @aetest.subsection
    def check_sut(self, testbed):
        """Check if the SUT is reachable and measure latency."""
        sut = testbed.devices['sut']
        protocol = sut.connections.rest.protocol
        host = sut.connections.rest.host


        endpoint = f"{protocol}://{host}/swagger-ui/index.html#/"

        try:
            start = time.time()
            response = requests.get(endpoint, timeout=5)
            latency = time.time() - start

            log.info("Latency: %.2f ms", latency)

            if response.status_code != 200:
                log.error("Unexpected status code: %s", response.status_code)
                self.failed(reason=f"SUT returned {response.status_code}")
                return

            log.info("Returned status code: %s", response.status_code)

        except requests.exceptions.RequestException as e:
            log.error("SUT unreachable: %s", e)
            self.failed("SUT unreachable")
            return

        log.info("SUT is reachable")

    @aetest.subsection
    def setup_environment(self):
        """Setup environment for all tests"""
        data_about_user = APIClient.authenticate()

        self.parent.parameters['api_url'] = \
            f"{Config.BASE_USER_API_URL}/user/{data_about_user['user_id']}/profile/"

        self.parent.parameters['access_token'] = data_about_user['token']
