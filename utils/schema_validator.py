"""Utility functions for validating data against JSON schemas."""
from jsonschema import validate, ValidationError

USER_PROFILE_SCHEMA = {
    "type": "object",
    "properties": {
        "userId": {"type": "integer"},
        "email": {
            "type": "string",
            "format": "email"
        },
        "name": {"type": "string"},
        "rating": {"type": ["number", "integer"]}
    },
    "required": ["userId", "email", "name", "rating"]
}

ERROR_SCHEMA = {
    "type": "object",
    "properties": {
        "message": {"type": "string"}
    },
    "required": ["message"]
}

def validate_schema(data, schema):
    """Validate data against a JSON schema."""
    try:
        validate(instance=data, schema=schema)
    except ValidationError as e:
        raise ValueError(
            f"Schema validation failed: {e.message}"
        ) from e
