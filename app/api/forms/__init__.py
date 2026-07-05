from app.bases.api.resource import Resource

from . import methods


class FormListResource(Resource):
    endpoint = "/api/forms"
