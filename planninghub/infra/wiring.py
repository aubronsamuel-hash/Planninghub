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


class PersistencePort(
    IdentityPersistencePort,
    ReservationPersistencePort,
    ConflictPersistencePort,
    Protocol,
):
    """Protocol for persistence adapters used by the application."""


@dataclass
class Application:
    """Container for application dependencies."""

    persistence: PersistencePort


def build_persistence_adapter(config: AppConfig) -> PersistencePort:
    """Build the configured persistence adapter."""

    if config.persistence_backend == "memory":
        return InMemoryPersistenceAdapter()
    if config.persistence_backend == "sqlite":
        if not config.sqlite_db_path:
            raise ValueError("sqlite_db_path is required for sqlite backend")
        return SQLitePersistenceAdapter(db_path=config.sqlite_db_path)

    raise ValueError(f"Unsupported persistence backend: {config.persistence_backend}")


def build_application(config: AppConfig) -> Application:
    """Build the application with the configured persistence adapter."""

    return Application(persistence=build_persistence_adapter(config))
