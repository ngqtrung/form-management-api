import pytest


@pytest.fixture()
def form_id(client, admin_headers):
    resp = client.post("/api/forms", json={"title": "Form with fields"}, headers=admin_headers)
    return resp.get_json()["id"]


def test_create_text_field(client, admin_headers, form_id):
    resp = client.post(
        f"/api/forms/{form_id}/fields",
        json={"label": "Name", "type": "text", "required": True, "order": 1},
        headers=admin_headers,
    )
    assert resp.status_code == 201
    assert resp.get_json()["type"] == "text"


def test_create_select_field_without_options_fails(client, admin_headers, form_id):
    resp = client.post(
        f"/api/forms/{form_id}/fields",
        json={"label": "Department", "type": "select", "order": 1},
        headers=admin_headers,
    )
    assert resp.status_code == 400


def test_create_select_field_with_options_succeeds(client, admin_headers, form_id):
    resp = client.post(
        f"/api/forms/{form_id}/fields",
        json={"label": "Department", "type": "select", "order": 1, "options": ["A", "B"]},
        headers=admin_headers,
    )
    assert resp.status_code == 201
    assert resp.get_json()["options"] == ["A", "B"]


def test_create_field_rejects_unknown_type(client, admin_headers, form_id):
    resp = client.post(
        f"/api/forms/{form_id}/fields",
        json={"label": "Bad", "type": "unknown", "order": 1},
        headers=admin_headers,
    )
    assert resp.status_code == 400


def test_update_field(client, admin_headers, form_id):
    field_id = client.post(
        f"/api/forms/{form_id}/fields",
        json={"label": "Name", "type": "text", "order": 1},
        headers=admin_headers,
    ).get_json()["id"]

    resp = client.put(
        f"/api/forms/{form_id}/fields/{field_id}", json={"label": "Full name"}, headers=admin_headers
    )
    assert resp.status_code == 200
    assert resp.get_json()["label"] == "Full name"


def test_delete_field(client, admin_headers, form_id):
    field_id = client.post(
        f"/api/forms/{form_id}/fields",
        json={"label": "Name", "type": "text", "order": 1},
        headers=admin_headers,
    ).get_json()["id"]

    resp = client.delete(f"/api/forms/{form_id}/fields/{field_id}", headers=admin_headers)
    assert resp.status_code == 204

    resp = client.get(f"/api/forms/{form_id}", headers=admin_headers)
    assert resp.get_json()["fields"] == []


def test_employee_cannot_manage_fields(client, employee_headers, form_id):
    resp = client.post(
        f"/api/forms/{form_id}/fields",
        json={"label": "Name", "type": "text", "order": 1},
        headers=employee_headers,
    )
    assert resp.status_code == 403
