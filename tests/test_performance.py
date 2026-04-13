import time
import logging
from pyats import aetest

from utils.shared_setup import AuthorizationSetup

log = logging.getLogger(__name__)

class CommonSetup(AuthorizationSetup):
    pass


class TestHabits(aetest.Testcase):

    @aetest.setup
    def setup(self):
        log.info("Preparing data for GET /habit/assign/allForCurrentUser requests")

        self.client = self.parent.parameters.get('authorized_client')
        self.iterations = 20
        self.latency_threshold = 0.5
        self.time_results = []


    @aetest.test
    def test_endpoint_stability(self):
        success_count = 0

        for i in range(1, self.iterations + 1):
            log.info(f"Iteration {i}")

            start_time = time.time()
            response = self.client.request(
                method="POST",
                endpoint=f"/habit/assign/{self.habit_id}"
            )
            end_time = time.time()

            duration = end_time - start_time
            self.time_results.append(duration)

            if response.status_code == 200:
                success_count += 1
            else:
                log.error(f"Iteration {i} failed with status: {response.status_code}")

            if duration > self.latency_threshold:
                log.warning(f"Iteration {i} exceeded latency: {duration:.4f}s")

        if success_count < self.iterations:
            self.failed(f"Flakiness detected. Success rate: {(success_count/self.iterations)*100}%")

        slow_responses = [r for r in self.time_results if r > self.latency_threshold]
        if slow_responses:
            self.failed(f"Performance issue: {len(slow_responses)} requests exceeded 500ms.")
