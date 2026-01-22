# Decision: Phase 4 scope alignment with implemented adapters

Date: 2026-01-22
Status: Accepted
Owners: documentation governance

## Context
Phase 4 documentation conflicts with implemented adapters. The codebase already contains
an in-memory persistence adapter and a minimal FastAPI HTTP adapter for reservation
evaluation, while Phase 4 previously disallowed API implementation.

## Decision
Phase 4 explicitly allows:
- In-memory persistence adapter implementing defined persistence ports.
- Minimal HTTP adapter using FastAPI for reservation evaluation.

Phase 4 explicitly does not include:
- Authentication or authorization.
- Workflow orchestration.
- External integrations.
- Business rule expansion beyond existing specs.

## Consequences
- Roadmap and readiness audit must acknowledge the allowed adapters.
- Phase 4 non-goals must exclude security, orchestration, and integrations.
- Documentation must align Phase 4 status with evidence in code.

## Evidence
- FastAPI reservation evaluation route: planninghub/adapters/fastapi_app/routes.py
- HTTP DTO/mappers: planninghub/adapters/http/dtos.py, planninghub/adapters/http/mappers.py
- In-memory persistence adapter: planninghub/adapters/persistence/in_memory.py
- Persistence ports and handlers: planninghub/application/ports/persistence.py,
  planninghub/application/handlers/time_reservation.py,
  planninghub/application/handlers/conflict.py,
  planninghub/application/handlers/identity.py
