AUTH_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "accessToken": {"type": "string"},
        "refreshToken": {"type": "string"}
    },
    "required": ["accessToken"],
    "additionalProperties": True
}