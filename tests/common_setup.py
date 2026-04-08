import time

import requests
from genie.testbed import load
from pyats.aetest import CommonSetup, subsection


class VerifySUT(CommonSetup):

    @subsection
    def check_sut_availability(self, testbed):

        sut = testbed.devices['sut']
        protocol = sut.connections.rest.protocol
        host = sut.connections.rest.host

        url = f"{protocol}://{host}/swagger-ui/index.html#/"
        print(f"url: {url}")
        # self.parent.logger.info(f"Checking SUT availability at URL: {url}")

        self.parameters['sut_url'] = url

        start_time = time.time()
        response = requests.get(url)
        print(f"response: {response}")
        latency = time.time() - start_time

        self.parameters['latency'] = latency


        if response.status_code != 200:
            self.parent.terminate()

        print(f"Successfully completed in {latency} seconds")