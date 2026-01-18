"""Inbound ports for time reservation operations."""

from __future__ import annotations

from typing import Protocol

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


class CreateReservationPort(Protocol):
    def handle(self, request: CreateReservationRequest) -> CreateReservationResponse:
        ...


class UpdateReservationPort(Protocol):
    def handle(self, request: UpdateReservationRequest) -> UpdateReservationResponse:
        ...


class GetReservationPort(Protocol):
    def handle(self, request: GetReservationRequest) -> GetReservationResponse:
        ...


class ListReservationsPort(Protocol):
    def handle(self, request: ListReservationsRequest) -> ListReservationsResponse:
        ...
