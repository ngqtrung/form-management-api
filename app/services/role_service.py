from app.errors import BadRequest, NotFound
from app.extensions import db
from app.models.permission import Permission
from app.models.role import Role


class RoleService:
    def list_roles(self):
        return Role.query.order_by(Role.name.asc()).all()

    def get_role(self, role_id):
        role = db.session.get(Role, role_id)
        if role is None:
            raise NotFound(f"Role '{role_id}' was not found.")
        return role

    def create_role(self, name, description):
        if Role.query.filter_by(name=name).first() is not None:
            raise BadRequest(f"A role named '{name}' already exists.")
        role = Role(name=name, description=description)
        db.session.add(role)
        db.session.commit()
        return role

    def update_role(self, role_id, data):
        role = self.get_role(role_id)
        role.update(**data)
        db.session.commit()
        return role

    def delete_role(self, role_id):
        role = self.get_role(role_id)
        db.session.delete(role)
        db.session.commit()

    def set_permissions(self, role_id, permission_codes):
        role = self.get_role(role_id)
        permissions = Permission.query.filter(Permission.code.in_(permission_codes)).all()
        found_codes = {permission.code for permission in permissions}
        missing = set(permission_codes) - found_codes
        if missing:
            raise BadRequest(f"Unknown permission code(s): {', '.join(sorted(missing))}.")
        role.permissions = permissions
        db.session.commit()
        return role
