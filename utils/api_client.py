"""Requests wrapper with logging"""

import requests
import logging

log = logging.getLogger(__name__)

class APIClient:
    def __init__(self, base_url, access_token=None, timeout=10):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})
        if access_token:
            self.session.headers.update({'Authorization': f'Bearer {access_token}'})

    def request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        kwargs.setdefault('timeout', self.timeout)

        log.info(f"Sending {method} request to {url}")
        response = self.session.request(method, url, **kwargs)
        log.info(f"Response Status: {response.status_code}")
        return response
