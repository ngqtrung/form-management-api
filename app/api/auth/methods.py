from app.bases.api.method_handler import MethodHandler
from app.services.auth_service import AuthService

from .schemas import PostSchema

service = AuthService()


class Post(MethodHandler):
    auth_required = False
    input_schema_class = PostSchema

    def _handle_api_logic(self):
        return service.login(**self.payload)
