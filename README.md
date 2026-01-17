# Planninghub

## Baseline commands
Stack: Python (pyproject.toml + ruff + pytest).

- Install (local or CI): python -m pip install -e ".[dev]"
- Build: python -m compileall .
- Test: python -m pytest
- Lint: ruff check .
- Guard: python tools/guards/import_policy_guard.py

## Docs
- Package boundaries and public API: docs/specs/package_boundaries_and_public_api.md
