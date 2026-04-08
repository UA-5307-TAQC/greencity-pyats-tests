import logging
import requests
import time
from pyats import aetest
from tests.base_test import BaseSetup, BaseCleanup

log = logging.getLogger(__name__)

class CommonSetup(BaseSetup):
    pass


class TestEndpointStability(aetest.Testcase):

    @aetest.test
    def test_latency_and_flakiness(self, steps):
        log.info("Task 10: Identifying 'flaky' endpoints and latency issues...")
        
        main_url = self.parent.parameters['main_api_url']
        headers = self.parent.parameters['headers']
        endpoint = f"{main_url}/habit/assign/allForCurrentUser"
        
        iterations = 20
        max_latency_sec = 0.5
        
        success_count = 0
        latencies = []

        log.info(f"Starting 20 iterations for: {endpoint}")

        for i in range(1, iterations + 1):
            with steps.start(f"Iteration {i}", continue_=True) as step:
                response = requests.get(endpoint, headers=headers, timeout=10)
                
                if response.status_code != 200:
                    step.failed(f"Stability Error! Iteration {i} failed with status {response.status_code}")
                

                latency = response.elapsed.total_seconds()
                latencies.append(latency)
                
                log.info(f"Iteration {i}: {latency:.3f}s")

                if latency > max_latency_sec:
                    step.failed(f"Latency Issue! Response took {latency:.3f}s (Max allowed: {max_latency_sec}s)")
                
                success_count += 1

        avg_latency = sum(latencies) / len(latencies)
        max_val = max(latencies)
        
        log.info(f"\n--- Performance Summary ---")
        log.info(f"Success Rate: {(success_count/iterations)*100}%")
        log.info(f"Average Latency: {avg_latency:.3f}s")
        log.info(f"Peak Latency: {max_val:.3f}s")
        log.info(f"---------------------------\n")

        if success_count < iterations:
            self.failed(f"Test failed stability check: {success_count}/{iterations} passed.")

class CommonCleanup(BaseCleanup):
    pass

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    aetest.main()