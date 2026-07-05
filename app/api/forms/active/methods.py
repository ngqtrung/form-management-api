from app.bases.api.method_handler import MethodHandler
from app.services.form_service import FormService

service = FormService()


class Get(MethodHandler):
    permission_requirements = ("forms:view_active",)

    def _handle_api_logic(self):
        return service.list_active_forms()
