import re

from app.validators.base import FieldValidationError, FieldValidator

HEX_COLOR_PATTERN = re.compile(r"^#[0-9A-Fa-f]{6}$")


class ColorValidator(FieldValidator):
    def validate(self, value, field):
        text = str(value)
        if not HEX_COLOR_PATTERN.match(text):
            raise FieldValidationError("Must be a valid HEX color, e.g. #RRGGBB.")
        return text.upper()
