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

    def test_get_reservation_missing_raises_key_error(self) -> None:
        adapter = InMemoryPersistenceAdapter()

        with pytest.raises(KeyError):
            adapter.get_reservation(GetReservationRequest(reservation_id="res-404"))

    def test_list_reservations_requires_non_empty_org(self) -> None:
        adapter = InMemoryPersistenceAdapter()

        with pytest.raises(ValueError):
            adapter.list_reservations(ListReservationsRequest(organization_id=""))


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
                DetectConflictsRequest(organization_id="org-2", reservation_id=reservation.id)
            )

    def test_list_conflicts_requires_non_empty_org(self) -> None:
        adapter = InMemoryPersistenceAdapter()

        with pytest.raises(ValueError):
            adapter.list_conflicts(ListConflictsRequest(organization_id=""))
