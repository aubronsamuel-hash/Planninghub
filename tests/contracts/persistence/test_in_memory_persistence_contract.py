"""Contract tests for the in-memory persistence adapter."""

from datetime import datetime, timezone

import pytest

from planninghub.adapters.persistence.in_memory import InMemoryPersistenceAdapter
from planninghub.application.dtos.conflict import DetectConflictsRequest, ListConflictsRequest
from planninghub.application.dtos.identity import (
    AddMembershipRequest,
    CreateOrganizationRequest,
    CreateUserRequest,
    DeactivateUserRequest,
    ListMembershipsRequest,
)
from planninghub.application.dtos.time_reservation import (
    CreateReservationRequest,
    GetReservationRequest,
    ListReservationsRequest,
    UpdateReservationRequest,
)


def _utc_datetime(year: int, month: int, day: int, hour: int, minute: int) -> datetime:
    return datetime(year, month, day, hour, minute, tzinfo=timezone.utc)


class TestIdentityPersistenceContract:
    def test_create_user_and_deactivate_preserves_id(self) -> None:
        adapter = InMemoryPersistenceAdapter()

        first = adapter.create_user(
            CreateUserRequest(email="first@example.com", display_name="First")
        )
        second = adapter.create_user(
            CreateUserRequest(email="second@example.com", display_name="Second")
        )

        assert first.id == "user-1"
        assert second.id == "user-2"

        updated = adapter.deactivate_user(DeactivateUserRequest(user_id=first.id))
        assert updated.id == first.id
        assert updated.status == "inactive"

    def test_deactivate_user_missing_raises_key_error(self) -> None:
        adapter = InMemoryPersistenceAdapter()

        with pytest.raises(KeyError):
            adapter.deactivate_user(DeactivateUserRequest(user_id="user-404"))

    def test_add_membership_rejects_empty_org_and_duplicates(self) -> None:
        adapter = InMemoryPersistenceAdapter()

        with pytest.raises(ValueError):
            adapter.add_membership(
                AddMembershipRequest(
                    user_id="user-1",
                    organization_id="",
                    role="owner",
                )
            )

        organization = adapter.create_organization(CreateOrganizationRequest(name="Org"))
        request = AddMembershipRequest(
            user_id="user-1",
            organization_id=organization.id,
            role="member",
        )
        adapter.add_membership(request)

        with pytest.raises(ValueError):
            adapter.add_membership(request)

    def test_list_memberships_scoped_to_org_is_deterministic(self) -> None:
        adapter = InMemoryPersistenceAdapter()
        org_one = adapter.create_organization(CreateOrganizationRequest(name="Org One"))
        org_two = adapter.create_organization(CreateOrganizationRequest(name="Org Two"))

        membership_one = adapter.add_membership(
            AddMembershipRequest(
                user_id="user-1",
                organization_id=org_one.id,
                role="member",
            )
        )
        adapter.add_membership(
            AddMembershipRequest(
                user_id="user-2",
                organization_id=org_two.id,
                role="member",
            )
        )
        membership_two = adapter.add_membership(
            AddMembershipRequest(
                user_id="user-3",
                organization_id=org_one.id,
                role="owner",
            )
        )

        first = adapter.list_memberships(
            ListMembershipsRequest(organization_id=org_one.id)
        )
        second = adapter.list_memberships(
            ListMembershipsRequest(organization_id=org_one.id)
        )

        assert [member.id for member in first] == [member.id for member in second]
        assert {member.id for member in first} == {membership_one.id, membership_two.id}


