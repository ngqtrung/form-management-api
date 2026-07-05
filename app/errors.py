from flask import jsonify

from app.common.utils import log


class APIError(Exception):
    status_code = 500
    error_code = "ServerError"

    def __init__(self, message, details=None, status_code=None):
        super().__init__(message)
        self.message = message
        self.details = details
        if status_code is not None:
            self.status_code = status_code

    def to_response(self):
        body = {"error": self.error_code, "message": self.message}
        if self.details is not None:
            body["details"] = self.details
        return jsonify(body), self.status_code


class BadRequest(APIError):
    status_code = 400
    error_code = "BadRequest"


class AuthenticationError(APIError):
    status_code = 401
    error_code = "AuthenticationError"

    def __init__(self, message="Authentication required.", details=None):
        super().__init__(message, details)


class PermissionError_(APIError):
    """Named with a trailing underscore to avoid shadowing the Python builtin PermissionError."""

    status_code = 403
    error_code = "PermissionError"

    def __init__(self, message="You do not have permission to perform this action.", details=None):
        super().__init__(message, details)


class NotFound(APIError):
    status_code = 404
    error_code = "NotFound"


class ValidationError(APIError):
    status_code = 422
    error_code = "ValidationError"


class ServerError(APIError):
    status_code = 500
    error_code = "ServerError"

    def __init__(self, message="Internal server error.", details=None):
        super().__init__(message, details)


def register_error_handlers(app):
    @app.errorhandler(APIError)
    def handle_api_error(err):
        if err.status_code >= 500:
            log.exception(err.message)
        return err.to_response()

    @app.errorhandler(404)
    def handle_404(err):
        return NotFound("The requested resource was not found.").to_response()

    @app.errorhandler(405)
    def handle_405(err):
        return BadRequest("This HTTP method is not allowed for this endpoint.").to_response()

    @app.errorhandler(Exception)
    def handle_unexpected_error(err):
        log.exception("Unhandled exception")
        return ServerError().to_response()
