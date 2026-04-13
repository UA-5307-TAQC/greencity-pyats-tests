import requests
from pyats import aetest

import logging
from data.config import Config
from utils.api_client import APIClient

log = logging.getLogger(__name__)

class BaseCommonSetup(aetest.CommonSetup):
    """Base setup class that prepares the API client"""

    @aetest.subsection
    def prepare_api_client(self, testbed):
        log.info("Creating API client")

        sut = testbed.devices['sut']
        protocol = sut.connections.rest.protocol
        host = sut.connections.rest.host

        base_url=f"{protocol}://{host}"
        client = APIClient(base_url)
        self.parent.parameters['base_url'] = base_url
        self.parent.parameters['api_client'] = client


class AuthorizationSetup(BaseCommonSetup):

    @aetest.subsection
    def login(self):
        """Authenticate users via the /ownSecurity/signIn flow"""
        log.info("Setup Loging")

        client = self.parent.parameters.get('api_client')
        payload = {
        "email": Config.USER_EMAIL,
        "password": Config.USER_PASSWORD,
        "projectName": "GREENCITY"
        }

        try:
            response = client.request(
                method="POST",
                endpoint="/ownSecurity/signIn",
                json=payload
            )
            if response.status_code != 200:
                log.error(f"Authentication failed: {response.status_code}")
                self.failed(f"Authentication request returned {response.status_code}",
                    goto=['exit']
                )

            data = response.json()
            user_id = data.get('userId')
            if not user_id:
                self.failed("Login successful but no accessToken returned")
            self.parent.parameters['user_id'] = user_id

            access_token = data.get('accessToken')
            if not access_token:
                self.failed("Login successful but no accessToken returned",
                    goto=['exit']
                )
            self.parent.parameters['access_token'] = access_token

        except requests.exceptions.RequestException as e:
            log.error(f"Login failed: {str(e)}")
            self.failed(
                reason="SUT is not reachable (connection error)",
                goto=['exit']
            )


    @aetest.subsection
    def create_authorized_client(self):
        log.info("Creating authorized client")

        base_url = self.parent.parameters.get('base_url')
        access_token = self.parent.parameters.get('access_token')
        authorized_client =  APIClient(base_url, access_token)
        self.parent.parameters['authorized_client'] = authorized_client