class TestReservationPersistenceContract:
    def test_create_and_get_reservation(self) -> None:
        adapter = InMemoryPersistenceAdapter()

        reservation = adapter.create_reservation(
            CreateReservationRequest(
                organization_id="org-1",
                resource_id="resrc-1",
                starts_at_utc=_utc_datetime(2024, 1, 1, 8, 0),
                ends_at_utc=_utc_datetime(2024, 1, 1, 9, 0),
                timezone="UTC",
                economic_value=None,
            )
        )

        fetched = adapter.get_reservation(
            GetReservationRequest(reservation_id=reservation.id)
        )
        assert fetched.id == reservation.id
        assert fetched.organization_id == reservation.organization_id
        assert fetched.status == "draft"

    def test_create_reservation_requires_valid_interval(self) -> None:
        adapter = InMemoryPersistenceAdapter()

        with pytest.raises(ValueError):
            adapter.create_reservation(
                CreateReservationRequest(
                    organization_id="org-1",
                    resource_id="resrc-1",
                    starts_at_utc=_utc_datetime(2024, 1, 1, 9, 0),
                    ends_at_utc=_utc_datetime(2024, 1, 1, 9, 0),
                    timezone="UTC",
                    economic_value=None,
                )
            )

    def test_update_reservation_missing_raises_key_error(self) -> None:
        adapter = InMemoryPersistenceAdapter()

        with pytest.raises(KeyError):
            adapter.update_reservation(
                UpdateReservationRequest(reservation_id="res-404", status="active")
            )

    def test_update_reservation_invalid_status_raises_value_error(self) -> None:
        adapter = InMemoryPersistenceAdapter()
        reservation = adapter.create_reservation(
            CreateReservationRequest(
                organization_id="org-1",
                resource_id="resrc-1",
                starts_at_utc=_utc_datetime(2024, 1, 1, 8, 0),
                ends_at_utc=_utc_datetime(2024, 1, 1, 9, 0),
                timezone="UTC",
                economic_value=None,
            )
        )

        with pytest.raises(ValueError):
            adapter.update_reservation(
                UpdateReservationRequest(reservation_id=reservation.id, status="invalid")
            )

    def test_update_reservation_preserves_id_without_creating_new(self) -> None:
        adapter = InMemoryPersistenceAdapter()
        reservation = adapter.create_reservation(
            CreateReservationRequest(
                organization_id="org-1",
                resource_id="resrc-1",
                starts_at_utc=_utc_datetime(2024, 1, 1, 8, 0),
                ends_at_utc=_utc_datetime(2024, 1, 1, 9, 0),
                timezone="UTC",
                economic_value=None,
            )
        )

        updated = adapter.update_reservation(
            UpdateReservationRequest(reservation_id=reservation.id, status="active")
        )
        listed = adapter.list_reservations(
            ListReservationsRequest(organization_id=reservation.organization_id)
        )

        assert updated.id == reservation.id
        assert len(listed) == 1
        assert listed[0].id == reservation.id

    def test_get_reservation_missing_raises_key_error(self) -> None:
        adapter = InMemoryPersistenceAdapter()

        with pytest.raises(KeyError):
            adapter.get_reservation(GetReservationRequest(reservation_id="res-404"))

    def test_list_reservations_requires_non_empty_org(self) -> None:
        adapter = InMemoryPersistenceAdapter()

        with pytest.raises(ValueError):
            adapter.list_reservations(ListReservationsRequest(organization_id=""))

    def test_list_reservations_scoped_to_org_is_deterministic(self) -> None:
        adapter = InMemoryPersistenceAdapter()

        org_one = "org-1"
        org_two = "org-2"
        first = adapter.create_reservation(
            CreateReservationRequest(
                organization_id=org_one,
                resource_id="resrc-1",
                starts_at_utc=_utc_datetime(2024, 1, 1, 8, 0),
                ends_at_utc=_utc_datetime(2024, 1, 1, 9, 0),
                timezone="UTC",
                economic_value=None,
            )
        )
        adapter.create_reservation(
            CreateReservationRequest(
                organization_id=org_two,
                resource_id="resrc-2",
                starts_at_utc=_utc_datetime(2024, 1, 2, 8, 0),
                ends_at_utc=_utc_datetime(2024, 1, 2, 9, 0),
                timezone="UTC",
                economic_value=None,
            )
        )
        second = adapter.create_reservation(
            CreateReservationRequest(
                organization_id=org_one,
                resource_id="resrc-3",
                starts_at_utc=_utc_datetime(2024, 1, 3, 8, 0),
                ends_at_utc=_utc_datetime(2024, 1, 3, 9, 0),
                timezone="UTC",
                economic_value=None,
            )
        )

        first_list = adapter.list_reservations(
            ListReservationsRequest(organization_id=org_one)
        )
        second_list = adapter.list_reservations(
            ListReservationsRequest(organization_id=org_one)
        )

        assert [reservation.id for reservation in first_list] == [
            reservation.id for reservation in second_list
        ]
        assert {reservation.id for reservation in first_list} == {
            first.id,
            second.id,
        }


