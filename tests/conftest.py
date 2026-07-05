import pytest

from app import create_app
from app.extensions import db as _db
from app.models.permission import Permission
from app.models.role import Role
from app.models.user import User
from scripts.seed import PERMISSIONS


@pytest.fixture()
def app():
    application = create_app("config.TestConfig")
    with application.app_context():
        _db.create_all()
        yield application
        _db.session.remove()
        _db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def db(app):
    return _db


def _seed_permissions(db):
    permissions = []
    for code, description in PERMISSIONS:
        permission = Permission(code=code, description=description)
        db.session.add(permission)
        permissions.append(permission)
    db.session.flush()
    return {permission.code: permission for permission in permissions}


@pytest.fixture()
def admin_user(db):
    permissions = _seed_permissions(db)
    role = Role(name="admin", description="Full access", permissions=list(permissions.values()))
    db.session.add(role)
    user = User(email="admin@test.local", full_name="Admin", status="active", roles=[role])
    user.set_password("Admin@123")
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture()
def employee_user(db, admin_user):
    permissions = {p.code: p for p in Permission.query.all()}
    role = Role(
        name="employee",
        description="Employee",
        permissions=[
            permissions["forms:view_active"],
            permissions["submissions:create"],
            permissions["submissions:view_own"],
        ],
    )
    db.session.add(role)
    user = User(email="employee@test.local", full_name="Employee", status="active", roles=[role])
    user.set_password("Employee@123")
    db.session.add(user)
    db.session.commit()
    return user


def auth_headers(client, email, password):
    resp = client.post("/api/auth/login", json={"email": email, "password": password})
    token = resp.get_json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def admin_headers(client, admin_user):
    return auth_headers(client, "admin@test.local", "Admin@123")


@pytest.fixture()
def employee_headers(client, employee_user):
    return auth_headers(client, "employee@test.local", "Employee@123")
