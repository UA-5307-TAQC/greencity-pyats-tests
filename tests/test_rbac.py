import logging
from pyats import aetest

from utils.shared_setup import AuthorizationSetup

log = logging.getLogger(__name__)

class CommonSetup(AuthorizationSetup):
    pass


class ForbiddenAccessTest(aetest.Testcase):

    @aetest.setup
    def setup(self):
        log.info("Preparing client for standard user")
        self.standard_client = self.parent.parameters.get('authorized_client')


    @aetest.test
    def test_get_all_users(self):
        log.info(f"Standard user requesting admin-only user list at /management/users")

        response = self.standard_client.request(
            method="GET",
            endpoint="/management/users"
        )

        if response.status_code != 403:
            self.failed(f"Expected 403 but got {response.status_code}")


    @aetest.test
    def test_delete_news_item(self):
        log.info(f"Standard user attempting to delete news item at /management/eco-news/1")

        response = self.standard_client.request(
            method="DELETE",
            endpoint="/management/eco-news/1"
        )

        if response.status_code != 403:
            self.failed(f"Expected 403 but got {response.status_code}")
