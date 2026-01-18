"""Handlers for identity ports."""

from __future__ import annotations

from planninghub.application.dtos.identity import (
    AddMembershipRequest,
    AddMembershipResponse,
    CreateOrganizationRequest,
    CreateOrganizationResponse,
    CreateUserRequest,
    CreateUserResponse,
    DeactivateUserRequest,
    DeactivateUserResponse,
    ListMembershipsRequest,
    ListMembershipsResponse,
)
from planninghub.application.ports.persistence import IdentityPersistencePort


def _require_org_id(organization_id: str) -> None:
    if not organization_id:
        raise ValueError("organization_id must be non-empty")


def _require_optional_id(value: str | None, field: str) -> None:
    if value is not None and not value:
        raise ValueError(f"{field} must be non-empty when provided")


class CreateUserHandler:
    def __init__(self, persistence: IdentityPersistencePort) -> None:
        self._persistence = persistence

    def handle(self, request: CreateUserRequest) -> CreateUserResponse:
        user = self._persistence.create_user(request)
        return CreateUserResponse(user=user)


class DeactivateUserHandler:
    def __init__(self, persistence: IdentityPersistencePort) -> None:
        self._persistence = persistence

    def handle(self, request: DeactivateUserRequest) -> DeactivateUserResponse:
        user = self._persistence.deactivate_user(request)
        return DeactivateUserResponse(user=user)


class CreateOrganizationHandler:
    def __init__(self, persistence: IdentityPersistencePort) -> None:
        self._persistence = persistence

    def handle(self, request: CreateOrganizationRequest) -> CreateOrganizationResponse:
        organization = self._persistence.create_organization(request)
        return CreateOrganizationResponse(organization=organization)


class AddMembershipHandler:
    def __init__(self, persistence: IdentityPersistencePort) -> None:
        self._persistence = persistence

    def handle(self, request: AddMembershipRequest) -> AddMembershipResponse:
        _require_org_id(request.organization_id)
        existing = self._persistence.list_memberships(
            ListMembershipsRequest(
                user_id=request.user_id,
                organization_id=request.organization_id,
            )
        )
        if existing:
            raise ValueError("duplicate membership for user and organization")
        membership = self._persistence.add_membership(request)
        return AddMembershipResponse(membership=membership)


class ListMembershipsHandler:
    def __init__(self, persistence: IdentityPersistencePort) -> None:
        self._persistence = persistence

    def handle(self, request: ListMembershipsRequest) -> ListMembershipsResponse:
        _require_optional_id(request.user_id, "user_id")
        _require_optional_id(request.organization_id, "organization_id")
        memberships = self._persistence.list_memberships(request)
        return ListMembershipsResponse(memberships=memberships)
