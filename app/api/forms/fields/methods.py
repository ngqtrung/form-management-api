from app.bases.api.method_handler import MethodHandler
from app.services.field_service import FieldService
from app.services.form_service import FormService

from .schemas import PostSchema

form_service = FormService()
service = FieldService()


class Post(MethodHandler):
    permission_requirements = ("fields:manage",)
    input_schema_class = PostSchema

    def _handle_api_logic(self):
        form = form_service.get_form(self.url_params["form_id"])
        field = service.create_field(form, self.payload)
        return field.to_json(), 201
