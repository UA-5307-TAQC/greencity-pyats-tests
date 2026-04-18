HABITS_SCHEMA = {
    "type": "object",
    "properties": {
        "page": {"type": "number"},
        "totalElements": {"type": "number"},
        "totalPages": {"type": "number"},
        "currentPage": {"type": "number"},
        "content": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "number"},
                    "title": {"type": "string"},
                    "description": {"type": "string"}
                },
                "required": ["id"],
                "additionalProperties": True
            }
        }
    },
    "required": ["content"],
    "additionalProperties": True
}