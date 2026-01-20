"""Persistence adapter stubs."""

from __future__ import annotations

from planninghub.application.dtos.conflict import (
    ConflictDTO,
    DetectConflictsRequest,
    ListConflictsRequest,
)
from planninghub.application.dtos.identity import (
    AddMembershipRequest,
    CreateOrganizationRequest,
    CreateUserRequest,
    DeactivateUserRequest,
    ListMembershipsRequest,
    MembershipDTO,
    OrganizationDTO,
    UserDTO,
)
from planninghub.application.dtos.project import (
    CreateProjectRequest,
    GetProjectRequest,
    ProjectDTO,
)
from planninghub.application.dtos.resource import (
    CreateResourceRequest,
    GetResourceRequest,
    ResourceDTO,
)
from planninghub.application.dtos.time_reservation import (
    CreateReservationRequest,
    GetReservationRequest,
    ListReservationsRequest,
    ReservationDTO,
    UpdateReservationRequest,
)
from planninghub.application.ports.persistence import (
    ConflictPersistencePort,
    IdentityPersistencePort,
    ProjectPersistencePort,
    ReservationPersistencePort,
    ResourcePersistencePort,
)


class StubPersistenceAdapter(
    IdentityPersistencePort,
    ReservationPersistencePort,
    ProjectPersistencePort,
    ResourcePersistencePort,
    ConflictPersistencePort,
):
    def create_user(self, request: CreateUserRequest) -> UserDTO:
        raise NotImplementedError

    def deactivate_user(self, request: DeactivateUserRequest) -> UserDTO:
        raise NotImplementedError

    def create_organization(self, request: CreateOrganizationRequest) -> OrganizationDTO:
        raise NotImplementedError

    def add_membership(self, request: AddMembershipRequest) -> MembershipDTO:
        raise NotImplementedError

    def list_memberships(self, request: ListMembershipsRequest) -> list[MembershipDTO]:
        raise NotImplementedError

    def create_project(self, request: CreateProjectRequest) -> ProjectDTO:
        raise NotImplementedError

    def get_project(self, request: GetProjectRequest) -> ProjectDTO:
        raise NotImplementedError

    def create_resource(self, request: CreateResourceRequest) -> ResourceDTO:
        raise NotImplementedError

    def get_resource(self, request: GetResourceRequest) -> ResourceDTO:
        raise NotImplementedError

    def create_reservation(self, request: CreateReservationRequest) -> ReservationDTO:
        raise NotImplementedError

    def update_reservation(self, request: UpdateReservationRequest) -> ReservationDTO:
        raise NotImplementedError

    def get_reservation(self, request: GetReservationRequest) -> ReservationDTO:
        raise NotImplementedError

    def list_reservations(self, request: ListReservationsRequest) -> list[ReservationDTO]:
        raise NotImplementedError

    def detect_conflicts(self, request: DetectConflictsRequest) -> list[ConflictDTO]:
        raise NotImplementedError

    def list_conflicts(self, request: ListConflictsRequest) -> list[ConflictDTO]:
        raise NotImplementedError
