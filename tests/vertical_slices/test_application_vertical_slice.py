from datetime import datetime, timezone

import pytest

from planninghub.adapters.persistence.in_memory import InMemoryPersistenceAdapter
from planninghub.application.dtos.conflict import DetectConflictsRequest
from planninghub.application.dtos.identity import CreateOrganizationRequest
from planninghub.application.dtos.project import CreateProjectRequest
from planninghub.application.dtos.resource import CreateResourceRequest
from planninghub.application.dtos.time_reservation import CreateReservationRequest
from planninghub.application.handlers.conflict import DetectConflictsHandler
from planninghub.application.handlers.identity import CreateOrganizationHandler
from planninghub.application.handlers.project import CreateProjectHandler
from planninghub.application.handlers.resource import CreateResourceHandler
from planninghub.application.handlers.time_reservation import CreateReservationHandler


def _run_minimal_workflow(adapter: InMemoryPersistenceAdapter):
    create_org = CreateOrganizationHandler(adapter)
    create_project = CreateProjectHandler(adapter)
    create_resource = CreateResourceHandler(adapter)
    create_reservation = CreateReservationHandler(adapter)
    detect_conflicts = DetectConflictsHandler(adapter)

    organization = create_org.handle(
        CreateOrganizationRequest(name="Acme Planning")
    ).organization
    project = create_project.handle(
        CreateProjectRequest(
            organization_id=organization.id,
            name="Main Program",
        )
    ).project
    resource = create_resource.handle(
        CreateResourceRequest(
            organization_id=organization.id,
            type="human",
            name="Planner One",
        )
    ).resource
    reservation = create_reservation.handle(
        CreateReservationRequest(
            organization_id=organization.id,
            resource_id=resource.id,
            starts_at_utc=datetime(2024, 1, 1, 10, 0, 0, tzinfo=timezone.utc),
            ends_at_utc=datetime(2024, 1, 1, 11, 0, 0, tzinfo=timezone.utc),
            timezone="UTC",
            economic_value=None,
        )
    ).reservation
    conflicts = detect_conflicts.handle(
        DetectConflictsRequest(
            organization_id=organization.id,
            reservation_id=reservation.id,
        )
    )
    return organization, project, resource, reservation, conflicts.conflicts


def test_minimal_workflow_happy_path():
    adapter = InMemoryPersistenceAdapter()
    organization, project, resource, reservation, conflicts = _run_minimal_workflow(
        adapter
    )

    assert organization.id == "org-1"
    assert project.id == "project-1"
    assert project.organization_id == organization.id
    assert resource.id == "resource-1"
    assert resource.organization_id == organization.id
    assert reservation.organization_id == organization.id
    assert reservation.resource_id == resource.id
    assert conflicts == []


def test_minimal_workflow_invariant_violation():
    adapter = InMemoryPersistenceAdapter()
    handler = CreateReservationHandler(adapter)

    with pytest.raises(ValueError, match="organization_id"):
        handler.handle(
            CreateReservationRequest(
                organization_id="",
                resource_id="resource-1",
                starts_at_utc=datetime(2024, 1, 1, 10, 0, 0, tzinfo=timezone.utc),
                ends_at_utc=datetime(2024, 1, 1, 11, 0, 0, tzinfo=timezone.utc),
                timezone="UTC",
                economic_value=None,
            )
        )


def test_minimal_workflow_determinism():
    first = _run_minimal_workflow(InMemoryPersistenceAdapter())
    second = _run_minimal_workflow(InMemoryPersistenceAdapter())

    assert first == second
