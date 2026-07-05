from app.validators.base import FieldValidationError, FieldValidator

DEFAULT_MAX_LENGTH = 200


class TextValidator(FieldValidator):
    def validate(self, value, field):
        text = str(value)
        max_length = (field.validation_rules or {}).get("max_length", DEFAULT_MAX_LENGTH)
        if len(text) > max_length:
            raise FieldValidationError(f"Must be at most {max_length} characters.")
        return text
