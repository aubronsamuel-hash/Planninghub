"""Contract tests for HTTP adapter DTO mappers."""

from datetime import datetime

import pytest

from planninghub.adapters.http.dtos import (
    EvaluateIncomingReservationRequestDTO,
)
from planninghub.adapters.http.mappers import (
    request_dto_to_command,
    response_to_response_dto,
)
from planninghub.application.ports import EvaluateIncomingReservationResponse
from planninghub.domain.entities import Reservation
from planninghub.domain.services.conflict_outcomes import (
    ResolutionOutcome,
    ResolutionOutcomeType,
)
from planninghub.domain.services.conflict_resolution import ResolutionProposal
from planninghub.domain.value_objects import ReservationStatus


def test_request_mapping_preserves_fields_and_defaults() -> None:
    dto = EvaluateIncomingReservationRequestDTO(
        organization_id="org-1",
        reservation_id="res-1",
        resource_id=None,
        starts_at_utc_iso="2024-01-01T09:00:00",
        ends_at_utc_iso="2024-01-01T10:00:00",
        timezone="UTC",
    )

    command = request_dto_to_command(dto)

    assert command.organization_id == dto.organization_id
    assert isinstance(command.reservation, Reservation)
    assert command.reservation.id == dto.reservation_id
    assert command.reservation.organization_id == dto.organization_id
    assert command.reservation.resource_id is None
    assert command.reservation.starts_at_utc == datetime(2024, 1, 1, 9, 0, 0)
    assert command.reservation.ends_at_utc == datetime(2024, 1, 1, 10, 0, 0)
    assert command.reservation.timezone == dto.timezone
    assert command.reservation.economic_value is None
    assert command.reservation.status == ReservationStatus.ACTIVE


def test_request_mapping_is_deterministic() -> None:
    dto = EvaluateIncomingReservationRequestDTO(
        organization_id="org-2",
        reservation_id="res-2",
        resource_id="resource-1",
        starts_at_utc_iso="2024-01-02T09:00:00",
        ends_at_utc_iso="2024-01-02T10:00:00",
        timezone="UTC",
    )

    first = request_dto_to_command(dto)
    second = request_dto_to_command(dto)

    assert first == second


def test_request_mapping_invalid_iso_raises_value_error() -> None:
    dto = EvaluateIncomingReservationRequestDTO(
        organization_id="org-1",
        reservation_id="res-1",
        resource_id="resource-1",
        starts_at_utc_iso="bad",
        ends_at_utc_iso="2024-01-01T10:00:00",
        timezone="UTC",
    )

    with pytest.raises(ValueError):
        request_dto_to_command(dto)


def test_response_mapping_preserves_fields() -> None:
    proposal = ResolutionProposal(
        reservation_id="res-1",
        strategy_id="strategy-1",
        action="suggest_manual_review",
        details={"reason": "x"},
    )
    outcome = ResolutionOutcome(
        reservation_id="res-1",
        outcome=ResolutionOutcomeType.NEEDS_MANUAL_REVIEW,
        reason="x",
    )
    response = EvaluateIncomingReservationResponse(
        reservation_id="res-1",
        conflict=True,
        proposal=proposal,
        outcome=outcome,
    )

    dto = response_to_response_dto(response)

    assert dto.reservation_id == response.reservation_id
    assert dto.conflict is True
    assert dto.outcome == "NEEDS_MANUAL_REVIEW"
    assert dto.action == "suggest_manual_review"
    assert dto.details == {"reason": "x"}


def test_response_mapping_none_fields_are_none() -> None:
    response = EvaluateIncomingReservationResponse(
        reservation_id="res-1",
        conflict=False,
        proposal=None,
        outcome=None,
    )

    dto = response_to_response_dto(response)

    assert dto.reservation_id == response.reservation_id
    assert dto.conflict is False
    assert dto.outcome is None
    assert dto.action is None
    assert dto.details is None


def test_response_mapping_is_deterministic() -> None:
    response = EvaluateIncomingReservationResponse(
        reservation_id="res-2",
        conflict=False,
        proposal=None,
        outcome=None,
    )

    first = response_to_response_dto(response)
    second = response_to_response_dto(response)

    assert first == second
