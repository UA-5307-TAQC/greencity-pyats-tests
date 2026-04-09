"""Test RBAC by verifying that a standard user cannot access admin-only endpoints."""
import logging

from pyats import aetest
from utils.api_client import APIClient
log: logging.Logger = logging.getLogger(__name__)

# pylint: disable=too-few-public-methods
class TestRBAC(aetest.Testcase):
    """Test RBAC by verifying that a standard user cannot access admin-only endpoints."""
    ADMIN_ENDPOINTS = [
        {
            "name": "Get all users",
            "method": "GET",
            "endpoint": "/management/users"
        },
        {
            "name": "Delete eco news",
            "method": "DELETE",
            "endpoint": "/management/eco-news/1"
        }
    ]

    def _validate_forbidden(self, response):
        assert response.status_code == 403, \
            f"Expected 403, got {response.status_code}"

        data = response.json()

        message = data.get("message") or data.get("error")

        assert message, "Missing error message"
        assert isinstance(message, str)
        assert len(message) > 5

        msg_lower = message.lower()

        assert any(word in msg_lower for word in [
            "forbidden", "access", "denied", "permission"
        ]), "Message does not indicate permission issue"

        log.info("RBAC message: %s", message)

    @aetest.test
    def verify_user_cannot_access_admin(self, testbed):
        """Verify that a standard user cannot access admin-only endpoints."""
        base_url = testbed.custom.get("sut_url")

        user_creds = testbed.custom["users"]["standard_user"]

        token = APIClient.authenticate_user(
            base_url,
            user_creds
        )

        headers = {
            "Authorization": f"Bearer {token}"
        }

        for api in self.ADMIN_ENDPOINTS:

            with self.steps.start(
                f"{api['name']} → expect 403",
                continue_=True
            ) as step:

                url = f"{base_url}{api['endpoint']}"

                if api["method"] == "GET":
                    response = APIClient.get(
                        url,
                        headers=headers,
                        testbed=testbed
                    )

                elif api["method"] == "DELETE":
                    response = APIClient.delete(
                        url,
                        headers=headers,
                        testbed=testbed
                    )

                else:
                    step.failed("Unsupported HTTP method")
                    continue

                try:
                    self._validate_forbidden(response)
                    step.passed("Access correctly denied")

                except AssertionError as e:
                    step.failed(str(e))
