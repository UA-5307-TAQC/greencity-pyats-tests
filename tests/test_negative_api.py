"""Test cases for negative scenarios of the API
endpoints, ensuring proper error handling and validation."""
import logging

from pyats import aetest
from utils.api_client import APIClient

log: logging.Logger = logging.getLogger(__name__)

class TestNegativeAPI(aetest.Testcase):
    """Test cases for negative scenarios of the API endpoints,
    ensuring proper error handling and validation."""
    def _validate_error(self, response, expected_status=400):
        """
        Helper to validate error responses
        """
        assert response.status_code == expected_status, \
            f"Expected {expected_status}, got {response.status_code}"

        data = response.json()

        assert isinstance(data, dict), "Error response is not JSON object"

        message = data.get("message") or data.get("error")

        assert message, "Error message is missing"
        assert isinstance(message, str), "Error message is not a string"
        assert len(message) > 5, "Error message too vague"

        log.info("Error message: %s", message)

    @aetest.test
    def empty_body(self, testbed):
        """Test API response to empty request body."""
        base_url = testbed.custom.get("sut_url")

        response = APIClient.post(
            f"{base_url}/ownSecurity/signIn",
            json={},
            testbed=testbed
        )

        self._validate_error(response)

    @aetest.test
    def invalid_email(self, testbed):
        """Test API response to invalid email format."""
        base_url = testbed.custom.get("sut_url")

        payload = {
            "email": "user_at_domain.com",
            "password": "somePassword123"
        }

        response = APIClient.post(
            f"{base_url}/ownSecurity/signIn",
            json=payload,
            testbed=testbed
        )

        self._validate_error(response)

        msg = response.json().get("message", "").lower()
        assert "email" in msg, "Error does not mention email issue"

    @aetest.test
    def invalid_id(self, testbed):
        """Test API response to invalid habit ID."""
        base_url = testbed.custom.get("sut_url")
        token = self.parent.parameters.get("access_token")

        headers = {
            "Authorization": f"Bearer {token}"
        }

        invalid_id = 999999999

        response = APIClient.get(
            f"{base_url}/habit/{invalid_id}",
            headers=headers,
            testbed=testbed
        )

        self._validate_error(response, expected_status=400)

        msg = response.json().get("message", "").lower()

        assert any(word in msg for word in ["not found", "invalid", "exist"]), \
            "Error message is not descriptive enough"
