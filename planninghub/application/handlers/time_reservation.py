"""Handlers for time reservation ports."""

from __future__ import annotations

from planninghub.application.dtos.time_reservation import (
    CreateReservationRequest,
    CreateReservationResponse,
    GetReservationRequest,
    GetReservationResponse,
    ListReservationsRequest,
    ListReservationsResponse,
    UpdateReservationRequest,
    UpdateReservationResponse,
)
from planninghub.application.ports.persistence import ReservationPersistencePort


def _require_org_id(organization_id: str) -> None:
    if not organization_id:
        raise ValueError("organization_id must be non-empty")


def _require_interval(start, end) -> None:
    if start >= end:
        raise ValueError("starts_at_utc must be before ends_at_utc")


class CreateReservationHandler:
    def __init__(self, persistence: ReservationPersistencePort) -> None:
        self._persistence = persistence

    def handle(self, request: CreateReservationRequest) -> CreateReservationResponse:
        _require_org_id(request.organization_id)
        _require_interval(request.starts_at_utc, request.ends_at_utc)
        reservation = self._persistence.create_reservation(request)
        return CreateReservationResponse(reservation=reservation)


class UpdateReservationHandler:
    def __init__(self, persistence: ReservationPersistencePort) -> None:
        self._persistence = persistence

    def handle(self, request: UpdateReservationRequest) -> UpdateReservationResponse:
        if request.starts_at_utc is not None and request.ends_at_utc is not None:
            _require_interval(request.starts_at_utc, request.ends_at_utc)
        reservation = self._persistence.update_reservation(request)
        return UpdateReservationResponse(reservation=reservation)


class GetReservationHandler:
    def __init__(self, persistence: ReservationPersistencePort) -> None:
        self._persistence = persistence

    def handle(self, request: GetReservationRequest) -> GetReservationResponse:
        reservation = self._persistence.get_reservation(request)
        return GetReservationResponse(reservation=reservation)


class ListReservationsHandler:
    def __init__(self, persistence: ReservationPersistencePort) -> None:
        self._persistence = persistence

    def handle(self, request: ListReservationsRequest) -> ListReservationsResponse:
        _require_org_id(request.organization_id)
        reservations = self._persistence.list_reservations(request)
        return ListReservationsResponse(reservations=reservations)
