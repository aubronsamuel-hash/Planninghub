"""Runtime configuration for Planninghub."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


@dataclass
class AppConfig:
    """Configuration for building the Planninghub application."""

    persistence_backend: Literal["memory", "sqlite"]
    sqlite_db_path: str | None = None


def default_config() -> AppConfig:
    """Return the default application configuration."""

    return AppConfig(persistence_backend="memory", sqlite_db_path=None)
