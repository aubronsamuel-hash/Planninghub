"""HTTP DTOs for reservation evaluation."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EvaluateIncomingReservationRequestDTO:
    organization_id: str
    reservation_id: str
    resource_id: str | None
    starts_at_utc_iso: str
    ends_at_utc_iso: str
    timezone: str


@dataclass(frozen=True, slots=True)
class EvaluateIncomingReservationResponseDTO:
    reservation_id: str
    conflict: bool
    outcome: str | None
    action: str | None
    details: dict[str, str] | None
