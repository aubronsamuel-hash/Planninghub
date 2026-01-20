"""DTOs for resource ports."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ResourceDTO:
    id: str
    organization_id: str
    type: str
    name: str


@dataclass(frozen=True, slots=True)
class CreateResourceRequest:
    organization_id: str
    type: str
    name: str


@dataclass(frozen=True, slots=True)
class CreateResourceResponse:
    resource: ResourceDTO


@dataclass(frozen=True, slots=True)
class GetResourceRequest:
    resource_id: str


@dataclass(frozen=True, slots=True)
class GetResourceResponse:
    resource: ResourceDTO
