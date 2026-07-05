from app.bases.api.method_handler import MethodHandler
from app.services.form_service import FormService
from app.services.submission_service import SubmissionService

from .schemas import PostSchema

form_service = FormService()
service = SubmissionService()


class Post(MethodHandler):
    permission_requirements = ("submissions:create",)
    input_schema_class = PostSchema

    def _handle_api_logic(self):
        form = form_service.get_form(self.url_params["form_id"])
        submission = service.submit(form, self.current_user, self.payload["answers"])
        return submission.to_json(), 201
