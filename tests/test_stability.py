import time

from pyats import aetest

from utils.api_client import APIClient
from utils.auth_helper import AuthHelper
from utils.config import Config
from utils.logger import get_logger


class CommonSetup(aetest.CommonSetup):

    @aetest.subsection
    def authenticate(self):
        auth_data = AuthHelper.login()
        self.parent.parameters["access_token"] = auth_data["accessToken"]


class StabilityTests(aetest.Testcase):
    logger = get_logger("StabilityTests")

    @aetest.test
    def verify_endpoint_stability_and_latency(self, steps):
        client = APIClient()
        access_token = self.parent.parameters["access_token"]

        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        url = f"{Config.BASE_URL}/habit/assign/allForCurrentUser"
        durations = []

        for attempt in range(1, 21):
            with steps.start(f"Request #{attempt}", continue_=True):
                start_time = time.perf_counter()
                response = client.get(url, headers=headers)
                duration_ms = (time.perf_counter() - start_time) * 1000

                durations.append(duration_ms)

                self.logger.info(
                    "Attempt %s: status=%s, response_time=%.2f ms",
                    attempt,
                    response.status_code,
                    duration_ms
                )

                assert response.status_code == 200, (
                    f"Attempt #{attempt}: expected 200, got {response.status_code}. "
                    f"Response: {response.text}"
                )

                assert duration_ms < 500, (
                    f"Attempt #{attempt}: response time is too high: "
                    f"{duration_ms:.2f} ms"
                )

        average_ms = sum(durations) / len(durations)
        max_ms = max(durations)
        min_ms = min(durations)

        self.logger.info("Average response time: %.2f ms", average_ms)
        self.logger.info("Min response time: %.2f ms", min_ms)
        self.logger.info("Max response time: %.2f ms", max_ms)