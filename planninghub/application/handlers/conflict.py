"""Handlers for conflict ports."""

from __future__ import annotations

from planninghub.application.dtos.conflict import (
    DetectConflictsRequest,
    DetectConflictsResponse,
    ListConflictsRequest,
    ListConflictsResponse,
)
from planninghub.application.ports.persistence import ConflictPersistencePort


def _require_org_id(organization_id: str) -> None:
    if not organization_id:
        raise ValueError("organization_id must be non-empty")


def _require_optional_id(value: str | None, field: str) -> None:
    if value is not None and not value:
        raise ValueError(f"{field} must be non-empty when provided")


class DetectConflictsHandler:
    def __init__(self, persistence: ConflictPersistencePort) -> None:
        self._persistence = persistence

    def handle(self, request: DetectConflictsRequest) -> DetectConflictsResponse:
        _require_org_id(request.organization_id)
        conflicts = self._persistence.detect_conflicts(request)
        return DetectConflictsResponse(conflicts=conflicts)


class ListConflictsHandler:
    def __init__(self, persistence: ConflictPersistencePort) -> None:
        self._persistence = persistence

    def handle(self, request: ListConflictsRequest) -> ListConflictsResponse:
        _require_org_id(request.organization_id)
        _require_optional_id(request.reservation_id, "reservation_id")
        conflicts = self._persistence.list_conflicts(request)
        return ListConflictsResponse(conflicts=conflicts)
