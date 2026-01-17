"""FastAPI routes for reservation evaluation."""

from fastapi import APIRouter, HTTPException

from planninghub.adapters.http.dtos import EvaluateIncomingReservationRequestDTO
from planninghub.adapters.http.mappers import (
    request_dto_to_command,
    response_to_response_dto,
)
from planninghub.application.handlers import EvaluateIncomingReservationHandler


class LocalReservationRepository:
    def add(self, reservation) -> None:
        return None

    def get_by_id(self, reservation_id):
        return None

    def list_by_org(self, organization_id):
        return []

    def list_by_resource(self, organization_id, resource_id):
        return []

    def list_overlapping(
        self,
        organization_id,
        resource_id,
        starts_at_utc,
        ends_at_utc,
    ):
        return []

router = APIRouter()


@router.post("/reservations/evaluate")
def evaluate_reservation(request: dict) -> dict:
    try:
        request_dto = EvaluateIncomingReservationRequestDTO(**request)
        command = request_dto_to_command(request_dto)
        handler = EvaluateIncomingReservationHandler(
            reservation_repo=LocalReservationRepository(),
            strategies=[],
        )
        response = handler.handle(command)
        response_dto = response_to_response_dto(response)
    except (TypeError, ValueError) as exc:
        raise HTTPException(
            status_code=400,
            detail="invalid request payload",
        ) from exc

    return {
        "reservation_id": response_dto.reservation_id,
        "conflict": response_dto.conflict,
        "outcome": response_dto.outcome,
        "action": response_dto.action,
        "details": response_dto.details,
    }
