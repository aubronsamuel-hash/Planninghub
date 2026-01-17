"""Tests for conflict detection service."""

from datetime import datetime, timedelta

from planninghub.domain.entities import Reservation
from planninghub.domain.services.conflict_detection import ConflictDetectionService
from planninghub.domain.value_objects import ConflictSeverity, ReservationStatus
from planninghub.infra.repositories_in_memory import InMemoryReservationRepository


def test_detects_overlapping_reservations() -> None:
    repo = InMemoryReservationRepository()
    service = ConflictDetectionService(repo)
    base_start = datetime(2024, 1, 1, 8, 0, 0)
    base_end = base_start + timedelta(hours=2)

    existing = Reservation(
        id="res-1",
        organization_id="org-1",
        resource_id="resrc-1",
        starts_at_utc=base_start,
        ends_at_utc=base_end,
        timezone="UTC",
        economic_value=None,
        status=ReservationStatus.ACTIVE,
    )
    repo.add(existing)

    incoming = Reservation(
        id="res-2",
        organization_id="org-1",
        resource_id="resrc-1",
        starts_at_utc=base_start + timedelta(minutes=30),
        ends_at_utc=base_end + timedelta(hours=1),
        timezone="UTC",
        economic_value=None,
        status=ReservationStatus.ACTIVE,
    )

    candidate = service.detect_for_reservation("org-1", incoming)

    assert candidate is not None
    assert candidate.reservation_id == "res-2"
    assert candidate.resource_id == "resrc-1"
    assert candidate.overlapping_reservation_ids == ["res-1"]
    assert candidate.severity == ConflictSeverity.HIGH
    assert candidate.reason == "overlapping_reservations"


def test_touching_reservations_are_not_overlaps() -> None:
    repo = InMemoryReservationRepository()
    service = ConflictDetectionService(repo)
    base_start = datetime(2024, 1, 1, 8, 0, 0)
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

    touching = Reservation(
        id="res-2",
        organization_id="org-1",
        resource_id="resrc-1",
        starts_at_utc=base_end,
        ends_at_utc=base_end + timedelta(hours=1),
        timezone="UTC",
        economic_value=None,
        status=ReservationStatus.ACTIVE,
    )

    assert service.detect_for_reservation("org-1", touching) is None


def test_missing_resource_id_returns_none() -> None:
    repo = InMemoryReservationRepository()
    service = ConflictDetectionService(repo)

    reservation = Reservation(
        id="res-1",
        organization_id="org-1",
        resource_id=None,
        starts_at_utc=datetime(2024, 1, 1, 8, 0, 0),
        ends_at_utc=datetime(2024, 1, 1, 9, 0, 0),
        timezone="UTC",
        economic_value=None,
        status=ReservationStatus.DRAFT,
    )

    assert service.detect_for_reservation("org-1", reservation) is None
