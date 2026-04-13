import logging
import json
from jsonschema import validate, ValidationError
from pyats import aetest

from utils.shared_setup import AuthorizationSetup
from utils.schema_validator import USER_PROFILE_SCHEMA

log = logging.getLogger(__name__)

class CommonSetup(AuthorizationSetup):
    pass


class TestUserProfile(aetest.Testcase):

    @aetest.test
    def test_user_profile(self):
        log.info("Sending GET /user/userId/profile request")

        client = self.parent.parameters.get('authorized_client')
        user_id = self.parent.parameters.get('user_id')
        response = client.request(
            method="POST",
            endpoint=f"/user/{user_id}/profile"
        )

        if response.status_code != 200:
           self.failed(f"Expected 200 but got {response.status_code}")

        data = response.json()

        log.info("Received User Profile Data:\n" + json.dumps(data, indent=4))
        try:
            validate(instance=data, schema=USER_PROFILE_SCHEMA)
        except ValidationError as e:
            log.error(str(e))
            self.failed("API Contract validation failed")
