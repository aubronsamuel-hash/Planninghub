"""Tests for SQLite repository implementations."""

from datetime import datetime, timedelta

from planninghub.domain.entities import Membership, Reservation
from planninghub.domain.value_objects import MembershipRole, ReservationStatus
from planninghub.infra.repositories_sqlite import (
    SQLiteMembershipRepository,
    SQLiteReservationRepository,
)


def test_membership_add_and_list_filters(tmp_path) -> None:
    repo = SQLiteMembershipRepository(db_path=str(tmp_path / "members.db"))
    repo.add(
        Membership(
            id="mem-1",
            organization_id="org-1",
            user_id="user-1",
            role=MembershipRole.MEMBER,
        )
    )
    repo.add(
        Membership(
            id="mem-2",
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

    assert repo.get_by_id("mem-1").user_id == "user-1"
    assert [m.id for m in repo.list_by_org("org-1")] == ["mem-1", "mem-2"]
    assert [m.id for m in repo.find_by_user("org-1", "user-2")] == ["mem-2"]


def test_reservation_roundtrip_and_overlap(tmp_path) -> None:
    repo = SQLiteReservationRepository(db_path=str(tmp_path / "res.db"))
    base_start = datetime(2024, 4, 1, 8, 0, 0)
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
            starts_at_utc=base_start + timedelta(minutes=30),
            ends_at_utc=base_end + timedelta(minutes=30),
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

    assert repo.get_by_id("res-1").organization_id == "org-1"
    assert [r.id for r in repo.list_by_org("org-1")] == ["res-1", "res-2"]
    assert [r.id for r in repo.list_by_resource("org-1", "resrc-1")] == [
        "res-1",
        "res-2",
    ]

    overlap = repo.list_overlapping(
        "org-1",
        "resrc-1",
        base_start + timedelta(minutes=15),
        base_end + timedelta(minutes=15),
    )
    assert [r.id for r in overlap] == ["res-1", "res-2"]

    non_overlap = repo.list_overlapping(
        "org-1",
        "resrc-1",
        base_end + timedelta(hours=1),
        base_end + timedelta(hours=2),
    )
    assert non_overlap == []
