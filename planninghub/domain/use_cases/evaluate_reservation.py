"""Use case for evaluating incoming reservations."""

from __future__ import annotations

from dataclasses import dataclass

from planninghub.domain.entities import Reservation
from planninghub.domain.services.conflict_orchestrator import ConflictOrchestrator
from planninghub.domain.services.conflict_outcomes import (
    ResolutionOutcome,
    resolve_outcome,
)
from planninghub.domain.services.conflict_resolution import ResolutionProposal


@dataclass(frozen=True, slots=True)
class EvaluationResult:
    reservation_id: str
    conflict: bool
    proposal: ResolutionProposal | None
    outcome: ResolutionOutcome | None


def evaluate_incoming_reservation(
    organization_id: str,
    reservation: Reservation,
    orchestrator: ConflictOrchestrator,
) -> EvaluationResult:
    orchestration_result = orchestrator.evaluate(organization_id, reservation)
    if orchestration_result.conflict is False:
        return EvaluationResult(
            reservation_id=orchestration_result.reservation_id,
            conflict=False,
            proposal=None,
            outcome=None,
        )

    proposal = orchestration_result.proposal
    return EvaluationResult(
        reservation_id=orchestration_result.reservation_id,
        conflict=True,
        proposal=proposal,
        outcome=resolve_outcome(proposal),
    )
