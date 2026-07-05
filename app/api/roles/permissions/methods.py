from app.bases.api.method_handler import MethodHandler
from app.services.role_service import RoleService

from .schemas import PostSchema

service = RoleService()


class Post(MethodHandler):
    permission_requirements = ("roles:manage",)
    input_schema_class = PostSchema

    def _handle_api_logic(self):
        role = service.set_permissions(self.url_params["role_id"], self.payload["permission_codes"])
        return role.to_json()
