from pyats import aetest
from utils.api_client import APIClient
from utils.config import Config
from utils.logger import get_logger


class EnvironmentHealthCheck(aetest.Testcase):
    logger = get_logger("EnvironmentHealthCheck")

    @aetest.test
    def verify_swagger_is_available(self):
        client = APIClient()
        url = f"{Config.BASE_URL}/swagger-ui/index.html#/"

        response = client.get(url)

        self.logger.info("Status code: %s", response.status_code)
        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}"
        )

    @aetest.test
    def verify_response_time_is_acceptable(self):
        client = APIClient()
        url = f"{Config.BASE_URL}/swagger-ui/index.html#/"

        response = client.get(url)
        response_time = response.elapsed.total_seconds()

        self.logger.info("Response time: %.2f sec", response_time)
        assert response_time < 5, (
            f"Response time is too high: {response_time} sec"
        )