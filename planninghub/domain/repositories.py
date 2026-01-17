"""Repository ports for PlanningHub domains."""

from __future__ import annotations

from datetime import datetime
from typing import Protocol, runtime_checkable

from planninghub.domain.entities import Membership, Reservation


@runtime_checkable
class MembershipRepository(Protocol):
    """Repository port for memberships."""

    def add(self, membership: Membership) -> None:
        """Persist a membership."""

    def get_by_id(self, membership_id: str) -> Membership | None:
        """Fetch a membership by identifier."""

    def list_by_org(self, organization_id: str) -> list[Membership]:
        """List memberships scoped to an organization."""

    def find_by_user(self, organization_id: str, user_id: str) -> list[Membership]:
        """List memberships in an organization for a user."""


@runtime_checkable
class ReservationRepository(Protocol):
    """Repository port for reservations."""

    def add(self, reservation: Reservation) -> None:
        """Persist a reservation."""

    def get_by_id(self, reservation_id: str) -> Reservation | None:
        """Fetch a reservation by identifier."""

    def list_by_org(self, organization_id: str) -> list[Reservation]:
        """List reservations scoped to an organization."""

    def list_by_resource(
        self, organization_id: str, resource_id: str
    ) -> list[Reservation]:
        """List reservations scoped to an organization and resource."""

    def list_overlapping(
        self,
        organization_id: str,
        resource_id: str,
        starts_at_utc: datetime,
        ends_at_utc: datetime,
    ) -> list[Reservation]:
        """List reservations overlapping a time interval."""
