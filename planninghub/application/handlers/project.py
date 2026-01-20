"""Handlers for project ports."""

from __future__ import annotations

from planninghub.application.dtos.project import (
    CreateProjectRequest,
    CreateProjectResponse,
    GetProjectRequest,
    GetProjectResponse,
)
from planninghub.application.ports.persistence import ProjectPersistencePort


class CreateProjectHandler:
    def __init__(self, persistence: ProjectPersistencePort) -> None:
        self._persistence = persistence

    def handle(self, request: CreateProjectRequest) -> CreateProjectResponse:
        project = self._persistence.create_project(request)
        return CreateProjectResponse(project=project)


class GetProjectHandler:
    def __init__(self, persistence: ProjectPersistencePort) -> None:
        self._persistence = persistence

    def handle(self, request: GetProjectRequest) -> GetProjectResponse:
        project = self._persistence.get_project(request)
        return GetProjectResponse(project=project)
