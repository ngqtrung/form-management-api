from marshmallow import Schema, fields


class PostSchema(Schema):
    answers = fields.Dict(required=True)
