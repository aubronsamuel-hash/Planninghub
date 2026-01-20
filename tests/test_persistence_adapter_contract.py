"""Compliance tests for persistence adapter contract."""

from datetime import datetime, timedelta

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
    TimeRangeDTO,
    UpdateReservationRequest,
)
from planninghub.application.ports.persistence import (
    ConflictPersistencePort,
    IdentityPersistencePort,
    ReservationPersistencePort,
)


@pytest.fixture()
def persistence_adapter() -> (
    IdentityPersistencePort & ReservationPersistencePort & ConflictPersistencePort
):
    return InMemoryPersistenceAdapter()


class TestIdentityContract:
    def test_create_user_returns_prefixed_id(
        self, persistence_adapter: IdentityPersistencePort
    ) -> None:
        user = persistence_adapter.create_user(
            CreateUserRequest(email="a@example.com", display_name="A")
        )
        assert user.id.startswith("user-")

    def test_deactivate_user_marks_inactive(
        self, persistence_adapter: IdentityPersistencePort
    ) -> None:
        user = persistence_adapter.create_user(
            CreateUserRequest(email="a@example.com", display_name="A")
        )
        updated = persistence_adapter.deactivate_user(
            DeactivateUserRequest(user_id=user.id)
        )
        assert updated.status == "inactive"

    def test_deactivate_user_missing_raises(
        self, persistence_adapter: IdentityPersistencePort
    ) -> None:
        with pytest.raises(KeyError):
            persistence_adapter.deactivate_user(DeactivateUserRequest(user_id="user-404"))

    def test_create_organization_returns_prefixed_id(
        self, persistence_adapter: IdentityPersistencePort
    ) -> None:
        organization = persistence_adapter.create_organization(
            CreateOrganizationRequest(name="Org")
        )
        assert organization.id.startswith("org-")

    def test_add_membership_accepts_arbitrary_user_id(
        self, persistence_adapter: IdentityPersistencePort
    ) -> None:
        organization = persistence_adapter.create_organization(
            CreateOrganizationRequest(name="Org")
        )
        membership = persistence_adapter.add_membership(
            AddMembershipRequest(
                user_id="user-external",
                organization_id=organization.id,
                role="owner",
            )
        )
        assert membership.user_id == "user-external"

    def test_add_membership_requires_non_empty_org(
        self, persistence_adapter: IdentityPersistencePort
    ) -> None:
        with pytest.raises(ValueError):
            persistence_adapter.add_membership(
                AddMembershipRequest(
                    user_id="user-1",
                    organization_id="",
                    role="owner",
                )
            )

    def test_add_membership_requires_valid_role(
        self, persistence_adapter: IdentityPersistencePort
    ) -> None:
        organization = persistence_adapter.create_organization(
            CreateOrganizationRequest(name="Org")
        )
        with pytest.raises(ValueError):
            persistence_adapter.add_membership(
                AddMembershipRequest(
                    user_id="user-1",
                    organization_id=organization.id,
                    role="invalid",
                )
            )

    def test_add_membership_rejects_duplicates(
        self, persistence_adapter: IdentityPersistencePort
    ) -> None:
        organization = persistence_adapter.create_organization(
            CreateOrganizationRequest(name="Org")
        )
        request = AddMembershipRequest(
            user_id="user-1",
            organization_id=organization.id,
            role="member",
        )
        persistence_adapter.add_membership(request)
        with pytest.raises(ValueError):
            persistence_adapter.add_membership(request)

    def test_list_memberships_filters(
        self, persistence_adapter: IdentityPersistencePort
    ) -> None:
        organization = persistence_adapter.create_organization(
            CreateOrganizationRequest(name="Org")
        )
        other_org = persistence_adapter.create_organization(
            CreateOrganizationRequest(name="Other")
        )
        membership = persistence_adapter.add_membership(
            AddMembershipRequest(
                user_id="user-1",
                organization_id=organization.id,
                role="owner",
            )
        )
        persistence_adapter.add_membership(
            AddMembershipRequest(
                user_id="user-2",
                organization_id=other_org.id,
                role="member",
            )
        )

        by_org = persistence_adapter.list_memberships(
            ListMembershipsRequest(organization_id=organization.id)
        )
        assert [item.id for item in by_org] == [membership.id]

        by_user = persistence_adapter.list_memberships(
            ListMembershipsRequest(user_id="user-1")
        )
        assert [item.id for item in by_user] == [membership.id]


