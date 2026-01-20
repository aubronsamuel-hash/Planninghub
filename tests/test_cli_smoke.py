"""CLI smoke tests."""

from __future__ import annotations

from planninghub.infra.cli_smoke import main


def test_cli_smoke_memory(monkeypatch):
    monkeypatch.setenv("PLANNINGHUB_PERSISTENCE_BACKEND", "memory")
    monkeypatch.delenv("PLANNINGHUB_SQLITE_DB_PATH", raising=False)

    assert main([]) == 0


def test_cli_smoke_sqlite(monkeypatch, tmp_path):
    db_path = tmp_path / "planninghub.sqlite3"
    monkeypatch.setenv("PLANNINGHUB_PERSISTENCE_BACKEND", "sqlite")
    monkeypatch.setenv("PLANNINGHUB_SQLITE_DB_PATH", str(db_path))

    assert main([]) == 0
