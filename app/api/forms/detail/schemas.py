from marshmallow import Schema, fields, validate

from app.api.forms.schemas import FORM_STATUSES


class PutSchema(Schema):
    title = fields.String(required=False, validate=validate.Length(min=1, max=200))
    description = fields.String(required=False, allow_none=True)
    order = fields.Integer(required=False)
    status = fields.String(required=False, validate=validate.OneOf(FORM_STATUSES))
