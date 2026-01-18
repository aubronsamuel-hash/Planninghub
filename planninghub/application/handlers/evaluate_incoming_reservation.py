"""Application handlers for reservation evaluation."""

from __future__ import annotations

from planninghub.application.ports import (
    EvaluateIncomingReservationCommand,
    EvaluateIncomingReservationResponse,
)
from planninghub.domain.repositories import ReservationRepository
from planninghub.domain.services.conflict_detection import ConflictDetectionService
from planninghub.domain.services.conflict_orchestrator import ConflictOrchestrator
from planninghub.domain.services.conflict_resolution import ConflictResolutionStrategy
from planninghub.domain.use_cases.evaluate_reservation import (
    evaluate_incoming_reservation,
)


class EvaluateIncomingReservationHandler:
    def __init__(
        self,
        reservation_repo: ReservationRepository,
        strategies: list[ConflictResolutionStrategy],
    ) -> None:
        self._reservation_repo = reservation_repo
        self._strategies = strategies

    def handle(
        self, cmd: EvaluateIncomingReservationCommand
    ) -> EvaluateIncomingReservationResponse:
        detection_service = ConflictDetectionService(self._reservation_repo)
        orchestrator = ConflictOrchestrator(detection_service, self._strategies)
        result = evaluate_incoming_reservation(
            cmd.organization_id,
            cmd.reservation,
            orchestrator,
        )
        return EvaluateIncomingReservationResponse(
            reservation_id=result.reservation_id,
            conflict=result.conflict,
            proposal=result.proposal,
            outcome=result.outcome,
        )
