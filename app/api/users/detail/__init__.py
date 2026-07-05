from app.bases.api.resource import Resource

from . import methods


class UserDetailResource(Resource):
    endpoint = "/api/users/<user_id>"
