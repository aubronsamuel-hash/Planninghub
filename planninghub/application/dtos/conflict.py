"""DTOs for conflict ports."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True, slots=True)
class ConflictDTO:
    id: str
    organization_id: str
    reservation_id: str
    resource_id: Optional[str]
    severity: str
    reason: str


@dataclass(frozen=True, slots=True)
class DetectConflictsRequest:
    organization_id: str
    reservation_id: str


@dataclass(frozen=True, slots=True)
class DetectConflictsResponse:
    conflicts: list[ConflictDTO]


@dataclass(frozen=True, slots=True)
class ListConflictsRequest:
    organization_id: str
    reservation_id: Optional[str] = None


@dataclass(frozen=True, slots=True)
class ListConflictsResponse:
    conflicts: list[ConflictDTO]
