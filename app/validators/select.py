from app.validators.base import FieldValidationError, FieldValidator


class SelectValidator(FieldValidator):
    def validate(self, value, field):
        options = field.options or []
        if value not in options:
            raise FieldValidationError(f"Must be one of: {', '.join(str(o) for o in options)}.")
        return value
