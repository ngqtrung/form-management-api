from app.bases.api.method_handler import MethodHandler
from app.models.permission import Permission


class Get(MethodHandler):
    permission_requirements = ("roles:manage",)

    def _handle_api_logic(self):
        permissions = Permission.query.order_by(Permission.code.asc()).all()
        return [permission.to_json() for permission in permissions]
