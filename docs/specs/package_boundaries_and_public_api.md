# Package Boundaries and Public API

## 1) Purpose
Define stable public import surfaces and layering rules.

## 2) Package boundaries
- domain: entities, value_objects, repositories (ports), services, use_cases
- application: commands/handlers that compose domain
- infra: in-memory implementations (testing/demo only)
- docs: non-code governance

## 3) Dependency rules (must)
- domain MUST NOT import application or infra
- application MAY import domain and infra (for wiring only)
- infra MAY import domain (implements ports)
- tests MAY import all layers

## 4) Public API surface (current)
Stable, intended public imports:
- planninghub.domain.entities
- planninghub.domain.value_objects
- planninghub.domain.repositories
- planninghub.domain.services (only exports in __init__)
- planninghub.domain.use_cases (only exports in __init__)
- planninghub.application (exports in __init__)

All other modules are internal unless explicitly exported.

## 5) Minimal usage example (deterministic, no IO)
```python
from datetime import datetime, timedelta

from planninghub.application import (
    EvaluateIncomingReservationCommand,
    EvaluateIncomingReservationHandler,
)
from planninghub.domain.entities import Reservation
from planninghub.domain.services import NoopResolutionStrategy
from planninghub.domain.value_objects import ReservationStatus
from planninghub.infra.repositories_in_memory import InMemoryReservationRepository

repo = InMemoryReservationRepository()
handler = EvaluateIncomingReservationHandler(
    reservation_repo=repo,
    strategies=[NoopResolutionStrategy()],
)

reservation = Reservation(
    id="res_1",
    organization_id="org_1",
    resource_id="resource_1",
    starts_at_utc=datetime(2030, 1, 1, 9, 0, 0),
    ends_at_utc=datetime(2030, 1, 1, 10, 0, 0),
    timezone="UTC",
    economic_value=None,
    status=ReservationStatus.ACTIVE,
)

cmd = EvaluateIncomingReservationCommand(
    organization_id="org_1",
    reservation=reservation,
)
response = handler.handle(cmd)
```

## 6) Non-goals
- No FastAPI, no persistence, no workflows, no UI
