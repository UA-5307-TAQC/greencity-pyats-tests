"""
GreenCity EcoNews — Create Tests
=================================
Black-box pyATS test script for POST /econews.

10 test cases
-------------
TC-01  Create EcoNews with all valid required fields            -> 201 Created
TC-02  Create EcoNews without an authentication token           -> 401 Unauthorized
TC-03  Create EcoNews with an invalid / malformed token         -> 401 or 403
TC-04  Create EcoNews with missing required 'title' field       -> 400 Bad Request
TC-05  Create EcoNews with missing required 'text' field        -> 400 Bad Request
TC-06  Create EcoNews with title exceeding maximum length       -> 400 Bad Request
TC-07  Create EcoNews with an empty tags list                   -> 400 Bad Request
TC-08  Create EcoNews with an invalid tag value                 -> 400 Bad Request
TC-09  Validate full response schema on successful creation     -> 201 + schema check
TC-10  Create EcoNews and verify it appears in GET /econews     -> 201 + 200 in list

Usage
-----
    pyats run job tests/eco_news/create_eco_news_job.py --testbed testbed.yaml
"""

import logging
import os
import sys
import uuid

from pyats import aetest

# Allow bare-script execution and imports from the project root.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from utils.api_client import GreenCityApiClient  # noqa: E402
from utils.auth_helper import INVALID_TOKEN       # noqa: E402

log = logging.getLogger(__name__)


# -----------------------------------------------------------------------------
# Helpers shared by multiple test cases
# -----------------------------------------------------------------------------

def _unique_title(label: str) -> str:
    """Return a title unique per run to avoid collisions on the shared env."""
    return f"[PyATS] {label} [{uuid.uuid4().hex[:8]}]"


def _valid_payload(title: str) -> dict:
    return {
        "title": title,
        "text": (
            "Automated pyATS test article. "
            "This content is created solely for API validation and will be removed."
        ),
        "source": "https://example.com/pyats-test",
        "tags": ["NEWS"],
        "imagePath": "",
    }


# -----------------------------------------------------------------------------
# Common Setup — runs once before all test cases
# -----------------------------------------------------------------------------

class CommonSetup(aetest.CommonSetup):
    """Authenticate and share the API client with every test case."""

    @aetest.subsection
    def initialize_api_client(self, testbed):
        """Instantiate GreenCityApiClient from testbed custom parameters."""
        custom = testbed.custom
        client = GreenCityApiClient(
            main_api_base_url=custom["main_api_base_url"],
            user_api_base_url=custom["user_api_base_url"],
        )
        self.parent.parameters["client"] = client
        self.parent.parameters["constraints"] = custom.get("eco_news_constraints", {})
        # Accumulates IDs of every article created during the run for cleanup.
        self.parent.parameters["created_news_ids"] = []
        log.info("API client initialised -> %s", custom["main_api_base_url"])

    @aetest.subsection
    def authenticate(self, testbed, client):
        """Obtain a JWT access token from the User API and store it."""
        creds = testbed.custom["test_credentials"]
        token = client.authenticate(creds["email"], creds["password"])
        if not token:
            self.failed("Authentication failed — cannot continue test run")
        self.parent.parameters["access_token"] = token
        log.info("Authentication successful")


# -----------------------------------------------------------------------------
# TC-01  Create EcoNews with valid data
# -----------------------------------------------------------------------------

class TC01_CreateEcoNewsWithValidData(aetest.Testcase):
    """Create EcoNews with all valid required fields.

    Sends a well-formed POST /econews request with a valid bearer token and
    asserts the server responds with 201 Created and returns the new resource
    identifier in the response body.
    """

    @aetest.test
    def test_returns_201_and_id(self, steps, client, created_news_ids):
        payload = _valid_payload(_unique_title("Valid Creation"))

        with steps.start("POST /econews with valid payload") as step:
            response = client.create_eco_news(payload, use_auth=True)
            log.info("Status: %s | Body: %.400s", response.status_code, response.text)
            if response.status_code != 201:
                step.failed(
                    f"Expected 201 Created, got {response.status_code}: {response.text}"
                )

        with steps.start("Response body contains 'id' field") as step:
            data = response.json()
            if "id" not in data:
                step.failed(f"'id' field missing from response: {data}")
            created_news_ids.append(data["id"])
            log.info("Created EcoNews id=%s", data["id"])

        with steps.start("Response 'title' matches the request") as step:
            if data.get("title") != payload["title"]:
                step.failed(
                    f"Title mismatch — sent '{payload['title']}', "
                    f"received '{data.get('title')}'"
                )


