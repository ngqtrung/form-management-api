from app.bases.api.method_handler import MethodHandler
from app.services.submission_service import SubmissionService

from .schemas import GetSchema

service = SubmissionService()


class Get(MethodHandler):
    permission_requirements = ("submissions:view_own", "submissions:view_all")
    input_schema_class = GetSchema

    def _handle_api_logic(self):
        return service.list_submissions(self.current_user, **self.payload)
