"""Minimal FastAPI application for the HTTP adapter."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from planninghub.application.dtos.time_reservation import (
    CreateReservationRequest,
    GetReservationRequest,
    ListReservationsRequest,
    ReservationDTO,
    TimeRangeDTO,
)
from planninghub.infra.config import default_config
from planninghub.infra.wiring import build_application


def _clean_exception_message(exc: Exception) -> str:
    if exc.args and isinstance(exc.args[0], str):
        return exc.args[0]
    return str(exc)


def _reservation_to_out(reservation: ReservationDTO) -> dict[str, Any]:
    return {
        "id": reservation.id,
        "organization_id": reservation.organization_id,
        "resource_id": reservation.resource_id,
        "starts_at_utc": reservation.starts_at_utc.isoformat(),
        "ends_at_utc": reservation.ends_at_utc.isoformat(),
        "timezone": reservation.timezone,
        "economic_value": reservation.economic_value,
        "status": reservation.status,
    }


def create_app() -> FastAPI:
    config = default_config()
    application = build_application(config)
    app = FastAPI()

    @app.exception_handler(KeyError)
    async def handle_key_error(_request, exc: KeyError) -> JSONResponse:
        return JSONResponse(
            status_code=404,
            content={"error": _clean_exception_message(exc)},
        )

    @app.exception_handler(ValueError)
    async def handle_value_error(_request, exc: ValueError) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={"error": _clean_exception_message(exc)},
        )

    @app.exception_handler(Exception)
    async def handle_exception(_request, _exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content={"error": "internal_error"},
        )

    @app.post("/reservations")
    def create_reservation(payload: dict[str, Any]) -> dict[str, Any]:
        starts_at_utc = datetime.fromisoformat(payload.get("starts_at_utc") or "")
        ends_at_utc = datetime.fromisoformat(payload.get("ends_at_utc") or "")
        request = CreateReservationRequest(
            organization_id=payload.get("organization_id") or "",
            resource_id=payload.get("resource_id"),
            starts_at_utc=starts_at_utc,
            ends_at_utc=ends_at_utc,
            timezone=payload.get("timezone") or "",
            economic_value=payload.get("economic_value"),
        )
        reservation = application.persistence.create_reservation(request)
        return {"reservation": _reservation_to_out(reservation)}

    @app.get("/reservations/{reservation_id}")
    def get_reservation(reservation_id: str) -> dict[str, Any]:
        request = GetReservationRequest(reservation_id=reservation_id)
        reservation = application.persistence.get_reservation(request)
        return {"reservation": _reservation_to_out(reservation)}

    @app.get("/reservations")
    def list_reservations(
        organization_id: str,
        resource_id: str | None = None,
        starts_at_utc: str | None = None,
        ends_at_utc: str | None = None,
    ) -> dict[str, Any]:
        time_range = None
        if starts_at_utc is not None or ends_at_utc is not None:
            if not starts_at_utc or not ends_at_utc:
                raise ValueError("time_range requires starts_at_utc and ends_at_utc")
            time_range = TimeRangeDTO(
                start_utc=datetime.fromisoformat(starts_at_utc),
                end_utc=datetime.fromisoformat(ends_at_utc),
            )
        request = ListReservationsRequest(
            organization_id=organization_id,
            resource_id=resource_id,
            time_range=time_range,
        )
        reservations = application.persistence.list_reservations(request)
        return {
            "reservations": [
                _reservation_to_out(reservation) for reservation in reservations
            ]
        }

    return app
