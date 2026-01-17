"""Tests for evaluate reservation use case."""

from datetime import datetime, timedelta

from planninghub.domain.entities import Reservation
from planninghub.domain.services.conflict_detection import ConflictDetectionService
from planninghub.domain.services.conflict_orchestrator import ConflictOrchestrator
from planninghub.domain.services.conflict_outcomes import ResolutionOutcomeType
from planninghub.domain.services.conflict_resolution import NoopResolutionStrategy
from planninghub.domain.use_cases import evaluate_incoming_reservation
from planninghub.domain.value_objects import ReservationStatus
from planninghub.infra.repositories_in_memory import InMemoryReservationRepository


def test_evaluate_incoming_reservation_overlapping() -> None:
    repo = InMemoryReservationRepository()
    detection = ConflictDetectionService(repo)
    orchestrator = ConflictOrchestrator(detection, [NoopResolutionStrategy()])
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

    result = evaluate_incoming_reservation("org-1", incoming, orchestrator)

    assert result.conflict is True
    assert result.proposal is not None
    assert result.outcome is not None
    assert result.outcome.outcome is ResolutionOutcomeType.NEEDS_MANUAL_REVIEW


def test_evaluate_incoming_reservation_non_overlapping() -> None:
    repo = InMemoryReservationRepository()
    detection = ConflictDetectionService(repo)
    orchestrator = ConflictOrchestrator(detection, [NoopResolutionStrategy()])
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

    incoming = Reservation(
        id="res-2",
        organization_id="org-1",
        resource_id="resrc-1",
        starts_at_utc=base_end + timedelta(hours=1),
        ends_at_utc=base_end + timedelta(hours=2),
        timezone="UTC",
        economic_value=None,
        status=ReservationStatus.ACTIVE,
    )

    result = evaluate_incoming_reservation("org-1", incoming, orchestrator)

    assert result.conflict is False
    assert result.proposal is None
    assert result.outcome is None
