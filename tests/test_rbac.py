from pyats import aetest
from utils.api_client import APIClient
from utils.auth_helper import AuthHelper
from utils.config import Config
from utils.logger import get_logger


class RBACTests(aetest.Testcase):
    logger = get_logger("RBACTests")

    @staticmethod
    def assert_forbidden_message(response):
        assert response.text.strip(), "Response body is empty"

        response_text = response.text.lower()
        keywords = ["forbidden", "access", "denied", "error"]

        assert any(keyword in response_text for keyword in keywords), (
            f"Response does not contain a descriptive forbidden message. "
            f"Response body: {response.text}"
        )

    @aetest.test
    def standard_user_cannot_access_admin_endpoint(self):
        client = APIClient()

        auth_data = AuthHelper.login()
        access_token = auth_data["accessToken"]

        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        url = f"{Config.USER_API_URL}/user/search"

        payload = {
            "id": "1",
            "name": "test",
            "email": "test@test.com",
            "role": "ROLE_USER",
            "userStatus": "CREATED"
        }

        response = client.post(url, headers=headers, json=payload)

        assert response.status_code == 403, (
            f"Expected 403, got {response.status_code}. "
            f"Response body: {response.text}"
        )

        self.assert_forbidden_message(response)