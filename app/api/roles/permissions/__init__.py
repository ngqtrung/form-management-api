from app.bases.api.resource import Resource

from . import methods


class RolePermissionsResource(Resource):
    endpoint = "/api/roles/<role_id>/permissions"