class TestReservationContract:
    def test_create_reservation_requires_org(
        self, persistence_adapter: ReservationPersistencePort
    ) -> None:
        with pytest.raises(ValueError):
            persistence_adapter.create_reservation(
                CreateReservationRequest(
                    organization_id="",
                    resource_id="resrc-1",
                    starts_at_utc=datetime(2024, 1, 1, 8, 0, 0),
                    ends_at_utc=datetime(2024, 1, 1, 9, 0, 0),
                    timezone="UTC",
                    economic_value=None,
                )
            )

    def test_create_reservation_requires_valid_interval(
        self, persistence_adapter: ReservationPersistencePort
    ) -> None:
        with pytest.raises(ValueError):
            persistence_adapter.create_reservation(
                CreateReservationRequest(
                    organization_id="org-1",
                    resource_id="resrc-1",
                    starts_at_utc=datetime(2024, 1, 1, 9, 0, 0),
                    ends_at_utc=datetime(2024, 1, 1, 9, 0, 0),
                    timezone="UTC",
                    economic_value=None,
                )
            )

    def test_create_reservation_defaults_to_draft(
        self, persistence_adapter: ReservationPersistencePort
    ) -> None:
        reservation = persistence_adapter.create_reservation(
            CreateReservationRequest(
                organization_id="org-1",
                resource_id="resrc-1",
                starts_at_utc=datetime(2024, 1, 1, 8, 0, 0),
                ends_at_utc=datetime(2024, 1, 1, 9, 0, 0),
                timezone="UTC",
                economic_value=None,
            )
        )
        assert reservation.status == "draft"

    def test_update_reservation_missing_raises(
        self, persistence_adapter: ReservationPersistencePort
    ) -> None:
        with pytest.raises(KeyError):
            persistence_adapter.update_reservation(
                UpdateReservationRequest(reservation_id="res-404", status="active")
            )

    def test_update_reservation_invalid_status_raises(
        self, persistence_adapter: ReservationPersistencePort
    ) -> None:
        reservation = persistence_adapter.create_reservation(
            CreateReservationRequest(
                organization_id="org-1",
                resource_id="resrc-1",
                starts_at_utc=datetime(2024, 1, 1, 8, 0, 0),
                ends_at_utc=datetime(2024, 1, 1, 9, 0, 0),
                timezone="UTC",
                economic_value=None,
            )
        )
        with pytest.raises(ValueError):
            persistence_adapter.update_reservation(
                UpdateReservationRequest(reservation_id=reservation.id, status="bogus")
            )

    def test_update_reservation_valid_status_updates(
        self, persistence_adapter: ReservationPersistencePort
    ) -> None:
        reservation = persistence_adapter.create_reservation(
            CreateReservationRequest(
                organization_id="org-1",
                resource_id="resrc-1",
                starts_at_utc=datetime(2024, 1, 1, 8, 0, 0),
                ends_at_utc=datetime(2024, 1, 1, 9, 0, 0),
                timezone="UTC",
                economic_value=None,
            )
        )
        updated = persistence_adapter.update_reservation(
            UpdateReservationRequest(reservation_id=reservation.id, status="active")
        )
        assert updated.status == "active"

    def test_get_reservation_missing_raises(
        self, persistence_adapter: ReservationPersistencePort
    ) -> None:
        with pytest.raises(KeyError):
            persistence_adapter.get_reservation(
                GetReservationRequest(reservation_id="res-404")
            )

    def test_list_reservations_requires_org(
        self, persistence_adapter: ReservationPersistencePort
    ) -> None:
        with pytest.raises(ValueError):
            persistence_adapter.list_reservations(ListReservationsRequest(organization_id=""))

    def test_list_reservations_filters_by_resource_id(
        self, persistence_adapter: ReservationPersistencePort
    ) -> None:
        reservation = persistence_adapter.create_reservation(
            CreateReservationRequest(
                organization_id="org-1",
                resource_id="resrc-1",
                starts_at_utc=datetime(2024, 1, 1, 8, 0, 0),
                ends_at_utc=datetime(2024, 1, 1, 9, 0, 0),
                timezone="UTC",
                economic_value=None,
            )
        )
        persistence_adapter.create_reservation(
            CreateReservationRequest(
                organization_id="org-1",
                resource_id="resrc-2",
                starts_at_utc=datetime(2024, 1, 1, 10, 0, 0),
                ends_at_utc=datetime(2024, 1, 1, 11, 0, 0),
                timezone="UTC",
                economic_value=None,
            )
        )

        listed = persistence_adapter.list_reservations(
            ListReservationsRequest(organization_id="org-1", resource_id="resrc-1")
        )
        assert [item.id for item in listed] == [reservation.id]

    def test_list_reservations_filters_by_time_range(
        self, persistence_adapter: ReservationPersistencePort
    ) -> None:
        reservation = persistence_adapter.create_reservation(
            CreateReservationRequest(
                organization_id="org-1",
                resource_id="resrc-1",
                starts_at_utc=datetime(2024, 1, 1, 8, 0, 0),
                ends_at_utc=datetime(2024, 1, 1, 9, 0, 0),
                timezone="UTC",
                economic_value=None,
            )
        )
        persistence_adapter.create_reservation(
            CreateReservationRequest(
                organization_id="org-1",
                resource_id="resrc-2",
                starts_at_utc=datetime(2024, 1, 1, 12, 0, 0),
                ends_at_utc=datetime(2024, 1, 1, 13, 0, 0),
                timezone="UTC",
                economic_value=None,
            )
        )

        listed = persistence_adapter.list_reservations(
            ListReservationsRequest(
                organization_id="org-1",
                time_range=TimeRangeDTO(
                    start_utc=datetime(2024, 1, 1, 8, 30, 0),
                    end_utc=datetime(2024, 1, 1, 9, 30, 0),
                ),
            )
        )
        assert [item.id for item in listed] == [reservation.id]

    def test_list_reservations_invalid_time_range_raises(
        self, persistence_adapter: ReservationPersistencePort
    ) -> None:
        with pytest.raises(ValueError):
            persistence_adapter.list_reservations(
                ListReservationsRequest(
                    organization_id="org-1",
                    time_range=TimeRangeDTO(
                        start_utc=datetime(2024, 1, 1, 9, 0, 0),
                        end_utc=datetime(2024, 1, 1, 9, 0, 0),
                    ),
                )
            )


