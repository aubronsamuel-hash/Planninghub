"""Conflict orchestration service for detection and resolution."""

from __future__ import annotations

from dataclasses import dataclass

from planninghub.domain.entities import Reservation
from planninghub.domain.services.conflict_detection import (
    ConflictCandidate,
    ConflictDetectionService,
)
from planninghub.domain.services.conflict_resolution import (
    ConflictResolutionStrategy,
    ResolutionProposal,
)


@dataclass(frozen=True, slots=True)
class OrchestrationResult:
    """Result of conflict orchestration for a reservation."""

    reservation_id: str
    conflict: bool
    candidate: ConflictCandidate | None
    proposal: ResolutionProposal | None


class ConflictOrchestrator:
    """Coordinate conflict detection and resolution strategies."""

    def __init__(
        self,
        detection_service: ConflictDetectionService,
        strategies: list[ConflictResolutionStrategy],
    ) -> None:
        self._detection_service = detection_service
        self._strategies = strategies

    def evaluate(
        self,
        organization_id: str,
        reservation: Reservation,
    ) -> OrchestrationResult:
        candidate = self._detection_service.detect_for_reservation(
            organization_id,
            reservation,
        )
        if candidate is None:
            return OrchestrationResult(
                reservation_id=reservation.id,
                conflict=False,
                candidate=None,
                proposal=None,
            )

        proposal = None
        for strategy in self._strategies:
            proposal = strategy.propose(candidate)
            if proposal is not None:
                break

        return OrchestrationResult(
            reservation_id=reservation.id,
            conflict=True,
            candidate=candidate,
            proposal=proposal,
        )
