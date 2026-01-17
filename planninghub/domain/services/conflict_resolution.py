"""Conflict resolution contracts for detected conflicts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from planninghub.domain.services.conflict_detection import ConflictCandidate


@dataclass(frozen=True, slots=True)
class ResolutionProposal:
    """Minimal resolution proposal returned by a strategy."""

    reservation_id: str
    strategy_id: str
    action: str
    details: dict[str, str]


class ConflictResolutionStrategy(Protocol):
    """Protocol for conflict resolution strategies."""

    id: str

    def propose(self, candidate: ConflictCandidate) -> ResolutionProposal | None:
        """Return a resolution proposal or None."""


class NoopResolutionStrategy:
    """Minimal strategy that suggests manual review."""

    id = "noop"

    def propose(self, candidate: ConflictCandidate) -> ResolutionProposal | None:
        return ResolutionProposal(
            reservation_id=candidate.reservation_id,
            strategy_id=self.id,
            action="suggest_manual_review",
            details={
                "reason": candidate.reason,
                "overlap_count": str(len(candidate.overlapping_reservation_ids)),
            },
        )
