from app.bases.api.resource import Resource

from . import methods


class RoleListResource(Resource):
    endpoint = "/api/roles"
