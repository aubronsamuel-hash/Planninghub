"""In-memory repository implementations."""

from __future__ import annotations

from datetime import datetime
from operator import attrgetter

from planninghub.domain.entities import Membership, Reservation


class InMemoryMembershipRepository:
    """In-memory membership repository."""

    def __init__(self) -> None:
        self._items: dict[str, Membership] = {}

    def add(self, membership: Membership) -> None:
        self._items[membership.id] = membership

    def get_by_id(self, membership_id: str) -> Membership | None:
        return self._items.get(membership_id)

    def list_by_org(self, organization_id: str) -> list[Membership]:
        items = [
            membership
            for membership in self._items.values()
            if membership.organization_id == organization_id
        ]
        return sorted(items, key=lambda membership: membership.id)

    def find_by_user(self, organization_id: str, user_id: str) -> list[Membership]:
        items = [
            membership
            for membership in self._items.values()
            if membership.organization_id == organization_id
            and membership.user_id == user_id
        ]
        return sorted(items, key=lambda membership: membership.id)


class InMemoryReservationRepository:
    """In-memory reservation repository."""

    def __init__(self) -> None:
        self._items: dict[str, Reservation] = {}

    def add(self, reservation: Reservation) -> None:
        self._items[reservation.id] = reservation

    def get_by_id(self, reservation_id: str) -> Reservation | None:
        return self._items.get(reservation_id)

    def list_by_org(self, organization_id: str) -> list[Reservation]:
        items = [
            reservation
            for reservation in self._items.values()
            if reservation.organization_id == organization_id
        ]
        return sorted(items, key=attrgetter("id"))

    def list_by_resource(
        self, organization_id: str, resource_id: str
    ) -> list[Reservation]:
        items = [
            reservation
            for reservation in self._items.values()
            if reservation.organization_id == organization_id
            and reservation.resource_id == resource_id
        ]
        return sorted(items, key=attrgetter("id"))

    def list_overlapping(
        self,
        organization_id: str,
        resource_id: str,
        starts_at_utc: datetime,
        ends_at_utc: datetime,
    ) -> list[Reservation]:
        items = [
            reservation
            for reservation in self._items.values()
            if reservation.organization_id == organization_id
            and reservation.resource_id == resource_id
            and reservation.starts_at_utc < ends_at_utc
            and reservation.ends_at_utc > starts_at_utc
        ]
        return sorted(
            items,
            key=lambda reservation: (reservation.starts_at_utc, reservation.id),
        )
