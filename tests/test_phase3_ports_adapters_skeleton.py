"""Phase 3 ports and adapters skeleton tests."""

from dataclasses import FrozenInstanceError
from datetime import datetime, timezone

import pytest

from planninghub.application.dtos.conflict import (
    ConflictDTO,
    DetectConflictsRequest,
    ListConflictsRequest,
)
from planninghub.application.dtos.identity import (
    AddMembershipRequest,
    CreateOrganizationRequest,
    CreateUserRequest,
    ListMembershipsRequest,
    MembershipDTO,
    OrganizationDTO,
    UserDTO,
)
from planninghub.application.dtos.time_reservation import (
    CreateReservationRequest,
    ListReservationsRequest,
    ReservationDTO,
)
from planninghub.application.handlers.conflict import (
    DetectConflictsHandler,
    ListConflictsHandler,
)
from planninghub.application.handlers.identity import (
    AddMembershipHandler,
    CreateOrganizationHandler,
    CreateUserHandler,
    ListMembershipsHandler,
)
from planninghub.application.handlers.time_reservation import (
    CreateReservationHandler,
    ListReservationsHandler,
)


def test_ports_modules_import() -> None:
    __import__("planninghub.application.ports.identity")
    __import__("planninghub.application.ports.time_reservation")
    __import__("planninghub.application.ports.conflict")
    __import__("planninghub.application.ports.persistence")
    __import__("planninghub.adapters.persistence.stub")


def test_dtos_are_frozen() -> None:
    user_request = CreateUserRequest(email="a@example.com", display_name="A")
    reservation = ReservationDTO(
        id="res-1",
        organization_id="org-1",
        resource_id=None,
        starts_at_utc=datetime(2024, 1, 1, tzinfo=timezone.utc),
        ends_at_utc=datetime(2024, 1, 2, tzinfo=timezone.utc),
        timezone="UTC",
        economic_value=None,
        status="draft",
    )
    conflict = ConflictDTO(
        id="conf-1",
        organization_id="org-1",
        reservation_id="res-1",
        resource_id=None,
        severity="low",
        reason="test",
    )
    with pytest.raises(FrozenInstanceError):
        user_request.email = "b@example.com"
    with pytest.raises(FrozenInstanceError):
        reservation.status = "active"
    with pytest.raises(FrozenInstanceError):
        conflict.reason = "changed"


class FakeIdentityPersistence:
    def __init__(self, memberships=None, user=None, organization=None) -> None:
        self._memberships = memberships or []
        self._user = user
        self._organization = organization

    def create_user(self, request: CreateUserRequest) -> UserDTO:
        return self._user or UserDTO(
            id="user-1",
            email=request.email,
            display_name=request.display_name,
            status="active",
        )

    def deactivate_user(self, request):  # pragma: no cover - not used
        raise NotImplementedError

    def create_organization(self, request: CreateOrganizationRequest) -> OrganizationDTO:
        return self._organization or OrganizationDTO(id="org-1", name=request.name)

    def add_membership(self, request: AddMembershipRequest) -> MembershipDTO:
        membership = MembershipDTO(
            id="mem-1",
            user_id=request.user_id,
            organization_id=request.organization_id,
            role=request.role,
        )
        self._memberships.append(membership)
        return membership

    def list_memberships(self, request: ListMembershipsRequest) -> list[MembershipDTO]:
        return list(self._memberships)


class FakeReservationPersistence:
    def __init__(self, reservation: ReservationDTO) -> None:
        self._reservation = reservation

    def create_reservation(self, request: CreateReservationRequest) -> ReservationDTO:
        return self._reservation

    def update_reservation(self, request):  # pragma: no cover - not used
        raise NotImplementedError

    def get_reservation(self, request):  # pragma: no cover - not used
        raise NotImplementedError

    def list_reservations(self, request):
        return [self._reservation]


