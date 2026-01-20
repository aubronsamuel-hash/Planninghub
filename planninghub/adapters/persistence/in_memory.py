"""In-memory persistence adapter."""

from __future__ import annotations

from dataclasses import replace
from typing import TypeVar

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
    TimeRangeDTO,
    UpdateReservationRequest,
)
from planninghub.application.ports.persistence import (
    ConflictPersistencePort,
    IdentityPersistencePort,
    ProjectPersistencePort,
    ReservationPersistencePort,
    ResourcePersistencePort,
)

ROLE_VALUES = {"owner", "admin", "member"}
RESOURCE_TYPE_VALUES = {"human", "asset", "service"}
RESERVATION_STATUS_VALUES = {"draft", "active", "cancelled"}
CONFLICT_SEVERITY_VALUES = {"critical", "high", "medium", "low"}

T = TypeVar("T")


class InMemoryPersistenceAdapter(
    IdentityPersistencePort,
    ReservationPersistencePort,
    ProjectPersistencePort,
    ResourcePersistencePort,
    ConflictPersistencePort,
):
    """Deterministic in-memory persistence adapter."""

    def __init__(self) -> None:
        self._users: dict[str, UserDTO] = {}
        self._organizations: dict[str, OrganizationDTO] = {}
        self._memberships: dict[str, MembershipDTO] = {}
        self._projects: dict[str, ProjectDTO] = {}
        self._resources: dict[str, ResourceDTO] = {}
        self._reservations: dict[str, ReservationDTO] = {}
        self._conflicts: dict[str, ConflictDTO] = {}
        self._membership_index: dict[tuple[str, str], str] = {}
        self._conflict_index: dict[tuple[str, str], str] = {}
        self._counters = {
            "user": 0,
            "org": 0,
            "mem": 0,
            "project": 0,
            "resource": 0,
            "res": 0,
            "conf": 0,
        }

    def create_user(self, request: CreateUserRequest) -> UserDTO:
        user_id = self._next_id("user")
        user = UserDTO(
            id=user_id,
            email=request.email,
            display_name=request.display_name,
            status="active",
        )
        self._users[user_id] = user
        return user

    def deactivate_user(self, request: DeactivateUserRequest) -> UserDTO:
        user = self._get_required(self._users, request.user_id, "user")
        updated = replace(user, status="inactive")
        self._users[user.id] = updated
        return updated

    def create_organization(self, request: CreateOrganizationRequest) -> OrganizationDTO:
        organization_id = self._next_id("org")
        organization = OrganizationDTO(id=organization_id, name=request.name)
        self._organizations[organization_id] = organization
        return organization

    def add_membership(self, request: AddMembershipRequest) -> MembershipDTO:
        self._require_organization_id(request.organization_id, "membership")
        self._require_role(request.role)
        key = (request.user_id, request.organization_id)
        if key in self._membership_index:
            raise ValueError("Duplicate membership for user and organization.")
        membership_id = self._next_id("mem")
        membership = MembershipDTO(
            id=membership_id,
            user_id=request.user_id,
            organization_id=request.organization_id,
            role=request.role,
        )
        self._memberships[membership_id] = membership
        self._membership_index[key] = membership_id
        return membership

    def list_memberships(self, request: ListMembershipsRequest) -> list[MembershipDTO]:
        if request.organization_id is not None:
            self._require_organization_id(request.organization_id, "membership")
        memberships = list(self._memberships.values())
        if request.user_id is not None:
            memberships = [m for m in memberships if m.user_id == request.user_id]
        if request.organization_id is not None:
            memberships = [
                m for m in memberships if m.organization_id == request.organization_id
            ]
        return memberships

    def create_project(self, request: CreateProjectRequest) -> ProjectDTO:
        self._require_organization_id(request.organization_id, "project")
        project_id = self._next_id("project")
        project = ProjectDTO(
            id=project_id,
            organization_id=request.organization_id,
            name=request.name,
        )
        self._projects[project_id] = project
        return project

    def get_project(self, request: GetProjectRequest) -> ProjectDTO:
        return self._get_required(self._projects, request.project_id, "project")

    def create_resource(self, request: CreateResourceRequest) -> ResourceDTO:
        self._require_organization_id(request.organization_id, "resource")
        self._require_resource_type(request.type)
        resource_id = self._next_id("resource")
        resource = ResourceDTO(
            id=resource_id,
            organization_id=request.organization_id,
            type=request.type,
            name=request.name,
        )
        self._resources[resource_id] = resource
        return resource

    def get_resource(self, request: GetResourceRequest) -> ResourceDTO:
        return self._get_required(self._resources, request.resource_id, "resource")

    def create_reservation(self, request: CreateReservationRequest) -> ReservationDTO:
        self._require_organization_id(request.organization_id, "reservation")
        self._require_valid_interval(request.starts_at_utc, request.ends_at_utc)
        reservation_id = self._next_id("res")
        reservation = ReservationDTO(
            id=reservation_id,
            organization_id=request.organization_id,
            resource_id=request.resource_id,
            starts_at_utc=request.starts_at_utc,
            ends_at_utc=request.ends_at_utc,
            timezone=request.timezone,
            economic_value=request.economic_value,
            status="draft",
        )
        self._reservations[reservation_id] = reservation
        return reservation

    def update_reservation(self, request: UpdateReservationRequest) -> ReservationDTO:
        reservation = self._get_required(
            self._reservations, request.reservation_id, "reservation"
        )
        starts_at_utc = request.starts_at_utc or reservation.starts_at_utc
        ends_at_utc = request.ends_at_utc or reservation.ends_at_utc
        self._require_valid_interval(starts_at_utc, ends_at_utc)
        resource_id = reservation.resource_id
        if request.resource_id is not None:
            resource_id = request.resource_id
        status = reservation.status
        if request.status is not None:
            self._require_reservation_status(request.status)
            status = request.status
        updated = ReservationDTO(
            id=reservation.id,
            organization_id=reservation.organization_id,
            resource_id=resource_id,
            starts_at_utc=starts_at_utc,
            ends_at_utc=ends_at_utc,
            timezone=reservation.timezone,
            economic_value=reservation.economic_value,
            status=status,
        )
        self._reservations[reservation.id] = updated
        return updated

    def get_reservation(self, request: GetReservationRequest) -> ReservationDTO:
        return self._get_required(self._reservations, request.reservation_id, "reservation")

    def list_reservations(self, request: ListReservationsRequest) -> list[ReservationDTO]:
        self._require_organization_id(request.organization_id, "reservation")
        reservations = [
            reservation
            for reservation in self._reservations.values()
            if reservation.organization_id == request.organization_id
        ]
        if request.resource_id is not None:
            reservations = [
                reservation
                for reservation in reservations
                if reservation.resource_id == request.resource_id
            ]
        if request.time_range is not None:
            self._require_valid_interval(
                request.time_range.start_utc,
                request.time_range.end_utc,
            )
            reservations = [
                reservation
                for reservation in reservations
                if self._overlaps(
                    reservation.starts_at_utc,
                    reservation.ends_at_utc,
                    request.time_range,
                )
            ]
        return reservations

    def detect_conflicts(self, request: DetectConflictsRequest) -> list[ConflictDTO]:
        self._require_organization_id(request.organization_id, "conflict")
        reservation = self._get_required(
            self._reservations, request.reservation_id, "reservation"
        )
        if reservation.organization_id != request.organization_id:
            raise ValueError("Reservation is not scoped to the organization.")
        if reservation.resource_id is None:
            return []
        conflicts: list[ConflictDTO] = []
        for other in self._reservations.values():
            if other.id == reservation.id:
                continue
            if other.organization_id != reservation.organization_id:
                continue
            if other.resource_id != reservation.resource_id:
                continue
            if not self._overlaps(
                reservation.starts_at_utc,
                reservation.ends_at_utc,
                TimeRangeDTO(
                    start_utc=other.starts_at_utc,
                    end_utc=other.ends_at_utc,
                ),
            ):
                continue
            key = (reservation.id, other.id)
            conflict_id = self._conflict_index.get(key)
            if conflict_id is None:
                self._require_conflict_severity("high")
                conflict_id = self._next_id("conf")
                conflict = ConflictDTO(
                    id=conflict_id,
                    organization_id=reservation.organization_id,
                    reservation_id=reservation.id,
                    resource_id=reservation.resource_id,
                    severity="high",
                    reason=f"overlap:{other.id}",
                )
                self._conflicts[conflict_id] = conflict
                self._conflict_index[key] = conflict_id
            conflicts.append(self._conflicts[conflict_id])
        return conflicts

    def list_conflicts(self, request: ListConflictsRequest) -> list[ConflictDTO]:
        self._require_organization_id(request.organization_id, "conflict")
        conflicts = [
            conflict
            for conflict in self._conflicts.values()
            if conflict.organization_id == request.organization_id
        ]
        if request.reservation_id is not None:
            conflicts = [
                conflict
                for conflict in conflicts
                if conflict.reservation_id == request.reservation_id
            ]
        return conflicts

    def _next_id(self, prefix: str) -> str:
        self._counters[prefix] += 1
        return f"{prefix}-{self._counters[prefix]}"

    @staticmethod
    def _get_required(data: dict[str, T], key: str, label: str) -> T:
        if key not in data:
            raise KeyError(f"{label} not found: {key}")
        return data[key]

    @staticmethod
    def _require_organization_id(organization_id: str, label: str) -> None:
        if not organization_id:
            raise ValueError(f"{label} requires a non-empty organization_id.")

    @staticmethod
    def _require_role(role: str) -> None:
        if role not in ROLE_VALUES:
            raise ValueError("Role must be one of: owner, admin, member.")

    @staticmethod
    def _require_resource_type(resource_type: str) -> None:
        if resource_type not in RESOURCE_TYPE_VALUES:
            raise ValueError("Resource type must be one of: human, asset, service.")

    @staticmethod
    def _require_reservation_status(status: str) -> None:
        if status not in RESERVATION_STATUS_VALUES:
            raise ValueError("Status must be one of: draft, active, cancelled.")

    @staticmethod
    def _require_conflict_severity(severity: str) -> None:
        if severity not in CONFLICT_SEVERITY_VALUES:
            raise ValueError("Severity must be one of: critical, high, medium, low.")

    @staticmethod
    def _require_valid_interval(starts_at_utc, ends_at_utc) -> None:
        if starts_at_utc >= ends_at_utc:
            raise ValueError("Reservation interval must have starts_at_utc < ends_at_utc.")

    @staticmethod
    def _overlaps(starts_at_utc, ends_at_utc, time_range: TimeRangeDTO) -> bool:
        return starts_at_utc < time_range.end_utc and ends_at_utc > time_range.start_utc
