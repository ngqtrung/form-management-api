from marshmallow import Schema, fields, validate


class PutSchema(Schema):
    name = fields.String(required=False, validate=validate.Length(min=1, max=100))
    description = fields.String(required=False, allow_none=True)
