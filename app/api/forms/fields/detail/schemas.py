from marshmallow import Schema, ValidationError, fields, validate, validates_schema

from app.models.field import FIELD_TYPES


class PutSchema(Schema):
    label = fields.String(required=False, validate=validate.Length(min=1, max=200))
    type = fields.String(required=False, validate=validate.OneOf(FIELD_TYPES))
    order = fields.Integer(required=False)
    required = fields.Boolean(required=False)
    options = fields.List(fields.String(), required=False, allow_none=True)
    validation_rules = fields.Dict(required=False, allow_none=True)

    @validates_schema
    def validate_select_has_options(self, data, **kwargs):
        if data.get("type") == "select" and "options" in data and not data.get("options"):
            raise ValidationError("options must be non-empty for type 'select'.", "options")
