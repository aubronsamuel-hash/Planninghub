"""Application wiring helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from planninghub.adapters.persistence.in_memory import InMemoryPersistenceAdapter
from planninghub.adapters.persistence.sqlite import SQLitePersistenceAdapter
from planninghub.application.ports.persistence import (
    ConflictPersistencePort,
    IdentityPersistencePort,
    ReservationPersistencePort,
)
from planninghub.infra.config import AppConfig


class PersistencePorts(
    IdentityPersistencePort,
    ReservationPersistencePort,
    ConflictPersistencePort,
    Protocol,
):
    """Protocol for persistence adapters used by the application."""


@dataclass
class Application:
    """Container for application dependencies."""

    persistence: PersistencePorts


def build_application(config: AppConfig) -> Application:
    """Build the application with the configured persistence adapter."""

    if config.persistence_backend == "memory":
        adapter = InMemoryPersistenceAdapter()
    elif config.persistence_backend == "sqlite":
        adapter = SQLitePersistenceAdapter(db_path=config.sqlite_db_path or ":memory:")
    else:
        raise ValueError(
            f"Unsupported persistence backend: {config.persistence_backend}"
        )

    return Application(persistence=adapter)
