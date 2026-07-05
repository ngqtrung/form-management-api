from marshmallow import Schema, fields, validate

FORM_STATUSES = ("active", "draft")


class GetSchema(Schema):
    page = fields.Integer(required=False, load_default=1, validate=validate.Range(min=1))
    per_page = fields.Integer(required=False, load_default=20, validate=validate.Range(min=1, max=100))
    status = fields.String(required=False, allow_none=True, validate=validate.OneOf(FORM_STATUSES))


class PostSchema(Schema):
    title = fields.String(required=True, validate=validate.Length(min=1, max=200))
    description = fields.String(required=False, allow_none=True, load_default=None)
    order = fields.Integer(required=False, load_default=0)
    status = fields.String(required=False, load_default="draft", validate=validate.OneOf(FORM_STATUSES))
