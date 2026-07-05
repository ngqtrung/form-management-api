from app.extensions import db
from app.models.base import BaseModel
from app.models.role_permission import RolePermission


class Role(BaseModel):
    __tablename__ = "roles"

    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)

    permissions = db.relationship(
        "Permission", secondary=RolePermission.__table__, backref=db.backref("roles", lazy="selectin")
    )

    def permission_codes(self):
        return {permission.code for permission in self.permissions}

    def to_json(self):
        data = super().to_json()
        data.update(
            {
                "name": self.name,
                "description": self.description,
                "permissions": [permission.to_json() for permission in self.permissions],
            }
        )
        return data
