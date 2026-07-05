from app.errors import NotFound
from app.extensions import db
from app.models.field import Field


class FieldService:
    def create_field(self, form, data):
        field = Field(form_id=form.id, **data)
        db.session.add(field)
        db.session.commit()
        return field

    def get_field(self, form_id, field_id):
        field = Field.query.filter_by(id=field_id, form_id=form_id).first()
        if field is None:
            raise NotFound(f"Field '{field_id}' was not found on form '{form_id}'.")
        return field

    def update_field(self, form_id, field_id, data):
        field = self.get_field(form_id, field_id)
        field.update(**data)
        db.session.commit()
        return field

    def delete_field(self, form_id, field_id):
        field = self.get_field(form_id, field_id)
        db.session.delete(field)
        db.session.commit()
