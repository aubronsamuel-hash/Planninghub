"""FastAPI server for reservation evaluation."""

from __future__ import annotations

import os
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from planninghub.adapters.http.dtos import EvaluateIncomingReservationRequestDTO
from planninghub.adapters.http.mappers import (
    request_dto_to_command,
    response_to_response_dto,
)
from planninghub.application.handlers import EvaluateIncomingReservationHandler
from planninghub.domain.repositories import ReservationRepository
from planninghub.domain.services.conflict_resolution import NoopResolutionStrategy
from planninghub.infra.repositories_sqlite import SQLiteReservationRepository


def create_app(
    reservation_repo: ReservationRepository | None = None,
    db_path: str | None = None,
) -> FastAPI:
    if reservation_repo is None:
        resolved_db_path = (
            db_path
            or os.getenv("PLANNINGHUB_SQLITE_DB_PATH")
            or ":memory:"
        )
        reservation_repo = SQLiteReservationRepository(db_path=resolved_db_path)

    app = FastAPI()

    @app.post("/reservations/evaluate")
    def evaluate_reservation(payload: dict[str, Any]):
        try:
            request_dto = EvaluateIncomingReservationRequestDTO(**payload)
            command = request_dto_to_command(request_dto)
            reservation_repo.add(command.reservation)
            handler = EvaluateIncomingReservationHandler(
                reservation_repo=reservation_repo,
                strategies=[NoopResolutionStrategy()],
            )
            response = handler.handle(command)
            response_dto = response_to_response_dto(response)
        except (TypeError, ValueError) as exc:
            raise HTTPException(
                status_code=400,
                detail="invalid request payload",
            ) from exc

        response_payload = {
            "reservation_id": response_dto.reservation_id,
            "conflict": response_dto.conflict,
            "outcome": response_dto.outcome,
            "action": response_dto.action,
            "details": response_dto.details,
        }
        if response_dto.conflict:
            return JSONResponse(status_code=409, content=response_payload)
        return response_payload

    return app
