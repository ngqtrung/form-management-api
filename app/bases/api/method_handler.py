from marshmallow import ValidationError as MarshmallowValidationError
from flask import jsonify

from app.errors import BadRequest, PermissionError_


class MethodHandler:
    """Base class for a single HTTP method on a Resource.

    Subclasses are auto-discovered from a sibling `methods` module by
    `MetaResource` based on their class name (Get/Post/Put/Patch/Delete).
    """

    # whether Resource.dispatch_request must resolve a logged-in user before
    # constructing this handler (enforced there, not here).
    auth_required = True

    # permission codes; current_user needs ANY of them (OR semantics).
    permission_requirements = None

    # Marshmallow schema class used to validate/parse the request payload.
    input_schema_class = None
    partial = False

    def __init__(self, request, current_user, url_params):
        self.request = request
        self.current_user = current_user
        self.url_params = url_params

        self._check_permission()

        self.raw_params = self._get_raw_params()
        self.payload = self._parse_raw_params()

    def _get_raw_params(self):
        if self.request.method in ("GET", "DELETE"):
            return self.request.args
        payload = self.request.get_json(silent=True)
        return payload if payload is not None else {}

    def _parse_raw_params(self):
        if self.input_schema_class is None:
            return {}

        schema = self.input_schema_class()
        try:
            return schema.load(self.raw_params, partial=self.partial)
        except MarshmallowValidationError as exc:
            details = [
                {"field": field, "message": messages[0] if messages else "Invalid value."}
                for field, messages in exc.messages.items()
            ]
            raise BadRequest("Invalid request payload.", details=details)

    def _check_permission(self):
        if self.permission_requirements and not self.current_user.has_permission(*self.permission_requirements):
            raise PermissionError_(
                "This action requires one of the following permissions: "
                + ", ".join(self.permission_requirements)
            )

    def _handle_api_logic(self):
        """Override in subclasses. Return `data` or `(data, status_code)`."""
        raise NotImplementedError

    def run(self):
        result = self._handle_api_logic()
        data, status_code = result if isinstance(result, tuple) else (result, 200)
        if data == "" or data is None:
            return "", status_code
        return jsonify(data), status_code
