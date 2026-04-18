from utils.api_client import APIClient
from utils.config import Config


class AuthHelper:
    @staticmethod
    def login():
        client = APIClient()

        payload = {
            "email": Config.USER_EMAIL,
            "password": Config.USER_PASSWORD,
            "projectName": "GREENCITY"
        }

        response = client.post(
            f"{Config.USER_API_URL}/ownSecurity/signIn",
            json=payload
        )

        assert response.status_code == 200, (
            f"Login failed. Expected 200, got {response.status_code}. "
            f"Response body: {response.text}"
        )

        response_json = response.json()

        assert response_json.get("accessToken"), "accessToken was not found in login response"
        assert response_json.get("userId") is not None, "userId was not found in login response"

        return response_json