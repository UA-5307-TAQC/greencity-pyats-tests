import time
import requests
import logging
from pyats import aetest

from utils.shared_setup import BaseCommonSetup

log = logging.getLogger(__name__)

class CommonSetup(BaseCommonSetup):

    @aetest.subsection
    def check_sut_reachability(self):
        log.info(f"Checking that the SUT is reachable")

        endpoint = "/swagger-ui/index.html#/"
        client = self.parent.parameters.get('api_client')

        try:
            start_time = time.time()
            response = client.request(
                method="GET",
                endpoint=endpoint
            )
            latency = (time.time() - start_time) * 1000

            log.info(f"SUT responded in {latency:.2f} ms")

            if response.status_code != 200:
                log.error(f"SUT health check failed! Status code: {response.status_code}")
                self.failed(
                    f"SUT returned {response.status_code}. Execution stopped.",
                    goto=['exit']
                )
                return

            log.info(f"SUT is reachable and healthy")

        except requests.exceptions.RequestException as e:
            log.error(f"Connection to SUT failed: {str(e)}")
            self.failed(
                reason="SUT is not reachable (connection error)",
                goto=['exit']
            )
