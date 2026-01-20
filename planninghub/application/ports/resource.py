"""Inbound ports for resource operations."""

from __future__ import annotations

from typing import Protocol

from planninghub.application.dtos.resource import (
    CreateResourceRequest,
    CreateResourceResponse,
    GetResourceRequest,
    GetResourceResponse,
)


class CreateResourcePort(Protocol):
    def handle(self, request: CreateResourceRequest) -> CreateResourceResponse:
        ...


class GetResourcePort(Protocol):
    def handle(self, request: GetResourceRequest) -> GetResourceResponse:
        ...
