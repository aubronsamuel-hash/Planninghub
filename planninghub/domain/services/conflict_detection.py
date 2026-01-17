"""Conflict detection service for reservations."""

from __future__ import annotations

from dataclasses import dataclass

from planninghub.domain.entities import Reservation
from planninghub.domain.repositories import ReservationRepository
from planninghub.domain.value_objects import ConflictSeverity


@dataclass(frozen=True, slots=True)
class ConflictCandidate:
    """Minimal conflict candidate returned by detection."""

    reservation_id: str
    resource_id: str
    overlapping_reservation_ids: list[str]
    severity: ConflictSeverity
    reason: str


class ConflictDetectionService:
    """Detect conflicts based on overlapping reservations."""

    def __init__(self, reservations: ReservationRepository) -> None:
        self._reservations = reservations

    def detect_for_reservation(
        self, organization_id: str, reservation: Reservation
    ) -> ConflictCandidate | None:
        if not reservation.resource_id:
            return None

        overlaps = self._reservations.list_overlapping(
            organization_id,
            reservation.resource_id,
            reservation.starts_at_utc,
            reservation.ends_at_utc,
        )
        overlapping_ids = sorted(
            overlap.id for overlap in overlaps if overlap.id != reservation.id
        )
        if not overlapping_ids:
            return None

        return ConflictCandidate(
            reservation_id=reservation.id,
            resource_id=reservation.resource_id,
            overlapping_reservation_ids=overlapping_ids,
            severity=ConflictSeverity.HIGH,
            reason="overlapping_reservations",
        )
