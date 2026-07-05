from app.bases.api.resource import Resource

from . import methods


class FieldDetailResource(Resource):
    endpoint = "/api/forms/<form_id>/fields/<field_id>"
