from app.bases.api.method_handler import MethodHandler
from app.services.form_service import FormService

from .schemas import PutSchema

service = FormService()


class Get(MethodHandler):
    permission_requirements = ("forms:view_all",)

    def _handle_api_logic(self):
        form = service.get_form(self.url_params["form_id"])
        return form.to_json()


class Put(MethodHandler):
    permission_requirements = ("forms:manage",)
    input_schema_class = PutSchema
    partial = True

    def _handle_api_logic(self):
        form = service.update_form(self.url_params["form_id"], self.payload)
        return form.to_json()


class Delete(MethodHandler):
    permission_requirements = ("forms:manage",)

    def _handle_api_logic(self):
        service.delete_form(self.url_params["form_id"])
        return "", 204
