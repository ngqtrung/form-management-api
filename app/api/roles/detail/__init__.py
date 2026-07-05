from app.bases.api.resource import Resource

from . import methods


class RoleDetailResource(Resource):
    endpoint = "/api/roles/<role_id>"
