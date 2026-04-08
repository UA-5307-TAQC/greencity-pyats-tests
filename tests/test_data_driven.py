import logging
import requests
import yaml
import os
from pyats import aetest

from tests.base_test import BaseSetup, BaseCleanup

log = logging.getLogger(__name__)


config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'test_data.yaml')
with open(config_path, 'r') as file:
    dataset = yaml.safe_load(file)

habit_scenarios = dataset.get('habit_scenarios', {})

class CommonSetup(BaseSetup):
    pass


class TestDataDrivenHabits(aetest.Testcase):

    @aetest.test.loop(scenario_name=habit_scenarios.keys())
    def test_habit_endpoints_from_yaml(self, scenario_name):
        data = habit_scenarios[scenario_name]
        habit_id = data['habit_id']
        expected_status = data['expected_status']
        
        log.info(f"Task 9: Running Data-Driven Test -> {scenario_name}")
        log.info(f"Checking Habit ID: {habit_id} | Expecting Status: {expected_status}")
        
        main_url = self.parent.parameters['main_api_url']
        headers = self.parent.parameters['headers']
        endpoint = f"{main_url}/habit/{habit_id}"
        
        res = requests.get(endpoint, headers=headers, timeout=10)
        
        if res.status_code != expected_status:
            self.failed(f"Expected {expected_status}, but got {res.status_code}. Response: {res.text}")
            
        log.info(f"Success! Received exactly what we expected: {expected_status}")

class CommonCleanup(BaseCleanup):
    pass

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    aetest.main()