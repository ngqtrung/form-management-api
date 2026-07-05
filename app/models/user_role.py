from app.extensions import db


class UserRole(db.Model):
    __tablename__ = "user_role"

    user_id = db.Column(db.String(36), db.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    role_id = db.Column(db.String(36), db.ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)
