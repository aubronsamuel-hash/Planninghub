"""Runtime configuration for Planninghub."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Literal


@dataclass
class AppConfig:
    """Configuration for building the Planninghub application."""

    persistence_backend: Literal["memory", "sqlite"]
    sqlite_db_path: str | None = None


def default_config() -> AppConfig:
    """Return the default application configuration."""

    persistence_backend = os.getenv("PLANNINGHUB_PERSISTENCE_BACKEND", "memory")
    sqlite_db_path = os.getenv("PLANNINGHUB_SQLITE_DB_PATH") or None

    if persistence_backend not in ("memory", "sqlite"):
        raise ValueError(
            "PLANNINGHUB_PERSISTENCE_BACKEND must be 'memory' or 'sqlite'"
        )

    if persistence_backend == "sqlite" and not sqlite_db_path:
        raise ValueError("PLANNINGHUB_SQLITE_DB_PATH is required for sqlite backend")

    return AppConfig(
        persistence_backend=persistence_backend, sqlite_db_path=sqlite_db_path
    )