# -----------------------------------------------------------------------------
# TC-02  Create EcoNews without auth token
# -----------------------------------------------------------------------------

class TC02_CreateEcoNewsWithoutAuth(aetest.Testcase):
    """Create EcoNews without an authentication token.

    Verifies that the API enforces authentication by returning 401 Unauthorized
    when no bearer token is present in the request.
    """

    @aetest.test
    def test_returns_401(self, steps, client):
        payload = _valid_payload(_unique_title("No Auth"))

        with steps.start("POST /econews — no Authorization header") as step:
            response = client.create_eco_news(payload, use_auth=False)
            log.info("Status: %s", response.status_code)
            if response.status_code != 401:
                step.failed(
                    f"Expected 401 Unauthorized, got {response.status_code}"
                )


# -----------------------------------------------------------------------------
# TC-03  Create EcoNews with an invalid / malformed token
# -----------------------------------------------------------------------------

class TC03_CreateEcoNewsWithInvalidToken(aetest.Testcase):
    """Create EcoNews with a tampered JWT token.

    Uses a JWT that is syntactically valid but has an incorrect signature.
    The API must reject this with 401 or 403 and must NOT create any resource.
    """

    @aetest.test
    def test_returns_401_or_403(self, steps, client):
        payload = _valid_payload(_unique_title("Invalid Token"))

        with steps.start("POST /econews with tampered JWT") as step:
            response = client.create_eco_news(
                payload, token=INVALID_TOKEN, use_auth=True
            )
            log.info("Status: %s", response.status_code)
            if response.status_code not in (401, 403):
                step.failed(
                    f"Expected 401 or 403, got {response.status_code}"
                )


# -----------------------------------------------------------------------------
# TC-04  Create EcoNews — missing required 'title'
# -----------------------------------------------------------------------------

class TC04_CreateEcoNewsMissingTitle(aetest.Testcase):
    """Create EcoNews with the 'title' field omitted from the request body.

    The API must validate required fields and return 400 Bad Request when
    the mandatory 'title' key is absent.
    """

    @aetest.test
    def test_returns_400(self, steps, client):
        payload = {
            "text": "This article has no title — validation should catch this.",
            "source": "https://example.com/pyats-test",
            "tags": ["NEWS"],
            "imagePath": "",
        }

        with steps.start("POST /econews without 'title'") as step:
            response = client.create_eco_news(payload, use_auth=True)
            log.info("Status: %s | Body: %.300s", response.status_code, response.text)
            if response.status_code != 400:
                step.failed(
                    f"Expected 400 Bad Request for missing title, "
                    f"got {response.status_code}"
                )


# -----------------------------------------------------------------------------
# TC-05  Create EcoNews — missing required 'text'
# -----------------------------------------------------------------------------

class TC05_CreateEcoNewsMissingText(aetest.Testcase):
    """Create EcoNews with the 'text' field omitted from the request body.

    The API must validate required fields and return 400 Bad Request when
    the mandatory 'text' key is absent.
    """

    @aetest.test
    def test_returns_400(self, steps, client):
        payload = {
            "title": _unique_title("Missing Text"),
            "source": "https://example.com/pyats-test",
            "tags": ["NEWS"],
            "imagePath": "",
        }

        with steps.start("POST /econews without 'text'") as step:
            response = client.create_eco_news(payload, use_auth=True)
            log.info("Status: %s | Body: %.300s", response.status_code, response.text)
            if response.status_code != 400:
                step.failed(
                    f"Expected 400 Bad Request for missing text, "
                    f"got {response.status_code}"
                )


# -----------------------------------------------------------------------------
# TC-06  Create EcoNews — title exceeds maximum allowed length
# -----------------------------------------------------------------------------

