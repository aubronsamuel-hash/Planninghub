from fastapi.testclient import TestClient

from planninghub.adapters.fastapi_app.app import app

client = TestClient(app)


def test_evaluate_reservation_valid_payload() -> None:
    payload = {
        "organization_id": "org-1",
        "reservation_id": "res-1",
        "resource_id": "room-1",
        "starts_at_utc_iso": "2024-01-01T08:00:00",
        "ends_at_utc_iso": "2024-01-01T09:00:00",
        "timezone": "UTC",
    }

    response = client.post("/reservations/evaluate", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert "reservation_id" in body
    assert "conflict" in body


def test_evaluate_reservation_invalid_datetime() -> None:
    payload = {
        "organization_id": "org-1",
        "reservation_id": "res-1",
        "resource_id": "room-1",
        "starts_at_utc_iso": "bad",
        "ends_at_utc_iso": "2024-01-01T09:00:00",
        "timezone": "UTC",
    }

    response = client.post("/reservations/evaluate", json=payload)

    assert response.status_code == 400