class TestConflictPersistenceContract:
    def test_detect_conflicts_requires_non_empty_org(self) -> None:
        adapter = InMemoryPersistenceAdapter()
        reservation = adapter.create_reservation(
            CreateReservationRequest(
                organization_id="org-1",
                resource_id="resrc-1",
                starts_at_utc=_utc_datetime(2024, 1, 1, 8, 0),
                ends_at_utc=_utc_datetime(2024, 1, 1, 9, 0),
                timezone="UTC",
                economic_value=None,
            )
        )

        with pytest.raises(ValueError):
            adapter.detect_conflicts(
                DetectConflictsRequest(organization_id="", reservation_id=reservation.id)
            )

    def test_detect_conflicts_missing_reservation_raises_key_error(self) -> None:
        adapter = InMemoryPersistenceAdapter()

        with pytest.raises(KeyError):
            adapter.detect_conflicts(
                DetectConflictsRequest(organization_id="org-1", reservation_id="res-404")
            )

    def test_detect_conflicts_reservation_org_mismatch_raises(self) -> None:
        adapter = InMemoryPersistenceAdapter()
        reservation = adapter.create_reservation(
            CreateReservationRequest(
                organization_id="org-1",
                resource_id="resrc-1",
                starts_at_utc=_utc_datetime(2024, 1, 1, 8, 0),
                ends_at_utc=_utc_datetime(2024, 1, 1, 9, 0),
                timezone="UTC",
                economic_value=None,
            )
        )

        with pytest.raises(ValueError):
            adapter.detect_conflicts(
                DetectConflictsRequest(
                    organization_id="org-2",
                    reservation_id=reservation.id,
                )
            )

    def test_list_conflicts_requires_non_empty_org(self) -> None:
        adapter = InMemoryPersistenceAdapter()

        with pytest.raises(ValueError):
            adapter.list_conflicts(ListConflictsRequest(organization_id=""))

    def test_list_conflicts_scoped_to_org_is_deterministic(self) -> None:
        adapter = InMemoryPersistenceAdapter()

        org_one = "org-1"
        org_two = "org-2"

        reservation_one = adapter.create_reservation(
            CreateReservationRequest(
                organization_id=org_one,
                resource_id="resrc-1",
                starts_at_utc=_utc_datetime(2024, 1, 1, 8, 0),
                ends_at_utc=_utc_datetime(2024, 1, 1, 10, 0),
                timezone="UTC",
                economic_value=None,
            )
        )
        adapter.create_reservation(
            CreateReservationRequest(
                organization_id=org_one,
                resource_id="resrc-1",
                starts_at_utc=_utc_datetime(2024, 1, 1, 9, 0),
                ends_at_utc=_utc_datetime(2024, 1, 1, 11, 0),
                timezone="UTC",
                economic_value=None,
            )
        )
        adapter.detect_conflicts(
            DetectConflictsRequest(
                organization_id=org_one,
                reservation_id=reservation_one.id,
            )
        )

        reservation_two = adapter.create_reservation(
            CreateReservationRequest(
                organization_id=org_two,
                resource_id="resrc-2",
                starts_at_utc=_utc_datetime(2024, 1, 2, 8, 0),
                ends_at_utc=_utc_datetime(2024, 1, 2, 10, 0),
                timezone="UTC",
                economic_value=None,
            )
        )
        adapter.create_reservation(
            CreateReservationRequest(
                organization_id=org_two,
                resource_id="resrc-2",
                starts_at_utc=_utc_datetime(2024, 1, 2, 9, 0),
                ends_at_utc=_utc_datetime(2024, 1, 2, 11, 0),
                timezone="UTC",
                economic_value=None,
            )
        )
        adapter.detect_conflicts(
            DetectConflictsRequest(
                organization_id=org_two,
                reservation_id=reservation_two.id,
            )
        )

        first = adapter.list_conflicts(
            ListConflictsRequest(organization_id=org_one)
        )
        second = adapter.list_conflicts(
            ListConflictsRequest(organization_id=org_one)
        )

        assert [conflict.id for conflict in first] == [
            conflict.id for conflict in second
        ]
        assert {conflict.organization_id for conflict in first} == {org_one}
