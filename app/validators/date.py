from datetime import date, datetime

from app.validators.base import FieldValidationError, FieldValidator


class DateValidator(FieldValidator):
    def validate(self, value, field):
        try:
            parsed = datetime.strptime(str(value), "%Y-%m-%d").date()
        except ValueError:
            raise FieldValidationError("Must be a valid date in YYYY-MM-DD format.")

        if parsed < date.today():
            raise FieldValidationError("Must not be a date in the past.")

        return parsed.isoformat()
