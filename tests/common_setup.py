from pyats import aetest
from utils.auth_helper import AuthHelper


class CommonSetup(aetest.CommonSetup):

    @aetest.subsection
    def authenticate(self):
        auth_data = AuthHelper.login()
        self.parent.parameters["access_token"] = auth_data["accessToken"]
        self.parent.parameters["user_id"] = auth_data["userId"]