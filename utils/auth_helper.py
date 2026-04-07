"""
Authentication helpers for GreenCity API tests.
"""

# A syntactically valid JWT whose signature is intentionally wrong.
# Used by TC-03 to verify the API rejects tampered tokens.
INVALID_TOKEN = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
    ".eyJzdWIiOiJ0ZXN0QGV4YW1wbGUuY29tIiwiaWF0IjoxNjAwMDAwMDAwfQ"
    ".INVALID_SIGNATURE_FOR_TESTING_PURPOSES_ONLY"
)
