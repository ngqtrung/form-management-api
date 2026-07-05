from app.errors import ValidationError
from app.extensions import db
from app.models.submission import Submission
from app.models.submission_answer import SubmissionAnswer
from app.validators.submission_validator import SubmissionValidator

validator = SubmissionValidator()


class SubmissionService:
    def submit(self, form, current_user, answers: dict):
        result = validator.validate(form, answers)
        if not result.is_valid:
            raise ValidationError("Submission has invalid fields.", details=result.errors)

        submission = Submission(form_id=form.id, submitted_by_id=current_user.id)
        db.session.add(submission)

        fields_by_id = {field.id: field for field in form.fields}
        for field_id, value in result.cleaned_data.items():
            field = fields_by_id[field_id]
            submission.answers.append(
                SubmissionAnswer(
                    field_id=field.id,
                    field_label=field.label,
                    field_type=field.type,
                    value=None if value is None else str(value),
                )
            )

        db.session.commit()
        return submission

    def list_submissions(self, current_user, page, per_page):
        query = Submission.query
        if not current_user.has_permission("submissions:view_all"):
            query = query.filter_by(submitted_by_id=current_user.id)

        query = query.order_by(Submission.created_at.desc())
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        return {
            "data": [submission.to_json() for submission in pagination.items],
            "meta": {
                "total": pagination.total,
                "page": page,
                "per_page": per_page,
                "pages": pagination.pages,
            },
        }
