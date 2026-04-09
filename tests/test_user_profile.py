"""Test case for validating the user profile API endpoint."""
import logging

from pyats import aetest
from utils.api_client import APIClient
from utils.schema_validator import validate_schema, USER_PROFILE_SCHEMA
log: logging.Logger = logging.getLogger(__name__)
# pylint: disable=too-few-public-methods
class TestUserProfile(aetest.Testcase):
    """Test case for validating the user profile API endpoint."""
    @aetest.test
    def validate_user_profile(self, testbed):
        """Validate the /user/profile endpoint."""
        base_url = testbed.custom.get("sut_url")
        token = self.parent.parameters.get("access_token")

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = APIClient.get(
            f"{base_url}/user/profile",
            headers=headers,
            testbed=testbed
        )

        assert response.status_code == 200, \
            f"Unexpected status: {response.status_code}"

        data = response.json()

        validate_schema(data, USER_PROFILE_SCHEMA)

        log.info("Schema validation passed")

        assert data.get("name") is not None, "Name is null"
        assert data.get("rating") is not None, "Rating is null"

        log.info("Business logic validation passed")
