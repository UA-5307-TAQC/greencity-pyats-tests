USER_PROFILE_SCHEMA = {
    "type": "object",
    "properties": {
        "userId": {"type": "integer"},
        "email": {
            "type": "string",
            "format": "email"
        },
        "name": {
            "type": "string",
            "minLength": 1
        },
        "rating": {"type": "number"},
    },
    "required": ["userId", "email", "name", "rating"]
}
