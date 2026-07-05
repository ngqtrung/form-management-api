from app.bases.api.method_handler import MethodHandler
from app.services.form_service import FormService

from .schemas import GetSchema, PostSchema

service = FormService()


class Get(MethodHandler):
    permission_requirements = ("forms:view_all",)
    input_schema_class = GetSchema

    def _handle_api_logic(self):
        return service.list_forms(**self.payload)


class Post(MethodHandler):
    permission_requirements = ("forms:manage",)
    input_schema_class = PostSchema

    def _handle_api_logic(self):
        form = service.create_form(self.payload)
        return form.to_json(), 201
