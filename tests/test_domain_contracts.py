"""Tests for core domain contracts."""

from datetime import datetime, timedelta

import pytest

from planninghub.domain.entities import Project, Reservation, Shift
from planninghub.domain.value_objects import (
    ConflictSeverity,
    MembershipRole,
    ReservationStatus,
    ResourceType,
    ShiftStatus,
)


def test_enum_values_match_specs() -> None:
    assert [role.value for role in MembershipRole] == ["owner", "admin", "member"]
    assert [resource.value for resource in ResourceType] == [
        "human",
        "asset",
        "service",
    ]
    assert [status.value for status in ShiftStatus] == [
        "proposed",
        "accepted",
        "confirmed",
        "in_progress",
        "completed",
        "validated",
        "closed",
    ]
    assert [status.value for status in ReservationStatus] == [
        "draft",
        "active",
        "cancelled",
    ]
    assert [severity.value for severity in ConflictSeverity] == [
        "critical",
        "high",
        "medium",
        "low",
    ]


def test_reservation_interval_invariant() -> None:
    starts_at = datetime(2024, 1, 1, 8, 0, 0)
    ends_at = starts_at + timedelta(hours=1)

    Reservation(
        id="res-1",
        organization_id="org-1",
        resource_id=None,
        starts_at_utc=starts_at,
        ends_at_utc=ends_at,
        timezone="UTC",
        economic_value=None,
        status=ReservationStatus.DRAFT,
    )

    with pytest.raises(ValueError):
        Reservation(
            id="res-2",
            organization_id="org-1",
            resource_id=None,
            starts_at_utc=starts_at,
            ends_at_utc=starts_at,
            timezone="UTC",
            economic_value=None,
            status=ReservationStatus.DRAFT,
        )

    with pytest.raises(ValueError):
        Reservation(
            id="res-3",
            organization_id="org-1",
            resource_id=None,
            starts_at_utc=ends_at,
            ends_at_utc=starts_at,
            timezone="UTC",
            economic_value=None,
            status=ReservationStatus.DRAFT,
        )


def test_org_scoped_entities_require_org_id() -> None:
    with pytest.raises(ValueError):
        Project(id="proj-1", organization_id="", name="Project")

    with pytest.raises(ValueError):
        Reservation(
            id="res-4",
            organization_id="",
            resource_id=None,
            starts_at_utc=datetime(2024, 1, 1, 9, 0, 0),
            ends_at_utc=datetime(2024, 1, 1, 10, 0, 0),
            timezone="UTC",
            economic_value=None,
            status=ReservationStatus.DRAFT,
        )


def test_shift_requires_reservation_id() -> None:
    with pytest.raises(ValueError):
        Shift(
            id="shift-1",
            mission_id="mission-1",
            reservation_id="",
            status=ShiftStatus.PROPOSED,
        )
