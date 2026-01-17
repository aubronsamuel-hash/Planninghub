"""Tests for conflict orchestrator."""

from datetime import datetime, timedelta

from planninghub.domain.entities import Reservation
from planninghub.domain.services.conflict_detection import ConflictDetectionService
from planninghub.domain.services.conflict_orchestrator import ConflictOrchestrator
from planninghub.domain.services.conflict_resolution import NoopResolutionStrategy
from planninghub.domain.value_objects import ReservationStatus
from planninghub.infra.repositories_in_memory import InMemoryReservationRepository


def test_orchestrator_handles_overlapping_reservation() -> None:
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

    result = orchestrator.evaluate("org-1", incoming)

    assert result.conflict is True
    assert result.candidate is not None
    assert result.proposal is not None
    assert result.proposal.strategy_id == "noop"


def test_orchestrator_handles_non_overlapping_reservation() -> None:
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

    result = orchestrator.evaluate("org-1", incoming)

    assert result.conflict is False
    assert result.candidate is None
    assert result.proposal is None
