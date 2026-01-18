"""DTOs for time reservation ports."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True, slots=True)
class ReservationDTO:
    id: str
    organization_id: str
    resource_id: Optional[str]
    starts_at_utc: datetime
    ends_at_utc: datetime
    timezone: str
    economic_value: Optional[float]
    status: str


@dataclass(frozen=True, slots=True)
class TimeRangeDTO:
    start_utc: datetime
    end_utc: datetime


@dataclass(frozen=True, slots=True)
class CreateReservationRequest:
    organization_id: str
    resource_id: Optional[str]
    starts_at_utc: datetime
    ends_at_utc: datetime
    timezone: str
    economic_value: Optional[float]


@dataclass(frozen=True, slots=True)
class CreateReservationResponse:
    reservation: ReservationDTO


@dataclass(frozen=True, slots=True)
class UpdateReservationRequest:
    reservation_id: str
    starts_at_utc: Optional[datetime] = None
    ends_at_utc: Optional[datetime] = None
    resource_id: Optional[str] = None
    status: Optional[str] = None


@dataclass(frozen=True, slots=True)
class UpdateReservationResponse:
    reservation: ReservationDTO


@dataclass(frozen=True, slots=True)
class GetReservationRequest:
    reservation_id: str


@dataclass(frozen=True, slots=True)
class GetReservationResponse:
    reservation: ReservationDTO


@dataclass(frozen=True, slots=True)
class ListReservationsRequest:
    organization_id: str
    resource_id: Optional[str] = None
    time_range: Optional[TimeRangeDTO] = None


@dataclass(frozen=True, slots=True)
class ListReservationsResponse:
    reservations: list[ReservationDTO]