class TC06_CreateEcoNewsTitleExceedsMaxLength(aetest.Testcase):
    """Create EcoNews with a title one character longer than the allowed maximum.

    Verifies that the API enforces the title length constraint defined in the
    testbed configuration and rejects the request with 400 Bad Request.
    """

    @aetest.test
    def test_returns_400(self, steps, client, constraints):
        max_len = constraints.get("title_max_length", 170)
        oversized_title = "A" * (max_len + 1)

        payload = {
            "title": oversized_title,
            "text": "This test verifies that title length constraints are enforced by the API.",
            "source": "https://example.com/pyats-test",
            "tags": ["NEWS"],
            "imagePath": "",
        }

        with steps.start(
            f"POST /econews with title length {len(oversized_title)} (max={max_len})"
        ) as step:
            response = client.create_eco_news(payload, use_auth=True)
            log.info("Status: %s | Body: %.300s", response.status_code, response.text)
            if response.status_code != 400:
                step.failed(
                    f"Expected 400 Bad Request for oversized title "
                    f"({len(oversized_title)} chars), got {response.status_code}"
                )


# -----------------------------------------------------------------------------
# TC-07  Create EcoNews — empty tags list
# -----------------------------------------------------------------------------

class TC07_CreateEcoNewsWithEmptyTags(aetest.Testcase):
    """Create EcoNews with an empty 'tags' list.

    The API requires at least one tag.  An empty list must be rejected with
    400 Bad Request.
    """

    @aetest.test
    def test_returns_400(self, steps, client):
        payload = {
            "title": _unique_title("Empty Tags"),
            "text": "This test verifies that the tags field must not be empty.",
            "source": "https://example.com/pyats-test",
            "tags": [],
            "imagePath": "",
        }

        with steps.start("POST /econews with tags=[]") as step:
            response = client.create_eco_news(payload, use_auth=True)
            log.info("Status: %s | Body: %.300s", response.status_code, response.text)
            if response.status_code != 400:
                step.failed(
                    f"Expected 400 Bad Request for empty tags, "
                    f"got {response.status_code}"
                )


# -----------------------------------------------------------------------------
# TC-08  Create EcoNews — invalid tag value
# -----------------------------------------------------------------------------

class TC08_CreateEcoNewsWithInvalidTag(aetest.Testcase):
    """Create EcoNews with a tag value that is not in the allowed enumeration.

    The API must validate tag values against its allowed set and return
    400 Bad Request for unknown tags.
    """

    @aetest.test
    def test_returns_400(self, steps, client):
        payload = {
            "title": _unique_title("Invalid Tag"),
            "text": "This test verifies that only valid tag values are accepted.",
            "source": "https://example.com/pyats-test",
            "tags": ["TOTALLY_UNKNOWN_TAG_XYZ_99"],
            "imagePath": "",
        }

        with steps.start("POST /econews with unrecognised tag value") as step:
            response = client.create_eco_news(payload, use_auth=True)
            log.info("Status: %s | Body: %.300s", response.status_code, response.text)
            if response.status_code != 400:
                step.failed(
                    f"Expected 400 Bad Request for invalid tag value, "
                    f"got {response.status_code}"
                )


# -----------------------------------------------------------------------------
# TC-09  Validate response schema on successful creation
# -----------------------------------------------------------------------------

class TC09_CreateEcoNewsResponseSchemaValidation(aetest.Testcase):
    """Validate the complete response schema returned by a successful POST /econews.

    Asserts that all expected top-level fields are present and carry the
    correct Python types, and that the nested 'author' object contains an 'id'.
    """

    # Maps field name -> expected Python type(s).
    EXPECTED_FIELDS: dict = {
        "id": int,
        "title": str,
        "creationDate": str,
        "imagePath": (str, type(None)),
        "author": dict,
        "tags": list,
    }

    @aetest.test
    def test_schema(self, steps, client, created_news_ids):
        payload = _valid_payload(_unique_title("Schema Validation"))

        with steps.start("POST /econews and receive 201") as step:
            response = client.create_eco_news(payload, use_auth=True)
            if response.status_code != 201:
                step.failed(
                    f"Expected 201 Created, got {response.status_code}: {response.text}"
                )

        with steps.start("Parse response as JSON") as step:
            try:
                data = response.json()
            except Exception as exc:
                step.failed(f"Response is not valid JSON: {exc}")

        created_news_ids.append(data["id"])

        with steps.start("All required fields are present") as step:
            missing = [f for f in self.EXPECTED_FIELDS if f not in data]
            if missing:
                step.failed(f"Missing fields in response: {missing}")

        with steps.start("Field types are correct") as step:
            errors = []
            for field, expected_type in self.EXPECTED_FIELDS.items():
                value = data.get(field)
                if not isinstance(value, expected_type):
                    errors.append(
                        f"'{field}': expected {expected_type}, "
                        f"got {type(value).__name__} = {value!r}"
                    )
            if errors:
                step.failed("Field type errors:\n" + "\n".join(errors))

        with steps.start("'author' object contains 'id'") as step:
            author = data.get("author", {})
            if "id" not in author:
                step.failed(f"'author.id' missing — author object: {author}")

        with steps.start("'tags' list is non-empty") as step:
            if not data.get("tags"):
                step.failed("'tags' field is empty in the response")


