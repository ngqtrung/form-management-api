from app.bases.api.resource import Resource

from . import methods


class FormSubmitResource(Resource):
    endpoint = "/api/forms/<form_id>/submit"
