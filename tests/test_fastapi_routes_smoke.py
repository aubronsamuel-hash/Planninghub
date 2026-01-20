from fastapi.testclient import TestClient

from planninghub.adapters.http.fastapi_app import create_app


def create_client(monkeypatch) -> TestClient:
    monkeypatch.setenv("PLANNINGHUB_PERSISTENCE_BACKEND", "memory")
    app = create_app()
    return TestClient(app)


def test_create_reservation_success(monkeypatch) -> None:
    client = create_client(monkeypatch)
    payload = {
        "organization_id": "org-1",
        "resource_id": None,
        "starts_at_utc": "2024-01-01T08:00:00",
        "ends_at_utc": "2024-01-01T09:00:00",
        "timezone": "UTC",
        "economic_value": None,
    }

    response = client.post("/reservations", json=payload)

    assert response.status_code == 200
    body = response.json()
    reservation = body["reservation"]
    assert reservation["organization_id"] == "org-1"
    assert reservation["resource_id"] is None
    assert reservation["economic_value"] is None
    assert reservation["starts_at_utc"] == "2024-01-01T08:00:00"
    assert reservation["ends_at_utc"] == "2024-01-01T09:00:00"


def test_get_reservation_success(monkeypatch) -> None:
    client = create_client(monkeypatch)
    payload = {
        "organization_id": "org-1",
        "resource_id": "room-1",
        "starts_at_utc": "2024-01-02T10:00:00",
        "ends_at_utc": "2024-01-02T11:00:00",
        "timezone": "UTC",
        "economic_value": 120.5,
    }

    create_response = client.post("/reservations", json=payload)
    reservation_id = create_response.json()["reservation"]["id"]

    response = client.get(f"/reservations/{reservation_id}")

    assert response.status_code == 200
    reservation = response.json()["reservation"]
    assert reservation["resource_id"] == "room-1"
    assert reservation["economic_value"] == 120.5


def test_get_reservation_not_found_message(monkeypatch) -> None:
    client = create_client(monkeypatch)

    response = client.get("/reservations/res-404")

    assert response.status_code == 404
    body = response.json()
    error = body.get("error", "")
    assert "error" in body
    assert not error.startswith("\"")
    assert not error.endswith("\"")


def test_list_reservations_includes_created(monkeypatch) -> None:
    client = create_client(monkeypatch)
    payload = {
        "organization_id": "org-2",
        "resource_id": "room-2",
        "starts_at_utc": "2024-01-03T08:00:00",
        "ends_at_utc": "2024-01-03T09:00:00",
        "timezone": "UTC",
        "economic_value": 50.0,
    }

    client.post("/reservations", json=payload)

    response = client.get("/reservations", params={"organization_id": "org-2"})

    assert response.status_code == 200
    reservations = response.json()["reservations"]
    assert len(reservations) == 1
    assert reservations[0]["organization_id"] == "org-2"


def test_list_reservations_invalid_interval(monkeypatch) -> None:
    client = create_client(monkeypatch)

    response = client.get(
        "/reservations",
        params={
            "organization_id": "org-1",
            "starts_at_utc": "2024-01-04T10:00:00",
            "ends_at_utc": "2024-01-04T09:00:00",
        },
    )

    assert response.status_code == 400
    error = response.json()["error"]
    assert "starts_at_utc < ends_at_utc" in error
