from pyats import aetest
import yaml

from utils.api_client import APIClient
from utils.auth_helper import AuthHelper
from utils.config import Config
from utils.logger import get_logger


def load_test_data():
    with open("config/test_data.yaml", "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


test_data = load_test_data()
habit_search_cases = test_data["habit_search_cases"]


class CommonSetup(aetest.CommonSetup):

    @aetest.subsection
    def authenticate(self):
        auth_data = AuthHelper.login()
        self.parent.parameters["access_token"] = auth_data["accessToken"]


@aetest.loop(case=habit_search_cases)
class HabitSearchDDTTests(aetest.Testcase):
    logger = get_logger("HabitSearchDDTTests")

    @aetest.test
    def verify_habit_search_with_multiple_datasets(self, case):
        client = APIClient()
        access_token = self.parent.parameters["access_token"]

        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        response = client.get(
            f"{Config.BASE_URL}/habit/search",
            headers=headers,
            params={
                "lang": case["lang"],
                "page": case["page"],
                "size": case["size"],
                "tags": case["tags"]
            }
        )

        assert response.status_code == 200, (
            f"Case '{case['name']}': expected 200, got {response.status_code}. "
            f"Response: {response.text}"
        )

        response_json = response.json()

        assert isinstance(response_json, dict), (
            f"Case '{case['name']}': response is not a dictionary"
        )

        assert "page" in response_json, (
            f"Case '{case['name']}': key 'page' was not found in response"
        )

        assert isinstance(response_json["page"], list), (
            f"Case '{case['name']}': 'page' is not a list"
        )