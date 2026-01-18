"""Inbound ports for identity operations."""

from __future__ import annotations

from typing import Protocol

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


class CreateUserPort(Protocol):
    def handle(self, request: CreateUserRequest) -> CreateUserResponse:
        ...


class DeactivateUserPort(Protocol):
    def handle(self, request: DeactivateUserRequest) -> DeactivateUserResponse:
        ...


class CreateOrganizationPort(Protocol):
    def handle(self, request: CreateOrganizationRequest) -> CreateOrganizationResponse:
        ...


class AddMembershipPort(Protocol):
    def handle(self, request: AddMembershipRequest) -> AddMembershipResponse:
        ...


class ListMembershipsPort(Protocol):
    def handle(self, request: ListMembershipsRequest) -> ListMembershipsResponse:
        ...
