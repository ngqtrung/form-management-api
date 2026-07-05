from abc import ABC, abstractmethod


class FieldValidationError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class FieldValidator(ABC):
    @abstractmethod
    def validate(self, value, field):
        """Return the cleaned/normalized value.

        Raise FieldValidationError(message) if the value is invalid for this field type.
        `field` exposes .options and .validation_rules for per-field overrides.
        """
        raise NotImplementedError