# -----------------------------------------------------------------------------
# TC-10  Create EcoNews and verify it appears in GET /econews list
# -----------------------------------------------------------------------------

class TC10_CreateEcoNewsVerifyInList(aetest.Testcase):
    """Create EcoNews and confirm it is retrievable via GET /econews.

    End-to-end flow:
        1. POST /econews  -> 201, capture returned id
        2. GET  /econews  -> 200, confirm the new id appears in the first page
        3. Fallback: GET  /econews/{id} -> 200  (in case article is not on page 0)
    """

    @aetest.setup
    def create_article(self, steps, client, created_news_ids):
        """Create the EcoNews article that will be verified in the test step."""
        self.test_title = _unique_title("Verify In List")
        payload = _valid_payload(self.test_title)

        with steps.start("POST /econews — setup article for list verification") as step:
            response = client.create_eco_news(payload, use_auth=True)
            if response.status_code != 201:
                self.skipped(
                    f"Setup failed: POST /econews returned {response.status_code}"
                )
            data = response.json()
            self.created_id = data["id"]
            created_news_ids.append(self.created_id)
            log.info("Setup created EcoNews id=%s", self.created_id)

    @aetest.test
    def test_article_is_visible_via_get(self, steps, client):
        with steps.start("GET /econews — check first page for created id") as step:
            response = client.get_eco_news_list(page=0, size=20)
            log.info("GET /econews status: %s", response.status_code)
            if response.status_code != 200:
                step.failed(
                    f"Expected 200 OK from GET /econews, got {response.status_code}"
                )

            body = response.json()
            # GreenCity returns {"page": [...], "currentPage": 0, "totalPages": N}
            items = (
                body if isinstance(body, list)
                else body.get("page", body.get("content", []))
            )
            found_in_list = any(item.get("id") == self.created_id for item in items)

        if found_in_list:
            log.info("EcoNews id=%s confirmed in list page 0", self.created_id)
            return

        # Fallback: retrieve directly by ID in case page 0 does not include it.
        with steps.start(
            f"Fallback: GET /econews/{self.created_id} — direct lookup"
        ) as step:
            id_response = client.get_eco_news_by_id(self.created_id)
            log.info("GET /econews/%s status: %s", self.created_id, id_response.status_code)
            if id_response.status_code != 200:
                step.failed(
                    f"EcoNews id={self.created_id} not found in list or by direct GET "
                    f"({id_response.status_code})"
                )
            log.info("EcoNews id=%s confirmed via direct GET", self.created_id)


# -----------------------------------------------------------------------------
# Common Cleanup — runs once after all test cases
# -----------------------------------------------------------------------------

class CommonCleanup(aetest.CommonCleanup):
    """Delete every EcoNews article created during this test run."""

    @aetest.subsection
    def delete_created_eco_news(self, client, created_news_ids):
        if not created_news_ids:
            log.info("No EcoNews articles to clean up")
            return

        failed = []
        for news_id in created_news_ids:
            response = client.delete_eco_news(news_id)
            if response.status_code in (200, 204):
                log.info("Deleted EcoNews id=%s", news_id)
            else:
                log.warning(
                    "Could not delete EcoNews id=%s: %s", news_id, response.status_code
                )
                failed.append(news_id)

        if failed:
            log.warning("Articles NOT deleted (manual cleanup required): %s", failed)


# -----------------------------------------------------------------------------
# Entrypoint for direct execution
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    aetest.main()
