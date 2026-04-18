from pyats import aetest
from utils.api_client import APIClient
from utils.auth_helper import AuthHelper
from utils.config import Config


class CommonSetup(aetest.CommonSetup):

    @aetest.subsection
    def authenticate(self):
        auth_data = AuthHelper.login()
        self.parent.parameters["access_token"] = auth_data["accessToken"]


class HabitsCrudTests(aetest.Testcase):

    @aetest.test
    def verify_habit_crud_lifecycle(self, steps):
        client = APIClient()
        access_token = self.parent.parameters["access_token"]

        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        habit_id = None

        with steps.start("Create: assign new habit"):

            response = client.get(
                f"{Config.BASE_URL}/habit/assign/allForCurrentUser",
                headers=headers
            )

            assert response.status_code == 200

            data = response.json()

            if isinstance(data, list):
                active_list = data
            else:
                active_list = data.get("content", [])

            # delete one existing habit to free space
            if active_list:
                first_id = (
                    active_list[0].get("habit", {}).get("id")
                    or active_list[0].get("habitId")
                    or active_list[0].get("id")
                )

                client.delete(
                    f"{Config.BASE_URL}/habit/assign/{first_id}",
                    headers=headers
                )

            active_ids = set()

            for item in active_list:
                found_id = (
                    item.get("habit", {}).get("id")
                    or item.get("habitId")
                    or item.get("id")
                )
                if found_id:
                    active_ids.add(found_id)

            habit_id = None

            for i in range(1, 50):
                if i not in active_ids:
                    habit_id = i
                    break

            assert habit_id is not None, "No available habit id"

            response = client.post(
                f"{Config.BASE_URL}/habit/assign/{habit_id}",
                headers=headers
            )

            if response.status_code in [200, 201]:
                pass  # все ок, продовжуємо
            else:
                assert response.status_code == 400, f"Unexpected error: {response.text}"
                return

        with steps.start("Read"):
            response = client.get(
                f"{Config.BASE_URL}/habit/assign/{habit_id}/active",
                headers=headers,
                params={"lang": "en"}
            )
            assert response.status_code == 200, f"Read failed: {response.text}"

        with steps.start("Update"):
            response = client.patch(
                f"{Config.BASE_URL}/habit/assign/{habit_id}",
                headers=headers,
                json={"status": "INPROGRESS"}
            )
            assert response.status_code in [200, 204], f"Update failed: {response.text}"

        with steps.start("Delete"):
            response = client.delete(
                f"{Config.BASE_URL}/habit/assign/{habit_id}",
                headers=headers
            )
            assert response.status_code in [200, 204], f"Delete failed: {response.text}"

        with steps.start("Verify delete"):
            response = client.get(
                f"{Config.BASE_URL}/habit/assign/{habit_id}/active",
                headers=headers,
                params={"lang": "en"}
            )
            assert response.status_code in [404, 400], f"Verify delete failed: {response.text}"