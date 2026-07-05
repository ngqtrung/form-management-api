def test_login_succeeds_with_correct_credentials(client, admin_user):
    resp = client.post("/api/auth/login", json={"email": "admin@test.local", "password": "Admin@123"})
    assert resp.status_code == 200
    body = resp.get_json()
    assert "access_token" in body
    assert "refresh_token" in body
    assert body["user"]["email"] == "admin@test.local"


def test_login_fails_with_wrong_password(client, admin_user):
    resp = client.post("/api/auth/login", json={"email": "admin@test.local", "password": "wrong"})
    assert resp.status_code == 401
    assert resp.get_json()["error"] == "AuthenticationError"


def test_login_fails_with_unknown_email(client):
    resp = client.post("/api/auth/login", json={"email": "nobody@test.local", "password": "whatever"})
    assert resp.status_code == 401


def test_protected_endpoint_requires_token(client):
    resp = client.get("/api/forms")
    assert resp.status_code == 401


def test_protected_endpoint_rejects_invalid_token(client):
    resp = client.get("/api/forms", headers={"Authorization": "Bearer not-a-real-token"})
    assert resp.status_code == 401


def test_employee_cannot_access_admin_only_endpoint(client, employee_headers):
    resp = client.get("/api/forms", headers=employee_headers)
    assert resp.status_code == 403
    assert resp.get_json()["error"] == "PermissionError"


def test_admin_can_access_admin_only_endpoint(client, admin_headers):
    resp = client.get("/api/forms", headers=admin_headers)
    assert resp.status_code == 200


def test_refresh_issues_new_access_token(client, admin_user):
    login_resp = client.post("/api/auth/login", json={"email": "admin@test.local", "password": "Admin@123"})
    refresh_token = login_resp.get_json()["refresh_token"]

    resp = client.post("/api/auth/refresh", json={"refresh_token": refresh_token})
    assert resp.status_code == 200
    assert "access_token" in resp.get_json()


def test_refresh_rejects_access_token(client, admin_user):
    login_resp = client.post("/api/auth/login", json={"email": "admin@test.local", "password": "Admin@123"})
    access_token = login_resp.get_json()["access_token"]

    resp = client.post("/api/auth/refresh", json={"refresh_token": access_token})
    assert resp.status_code == 401


def test_logout_revokes_access_token(client, admin_user):
    login_resp = client.post("/api/auth/login", json={"email": "admin@test.local", "password": "Admin@123"})
    access_token = login_resp.get_json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    resp = client.post("/api/auth/logout", headers=headers)
    assert resp.status_code == 204

    resp = client.get("/api/forms", headers=headers)
    assert resp.status_code == 401
