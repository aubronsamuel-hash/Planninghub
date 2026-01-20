# Persistence smoke runbook

## Prerequisites
- python 3.11
- venv with dependencies
- install dev dependencies:
  - pip install -e ".[dev]"

## Run memory backend
- set env:
  - Bash:
    - export PLANNINGHUB_PERSISTENCE_BACKEND=memory
    - unset PLANNINGHUB_SQLITE_DB_PATH
  - PowerShell:
    - setx PLANNINGHUB_PERSISTENCE_BACKEND "memory"
    - $env:PLANNINGHUB_PERSISTENCE_BACKEND = "memory"
    - Remove-Item Env:PLANNINGHUB_SQLITE_DB_PATH
- run:
  - python -m planninghub.infra.cli_smoke

Expected output example:
- SMOKE OK: backend=memory org=org-1 res=res-1 conflicts=1

## Run sqlite backend
- set env:
  - Bash:
    - export PLANNINGHUB_PERSISTENCE_BACKEND=sqlite
    - export PLANNINGHUB_SQLITE_DB_PATH=./.local/planninghub.sqlite3
  - PowerShell:
    - setx PLANNINGHUB_PERSISTENCE_BACKEND "sqlite"
    - setx PLANNINGHUB_SQLITE_DB_PATH ".\\.local\\planninghub.sqlite3"
    - $env:PLANNINGHUB_PERSISTENCE_BACKEND = "sqlite"
    - $env:PLANNINGHUB_SQLITE_DB_PATH = ".\\.local\\planninghub.sqlite3"
- run:
  - python -m planninghub.infra.cli_smoke

Expected output example:
- SMOKE OK: backend=sqlite org=org-1 res=res-1 conflicts=1
