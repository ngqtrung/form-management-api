from app.bases.api.method_handler import MethodHandler
from app.services.role_service import RoleService

from .schemas import PutSchema

service = RoleService()


class Put(MethodHandler):
    permission_requirements = ("roles:manage",)
    input_schema_class = PutSchema
    partial = True

    def _handle_api_logic(self):
        role = service.update_role(self.url_params["role_id"], self.payload)
        return role.to_json()


class Delete(MethodHandler):
    permission_requirements = ("roles:manage",)

    def _handle_api_logic(self):
        service.delete_role(self.url_params["role_id"])
        return "", 204
