from marshmallow import Schema, fields, validate

from app.api.users.schemas import USER_STATUSES


class PutSchema(Schema):
    password = fields.String(required=False, validate=validate.Length(min=6))
    full_name = fields.String(required=False, allow_none=True)
    status = fields.String(required=False, validate=validate.OneOf(USER_STATUSES))
    role_names = fields.List(fields.String(), required=False)
