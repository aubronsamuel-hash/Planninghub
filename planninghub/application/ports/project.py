"""Inbound ports for project operations."""

from __future__ import annotations

from typing import Protocol

from planninghub.application.dtos.project import (
    CreateProjectRequest,
    CreateProjectResponse,
    GetProjectRequest,
    GetProjectResponse,
)


class CreateProjectPort(Protocol):
    def handle(self, request: CreateProjectRequest) -> CreateProjectResponse:
        ...


class GetProjectPort(Protocol):
    def handle(self, request: GetProjectRequest) -> GetProjectResponse:
        ...
