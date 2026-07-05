from app.bases.api.resource import Resource

from . import methods


class RefreshResource(Resource):
    endpoint = "/api/auth/refresh"
