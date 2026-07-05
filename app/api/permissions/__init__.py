from app.bases.api.resource import Resource

from . import methods


class PermissionListResource(Resource):
    endpoint = "/api/permissions"
