from pyats import aetest
from utils.api_client import APIClient
from utils.config import Config
from utils.logger import get_logger


class NegativeTests(aetest.Testcase):
    logger = get_logger("NegativeTests")

    @staticmethod
    def assert_descriptive_error(response):
        assert response.text.strip(), "Response body is empty"

        response_text = response.text.lower()

        keywords = ["error", "message", "invalid", "bad request"]

        assert any(keyword in response_text for keyword in keywords), (
            f"Response does not contain a descriptive error message. "
            f"Response body: {response.text}"
        )

    # ✅ 1. Empty JSON body
    @aetest.test
    def empty_json_body_signin(self):
        client = APIClient()
        url = f"{Config.USER_API_URL}/ownSecurity/signIn"

        response = client.post(url, json={})

        assert response.status_code == 400, (
            f"Expected 400, got {response.status_code}. "
            f"{response.text}"
        )

        self.assert_descriptive_error(response)

    # ✅ 2. Invalid email format
    @aetest.test
    def invalid_email_format(self):
        client = APIClient()
        url = f"{Config.USER_API_URL}/ownSecurity/signIn"

        payload = {
            "email": "user_at_domain.com",  # ❌ невалідний email
            "password": "12345678",
            "projectName": "GREENCITY"
        }

        response = client.post(url, json=payload)

        assert response.status_code == 400, (
            f"Expected 400, got {response.status_code}. "
            f"{response.text}"
        )

        self.assert_descriptive_error(response)

    # ✅ 3. Invalid signup data
    @aetest.test
    def invalid_signup_data(self):
        client = APIClient()
        url = f"{Config.USER_API_URL}/ownSecurity/signUp"

        payload = {
            "email": "invalid_email",
            "password": "123",
            "name": ""
        }

        response = client.post(url, json=payload)

        assert response.status_code == 400, (
            f"Expected 400, got {response.status_code}. {response.text}"
        )

        self.assert_descriptive_error(response)