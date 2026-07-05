from app.bases.api.resource import Resource

from . import methods


class FieldListResource(Resource):
    endpoint = "/api/forms/<form_id>/fields"
