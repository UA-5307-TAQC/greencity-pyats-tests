PROFILE_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "userId": {"type": "integer"},
        "name": {"type": "string"},
        "email": {
            "type": "string",
            "pattern": r"^[^@]+@[^@]+\.[^@]+$"
        },
        "rating": {
            "type": ["integer", "number"]
        }
    },
    "required": ["userId", "name", "email", "rating"]
}