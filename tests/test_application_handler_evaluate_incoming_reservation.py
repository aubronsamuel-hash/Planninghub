"""Tests for the application reservation handler."""

from datetime import datetime, timedelta

from planninghub.application import (
    EvaluateIncomingReservationCommand,
    EvaluateIncomingReservationHandler,
)
from planninghub.domain.entities import Reservation
from planninghub.domain.services.conflict_outcomes import ResolutionOutcomeType
from planninghub.domain.services.conflict_resolution import NoopResolutionStrategy
from planninghub.domain.value_objects import ReservationStatus
from planninghub.infra.repositories_in_memory import InMemoryReservationRepository


def test_handler_evaluate_incoming_reservation_conflict() -> None:
    repo = InMemoryReservationRepository()
    handler = EvaluateIncomingReservationHandler(repo, [NoopResolutionStrategy()])
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
        starts_at_utc=base_start + timedelta(hours=1),
        ends_at_utc=base_end + timedelta(hours=1),
        timezone="UTC",
        economic_value=None,
        status=ReservationStatus.ACTIVE,
    )

    response = handler.handle(
        EvaluateIncomingReservationCommand(
            organization_id="org-1",
            reservation=incoming,
        )
    )

    assert response.conflict is True
    assert response.proposal is not None
    assert response.outcome is not None
    assert response.outcome.outcome is ResolutionOutcomeType.NEEDS_MANUAL_REVIEW


def test_handler_evaluate_incoming_reservation_no_conflict() -> None:
    repo = InMemoryReservationRepository()
    handler = EvaluateIncomingReservationHandler(repo, [NoopResolutionStrategy()])
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

    response = handler.handle(
        EvaluateIncomingReservationCommand(
            organization_id="org-1",
            reservation=incoming,
        )
    )

    assert response.conflict is False
    assert response.proposal is None
    assert response.outcome is None
