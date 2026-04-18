from pyats import aetest
from utils.api_client import APIClient
from utils.auth_helper import AuthHelper
from utils.config import Config


class CommonSetup(aetest.CommonSetup):

    @aetest.subsection
    def authenticate(self):
        auth_data = AuthHelper.login()
        self.parent.parameters["access_token"] = auth_data["accessToken"]


class ProfileTests(aetest.Testcase):

    @aetest.test
    def verify_user_profile_schema_and_business_logic(self):
        client = APIClient()

        access_token = self.parent.parameters["access_token"]

        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        user_response = client.get(
            f"{Config.USER_API_URL}/user/findByEmail",
            headers=headers,
            params={"email": Config.USER_EMAIL}
        )

        assert user_response.status_code == 200, (
            f"Failed to get user info: {user_response.text}"
        )

        user_data = user_response.json()
        user_id = user_data.get("id")

        assert user_id is not None, "userId not found"

        response = client.get(
            f"{Config.USER_API_URL}/user/{user_id}/profile",
            headers=headers
        )

        assert response.status_code in [200, 403], (
            f"Unexpected status code: {response.status_code}"
        )

        if response.status_code == 200:
            data = response.json()

            # schema
            assert isinstance(data.get("userId"), int)
            assert isinstance(data.get("email"), str)

            # business logic
            assert data.get("name") is not None
            assert data.get("name").strip() != ""

            assert data.get("rating") is not None

        elif response.status_code == 403:
            assert "Forbidden" in response.text