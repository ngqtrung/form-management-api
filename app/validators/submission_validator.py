from dataclasses import dataclass, field as dataclass_field
from typing import Any

from app.validators.base import FieldValidationError
from app.validators.registry import get_validator


@dataclass
class SubmissionValidationResult:
    is_valid: bool
    cleaned_data: dict = dataclass_field(default_factory=dict)  # field_id -> cleaned value
    errors: list = dataclass_field(default_factory=list)  # [{"field_id", "label", "message"}]


class SubmissionValidator:
    """Validates a dict of submitted answers against a Form's configured fields.

    The required-check is centralized here so each per-type FieldValidator only
    has to worry about type-specific rules, keeping those validators trivially
    unit-testable in isolation.
    """

    def validate(self, form, answers: dict) -> SubmissionValidationResult:
        cleaned = {}
        errors = []

        for field in sorted(form.fields, key=lambda f: f.order):
            value = answers.get(field.id)

            is_empty = value is None or value == ""
            if field.required and is_empty:
                errors.append(
                    {"field_id": field.id, "label": field.label, "message": "This field is required."}
                )
                continue

            if is_empty:
                cleaned[field.id] = None
                continue

            try:
                cleaned[field.id] = get_validator(field.type).validate(value, field)
            except FieldValidationError as exc:
                errors.append({"field_id": field.id, "label": field.label, "message": exc.message})

        return SubmissionValidationResult(is_valid=not errors, cleaned_data=cleaned, errors=errors)
