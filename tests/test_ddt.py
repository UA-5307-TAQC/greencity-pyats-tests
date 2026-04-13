import logging
from yaml import safe_load
from pyats import aetest

from utils.shared_setup import BaseCommonSetup

log = logging.getLogger(__name__)

class CommonSetup(BaseCommonSetup):

    @aetest.subsection
    def load_data(self):
        log.info("Preparing test data for habit tests")

        with open('config/test_data.yaml', 'r') as f:
            data = safe_load(f)
        habits = data.get('habit_data', [])

        aetest.loop.mark(
            DataDrivenTestcase.test_get_habit,
            habit_data=habits,
            ids=[item['name'] for item in habits]
        )


class DataDrivenTestcase(aetest.Testcase):

    @aetest.setup
    def setup(self):
        log.info("Preparing client for GET habit/habitId requests")
        self.client = self.parent.parameters.get('api_client')



    @aetest.test
    def test_get_habit(self, habit_data):
        log.info(f"Sending GET habit/habitId request with {habit_data}")

        habit_id = habit_data['habit_id']
        expected_status = habit_data['status_code']
        response = self.client.request(
            method="GET",
            endpoint=f"/habit/{habit_id}"
        )

        if response.status_code != expected_status:
            self.failed(f"Expected {expected_status} but got {response.status_code}")
