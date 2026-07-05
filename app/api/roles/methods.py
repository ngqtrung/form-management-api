from app.bases.api.method_handler import MethodHandler
from app.services.role_service import RoleService

from .schemas import PostSchema

service = RoleService()


class Get(MethodHandler):
    permission_requirements = ("roles:manage",)

    def _handle_api_logic(self):
        return [role.to_json() for role in service.list_roles()]


class Post(MethodHandler):
    permission_requirements = ("roles:manage",)
    input_schema_class = PostSchema

    def _handle_api_logic(self):
        role = service.create_role(**self.payload)
        return role.to_json(), 201
