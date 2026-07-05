"""Idempotent seed script: fixed permissions, admin/employee roles, demo users and a demo form.

Run via: python run.py seed
"""

from app.extensions import db
from app.models.field import Field
from app.models.form import Form
from app.models.permission import Permission
from app.models.role import Role
from app.models.user import User

PERMISSIONS = [
    ("forms:manage", "Create, update and delete forms"),
    ("forms:view_all", "View all forms, including drafts"),
    ("forms:view_active", "View active forms"),
    ("fields:manage", "Create, update and delete fields"),
    ("submissions:create", "Submit a form"),
    ("submissions:view_own", "View submissions created by the current user"),
    ("submissions:view_all", "View all submissions from every user"),
    ("users:manage", "Create, update and delete users"),
    ("roles:manage", "Create, update and delete roles, and assign permissions to them"),
]

EMPLOYEE_PERMISSION_CODES = ["forms:view_active", "submissions:create", "submissions:view_own"]

DEMO_USERS = [
    {
        "email": "admin@example.com",
        "password": "Admin@123",
        "full_name": "System Admin",
        "role_name": "admin",
    },
    {
        "email": "employee@example.com",
        "password": "Employee@123",
        "full_name": "Demo Employee",
        "role_name": "employee",
    },
]


def _get_or_create_permission(code, description):
    permission = Permission.query.filter_by(code=code).first()
    if permission is None:
        permission = Permission(code=code, description=description)
        db.session.add(permission)
        db.session.flush()
    return permission


def _get_or_create_role(name, description, permissions):
    role = Role.query.filter_by(name=name).first()
    if role is None:
        role = Role(name=name, description=description)
        db.session.add(role)
        db.session.flush()
    role.permissions = permissions
    return role


def _get_or_create_user(email, password, full_name, role):
    user = User.query.filter_by(email=email).first()
    if user is None:
        user = User(email=email, full_name=full_name, status="active")
        user.set_password(password)
        db.session.add(user)
        db.session.flush()
    user.roles = [role]
    return user


def _seed_demo_form():
    if Form.query.filter_by(title="Employee Onboarding").first() is not None:
        return

    form = Form(title="Employee Onboarding", description="Basic onboarding info form", order=1, status="active")
    db.session.add(form)
    db.session.flush()

    fields = [
        Field(form_id=form.id, label="Full name", type="text", order=1, required=True),
        Field(form_id=form.id, label="Age", type="number", order=2, required=True),
        Field(form_id=form.id, label="Start date", type="date", order=3, required=True),
        Field(form_id=form.id, label="Favorite color", type="color", order=4, required=False),
        Field(
            form_id=form.id,
            label="Department",
            type="select",
            order=5,
            required=True,
            options=["Engineering", "Sales", "Marketing", "Support"],
        ),
    ]
    db.session.add_all(fields)


def seed():
    permissions = [_get_or_create_permission(code, description) for code, description in PERMISSIONS]
    permissions_by_code = {permission.code: permission for permission in permissions}

    admin_role = _get_or_create_role("admin", "Full access to everything", permissions)
    employee_role = _get_or_create_role(
        "employee",
        "Can view active forms, submit them and view their own submissions",
        [permissions_by_code[code] for code in EMPLOYEE_PERMISSION_CODES],
    )

    roles_by_name = {"admin": admin_role, "employee": employee_role}
    for demo_user in DEMO_USERS:
        _get_or_create_user(
            demo_user["email"],
            demo_user["password"],
            demo_user["full_name"],
            roles_by_name[demo_user["role_name"]],
        )

    _seed_demo_form()

    db.session.commit()
    print("Seed complete. Demo accounts:")
    for demo_user in DEMO_USERS:
        print(f"  {demo_user['email']} / {demo_user['password']} ({demo_user['role_name']})")
