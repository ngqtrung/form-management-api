from marshmallow import Schema, fields


class PostSchema(Schema):
    permission_codes = fields.List(fields.String(), required=True)
