"""Tests for in-memory repository implementations."""

from datetime import datetime, timedelta

from planninghub.domain.entities import Membership, Reservation
from planninghub.domain.value_objects import MembershipRole, ReservationStatus
from planninghub.infra.repositories_in_memory import (
    InMemoryMembershipRepository,
    InMemoryReservationRepository,
)


def test_membership_add_and_get_by_id() -> None:
    repo = InMemoryMembershipRepository()
    membership = Membership(
        id="mem-1",
        organization_id="org-1",
        user_id="user-1",
        role=MembershipRole.MEMBER,
    )

    repo.add(membership)

    assert repo.get_by_id("mem-1") == membership
    assert repo.get_by_id("missing") is None


def test_membership_list_by_org_filters() -> None:
    repo = InMemoryMembershipRepository()
    repo.add(
        Membership(
            id="mem-2",
            organization_id="org-1",
            user_id="user-1",
            role=MembershipRole.MEMBER,
        )
    )
    repo.add(
        Membership(
            id="mem-1",
            organization_id="org-2",
            user_id="user-2",
            role=MembershipRole.ADMIN,
        )
    )
    repo.add(
        Membership(
            id="mem-3",
            organization_id="org-1",
            user_id="user-3",
            role=MembershipRole.OWNER,
        )
    )

    assert [m.id for m in repo.list_by_org("org-1")] == ["mem-2", "mem-3"]
    assert repo.list_by_org("missing") == []


def test_membership_find_by_user_filters() -> None:
    repo = InMemoryMembershipRepository()
    repo.add(
        Membership(
            id="mem-2",
            organization_id="org-1",
            user_id="user-1",
            role=MembershipRole.MEMBER,
        )
    )
    repo.add(
        Membership(
            id="mem-1",
            organization_id="org-1",
            user_id="user-2",
            role=MembershipRole.ADMIN,
        )
    )
    repo.add(
        Membership(
            id="mem-3",
            organization_id="org-2",
            user_id="user-1",
            role=MembershipRole.OWNER,
        )
    )

    assert [m.id for m in repo.find_by_user("org-1", "user-1")] == ["mem-2"]
    assert repo.find_by_user("org-2", "user-2") == []


def test_reservation_add_and_get_by_id() -> None:
    repo = InMemoryReservationRepository()
    reservation = Reservation(
        id="res-1",
        organization_id="org-1",
        resource_id="resrc-1",
        starts_at_utc=datetime(2024, 1, 1, 8, 0, 0),
        ends_at_utc=datetime(2024, 1, 1, 9, 0, 0),
        timezone="UTC",
        economic_value=None,
        status=ReservationStatus.ACTIVE,
    )

    repo.add(reservation)

    assert repo.get_by_id("res-1") == reservation
    assert repo.get_by_id("missing") is None


def test_reservation_list_by_resource_filters() -> None:
    repo = InMemoryReservationRepository()
    repo.add(
        Reservation(
            id="res-1",
            organization_id="org-1",
            resource_id="resrc-1",
            starts_at_utc=datetime(2024, 1, 1, 8, 0, 0),
            ends_at_utc=datetime(2024, 1, 1, 9, 0, 0),
            timezone="UTC",
            economic_value=None,
            status=ReservationStatus.ACTIVE,
        )
    )
    repo.add(
        Reservation(
            id="res-2",
            organization_id="org-1",
            resource_id="resrc-2",
            starts_at_utc=datetime(2024, 1, 1, 9, 0, 0),
            ends_at_utc=datetime(2024, 1, 1, 10, 0, 0),
            timezone="UTC",
            economic_value=None,
            status=ReservationStatus.DRAFT,
        )
    )
    repo.add(
        Reservation(
            id="res-3",
            organization_id="org-2",
            resource_id="resrc-1",
            starts_at_utc=datetime(2024, 1, 1, 10, 0, 0),
            ends_at_utc=datetime(2024, 1, 1, 11, 0, 0),
            timezone="UTC",
            economic_value=None,
            status=ReservationStatus.CANCELLED,
        )
    )

    assert [r.id for r in repo.list_by_resource("org-1", "resrc-1")] == ["res-1"]
    assert repo.list_by_resource("org-1", "missing") == []


def test_reservation_list_overlapping_cases() -> None:
    repo = InMemoryReservationRepository()
    base_start = datetime(2024, 1, 1, 8, 0, 0)
    base_end = base_start + timedelta(hours=2)

    repo.add(
        Reservation(
            id="res-1",
            organization_id="org-1",
            resource_id="resrc-1",
            starts_at_utc=base_start,
            ends_at_utc=base_end,
            timezone="UTC",
            economic_value=None,
            status=ReservationStatus.ACTIVE,
        )
    )
    repo.add(
        Reservation(
            id="res-2",
            organization_id="org-1",
            resource_id="resrc-1",
            starts_at_utc=base_end,
            ends_at_utc=base_end + timedelta(hours=1),
            timezone="UTC",
            economic_value=None,
            status=ReservationStatus.ACTIVE,
        )
    )
    repo.add(
        Reservation(
            id="res-3",
            organization_id="org-2",
            resource_id="resrc-1",
            starts_at_utc=base_start,
            ends_at_utc=base_end,
            timezone="UTC",
            economic_value=None,
            status=ReservationStatus.ACTIVE,
        )
    )
    repo.add(
        Reservation(
            id="res-4",
            organization_id="org-1",
            resource_id="resrc-2",
            starts_at_utc=base_start,
            ends_at_utc=base_end,
            timezone="UTC",
            economic_value=None,
            status=ReservationStatus.ACTIVE,
        )
    )

    overlap = repo.list_overlapping(
        "org-1",
        "resrc-1",
        base_start + timedelta(minutes=30),
        base_end,
    )
    assert [r.id for r in overlap] == ["res-1"]

    touching = repo.list_overlapping(
        "org-1",
        "resrc-1",
        base_start - timedelta(hours=1),
        base_start,
    )
    assert touching == []

    mismatched = repo.list_overlapping(
        "org-2",
        "resrc-2",
        base_start + timedelta(minutes=30),
        base_end + timedelta(minutes=30),
    )
    assert mismatched == []
