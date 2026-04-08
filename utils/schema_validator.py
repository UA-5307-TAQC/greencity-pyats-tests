import logging
from jsonschema import validate, ValidationError

log = logging.getLogger(__name__)

USER_PROFILE_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "rating": {"type": "number"},
        "role": {"type": "string"}
    },
    "required": ["name", "rating", "role"]
}

def validate_user_profile(instance_data):
    """
    Validates the given JSON data against the USER_PROFILE_SCHEMA.
    """
    log.info("Starting JSON Schema validation...")
    try:
        validate(instance=instance_data, schema=USER_PROFILE_SCHEMA)
        log.info("JSON Schema validation passed! Data types and patterns are correct.")
        return True
    except ValidationError as e:
        # Якщо тип не співпав (наприклад, прийшов string замість int), логуємо конкретну помилку
        log.error(f"JSON Schema validation failed: {e.message}")
        raise