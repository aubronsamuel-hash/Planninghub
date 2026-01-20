"""Handlers for resource ports."""

from __future__ import annotations

from planninghub.application.dtos.resource import (
    CreateResourceRequest,
    CreateResourceResponse,
    GetResourceRequest,
    GetResourceResponse,
)
from planninghub.application.ports.persistence import ResourcePersistencePort


class CreateResourceHandler:
    def __init__(self, persistence: ResourcePersistencePort) -> None:
        self._persistence = persistence

    def handle(self, request: CreateResourceRequest) -> CreateResourceResponse:
        resource = self._persistence.create_resource(request)
        return CreateResourceResponse(resource=resource)


class GetResourceHandler:
    def __init__(self, persistence: ResourcePersistencePort) -> None:
        self._persistence = persistence

    def handle(self, request: GetResourceRequest) -> GetResourceResponse:
        resource = self._persistence.get_resource(request)
        return GetResourceResponse(resource=resource)
