import requests
from utils.config import Config
from utils.logger import get_logger


class APIClient:
    def __init__(self):
        self.timeout = Config.REQUEST_TIMEOUT
        self.logger = get_logger(self.__class__.__name__)

    def get(self, url, headers=None, params=None):
        self.logger.info("GET %s", url)
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=self.timeout
        )
        self.logger.info("Response status: %s", response.status_code)
        return response

    def post(self, url, headers=None, json=None, data=None):
        self.logger.info("POST %s", url)
        response = requests.post(
            url,
            headers=headers,
            json=json,
            data=data,
            timeout=self.timeout
        )
        self.logger.info("Response status: %s", response.status_code)
        return response

    def put(self, url, headers=None, json=None):
        self.logger.info("PUT %s", url)
        response = requests.put(
            url,
            headers=headers,
            json=json,
            timeout=self.timeout
        )
        self.logger.info("Response status: %s", response.status_code)
        return response

    def patch(self, url, headers=None, json=None):
        self.logger.info("PATCH %s", url)
        response = requests.patch(
            url,
            headers=headers,
            json=json,
            timeout=self.timeout
        )
        self.logger.info("Response status: %s", response.status_code)
        return response

    def delete(self, url, headers=None):
        self.logger.info("DELETE %s", url)
        response = requests.delete(
            url,
            headers=headers,
            timeout=self.timeout
        )
        self.logger.info("Response status: %s", response.status_code)
        return response
