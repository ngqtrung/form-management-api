from app.validators.color import ColorValidator
from app.validators.date import DateValidator
from app.validators.number import NumberValidator
from app.validators.select import SelectValidator
from app.validators.text import TextValidator

_VALIDATORS = {
    "text": TextValidator(),
    "number": NumberValidator(),
    "date": DateValidator(),
    "color": ColorValidator(),
    "select": SelectValidator(),
}


def get_validator(field_type):
    validator = _VALIDATORS.get(field_type)
    if validator is None:
        raise ValueError(f"No validator registered for field type '{field_type}'.")
    return validator
