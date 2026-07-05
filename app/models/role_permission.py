from app.extensions import db


class RolePermission(db.Model):
    __tablename__ = "role_permission"

    role_id = db.Column(db.String(36), db.ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)
    permission_id = db.Column(
        db.String(36), db.ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True
    )
