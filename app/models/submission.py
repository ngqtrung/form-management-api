from app.extensions import db
from app.models.base import BaseModel


class Submission(BaseModel):
    __tablename__ = "submissions"

    form_id = db.Column(db.String(36), db.ForeignKey("forms.id", ondelete="CASCADE"), nullable=False, index=True)
    submitted_by_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False, index=True)

    form = db.relationship("Form", back_populates="submissions")
    submitted_by = db.relationship("User")
    answers = db.relationship("SubmissionAnswer", back_populates="submission", cascade="all, delete-orphan")

    def to_json(self):
        data = super().to_json()
        data.update(
            {
                "form_id": self.form_id,
                "form_title": self.form.title if self.form else None,
                "submitted_by_id": self.submitted_by_id,
                "submitted_by_email": self.submitted_by.email if self.submitted_by else None,
                "answers": [answer.to_json() for answer in self.answers],
            }
        )
        return data
