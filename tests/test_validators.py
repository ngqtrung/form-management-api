from dataclasses import dataclass
from datetime import date, timedelta
from typing import Any

import pytest

from app.validators.base import FieldValidationError
from app.validators.color import ColorValidator
from app.validators.date import DateValidator
from app.validators.number import NumberValidator
from app.validators.registry import get_validator
from app.validators.select import SelectValidator
from app.validators.submission_validator import SubmissionValidator
from app.validators.text import TextValidator


@dataclass
class FakeField:
    id: str = "field-1"
    label: str = "Field"
    type: str = "text"
    required: bool = False
    options: Any = None
    validation_rules: Any = None
    order: int = 0


@dataclass
class FakeForm:
    fields: list


# --- text ---


def test_text_validator_accepts_within_max_length():
    assert TextValidator().validate("hello", FakeField()) == "hello"


def test_text_validator_rejects_over_default_max_length():
    with pytest.raises(FieldValidationError):
        TextValidator().validate("x" * 201, FakeField())


def test_text_validator_respects_custom_max_length():
    field = FakeField(validation_rules={"max_length": 3})
    with pytest.raises(FieldValidationError):
        TextValidator().validate("abcd", field)


# --- number ---


def test_number_validator_accepts_within_default_range():
    assert NumberValidator().validate("50", FakeField()) == 50


def test_number_validator_rejects_out_of_range():
    with pytest.raises(FieldValidationError):
        NumberValidator().validate("101", FakeField())


def test_number_validator_rejects_non_numeric():
    with pytest.raises(FieldValidationError):
        NumberValidator().validate("abc", FakeField())


def test_number_validator_respects_custom_range():
    field = FakeField(validation_rules={"min": 10, "max": 20})
    assert NumberValidator().validate("15", field) == 15
    with pytest.raises(FieldValidationError):
        NumberValidator().validate("5", field)


# --- date ---


def test_date_validator_rejects_past_date():
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    with pytest.raises(FieldValidationError):
        DateValidator().validate(yesterday, FakeField())


def test_date_validator_accepts_today_and_future():
    today = date.today().isoformat()
    assert DateValidator().validate(today, FakeField()) == today


def test_date_validator_rejects_malformed_date():
    with pytest.raises(FieldValidationError):
        DateValidator().validate("not-a-date", FakeField())


# --- color ---


def test_color_validator_accepts_valid_hex():
    assert ColorValidator().validate("#1a2b3c", FakeField()) == "#1A2B3C"


@pytest.mark.parametrize("bad_value", ["1a2b3c", "#1a2b3", "#zzzzzz", "red"])
def test_color_validator_rejects_invalid_hex(bad_value):
    with pytest.raises(FieldValidationError):
        ColorValidator().validate(bad_value, FakeField())


# --- select ---


def test_select_validator_accepts_configured_option():
    field = FakeField(options=["a", "b", "c"])
    assert SelectValidator().validate("b", field) == "b"


def test_select_validator_rejects_unknown_option():
    field = FakeField(options=["a", "b", "c"])
    with pytest.raises(FieldValidationError):
        SelectValidator().validate("d", field)


# --- registry ---


def test_registry_returns_matching_validator_for_each_type():
    for field_type in ("text", "number", "date", "color", "select"):
        assert get_validator(field_type) is not None


def test_registry_raises_for_unknown_type():
    with pytest.raises(ValueError):
        get_validator("unknown")


# --- SubmissionValidator ---


def test_submission_validator_flags_missing_required_field():
    form = FakeForm(fields=[FakeField(id="f1", label="Name", type="text", required=True, order=0)])
    result = SubmissionValidator().validate(form, {})
    assert not result.is_valid
    assert result.errors[0]["field_id"] == "f1"


def test_submission_validator_allows_empty_optional_field():
    form = FakeForm(fields=[FakeField(id="f1", label="Nickname", type="text", required=False, order=0)])
    result = SubmissionValidator().validate(form, {})
    assert result.is_valid
    assert result.cleaned_data["f1"] is None


def test_submission_validator_collects_multiple_field_errors():
    form = FakeForm(
        fields=[
            FakeField(id="f1", label="Age", type="number", required=True, order=0),
            FakeField(id="f2", label="Color", type="color", required=True, order=1),
        ]
    )
    result = SubmissionValidator().validate(form, {"f1": "999", "f2": "not-a-color"})
    assert not result.is_valid
    assert {err["field_id"] for err in result.errors} == {"f1", "f2"}


def test_submission_validator_returns_cleaned_data_when_valid():
    form = FakeForm(
        fields=[
            FakeField(id="f1", label="Age", type="number", required=True, order=0),
            FakeField(id="f2", label="Color", type="color", required=True, order=1),
        ]
    )
    result = SubmissionValidator().validate(form, {"f1": "42", "f2": "#ffffff"})
    assert result.is_valid
    assert result.cleaned_data == {"f1": 42, "f2": "#FFFFFF"}
