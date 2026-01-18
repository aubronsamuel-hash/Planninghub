"""DTOs for identity ports."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True, slots=True)
class UserDTO:
    id: str
    email: str
    display_name: str
    status: str


@dataclass(frozen=True, slots=True)
class OrganizationDTO:
    id: str
    name: str


@dataclass(frozen=True, slots=True)
class MembershipDTO:
    id: str
    user_id: str
    organization_id: str
    role: str


@dataclass(frozen=True, slots=True)
class CreateUserRequest:
    email: str
    display_name: str


@dataclass(frozen=True, slots=True)
class CreateUserResponse:
    user: UserDTO


@dataclass(frozen=True, slots=True)
class DeactivateUserRequest:
    user_id: str


@dataclass(frozen=True, slots=True)
class DeactivateUserResponse:
    user: UserDTO


@dataclass(frozen=True, slots=True)
class CreateOrganizationRequest:
    name: str


@dataclass(frozen=True, slots=True)
class CreateOrganizationResponse:
    organization: OrganizationDTO


@dataclass(frozen=True, slots=True)
class AddMembershipRequest:
    user_id: str
    organization_id: str
    role: str


@dataclass(frozen=True, slots=True)
class AddMembershipResponse:
    membership: MembershipDTO


@dataclass(frozen=True, slots=True)
class ListMembershipsRequest:
    user_id: Optional[str] = None
    organization_id: Optional[str] = None


@dataclass(frozen=True, slots=True)
class ListMembershipsResponse:
    memberships: list[MembershipDTO]
