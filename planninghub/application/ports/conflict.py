"""Inbound ports for conflict operations."""

from __future__ import annotations

from typing import Protocol

from planninghub.application.dtos.conflict import (
    DetectConflictsRequest,
    DetectConflictsResponse,
    ListConflictsRequest,
    ListConflictsResponse,
)


class DetectConflictsPort(Protocol):
    def handle(self, request: DetectConflictsRequest) -> DetectConflictsResponse:
        ...


class ListConflictsPort(Protocol):
    def handle(self, request: ListConflictsRequest) -> ListConflictsResponse:
        ...
