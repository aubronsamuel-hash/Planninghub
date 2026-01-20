"""Smoke tests for application wiring."""

from datetime import datetime
from pathlib import Path

import pytest

from planninghub.application.dtos.identity import CreateOrganizationRequest
from planninghub.application.dtos.time_reservation import (
    CreateReservationRequest,
    GetReservationRequest,
)
from planninghub.infra.config import AppConfig, default_config
from planninghub.infra.wiring import build_persistence_adapter


def test_default_config_uses_memory_backend(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("PLANNINGHUB_PERSISTENCE_BACKEND", raising=False)
    monkeypatch.delenv("PLANNINGHUB_SQLITE_DB_PATH", raising=False)

    config = default_config()

    assert config.persistence_backend == "memory"
    assert config.sqlite_db_path is None


def test_sqlite_backend_requires_db_path() -> None:
    config = AppConfig(persistence_backend="sqlite", sqlite_db_path=None)

    with pytest.raises(ValueError):
        build_persistence_adapter(config)


def test_sqlite_file_backed_smoke(tmp_path: Path) -> None:
    db_path = tmp_path / "planninghub.sqlite3"
    config = AppConfig(persistence_backend="sqlite", sqlite_db_path=str(db_path))

    adapter = build_persistence_adapter(config)
    organization = adapter.create_organization(CreateOrganizationRequest(name="Org"))
    reservation = adapter.create_reservation(
        CreateReservationRequest(
            organization_id=organization.id,
            resource_id="resrc-1",
            starts_at_utc=datetime(2024, 1, 1, 8, 0, 0),
            ends_at_utc=datetime(2024, 1, 1, 9, 0, 0),
            timezone="UTC",
            economic_value=None,
        )
    )
    persisted_id = reservation.id

    new_adapter = build_persistence_adapter(config)
    fetched = new_adapter.get_reservation(
        GetReservationRequest(reservation_id=persisted_id)
    )

    assert fetched.id == persisted_id
