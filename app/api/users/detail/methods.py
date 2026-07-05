from app.bases.api.method_handler import MethodHandler
from app.services.user_service import UserService

from .schemas import PutSchema

service = UserService()


class Put(MethodHandler):
    permission_requirements = ("users:manage",)
    input_schema_class = PutSchema
    partial = True

    def _handle_api_logic(self):
        user = service.update_user(self.url_params["user_id"], self.payload)
        return user.to_json()


class Delete(MethodHandler):
    permission_requirements = ("users:manage",)

    def _handle_api_logic(self):
        service.delete_user(self.url_params["user_id"])
        return "", 204
