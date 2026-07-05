from app.bases.api.resource import Resource

from . import methods


class FormDetailResource(Resource):
    endpoint = "/api/forms/<form_id>"
