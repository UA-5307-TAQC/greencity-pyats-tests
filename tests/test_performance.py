"""Test case for performance and stability of the /habit/assigned endpoint."""
import logging
import time
from pyats import aetest
from utils.api_client import APIClient

log: logging.Logger = logging.getLogger(__name__)
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-locals
class TestPerformance(aetest.Testcase):
    """Test case for performance and stability of the /habit/assigned endpoint."""
    @aetest.test
    def test_habits_stability(self, testbed):
        """Test the stability and performance of the /habit/assigned endpoint."""
        base_url = testbed.custom.get("sut_url")
        token = self.parent.parameters.get("access_token")

        headers = {
            "Authorization": f"Bearer {token}"
        }

        iterations = 20
        max_latency_ms = 500

        latencies = []
        failures = []

        for i in range(iterations):

            start_time = time.time()

            response = APIClient.get(
                f"{base_url}/habit/assigned",
                headers=headers,
                testbed=testbed
            )

            elapsed_ms = (time.time() - start_time) * 1000
            latencies.append(elapsed_ms)

            log.info(
                "Request %s: status=%s, time=%.2fms",
                i + 1,
                response.status_code,
                elapsed_ms
            )



            if response.status_code != 200:
                failures.append(f"Iteration {i+1}: {response.status_code}")


            if elapsed_ms > max_latency_ms:
                failures.append(
                    f"Iteration {i+1}: slow response {elapsed_ms:.2f}ms"
                )

        success_rate = (
            (iterations - len(failures)) / iterations * 100
        )

        avg_latency = sum(latencies) / len(latencies)
        max_latency = max(latencies)

        log.info("Success rate: %.2f%%", success_rate)
        log.info("Average latency: %.2fms", avg_latency)
        log.info("Max latency: %.2fms", max_latency)

        assert success_rate == 100, \
            f"Flaky endpoint detected: {failures}"

        assert max_latency < max_latency_ms, \
            f"Latency spike detected: max={max_latency:.2f}ms"
