"""Tests for HTTP adapter DTO mapping."""

from datetime import datetime

import pytest

from planninghub.adapters.http.dtos import EvaluateIncomingReservationRequestDTO
from planninghub.adapters.http.mappers import (
    request_dto_to_command,
    response_to_response_dto,
)
from planninghub.application.ports import EvaluateIncomingReservationResponse
from planninghub.domain.services.conflict_outcomes import (
    ResolutionOutcome,
    ResolutionOutcomeType,
)
from planninghub.domain.services.conflict_resolution import ResolutionProposal


def test_request_mapping_success() -> None:
    dto = EvaluateIncomingReservationRequestDTO(
        organization_id="org-1",
        reservation_id="res-1",
        resource_id="resource-1",
        starts_at_utc_iso="2024-01-01T09:00:00",
        ends_at_utc_iso="2024-01-01T10:00:00",
        timezone="UTC",
    )

    command = request_dto_to_command(dto)

    assert command.organization_id == "org-1"
    assert command.reservation.id == "res-1"
    assert command.reservation.starts_at_utc == datetime(2024, 1, 1, 9, 0, 0)
    assert command.reservation.starts_at_utc.tzinfo is None


def test_request_mapping_invalid_datetime() -> None:
    dto = EvaluateIncomingReservationRequestDTO(
        organization_id="org-1",
        reservation_id="res-1",
        resource_id=None,
        starts_at_utc_iso="bad",
        ends_at_utc_iso="2024-01-01T10:00:00",
        timezone="UTC",
    )

    with pytest.raises(ValueError):
        request_dto_to_command(dto)


def test_response_mapping() -> None:
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

    assert dto.outcome == "NEEDS_MANUAL_REVIEW"
    assert dto.action == "suggest_manual_review"
    assert dto.details["reason"] == "x"
