"""Application layer demo wiring for conflict detection."""

from __future__ import annotations

from datetime import datetime, timezone

from planninghub.domain.entities import Reservation
from planninghub.domain.services import ConflictDetectionService
from planninghub.domain.value_objects import ReservationStatus
from planninghub.infra.repositories_in_memory import InMemoryReservationRepository


def run_demo() -> dict[str, object]:
    """Run the minimal conflict detection demo."""
    organization_id = "org-1"
    resource_id = "resrc-1"
    reservation_repo = InMemoryReservationRepository()
    conflict_service = ConflictDetectionService(reservation_repo)

    existing_reservation = Reservation(
        id="res-1",
        organization_id=organization_id,
        resource_id=resource_id,
        starts_at_utc=datetime(2024, 1, 1, 8, 0, tzinfo=timezone.utc),
        ends_at_utc=datetime(2024, 1, 1, 10, 0, tzinfo=timezone.utc),
        timezone="UTC",
        economic_value=None,
        status=ReservationStatus.ACTIVE,
    )
    reservation_repo.add(existing_reservation)

    incoming_reservation = Reservation(
        id="res-2",
        organization_id=organization_id,
        resource_id=resource_id,
        starts_at_utc=datetime(2024, 1, 1, 9, 0, tzinfo=timezone.utc),
        ends_at_utc=datetime(2024, 1, 1, 11, 0, tzinfo=timezone.utc),
        timezone="UTC",
        economic_value=None,
        status=ReservationStatus.ACTIVE,
    )

    conflict = conflict_service.detect_for_reservation(
        organization_id=organization_id,
        reservation=incoming_reservation,
    )

    return {
        "conflict": conflict is not None,
        "overlaps": conflict.overlapping_reservation_ids if conflict else [],
        "severity": conflict.severity.value if conflict else None,
    }
