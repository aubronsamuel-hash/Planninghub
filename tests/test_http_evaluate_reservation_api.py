"""Tests for the reservation evaluation HTTP API."""

from datetime import datetime, timedelta

from fastapi.testclient import TestClient

from planninghub.adapters.http.server import create_app
from planninghub.domain.entities import Reservation
from planninghub.domain.value_objects import ReservationStatus
from planninghub.infra.repositories_sqlite import SQLiteReservationRepository


def test_evaluate_reservation_no_conflict(tmp_path) -> None:
    repo = SQLiteReservationRepository(db_path=str(tmp_path / "eval.db"))
    app = create_app(reservation_repo=repo)
    client = TestClient(app)

    payload = {
        "organization_id": "org-1",
        "reservation_id": "res-1",
        "resource_id": "resrc-1",
        "starts_at_utc_iso": "2024-05-01T08:00:00",
        "ends_at_utc_iso": "2024-05-01T09:00:00",
        "timezone": "UTC",
    }

    response = client.post("/reservations/evaluate", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["conflict"] is False
    assert body["reservation_id"] == "res-1"


def test_evaluate_reservation_conflict_returns_409(tmp_path) -> None:
    repo = SQLiteReservationRepository(db_path=str(tmp_path / "eval.db"))
    base_start = datetime(2024, 5, 1, 8, 0, 0)
    base_end = base_start + timedelta(hours=2)
    repo.add(
        Reservation(
            id="res-1",
            organization_id="org-1",
            resource_id="resrc-1",
            starts_at_utc=base_start,
            ends_at_utc=base_end,
            timezone="UTC",
            economic_value=None,
            status=ReservationStatus.ACTIVE,
        )
    )

    app = create_app(reservation_repo=repo)
    client = TestClient(app)
    payload = {
        "organization_id": "org-1",
        "reservation_id": "res-2",
        "resource_id": "resrc-1",
        "starts_at_utc_iso": "2024-05-01T09:00:00",
        "ends_at_utc_iso": "2024-05-01T10:00:00",
        "timezone": "UTC",
    }

    response = client.post("/reservations/evaluate", json=payload)

    assert response.status_code == 409
    body = response.json()
    assert body["conflict"] is True
    assert body["reservation_id"] == "res-2"
