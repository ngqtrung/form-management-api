from app.bases.api.resource import Resource

from . import methods


class UserListResource(Resource):
    endpoint = "/api/users"
