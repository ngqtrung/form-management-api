from app.validators.base import FieldValidationError, FieldValidator

DEFAULT_MIN = 0
DEFAULT_MAX = 100


class NumberValidator(FieldValidator):
    def validate(self, value, field):
        try:
            number = float(value)
        except (TypeError, ValueError):
            raise FieldValidationError("Must be a valid number.")

        rules = field.validation_rules or {}
        minimum = rules.get("min", DEFAULT_MIN)
        maximum = rules.get("max", DEFAULT_MAX)
        if number < minimum or number > maximum:
            raise FieldValidationError(f"Must be between {minimum} and {maximum}.")

        return int(number) if number.is_integer() else number
