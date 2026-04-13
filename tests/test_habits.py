import random
import logging
from pyats import aetest

from utils.shared_setup import AuthorizationSetup

log = logging.getLogger(__name__)

class CommonSetup(AuthorizationSetup):
    pass


class TestHabits(aetest.Testcase):

    @aetest.setup
    def get_available_habits(self):
        log.info("Sending GET /habits request")

        client = self.parent.parameters.get('api_client')
        payload = {
            "page": 0,
            "size": 20
        }
        response = client.request(
            method="GET",
            endpoint="/habits",
            json=payload
        )

        if response.status_code != 200:
            self.failed(f"Expected 200 but got {response.status_code}")

        data = response.json()
        if isinstance(data, list):
            habits = data
        elif isinstance(data, dict):
            habits = data.get('content')

        if not habits or not isinstance(habits, list):
            self.failed(f"Could not find a list of habits in response: {data}")

        self.habit_id = random.choice(habits).get('id')

        if not self.habit_id:
            self.failed("Selected habit object missing habit ID")


    @aetest.test
    def validate_habit_state_machine(self, steps):
        client = self.parent.parameters.get('authorized_client')
        self.habit_assign_id = None

        with steps.start("1. Create: Assign a new habit") as step:
            log.info("Sending POST /habit/assign/habitID request")

            assign_response = client.request(
                method="POST",
                endpoint=f"/habit/assign/{self.habit_id}"
            )

            if assign_response.status_code != 201:
                step.failed(f"Expected 201 but got {assign_response.status_code}")


        with steps.start("2. Check the habit appears in the user's active list") as step:
            log.info("Sending GET /habit/assign/allForCurrentUser request")

            all_assign_response = client.request(
                method="GET",
                endpoint="/habit/assign/allForCurrentUser"
            )
            if all_assign_response.status_code != 200:
                step.failed(f"Expected 200 but got {all_assign_response.status_code}")

            data = all_assign_response.json()
            for habit in data:
                original_id = habit['habit']['id']
                if original_id == self.habit_id:
                    self.habit_assign_id = habit.get('id')
                    break

            if not self.habit_assign_id:
                step.failed("Selected habit object missing assigned habit ID")


        with steps.start("3. Read: Retrieve details of the assigned habit by ID") as step:
            log.info("Sending GET /habit/assign/habitAssignId request")

            one_assign_response = client.request(
                method="GET",
                endpoint=f"/habit/assign/{self.habit_assign_id}"
            )

            if one_assign_response.status_code != 200:
                step.failed(f"Expected 200 but got {one_assign_response.status_code}")


        with steps.start("4. Update: Update the status or frequency of the habit") as step:
            log.info("Sending PATCH /habit/assign/habitAssignId request")

            payload = {
                "habitAssignStatus": "EXPIRED"
            }
            update_assign_response = client.request(
                method="PATCH",
                endpoint=f"/habit/assign/{self.habit_assign_id}",
                json=payload
            )

            if update_assign_response.status_code not in [200, 204]:
                step.failed(f"Expected 200/204 but got {update_assign_response.status_code}")


        with steps.start("5. Delete: Unassign/Delete the habit") as step:
            log.info("Sending DELETE /habit/assign/delete/habitAssignId request")
            
            delete_assign_response = client.request(
                method="DELETE",
                endpoint=f"/habit/assign/delete/{self.habit_assign_id}",
            )
            if delete_assign_response.status_code not in [200, 204]:
                step.failed(f"Expected 200/204 but got {delete_assign_response.status_code}")
