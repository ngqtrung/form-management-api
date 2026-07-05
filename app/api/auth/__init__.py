from app.bases.api.resource import Resource

from . import methods


class LoginResource(Resource):
    endpoint = "/api/auth/login"
