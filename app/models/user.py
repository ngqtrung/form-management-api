from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db
from app.models.base import BaseModel
from app.models.user_role import UserRole


class User(BaseModel):
    __tablename__ = "users"

    email = db.Column(db.String(200), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(200), nullable=True)
    status = db.Column(db.Enum("active", "inactive", name="user_status"), nullable=False, default="active")

    roles = db.relationship("Role", secondary=UserRole.__table__, backref=db.backref("users", lazy="selectin"))

    def set_password(self, raw_password):
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password_hash, raw_password)

    def role_names(self):
        return [role.name for role in self.roles]

    def permission_codes(self):
        codes = set()
        for role in self.roles:
            codes |= role.permission_codes()
        return codes

    def has_permission(self, *codes):
        return bool(self.permission_codes() & set(codes))

    def to_json(self):
        data = super().to_json()
        data.update(
            {
                "email": self.email,
                "full_name": self.full_name,
                "status": self.status,
                "roles": [role.name for role in self.roles],
            }
        )
        return data
