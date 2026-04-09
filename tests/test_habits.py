"""Test case for the /habits endpoint."""
import logging
# pylint: disable=too-few-public-methods
import random
from pyats import aetest

from utils.api_client import APIClient
from utils.data_loader import load_test_data

log: logging.Logger = logging.getLogger(__name__)

class TestHabits(aetest.Testcase):
    """Test case for the /habits endpoint."""

    def __init__(self, *args, **kwargs):
        """Initialize test data variable."""
        super().__init__(*args, **kwargs)
        self.test_data = None

    @aetest.setup
    def load_data(self, testbed):
        """Load test data for DDT."""
        path = testbed.custom.get("test_data_file")
        self.test_data = load_test_data(path)

    @aetest.test
    def get_habits(self, testbed):
        """Test the GET /habits endpoint."""
        token = self.parent.parameters.get("access_token")
        base_url = testbed.custom.get("sut_url")

        headers = {"Authorization": f"Bearer {token}"}

        response = APIClient.get(
            f"{base_url}/habits",
            headers=headers,
            testbed=testbed
        )

        assert response.status_code == 200


    @aetest.test.loop(data=lambda self: self.test_data["habits_tests"])
    def assign_habit_ddt(self, data, testbed):
        """Test assigning a habit using DDT."""
        base_url = testbed.custom.get("sut_url")
        token = self.parent.parameters.get("access_token")

        headers = {"Authorization": f"Bearer {token}"}

        if data["mode"] == "random":

            response = APIClient.get(
                f"{base_url}/habit",
                headers=headers,
                testbed=testbed
            )

            assert response.status_code == 200

            habits = response.json()
            assert habits, "No habits available"

            habit_id = random.choice(habits).get("id")

        else:
            habit_id = data["habit_id"]

        assert habit_id is not None, "Habit ID is missing"

        log.info("Using habit_id= %s", habit_id)

        assign_response = APIClient.post(
            f"{base_url}/habit/assign/{habit_id}",
            headers=headers,
            testbed=testbed
        )

        assert assign_response.status_code == 201, \
            f"Assign failed: {assign_response.status_code}"

        active_response = APIClient.get(
            f"{base_url}/habit/assigned",
            headers=headers,
            testbed=testbed
        )

        active_ids = [h.get("id") for h in active_response.json()]

        assert habit_id in active_ids, \
            f"Habit {habit_id} not in active list"


    @aetest.test.loop(data=lambda self: self.test_data["habits_tests"])
    def habit_lifecycle_ddt(self, steps, data, testbed):  # pylint: disable=too-many-return-statements
        """Test the full lifecycle of a habit using DDT."""
        if "update_payload" not in data:
            self.skipped(f"Skipping {data['name']} (no lifecycle config)")
            return

        base_url = testbed.custom.get("sut_url")
        token = self.parent.parameters.get("access_token")

        headers = {"Authorization": f"Bearer {token}"}
        habit_id = None

        # CREATE
        with steps.start(f"{data['name']} → Create", continue_=True) as step:

            response = APIClient.get(
                f"{base_url}/habit",
                headers=headers,
                testbed=testbed
            )

            if response.status_code != 200:
                step.failed("Failed to fetch habits")
                return

            habits = response.json()
            if not habits:
                step.failed("No habits available")
                return

            habit_id = random.choice(habits).get("id")

            assign_response = APIClient.post(
                f"{base_url}/habit/assign/{habit_id}",
                headers=headers,
                testbed=testbed
            )

            if assign_response.status_code != 201:
                step.failed("Assign failed")
                return

            step.passed(f"Created habit {habit_id}")

        if step.failed:
            self.skipped("Skipping rest due to create failure")
            return

        # READ
        with steps.start(f"{data['name']} → Read", continue_=True) as step:

            response = APIClient.get(
                f"{base_url}/habit/{habit_id}",
                headers=headers,
                testbed=testbed
            )

            if response.status_code != 200:
                step.failed("Read failed")
                return

            step.passed()

        # UPDATE
        with steps.start(f"{data['name']} → Update", continue_=True) as step:

            response = APIClient.put(
                f"{base_url}/habit/{habit_id}",
                json=data["update_payload"],
                headers=headers,
                testbed=testbed
            )

            if response.status_code not in (200, 204):
                step.failed("Update failed")
                return

            step.passed()

        # DELETE
        with steps.start(f"{data['name']} → Delete", continue_=True) as step:

            response = APIClient.delete(
                f"{base_url}/habit/assign/{habit_id}",
                headers=headers,
                testbed=testbed
            )

            if response.status_code not in (200, 204):
                step.failed("Delete failed")
                return

            step.passed()

        # VERIFY
        with steps.start(f"{data['name']} → Verify", continue_=True) as step:

            response = APIClient.get(
                f"{base_url}/habit/assigned",
                headers=headers,
                testbed=testbed
            )

            active_ids = [h.get("id") for h in response.json()]

            if habit_id in active_ids:
                step.failed("Still present after delete")
                return

            step.passed("Lifecycle complete")
