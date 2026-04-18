from pyats import aetest
from utils.api_client import APIClient
from utils.config import Config
from utils.logger import get_logger


class AuthenticationIntegrityTests(aetest.Testcase):
    logger = get_logger("AuthenticationIntegrityTests")

    @staticmethod
    def assert_unauthorized_message(response):
        assert response.text.strip(), "Response body is empty"

        response_text = response.text.lower()
        keywords = ["unauthorized", "invalid", "token", "forbidden", "error"]

        assert any(keyword in response_text for keyword in keywords), (
            f"Response does not contain an auth-related error message. "
            f"Response body: {response.text}"
        )

    @aetest.test
    def verify_private_endpoint_denies_missing_and_invalid_token(self, steps):
        client = APIClient()
        url = f"{Config.BASE_URL}/user"

        scenarios = [
            {
                "name": "missing_token",
                "headers": None
            },
            {
                "name": "invalid_token",
                "headers": {
                    "Authorization": "Bearer invalid_token_123"
                }
            }
        ]

        for scenario in scenarios:
            with steps.start(f"Verify {scenario['name']} returns 401", continue_=True):
                response = client.get(url, headers=scenario["headers"])

                assert response.status_code == 401, (
                    f"Scenario '{scenario['name']}': expected 401, "
                    f"got {response.status_code}. Response body: {response.text}"
                )

                self.assert_unauthorized_message(response)