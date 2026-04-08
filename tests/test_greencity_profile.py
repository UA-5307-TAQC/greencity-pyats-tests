"""Test user data api"""
import requests
from pyats import aetest
from pyats.log.utils import banner
from pydantic import ValidationError
from data.config import Config
from schema.user_profile_schema import UserProfileSchema
from utils.api_auth_token import get_auth_token


class CommonSetup(aetest.CommonSetup):
    """Common Setup class for all tests"""
    @aetest.subsection
    def setup_environment(self):
        """Setup environment for all tests"""
        data_about_user = get_auth_token()

        self.parent.parameters['api_url'] = f"{Config.BASE_API_URL_LOGIN}/user/{data_about_user['user_id']}/profile/"

        self.parent.parameters['access_token'] = data_about_user['token']

        print(banner("Починаємо тестування контракту GreenCity API"))


class UserProfileContractTest(aetest.Testcase):
    """Check user profile data"""
    @aetest.setup
    def prepare_request(self):
        """Prepare request data"""
        self.url = self.parent.parameters['api_url']
        token = self.parent.parameters['access_token']

        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        self.response = None

    @aetest.test
    def test_status_code(self):
        """Check status code"""
        self.response = requests.get(self.url, headers=self.headers, timeout=10)

        if self.response.status_code == 200:
            self.passed("Успіх! Статус код 200.")
        elif self.response.status_code == 401:
            self.failed("Помилка 401: Токен недійсний або відсутній. Тест зупинено.")
        else:
            self.failed(f"Очікували 200, але отримали {self.response.status_code}. Відповідь: {self.response.text}")

    @aetest.test
    def test_schema_and_business_logic(self):
        """Validate schema and business logic"""
        try:
            json_data = self.response.json()
        except ValueError:
            self.failed("Відповідь сервера не є валідним форматом JSON.")

        try:
            validated_data = UserProfileSchema(**json_data)
        except ValidationError as e:
            error_details = e.json()
            self.failed(f"API КОНТРАКТ ПОРУШЕНО!\nДеталі помилки:\n{error_details}")

        self.passed(f"Контракт API повністю валідний! Ім'я користувача: {validated_data.name}")

class CommonCleanup(aetest.CommonCleanup):
    """Common Cleanup class for all tests"""
    @aetest.subsection
    def cleanup(self):
        """Clean up after all tests"""
        print(banner("Тестування завершено."))
