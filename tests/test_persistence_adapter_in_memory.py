"""Tests for the in-memory persistence adapter."""

from datetime import datetime, timedelta

import pytest

from planninghub.adapters.persistence.in_memory import InMemoryPersistenceAdapter
from planninghub.application.dtos.conflict import DetectConflictsRequest, ListConflictsRequest
from planninghub.application.dtos.identity import (
    AddMembershipRequest,
    CreateOrganizationRequest,
    CreateUserRequest,
    ListMembershipsRequest,
)
from planninghub.application.dtos.time_reservation import (
    CreateReservationRequest,
    ListReservationsRequest,
    TimeRangeDTO,
    UpdateReservationRequest,
)


def test_create_membership_and_list_filters() -> None:
    adapter = InMemoryPersistenceAdapter()
    organization = adapter.create_organization(CreateOrganizationRequest(name="Org"))
    user = adapter.create_user(CreateUserRequest(email="a@example.com", display_name="A"))

    membership = adapter.add_membership(
        AddMembershipRequest(
            user_id=user.id,
            organization_id=organization.id,
            role="owner",
        )
    )

    assert membership.organization_id == organization.id
    assert membership.user_id == user.id

    by_org = adapter.list_memberships(
        ListMembershipsRequest(organization_id=organization.id)
    )
    assert [m.id for m in by_org] == [membership.id]

    by_user = adapter.list_memberships(ListMembershipsRequest(user_id=user.id))
    assert [m.id for m in by_user] == [membership.id]


def test_duplicate_membership_rejected() -> None:
    adapter = InMemoryPersistenceAdapter()
    organization = adapter.create_organization(CreateOrganizationRequest(name="Org"))
    user = adapter.create_user(CreateUserRequest(email="a@example.com", display_name="A"))

    request = AddMembershipRequest(
        user_id=user.id,
        organization_id=organization.id,
        role="member",
    )
    adapter.add_membership(request)

    with pytest.raises(ValueError):
        adapter.add_membership(request)


def test_create_update_and_list_reservation() -> None:
    adapter = InMemoryPersistenceAdapter()
    organization = adapter.create_organization(CreateOrganizationRequest(name="Org"))
    starts_at = datetime(2024, 1, 1, 8, 0, 0)
    ends_at = datetime(2024, 1, 1, 9, 0, 0)

    reservation = adapter.create_reservation(
        CreateReservationRequest(
            organization_id=organization.id,
            resource_id="resrc-1",
            starts_at_utc=starts_at,
            ends_at_utc=ends_at,
            timezone="UTC",
            economic_value=None,
        )
    )

    assert reservation.status == "draft"

    listed = adapter.list_reservations(
        ListReservationsRequest(organization_id=organization.id)
    )
    assert [item.id for item in listed] == [reservation.id]

    updated = adapter.update_reservation(
        UpdateReservationRequest(
            reservation_id=reservation.id,
            status="active",
        )
    )
    assert updated.status == "active"

    by_range = adapter.list_reservations(
        ListReservationsRequest(
            organization_id=organization.id,
            time_range=TimeRangeDTO(start_utc=starts_at, end_utc=ends_at),
        )
    )
    assert [item.id for item in by_range] == [reservation.id]


def test_reservation_interval_invariant_enforced() -> None:
    adapter = InMemoryPersistenceAdapter()
    organization = adapter.create_organization(CreateOrganizationRequest(name="Org"))
    starts_at = datetime(2024, 1, 1, 9, 0, 0)
    ends_at = datetime(2024, 1, 1, 9, 0, 0)

    with pytest.raises(ValueError):
        adapter.create_reservation(
            CreateReservationRequest(
                organization_id=organization.id,
                resource_id=None,
                starts_at_utc=starts_at,
                ends_at_utc=ends_at,
                timezone="UTC",
                economic_value=None,
            )
        )


def test_detect_conflicts_emits_overlap() -> None:
    adapter = InMemoryPersistenceAdapter()
    organization = adapter.create_organization(CreateOrganizationRequest(name="Org"))
    starts_at = datetime(2024, 1, 1, 8, 0, 0)
    ends_at = datetime(2024, 1, 1, 9, 0, 0)

    first = adapter.create_reservation(
        CreateReservationRequest(
            organization_id=organization.id,
            resource_id="resrc-1",
            starts_at_utc=starts_at,
            ends_at_utc=ends_at,
            timezone="UTC",
            economic_value=None,
        )
    )
    adapter.create_reservation(
        CreateReservationRequest(
            organization_id=organization.id,
            resource_id="resrc-1",
            starts_at_utc=starts_at + timedelta(minutes=15),
            ends_at_utc=ends_at + timedelta(minutes=15),
            timezone="UTC",
            economic_value=None,
        )
    )

    conflicts = adapter.detect_conflicts(
        DetectConflictsRequest(organization_id=organization.id, reservation_id=first.id)
    )
    assert len(conflicts) >= 1

    listed = adapter.list_conflicts(
        ListConflictsRequest(organization_id=organization.id, reservation_id=first.id)
    )
    assert [conflict.id for conflict in listed] == [conflict.id for conflict in conflicts]
