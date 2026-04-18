import random

from pyats import aetest

from utils.api_client import APIClient
from utils.auth_helper import AuthHelper
from utils.config import Config


class CommonSetup(aetest.CommonSetup):

    @aetest.subsection
    def authenticate(self):
        auth_data = AuthHelper.login()
        self.parent.parameters["access_token"] = auth_data["accessToken"]


class HabitsTests(aetest.Testcase):

    @aetest.test
    def verify_dynamic_habit_subscription(self):
        client = APIClient()
        access_token = self.parent.parameters["access_token"]

        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        # 1. Get active habits first to understand current state
        active_response = client.get(
            f"{Config.BASE_URL}/habit/assign/allForCurrentUser",
            headers=headers
        )

        assert active_response.status_code == 200, (
            f"Expected 200 for /habit/assign/allForCurrentUser, "
            f"got {active_response.status_code}. "
            f"Response: {active_response.text}"
        )

        active_data = active_response.json()

        if isinstance(active_data, list):
            active_list = active_data
        else:
            active_list = active_data.get("content", [])

        active_ids = set()

        for item in active_list:
            found_id = (
                item.get("habit", {}).get("id")
                or item.get("habitId")
                or item.get("id")
            )
            if found_id is not None:
                active_ids.add(found_id)

        # If user already has max active habits, this task cannot produce 201
        assert len(active_ids) < 6, (
            f"User already has {len(active_ids)} active habits. "
            f"Subscription test cannot satisfy expected 201 until one habit is removed."
        )

        # 2. Get tags
        tags_response = client.get(
            f"{Config.BASE_URL}/habit/tags",
            headers=headers
        )

        assert tags_response.status_code == 200, (
            f"Expected 200 for /habit/tags, got {tags_response.status_code}. "
            f"Response: {tags_response.text}"
        )

        tags_data = tags_response.json()
        tags = tags_data if isinstance(tags_data, list) else []
        assert tags, "No tags returned from /habit/tags"

        random.shuffle(tags)

        selected_habits = []

        # 3. Search available habits dynamically by tags
        for tag in tags:
            tag_value = tag.get("name") if isinstance(tag, dict) else tag

            search_response = client.get(
                f"{Config.BASE_URL}/habit/search",
                headers=headers,
                params={
                    "lang": "en",
                    "page": 0,
                    "size": 20,
                    "tags": tag_value
                }
            )

            assert search_response.status_code == 200, (
                f"Expected 200 for /habit/search, got {search_response.status_code}. "
                f"Response: {search_response.text}"
            )

            search_data = search_response.json()
            habits = search_data.get("page", []) if isinstance(search_data, dict) else []

            for habit in habits:
                current_habit_id = habit.get("id")
                if current_habit_id and current_habit_id not in active_ids:
                    selected_habits.append(current_habit_id)

            if selected_habits:
                break

        assert selected_habits, "No available habits found for subscription"

        # 4. Randomly select habitId
        habit_id = random.choice(selected_habits)

        # 5. Subscribe
        subscribe_response = client.post(
            f"{Config.BASE_URL}/habit/assign/{habit_id}",
            headers=headers
        )

        assert subscribe_response.status_code == 201, (
            f"Expected 201 for /habit/assign/{habit_id}, "
            f"got {subscribe_response.status_code}. "
            f"Response: {subscribe_response.text}"
        )

        # 6. Verify habit is in active list
        verify_response = client.get(
            f"{Config.BASE_URL}/habit/assign/allForCurrentUser",
            headers=headers
        )

        assert verify_response.status_code == 200, (
            f"Expected 200 for verification, got {verify_response.status_code}. "
            f"Response: {verify_response.text}"
        )

        verify_data = verify_response.json()

        if isinstance(verify_data, list):
            verify_list = verify_data
        else:
            verify_list = verify_data.get("content", [])

        verify_ids = set()

        for item in verify_list:
            found_id = (
                item.get("habit", {}).get("id")
                or item.get("habitId")
                or item.get("id")
            )
            if found_id is not None:
                verify_ids.add(found_id)

        assert habit_id in verify_ids, (
            f"Habit with id {habit_id} was not found in active list after subscription"
        )