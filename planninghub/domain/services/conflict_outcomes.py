"""Outcome contracts for conflict resolution proposals."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from planninghub.domain.services.conflict_resolution import ResolutionProposal


class ResolutionOutcomeType(str, Enum):
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    NEEDS_MANUAL_REVIEW = "NEEDS_MANUAL_REVIEW"


@dataclass(frozen=True, slots=True)
class ResolutionOutcome:
    reservation_id: str
    outcome: ResolutionOutcomeType
    reason: str


def resolve_outcome(
    proposal: ResolutionProposal | None,
) -> ResolutionOutcome | None:
    if proposal is None:
        return None

    if proposal.action == "suggest_manual_review":
        return ResolutionOutcome(
            reservation_id=proposal.reservation_id,
            outcome=ResolutionOutcomeType.NEEDS_MANUAL_REVIEW,
            reason=proposal.details.get("reason", ""),
        )

    return ResolutionOutcome(
        reservation_id=proposal.reservation_id,
        outcome=ResolutionOutcomeType.NEEDS_MANUAL_REVIEW,
        reason="unknown_action",
    )
