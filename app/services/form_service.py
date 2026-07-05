from app.errors import NotFound
from app.extensions import db
from app.models.form import Form


class FormService:
    def list_forms(self, page, per_page, status=None):
        query = Form.query.filter_by(deleted=False)
        if status:
            query = query.filter_by(status=status)
        query = query.order_by(Form.order.asc())

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        return {
            "data": [form.to_json(include_fields=False) for form in pagination.items],
            "meta": {
                "total": pagination.total,
                "page": page,
                "per_page": per_page,
                "pages": pagination.pages,
            },
        }

    def list_active_forms(self):
        forms = (
            Form.query.filter_by(deleted=False, status="active").order_by(Form.order.asc()).all()
        )
        return [form.to_json() for form in forms]

    def get_form(self, form_id):
        form = Form.query.filter_by(id=form_id, deleted=False).first()
        if form is None:
            raise NotFound(f"Form '{form_id}' was not found.")
        return form

    def create_form(self, data):
        form = Form(**data)
        db.session.add(form)
        db.session.commit()
        return form

    def update_form(self, form_id, data):
        form = self.get_form(form_id)
        form.update(**data)
        db.session.commit()
        return form

    def delete_form(self, form_id):
        form = self.get_form(form_id)
        form.deleted = True
        db.session.commit()
