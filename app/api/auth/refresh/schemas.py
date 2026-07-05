from marshmallow import Schema, fields


class PostSchema(Schema):
    refresh_token = fields.String(required=True)
