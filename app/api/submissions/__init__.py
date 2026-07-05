from app.bases.api.resource import Resource

from . import methods


class SubmissionListResource(Resource):
    endpoint = "/api/submissions"
