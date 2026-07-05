from marshmallow import Schema, fields, validate


class PostSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    description = fields.String(required=False, allow_none=True, load_default=None)
