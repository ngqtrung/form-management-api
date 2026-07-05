import pytest
from datetime import date, timedelta


@pytest.fixture()
def active_form(client, admin_headers):
    form_id = client.post(
        "/api/forms", json={"title": "Onboarding", "status": "active"}, headers=admin_headers
    ).get_json()["id"]

    fields = {}
    for payload in [
        {"label": "Name", "type": "text", "order": 1, "required": True},
        {"label": "Age", "type": "number", "order": 2, "required": True},
        {"label": "Start date", "type": "date", "order": 3, "required": True},
        {"label": "Favorite color", "type": "color", "order": 4, "required": False},
        {"label": "Team", "type": "select", "order": 5, "required": True, "options": ["A", "B"]},
    ]:
        resp = client.post(f"/api/forms/{form_id}/fields", json=payload, headers=admin_headers)
        fields[payload["label"]] = resp.get_json()["id"]

    return {"form_id": form_id, "fields": fields}


def valid_answers(fields):
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    return {
        fields["Name"]: "Alice",
        fields["Age"]: 30,
        fields["Start date"]: tomorrow,
        fields["Favorite color"]: "#ff0000",
        fields["Team"]: "A",
    }


def test_employee_can_submit_valid_form(client, employee_headers, active_form):
    resp = client.post(
        f"/api/forms/{active_form['form_id']}/submit",
        json={"answers": valid_answers(active_form["fields"])},
        headers=employee_headers,
    )
    assert resp.status_code == 201
    assert len(resp.get_json()["answers"]) == 5


def test_submit_missing_required_field_returns_422_with_details(client, employee_headers, active_form):
    answers = valid_answers(active_form["fields"])
    del answers[active_form["fields"]["Name"]]

    resp = client.post(
        f"/api/forms/{active_form['form_id']}/submit", json={"answers": answers}, headers=employee_headers
    )
    assert resp.status_code == 422
    body = resp.get_json()
    assert body["error"] == "ValidationError"
    assert any(err["field_id"] == active_form["fields"]["Name"] for err in body["details"])


def test_submit_invalid_number_out_of_range(client, employee_headers, active_form):
    answers = valid_answers(active_form["fields"])
    answers[active_form["fields"]["Age"]] = 999

    resp = client.post(
        f"/api/forms/{active_form['form_id']}/submit", json={"answers": answers}, headers=employee_headers
    )
    assert resp.status_code == 422


def test_submit_invalid_color(client, employee_headers, active_form):
    answers = valid_answers(active_form["fields"])
    answers[active_form["fields"]["Favorite color"]] = "not-a-color"

    resp = client.post(
        f"/api/forms/{active_form['form_id']}/submit", json={"answers": answers}, headers=employee_headers
    )
    assert resp.status_code == 422


def test_submit_past_date_rejected(client, employee_headers, active_form):
    answers = valid_answers(active_form["fields"])
    answers[active_form["fields"]["Start date"]] = "2000-01-01"

    resp = client.post(
        f"/api/forms/{active_form['form_id']}/submit", json={"answers": answers}, headers=employee_headers
    )
    assert resp.status_code == 422


def test_submit_select_invalid_option(client, employee_headers, active_form):
    answers = valid_answers(active_form["fields"])
    answers[active_form["fields"]["Team"]] = "Z"

    resp = client.post(
        f"/api/forms/{active_form['form_id']}/submit", json={"answers": answers}, headers=employee_headers
    )
    assert resp.status_code == 422


def test_employee_sees_only_own_submissions(client, employee_headers, admin_headers, active_form):
    client.post(
        f"/api/forms/{active_form['form_id']}/submit",
        json={"answers": valid_answers(active_form["fields"])},
        headers=employee_headers,
    )

    resp = client.get("/api/submissions", headers=employee_headers)
    assert resp.status_code == 200
    assert resp.get_json()["meta"]["total"] == 1


def test_admin_sees_all_submissions(client, employee_headers, admin_headers, active_form):
    client.post(
        f"/api/forms/{active_form['form_id']}/submit",
        json={"answers": valid_answers(active_form["fields"])},
        headers=employee_headers,
    )

    resp = client.get("/api/submissions", headers=admin_headers)
    assert resp.status_code == 200
    assert resp.get_json()["meta"]["total"] == 1


def test_deleting_form_keeps_submission_history(client, employee_headers, admin_headers, active_form):
    client.post(
        f"/api/forms/{active_form['form_id']}/submit",
        json={"answers": valid_answers(active_form["fields"])},
        headers=employee_headers,
    )

    client.delete(f"/api/forms/{active_form['form_id']}", headers=admin_headers)

    resp = client.get("/api/submissions", headers=admin_headers)
    assert resp.get_json()["meta"]["total"] == 1
