"""CLI smoke test for persistence adapters."""

from __future__ import annotations

from datetime import datetime

from planninghub.adapters.persistence.sqlite import SQLitePersistenceAdapter
from planninghub.application.dtos.conflict import DetectConflictsRequest
from planninghub.application.dtos.identity import CreateOrganizationRequest
from planninghub.application.dtos.time_reservation import (
    CreateReservationRequest,
    GetReservationRequest,
)
from planninghub.infra.config import default_config
from planninghub.infra.wiring import build_persistence_adapter


def main(argv: list[str] | None = None) -> int:
    """Run a deterministic persistence smoke scenario."""

    _ = argv
    try:
        config = default_config()
        persistence = build_persistence_adapter(config)

        organization = persistence.create_organization(
            CreateOrganizationRequest(name="Org")
        )

        reservation = persistence.create_reservation(
            CreateReservationRequest(
                organization_id=organization.id,
                resource_id="resrc-1",
                starts_at_utc=datetime(2024, 1, 1, 8, 0, 0),
                ends_at_utc=datetime(2024, 1, 1, 9, 0, 0),
                timezone="UTC",
                economic_value=None,
            )
        )

        fetched = persistence.get_reservation(
            GetReservationRequest(reservation_id=reservation.id)
        )
        if fetched.id != reservation.id:
            raise AssertionError("reservation id mismatch")

        if config.persistence_backend == "sqlite":
            if not config.sqlite_db_path:
                raise AssertionError("sqlite db path missing")
            second_adapter = SQLitePersistenceAdapter(db_path=config.sqlite_db_path)
            persisted = second_adapter.get_reservation(
                GetReservationRequest(reservation_id=reservation.id)
            )
            if persisted.id != reservation.id:
                raise AssertionError("sqlite persistence mismatch")

        persistence.create_reservation(
            CreateReservationRequest(
                organization_id=organization.id,
                resource_id="resrc-1",
                starts_at_utc=datetime(2024, 1, 1, 8, 30, 0),
                ends_at_utc=datetime(2024, 1, 1, 9, 30, 0),
                timezone="UTC",
                economic_value=None,
            )
        )

        conflicts = persistence.detect_conflicts(
            DetectConflictsRequest(
                organization_id=organization.id,
                reservation_id=reservation.id,
            )
        )
        if not conflicts:
            raise AssertionError("expected conflicts")
        if not any(conflict.severity == "high" for conflict in conflicts):
            raise AssertionError("expected high severity conflict")

        print(
            "SMOKE OK: backend={} org={} res={} conflicts={}".format(
                config.persistence_backend,
                organization.id,
                reservation.id,
                len(conflicts),
            )
        )
        return 0
    except Exception as exc:
        print(f"SMOKE FAIL: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
