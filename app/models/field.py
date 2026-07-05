from app.extensions import db
from app.models.base import BaseModel

FIELD_TYPES = ("text", "number", "date", "color", "select")


class Field(BaseModel):
    __tablename__ = "fields"

    form_id = db.Column(db.String(36), db.ForeignKey("forms.id", ondelete="CASCADE"), nullable=False, index=True)
    label = db.Column(db.String(200), nullable=False)
    type = db.Column(db.Enum(*FIELD_TYPES, name="field_type"), nullable=False)
    order = db.Column(db.Integer, nullable=False, default=0)
    required = db.Column(db.Boolean, nullable=False, default=False)
    options = db.Column(db.JSON, nullable=True)  # list[str], only for type == "select"
    validation_rules = db.Column(db.JSON, nullable=True)  # e.g. {"max_length": 150} / {"min": 10, "max": 90}

    form = db.relationship("Form", back_populates="fields")

    def to_json(self):
        data = super().to_json()
        data.update(
            {
                "form_id": self.form_id,
                "label": self.label,
                "type": self.type,
                "order": self.order,
                "required": self.required,
                "options": self.options,
                "validation_rules": self.validation_rules,
            }
        )
        return data
