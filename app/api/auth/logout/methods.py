from datetime import datetime, timezone

from app.auth.decorators import decode_bearer_token
from app.bases.api.method_handler import MethodHandler
from app.services.auth_service import AuthService

service = AuthService()


class Post(MethodHandler):
    def _handle_api_logic(self):
        payload = decode_bearer_token(required_type="access")
        expires_at = datetime.fromtimestamp(payload["exp"], tz=timezone.utc).replace(tzinfo=None)
        service.logout(payload["jti"], expires_at)
        return "", 204