class TestConflictContract:
    def test_detect_conflicts_missing_reservation_raises(
        self, persistence_adapter: ConflictPersistencePort
    ) -> None:
        with pytest.raises(KeyError):
            persistence_adapter.detect_conflicts(
                DetectConflictsRequest(organization_id="org-1", reservation_id="res-404")
            )

    def test_detect_conflicts_wrong_org_raises(
        self, persistence_adapter: ConflictPersistencePort
    ) -> None:
        reservation = persistence_adapter.create_reservation(
            CreateReservationRequest(
                organization_id="org-1",
                resource_id="resrc-1",
                starts_at_utc=datetime(2024, 1, 1, 8, 0, 0),
                ends_at_utc=datetime(2024, 1, 1, 9, 0, 0),
                timezone="UTC",
                economic_value=None,
            )
        )
        with pytest.raises(ValueError):
            persistence_adapter.detect_conflicts(
                DetectConflictsRequest(organization_id="org-2", reservation_id=reservation.id)
            )

    def test_detect_conflicts_resource_none_returns_empty(
        self, persistence_adapter: ConflictPersistencePort
    ) -> None:
        reservation = persistence_adapter.create_reservation(
            CreateReservationRequest(
                organization_id="org-1",
                resource_id=None,
                starts_at_utc=datetime(2024, 1, 1, 8, 0, 0),
                ends_at_utc=datetime(2024, 1, 1, 9, 0, 0),
                timezone="UTC",
                economic_value=None,
            )
        )
        conflicts = persistence_adapter.detect_conflicts(
            DetectConflictsRequest(organization_id="org-1", reservation_id=reservation.id)
        )
        assert conflicts == []

    def test_detect_conflicts_overlap_emits_high_severity(
        self, persistence_adapter: ConflictPersistencePort
    ) -> None:
        starts_at = datetime(2024, 1, 1, 8, 0, 0)
        ends_at = datetime(2024, 1, 1, 9, 0, 0)
        first = persistence_adapter.create_reservation(
            CreateReservationRequest(
                organization_id="org-1",
                resource_id="resrc-1",
                starts_at_utc=starts_at,
                ends_at_utc=ends_at,
                timezone="UTC",
                economic_value=None,
            )
        )
        other = persistence_adapter.create_reservation(
            CreateReservationRequest(
                organization_id="org-1",
                resource_id="resrc-1",
                starts_at_utc=starts_at + timedelta(minutes=15),
                ends_at_utc=ends_at + timedelta(minutes=15),
                timezone="UTC",
                economic_value=None,
            )
        )

        conflicts = persistence_adapter.detect_conflicts(
            DetectConflictsRequest(organization_id="org-1", reservation_id=first.id)
        )
        assert len(conflicts) >= 1
        assert conflicts[0].severity == "high"
        assert conflicts[0].reason == f"overlap:{other.id}"

    def test_list_conflicts_filters(self, persistence_adapter: ConflictPersistencePort) -> None:
        starts_at = datetime(2024, 1, 1, 8, 0, 0)
        ends_at = datetime(2024, 1, 1, 9, 0, 0)
        first = persistence_adapter.create_reservation(
            CreateReservationRequest(
                organization_id="org-1",
                resource_id="resrc-1",
                starts_at_utc=starts_at,
                ends_at_utc=ends_at,
                timezone="UTC",
                economic_value=None,
            )
        )
        persistence_adapter.create_reservation(
            CreateReservationRequest(
                organization_id="org-1",
                resource_id="resrc-1",
                starts_at_utc=starts_at + timedelta(minutes=15),
                ends_at_utc=ends_at + timedelta(minutes=15),
                timezone="UTC",
                economic_value=None,
            )
        )
        persistence_adapter.detect_conflicts(
            DetectConflictsRequest(organization_id="org-1", reservation_id=first.id)
        )

        by_org = persistence_adapter.list_conflicts(ListConflictsRequest(organization_id="org-1"))
        assert len(by_org) == 1

        by_reservation = persistence_adapter.list_conflicts(
            ListConflictsRequest(organization_id="org-1", reservation_id=first.id)
        )
        assert [item.id for item in by_reservation] == [item.id for item in by_org]
