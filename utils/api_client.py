"""
GreenCity API Client
--------------------
Thin HTTP wrapper around the GreenCity REST API endpoints.

EcoNews create requests use multipart/form-data with the DTO part sent as
an application/json string, which matches the GreenCity API contract.
"""

import json
import logging

import requests

log = logging.getLogger(__name__)


class GreenCityApiClient:
    """HTTP client for the GreenCity REST API."""

    def __init__(self, main_api_base_url: str, user_api_base_url: str) -> None:
        self.main_api_base_url = main_api_base_url.rstrip("/")
        self.user_api_base_url = user_api_base_url.rstrip("/")
        self.access_token: str | None = None

    # ------------------------------------------------------------------
    # Authentication
    # ------------------------------------------------------------------

    def authenticate(self, email: str, password: str) -> str | None:
        """POST /ownSecurity/signIn — return JWT access token or None."""
        url = f"{self.user_api_base_url}/ownSecurity/signIn"
        response = requests.post(
            url,
            json={"email": email, "password": password},
            headers={"Content-Type": "application/json"},
            timeout=30,
        )
        log.debug("Auth response: %s", response.status_code)
        if response.status_code == 200:
            data = response.json()
            self.access_token = data.get("accessToken")
            return self.access_token
        log.error("Authentication failed: %s %s", response.status_code, response.text)
        return None

    # ------------------------------------------------------------------
    # EcoNews endpoints
    # ------------------------------------------------------------------

    def create_eco_news(
        self,
        payload: dict,
        token: str | None = None,
        use_auth: bool = True,
    ) -> requests.Response:
        """POST /econews — create a new EcoNews article.

        The API expects multipart/form-data with a single part named
        ``addEcoNewsDtoRequest`` carrying the JSON-serialised DTO.
        """
        url = f"{self.main_api_base_url}/econews"
        headers: dict = {}
        if use_auth:
            bearer = token or self.access_token
            if bearer:
                headers["Authorization"] = f"Bearer {bearer}"

        files = {
            "addEcoNewsDtoRequest": (None, json.dumps(payload), "application/json"),
        }
        log.debug("POST %s | use_auth=%s", url, use_auth)
        return requests.post(url, files=files, headers=headers, timeout=30)

    def get_eco_news_by_id(self, news_id: int) -> requests.Response:
        """GET /econews/{id} — fetch a single EcoNews by ID."""
        url = f"{self.main_api_base_url}/econews/{news_id}"
        return requests.get(url, timeout=30)

    def get_eco_news_list(self, page: int = 0, size: int = 20) -> requests.Response:
        """GET /econews — fetch a paginated list of EcoNews."""
        url = f"{self.main_api_base_url}/econews"
        return requests.get(url, params={"page": page, "size": size}, timeout=30)

    def delete_eco_news(self, news_id: int) -> requests.Response:
        """DELETE /econews/{id} — delete EcoNews by ID (requires auth)."""
        url = f"{self.main_api_base_url}/econews/{news_id}"
        headers: dict = {}
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        log.debug("DELETE %s", url)
        return requests.delete(url, headers=headers, timeout=30)
