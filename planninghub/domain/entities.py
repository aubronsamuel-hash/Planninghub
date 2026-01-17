"""Core PlanningHub domain entities."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from planninghub.domain.value_objects import (
    ConflictSeverity,
    MembershipRole,
    ReservationStatus,
    ResourceType,
    ShiftStatus,
)


def _require_org_id(organization_id: str) -> None:
    if not organization_id:
        raise ValueError("organization_id must be non-empty")


@dataclass(frozen=True, slots=True)
class Organization:
    """Organization aggregate root."""

    id: str
    name: str
    timezone: str


@dataclass(frozen=True, slots=True)
class User:
    """User entity."""

    id: str
    email: str
    display_name: str


@dataclass(frozen=True, slots=True)
class Membership:
    """Organization membership."""

    id: str
    organization_id: str
    user_id: str
    role: MembershipRole

    def __post_init__(self) -> None:
        _require_org_id(self.organization_id)


@dataclass(frozen=True, slots=True)
class Project:
    """Project entity."""

    id: str
    organization_id: str
    name: str

    def __post_init__(self) -> None:
        _require_org_id(self.organization_id)


@dataclass(frozen=True, slots=True)
class Site:
    """Site entity."""

    id: str
    organization_id: str
    name: str
    location_text: str

    def __post_init__(self) -> None:
        _require_org_id(self.organization_id)


@dataclass(frozen=True, slots=True)
class Mission:
    """Mission entity."""

    id: str
    organization_id: str
    project_id: Optional[str]
    site_id: Optional[str]
    name: str

    def __post_init__(self) -> None:
        _require_org_id(self.organization_id)


@dataclass(frozen=True, slots=True)
class Resource:
    """Resource entity."""

    id: str
    organization_id: str
    type: ResourceType
    name: str

    def __post_init__(self) -> None:
        _require_org_id(self.organization_id)


@dataclass(frozen=True, slots=True)
class Reservation:
    """Reservation entity."""

    id: str
    organization_id: str
    resource_id: Optional[str]
    starts_at_utc: datetime
    ends_at_utc: datetime
    timezone: str
    economic_value: Optional[float]
    status: ReservationStatus

    def __post_init__(self) -> None:
        _require_org_id(self.organization_id)
        if self.starts_at_utc >= self.ends_at_utc:
            raise ValueError("starts_at_utc must be before ends_at_utc")


@dataclass(frozen=True, slots=True)
class Shift:
    """Shift entity."""

    id: str
    mission_id: str
    reservation_id: str
    status: ShiftStatus

    def __post_init__(self) -> None:
        if not self.mission_id:
            raise ValueError("mission_id must be non-empty")
        if not self.reservation_id:
            raise ValueError("reservation_id must be non-empty")


@dataclass(frozen=True, slots=True)
class Conflict:
    """Conflict entity."""

    id: str
    organization_id: str
    reservation_id: str
    resource_id: Optional[str]
    severity: ConflictSeverity
    reason: str

    def __post_init__(self) -> None:
        _require_org_id(self.organization_id)
