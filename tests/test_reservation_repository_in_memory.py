"""Tests for in-memory reservation repository."""

from datetime import datetime, timedelta

from planninghub.domain.entities import Reservation
from planninghub.domain.value_objects import ReservationStatus
from planninghub.infra.repositories_in_memory import InMemoryReservationRepository


def test_add_and_get_by_id_roundtrip() -> None:
    repo = InMemoryReservationRepository()
    reservation = Reservation(
        id="res-1",
        organization_id="org-1",
        resource_id="resrc-1",
        starts_at_utc=datetime(2024, 2, 1, 9, 0, 0),
        ends_at_utc=datetime(2024, 2, 1, 10, 0, 0),
        timezone="UTC",
        economic_value=None,
        status=ReservationStatus.ACTIVE,
    )

    repo.add(reservation)

    assert repo.get_by_id("res-1") == reservation
    assert repo.get_by_id("missing") is None


def test_list_overlapping_filters_and_ordering() -> None:
    repo = InMemoryReservationRepository()
    base_start = datetime(2024, 3, 1, 8, 0, 0)
    base_end = base_start + timedelta(hours=2)

    repo.add(
        Reservation(
            id="res-2",
            organization_id="org-1",
            resource_id="resrc-1",
            starts_at_utc=base_start + timedelta(minutes=30),
            ends_at_utc=base_end,
            timezone="UTC",
            economic_value=None,
            status=ReservationStatus.ACTIVE,
        )
    )
    repo.add(
        Reservation(
            id="res-1",
            organization_id="org-1",
            resource_id="resrc-1",
            starts_at_utc=base_start,
            ends_at_utc=base_start + timedelta(minutes=45),
            timezone="UTC",
            economic_value=None,
            status=ReservationStatus.ACTIVE,
        )
    )
    repo.add(
        Reservation(
            id="res-3",
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
        base_start + timedelta(minutes=15),
        base_end,
    )

    assert [reservation.id for reservation in overlap] == ["res-1", "res-2"]

    non_overlap = repo.list_overlapping(
        "org-1",
        "resrc-1",
        base_end,
        base_end + timedelta(hours=1),
    )

    assert non_overlap == []
