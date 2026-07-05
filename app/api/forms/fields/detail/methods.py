from app.bases.api.method_handler import MethodHandler
from app.services.field_service import FieldService

from .schemas import PutSchema

service = FieldService()


class Put(MethodHandler):
    permission_requirements = ("fields:manage",)
    input_schema_class = PutSchema
    partial = True

    def _handle_api_logic(self):
        field = service.update_field(self.url_params["form_id"], self.url_params["field_id"], self.payload)
        return field.to_json()


class Delete(MethodHandler):
    permission_requirements = ("fields:manage",)

    def _handle_api_logic(self):
        service.delete_field(self.url_params["form_id"], self.url_params["field_id"])
        return "", 204
