"""Test unauthorized access to protected endpoints"""
import logging

from pyats import aetest

from utils.api_client import APIClient
log: logging.Logger = logging.getLogger(__name__)
# pylint: disable=too-few-public-methods
class TestUnauthorizedAccess(aetest.Testcase):
    """Test unauthorized access to protected endpoints"""
    PRIVATE_ENDPOINTS = [
        "/user/profile",
        "/habit/assign/1"
    ]

    SCENARIOS = [
        {
            "name": "missing_token",
            "headers": {}
        },
        {
            "name": "invalid_token",
            "headers": {
                "Authorization": "Bearer invalid_token_123"
            }
        }
    ]

    def _validate_unauthorized(self, response):
        """
        Validate 401 response and error message
        """
        assert response.status_code == 401, \
            f"Expected 401, got {response.status_code}"

        data = response.json()

        message = data.get("message") or data.get("error")

        assert message, "Missing error message"
        assert isinstance(message, str), "Message is not a string"
        assert len(message) > 5, "Message too vague"

        msg_lower = message.lower()

        assert any(word in msg_lower for word in [
            "unauthorized", "invalid", "token", "expired", "missing"
        ]), "Error message is not descriptive"

        log.info("Error message: %s", message)

    @aetest.test
    def verify_unauthorized_access(self,steps, testbed):
        """Verify that protected endpoints deny access without valid token"""
        base_url = testbed.custom.get("sut_url")

        for scenario in self.SCENARIOS:
            for endpoint in self.PRIVATE_ENDPOINTS:

                with steps.start(
                    f"{scenario['name']} → {endpoint}",
                    continue_=True
                ) as step:

                    response = APIClient.get(
                        f"{base_url}{endpoint}",
                        headers=scenario["headers"],
                        testbed=testbed
                    )

                    try:
                        self._validate_unauthorized(response)
                        step.passed("Correctly denied access")

                    except AssertionError as e:
                        step.failed(str(e))
