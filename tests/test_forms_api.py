def create_form(client, headers, **overrides):
    payload = {"title": "Test Form", "description": "desc", "order": 1, "status": "draft"}
    payload.update(overrides)
    return client.post("/api/forms", json=payload, headers=headers)


def test_create_form(client, admin_headers):
    resp = create_form(client, admin_headers)
    assert resp.status_code == 201
    body = resp.get_json()
    assert body["title"] == "Test Form"
    assert body["status"] == "draft"
    assert body["fields"] == []


def test_create_form_requires_title(client, admin_headers):
    resp = client.post("/api/forms", json={"description": "no title"}, headers=admin_headers)
    assert resp.status_code == 400


def test_list_forms_paginated(client, admin_headers):
    for i in range(3):
        create_form(client, admin_headers, title=f"Form {i}", order=i)

    resp = client.get("/api/forms?page=1&per_page=2", headers=admin_headers)
    assert resp.status_code == 200
    body = resp.get_json()
    assert len(body["data"]) == 2
    assert body["meta"]["total"] == 3


def test_get_form_detail(client, admin_headers):
    form_id = create_form(client, admin_headers).get_json()["id"]
    resp = client.get(f"/api/forms/{form_id}", headers=admin_headers)
    assert resp.status_code == 200
    assert resp.get_json()["id"] == form_id


def test_get_form_not_found(client, admin_headers):
    resp = client.get("/api/forms/does-not-exist", headers=admin_headers)
    assert resp.status_code == 404


def test_update_form(client, admin_headers):
    form_id = create_form(client, admin_headers).get_json()["id"]
    resp = client.put(f"/api/forms/{form_id}", json={"status": "active"}, headers=admin_headers)
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "active"


def test_delete_form_is_soft_delete_and_hides_from_list(client, admin_headers):
    form_id = create_form(client, admin_headers).get_json()["id"]

    resp = client.delete(f"/api/forms/{form_id}", headers=admin_headers)
    assert resp.status_code == 204

    resp = client.get(f"/api/forms/{form_id}", headers=admin_headers)
    assert resp.status_code == 404

    resp = client.get("/api/forms", headers=admin_headers)
    ids = [form["id"] for form in resp.get_json()["data"]]
    assert form_id not in ids


def test_employee_sees_only_active_forms(client, admin_headers, employee_headers):
    create_form(client, admin_headers, title="Draft form", status="draft")
    create_form(client, admin_headers, title="Active form", status="active")

    resp = client.get("/api/forms/active", headers=employee_headers)
    assert resp.status_code == 200
    titles = [form["title"] for form in resp.get_json()]
    assert titles == ["Active form"]
