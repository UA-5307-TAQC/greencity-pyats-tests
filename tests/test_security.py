from pyats import aetest
from utils.api_client import APIClient
from utils.config import Config
from utils.logger import get_logger


class SecurityTests(aetest.Testcase):
    logger = get_logger("SecurityTests")

    @aetest.test
    def access_endpoint_with_invalid_token(self):
        client = APIClient()
        url = f"{Config.BASE_URL}/management/info"
        headers = {
            "Authorization": "Bearer invalid_token_123"
        }

        response = client.get(url, headers=headers)

        assert response.status_code in [401, 403], (
            f"Expected 401 or 403, got {response.status_code}"
        )