from app.extensions import db
from app.models.base import BaseModel


class Form(BaseModel):
    __tablename__ = "forms"

    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    order = db.Column(db.Integer, nullable=False, default=0, index=True)
    status = db.Column(db.Enum("active", "draft", name="form_status"), nullable=False, default="draft", index=True)
    deleted = db.Column(db.Boolean, nullable=False, default=False, index=True)

    fields = db.relationship(
        "Field",
        back_populates="form",
        order_by="Field.order",
        cascade="all, delete-orphan",
    )
    submissions = db.relationship("Submission", back_populates="form")

    def to_json(self, include_fields=True):
        data = super().to_json()
        data.update(
            {
                "title": self.title,
                "description": self.description,
                "order": self.order,
                "status": self.status,
            }
        )
        if include_fields:
            data["fields"] = [field.to_json() for field in self.fields]
        return data