class FakeConflictPersistence:
    def __init__(self, conflicts: list[ConflictDTO]) -> None:
        self._conflicts = conflicts

    def detect_conflicts(self, request: DetectConflictsRequest) -> list[ConflictDTO]:
        return list(self._conflicts)

    def list_conflicts(self, request: ListConflictsRequest) -> list[ConflictDTO]:
        return list(self._conflicts)


def test_identity_handlers_map_to_persistence() -> None:
    persistence = FakeIdentityPersistence()
    create_handler = CreateUserHandler(persistence)
    response = create_handler.handle(
        CreateUserRequest(email="user@example.com", display_name="User")
    )
    assert response.user.email == "user@example.com"

    org_handler = CreateOrganizationHandler(persistence)
    org_response = org_handler.handle(CreateOrganizationRequest(name="Org"))
    assert org_response.organization.name == "Org"


def test_add_membership_duplicate_membership_raises() -> None:
    existing_membership = MembershipDTO(
        id="mem-1",
        user_id="user-1",
        organization_id="org-1",
        role="member",
    )
    persistence = FakeIdentityPersistence(memberships=[existing_membership])
    handler = AddMembershipHandler(persistence)
    with pytest.raises(ValueError):
        handler.handle(
            AddMembershipRequest(
                user_id="user-1",
                organization_id="org-1",
                role="member",
            )
        )


def test_add_membership_requires_org_id() -> None:
    persistence = FakeIdentityPersistence()
    handler = AddMembershipHandler(persistence)
    with pytest.raises(ValueError):
        handler.handle(
            AddMembershipRequest(user_id="user-1", organization_id="", role="member")
        )


def test_list_memberships_requires_non_empty_filters() -> None:
    persistence = FakeIdentityPersistence()
    handler = ListMembershipsHandler(persistence)
    with pytest.raises(ValueError):
        handler.handle(ListMembershipsRequest(user_id="", organization_id=None))


def test_reservation_invariants_enforced() -> None:
    reservation = ReservationDTO(
        id="res-1",
        organization_id="org-1",
        resource_id=None,
        starts_at_utc=datetime(2024, 1, 1, tzinfo=timezone.utc),
        ends_at_utc=datetime(2024, 1, 2, tzinfo=timezone.utc),
        timezone="UTC",
        economic_value=None,
        status="draft",
    )
    handler = CreateReservationHandler(FakeReservationPersistence(reservation))
    with pytest.raises(ValueError):
        handler.handle(
            CreateReservationRequest(
                organization_id="org-1",
                resource_id=None,
                starts_at_utc=datetime(2024, 1, 2, tzinfo=timezone.utc),
                ends_at_utc=datetime(2024, 1, 1, tzinfo=timezone.utc),
                timezone="UTC",
                economic_value=None,
            )
        )


def test_list_reservations_requires_org_id() -> None:
    reservation = ReservationDTO(
        id="res-1",
        organization_id="org-1",
        resource_id=None,
        starts_at_utc=datetime(2024, 1, 1, tzinfo=timezone.utc),
        ends_at_utc=datetime(2024, 1, 2, tzinfo=timezone.utc),
        timezone="UTC",
        economic_value=None,
        status="draft",
    )
    handler = ListReservationsHandler(FakeReservationPersistence(reservation))
    with pytest.raises(ValueError):
        handler.handle(ListReservationsRequest(organization_id=""))


def test_conflict_handlers_require_org_id() -> None:
    conflicts = [
        ConflictDTO(
            id="conf-1",
            organization_id="org-1",
            reservation_id="res-1",
            resource_id=None,
            severity="low",
            reason="test",
        )
    ]
    persistence = FakeConflictPersistence(conflicts)
    detect_handler = DetectConflictsHandler(persistence)
    with pytest.raises(ValueError):
        detect_handler.handle(DetectConflictsRequest(organization_id="", reservation_id="res-1"))

    list_handler = ListConflictsHandler(persistence)
    with pytest.raises(ValueError):
        list_handler.handle(ListConflictsRequest(organization_id="", reservation_id=None))
