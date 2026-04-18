from pyats import aetest
from utils.api_client import APIClient
from utils.config import Config
from utils.logger import get_logger
from utils.schema_validator import validate_schema
from schemas.auth_schema import AUTH_RESPONSE_SCHEMA
from pyats import aetest
from utils.auth_helper import AuthHelper


class AuthTests(aetest.Testcase):
    logger = get_logger("AuthTests")

    @aetest.test
    def login_with_valid_credentials(self):
        client = APIClient()
        url = f"{Config.USER_API_URL}/ownSecurity/signIn"

        payload = {
            "email": Config.USER_EMAIL,
            "password": Config.USER_PASSWORD,
            "projectName": "GREENCITY"
        }

        response = client.post(url, json=payload)

        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}"
        )

        response_json = response.json()
        validate_schema(response_json, AUTH_RESPONSE_SCHEMA)

    @aetest.test
    def login_with_invalid_password(self):
        client = APIClient()
        url = f"{Config.USER_API_URL}/ownSecurity/signIn"
        payload = {
            "email": Config.USER_EMAIL,
            "password": "wrong_password_123",
            "projectName": "GREENCITY"
        }

        response = client.post(url, json=payload)

        assert response.status_code in [400, 401], (
            f"Expected 400 or 401, got {response.status_code}"
        )

class CommonSetup(aetest.CommonSetup):

    @aetest.subsection
    def authenticate(self):
        auth_data = AuthHelper.login()

        self.parent.parameters["access_token"] = auth_data["accessToken"]
        self.parent.parameters["user_id"] = auth_data["userId"]
