from app.bases.api.method_handler import MethodHandler
from app.services.user_service import UserService

from .schemas import PostSchema

service = UserService()


class Get(MethodHandler):
    permission_requirements = ("users:manage",)

    def _handle_api_logic(self):
        return [user.to_json() for user in service.list_users()]


class Post(MethodHandler):
    permission_requirements = ("users:manage",)
    input_schema_class = PostSchema

    def _handle_api_logic(self):
        user = service.create_user(**self.payload)
        return user.to_json(), 201
