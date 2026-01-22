# Setup and run

## Required runtimes
- Python 3.11 (see pyproject.toml requires-python)

## Virtual environment
- Create a venv:
  - python -m venv .venv
- Activate it:
  - source .venv/bin/activate

## Install dependencies
- Editable install with dev extras:
  - python -m pip install --upgrade pip
  - python -m pip install -e ".[dev]"

## Run the application

### CLI smoke path (supported)
- Command:
  - planninghub-smoke
- Expected output:
  - A single line starting with "SMOKE OK:" and a summary of backend, org, res, conflicts.

### HTTP server
- UNKNOWN / NOT IMPLEMENTED YET
- A FastAPI app exists under planninghub/adapters/fastapi_app/, but no supported server command is documented in this repo.
- If you need an HTTP server, add a spec and decision entry first.

## Known limitations
- Full application runtime and production wiring are not defined.
- Some roadmap phases are spec-only and not implemented.
