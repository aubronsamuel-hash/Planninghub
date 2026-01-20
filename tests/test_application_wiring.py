"""Smoke tests for application wiring."""

from datetime import datetime

from planninghub.application.dtos.identity import CreateOrganizationRequest
from planninghub.application.dtos.time_reservation import CreateReservationRequest
from planninghub.infra.wiring import AppConfig, build_application


def _assert_persistence_operations(app_config: AppConfig) -> None:
    app = build_application(app_config)
    organization = app.persistence.create_organization(
        CreateOrganizationRequest(name="Org")
    )
    reservation = app.persistence.create_reservation(
        CreateReservationRequest(
            organization_id=organization.id,
            resource_id="resrc-1",
            starts_at_utc=datetime(2024, 1, 1, 8, 0, 0),
            ends_at_utc=datetime(2024, 1, 1, 9, 0, 0),
            timezone="UTC",
            economic_value=None,
        )
    )
    assert reservation.organization_id == organization.id


def test_build_application_with_memory_backend() -> None:
    _assert_persistence_operations(
        AppConfig(persistence_backend="memory", sqlite_db_path=None)
    )


def test_build_application_with_sqlite_backend() -> None:
    _assert_persistence_operations(
        AppConfig(persistence_backend="sqlite", sqlite_db_path=":memory:")
    )
