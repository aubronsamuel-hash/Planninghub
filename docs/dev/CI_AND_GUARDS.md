# CI and guards

## CI pipeline (GitHub Actions)
File: .github/workflows/ci.yml

Steps:
1) Set up Python 3.11
2) Install deps: python -m pip install -e ".[dev]"
3) Lint: ruff check .
4) Sanity import: python -c "import fastapi; print(fastapi.__version__)"
5) Test: python -m pytest

## Local guards

### Import policy guard
- Command: python tools/guards/import_policy_guard.py
- Enforces: domain modules must not import planninghub.application or planninghub.infra.
- Scope: planninghub/domain/**/*.py

### Build sanity
- Command: python -m compileall .
- Purpose: catch syntax errors and import-time issues.

## Common CI failures and fixes
- Ruff failures: fix formatting or unused imports, then rerun ruff check .
- Pytest failures: update implementation or revert behavior to match specs.
- FastAPI import failure: ensure fastapi is installed via pip install -e ".[dev]".

## UNKNOWN / NOT IMPLEMENTED YET
- No documented docs linter or formatting guard found.
- No type checking guard configured.
