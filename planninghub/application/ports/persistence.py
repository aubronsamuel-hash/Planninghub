"""Outbound ports for persistence operations."""

from __future__ import annotations

from typing import Protocol

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


class IdentityPersistencePort(Protocol):
    def create_user(self, request: CreateUserRequest) -> UserDTO:
        ...

    def deactivate_user(self, request: DeactivateUserRequest) -> UserDTO:
        ...

    def create_organization(self, request: CreateOrganizationRequest) -> OrganizationDTO:
        ...

    def add_membership(self, request: AddMembershipRequest) -> MembershipDTO:
        ...

    def list_memberships(self, request: ListMembershipsRequest) -> list[MembershipDTO]:
        ...


class ReservationPersistencePort(Protocol):
    def create_reservation(self, request: CreateReservationRequest) -> ReservationDTO:
        ...

    def update_reservation(self, request: UpdateReservationRequest) -> ReservationDTO:
        ...

    def get_reservation(self, request: GetReservationRequest) -> ReservationDTO:
        ...

    def list_reservations(self, request: ListReservationsRequest) -> list[ReservationDTO]:
        ...


class ProjectPersistencePort(Protocol):
    def create_project(self, request: CreateProjectRequest) -> ProjectDTO:
        ...

    def get_project(self, request: GetProjectRequest) -> ProjectDTO:
        ...


class ResourcePersistencePort(Protocol):
    def create_resource(self, request: CreateResourceRequest) -> ResourceDTO:
        ...

    def get_resource(self, request: GetResourceRequest) -> ResourceDTO:
        ...


class ConflictPersistencePort(Protocol):
    def detect_conflicts(self, request: DetectConflictsRequest) -> list[ConflictDTO]:
        ...

    def list_conflicts(self, request: ListConflictsRequest) -> list[ConflictDTO]:
        ...
