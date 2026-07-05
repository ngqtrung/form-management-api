from app.bases.api.resource import Resource

from . import methods


class LogoutResource(Resource):
    endpoint = "/api/auth/logout"
