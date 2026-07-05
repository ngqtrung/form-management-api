from app.extensions import db
from app.models.base import BaseModel


class Permission(BaseModel):
    __tablename__ = "permissions"

    code = db.Column(db.String(100), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)

    def to_json(self):
        data = super().to_json()
        data.update({"code": self.code, "description": self.description})
        return data
