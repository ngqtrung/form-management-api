from app.bases.api.resource import Resource

from . import methods


class FormActiveResource(Resource):
    endpoint = "/api/forms/active"
