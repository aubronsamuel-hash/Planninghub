"""HTTP adapter mappers for reservation evaluation."""

from __future__ import annotations

from datetime import datetime

from planninghub.adapters.http.dtos import (
    EvaluateIncomingReservationRequestDTO,
    EvaluateIncomingReservationResponseDTO,
)
from planninghub.application.ports import (
    EvaluateIncomingReservationCommand,
    EvaluateIncomingReservationResponse,
)
from planninghub.domain.entities import Reservation
from planninghub.domain.value_objects import ReservationStatus


def request_dto_to_command(
    dto: EvaluateIncomingReservationRequestDTO,
) -> EvaluateIncomingReservationCommand:
    starts_at_utc = datetime.fromisoformat(dto.starts_at_utc_iso)
    ends_at_utc = datetime.fromisoformat(dto.ends_at_utc_iso)
    reservation = Reservation(
        id=dto.reservation_id,
        organization_id=dto.organization_id,
        resource_id=dto.resource_id,
        starts_at_utc=starts_at_utc,
        ends_at_utc=ends_at_utc,
        timezone=dto.timezone,
        economic_value=None,
        status=ReservationStatus.ACTIVE,
    )
    return EvaluateIncomingReservationCommand(
        organization_id=dto.organization_id,
        reservation=reservation,
    )


def response_to_response_dto(
    resp: EvaluateIncomingReservationResponse,
) -> EvaluateIncomingReservationResponseDTO:
    return EvaluateIncomingReservationResponseDTO(
        reservation_id=resp.reservation_id,
        conflict=resp.conflict,
        outcome=resp.outcome.outcome.value if resp.outcome else None,
        action=resp.proposal.action if resp.proposal else None,
        details=resp.proposal.details if resp.proposal else None,
    )
