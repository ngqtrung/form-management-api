from app.extensions import db
from app.models.base import BaseModel


class SubmissionAnswer(BaseModel):
    __tablename__ = "submission_answers"

    submission_id = db.Column(
        db.String(36), db.ForeignKey("submissions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    field_id = db.Column(db.String(36), db.ForeignKey("fields.id", ondelete="SET NULL"), nullable=True, index=True)
    field_label = db.Column(db.String(200), nullable=False)  # snapshot at submit time
    field_type = db.Column(db.String(20), nullable=False)  # snapshot at submit time
    value = db.Column(db.Text, nullable=True)

    submission = db.relationship("Submission", back_populates="answers")
    field = db.relationship("Field")

    def to_json(self):
        data = super().to_json()
        data.update(
            {
                "field_id": self.field_id,
                "field_label": self.field_label,
                "field_type": self.field_type,
                "value": self.value,
            }
        )
        return data
