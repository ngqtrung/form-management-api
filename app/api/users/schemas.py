from marshmallow import Schema, fields, validate

USER_STATUSES = ("active", "inactive")


class PostSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6))
    full_name = fields.String(required=False, allow_none=True, load_default=None)
    status = fields.String(required=False, load_default="active", validate=validate.OneOf(USER_STATUSES))
    role_names = fields.List(fields.String(), required=False, load_default=list)
