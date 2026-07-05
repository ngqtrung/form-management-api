from sqlalchemy.exc import IntegrityError

from app.errors import BadRequest, NotFound
from app.extensions import db
from app.models.role import Role
from app.models.user import User


class UserService:
    def list_users(self):
        return User.query.order_by(User.created_at.asc()).all()

    def get_user(self, user_id):
        user = db.session.get(User, user_id)
        if user is None:
            raise NotFound(f"User '{user_id}' was not found.")
        return user

    def _resolve_roles(self, role_names):
        if not role_names:
            return []
        roles = Role.query.filter(Role.name.in_(role_names)).all()
        found_names = {role.name for role in roles}
        missing = set(role_names) - found_names
        if missing:
            raise BadRequest(f"Unknown role(s): {', '.join(sorted(missing))}.")
        return roles

    def create_user(self, email, password, full_name, status, role_names):
        if User.query.filter_by(email=email).first() is not None:
            raise BadRequest(f"A user with email '{email}' already exists.")

        user = User(email=email, full_name=full_name, status=status)
        user.set_password(password)
        user.roles = self._resolve_roles(role_names)
        db.session.add(user)
        db.session.commit()
        return user

    def update_user(self, user_id, data):
        user = self.get_user(user_id)

        if "password" in data:
            user.set_password(data.pop("password"))
        if "role_names" in data:
            user.roles = self._resolve_roles(data.pop("role_names"))

        user.update(**data)
        db.session.commit()
        return user

    def delete_user(self, user_id):
        user = self.get_user(user_id)
        try:
            db.session.delete(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise BadRequest("Cannot delete a user that has existing submissions.")
