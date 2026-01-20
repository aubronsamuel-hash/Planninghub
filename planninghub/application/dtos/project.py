"""DTOs for project ports."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProjectDTO:
    id: str
    organization_id: str
    name: str


@dataclass(frozen=True, slots=True)
class CreateProjectRequest:
    organization_id: str
    name: str


@dataclass(frozen=True, slots=True)
class CreateProjectResponse:
    project: ProjectDTO


@dataclass(frozen=True, slots=True)
class GetProjectRequest:
    project_id: str


@dataclass(frozen=True, slots=True)
class GetProjectResponse:
    project: ProjectDTO
