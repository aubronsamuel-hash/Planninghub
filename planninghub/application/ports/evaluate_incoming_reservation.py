"""Application ports for reservation evaluation."""

from __future__ import annotations

from dataclasses import dataclass

from planninghub.domain.entities import Reservation
from planninghub.domain.services.conflict_outcomes import ResolutionOutcome
from planninghub.domain.services.conflict_resolution import ResolutionProposal


@dataclass(frozen=True, slots=True)
class EvaluateIncomingReservationCommand:
    organization_id: str
    reservation: Reservation


@dataclass(frozen=True, slots=True)
class EvaluateIncomingReservationResponse:
    reservation_id: str
    conflict: bool
    proposal: ResolutionProposal | None
    outcome: ResolutionOutcome | None
