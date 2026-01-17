"""Tests for the application demo wiring."""

from __future__ import annotations

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def _load_demo_module():
    demo_path = Path(__file__).resolve().parents[1] / "planninghub" / "app" / "demo.py"
    spec = spec_from_file_location("planninghub.app.demo", demo_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load demo module.")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_run_demo_detects_conflict():
    demo = _load_demo_module()

    result = demo.run_demo()

    assert result["conflict"] is True
    assert result["overlaps"] == ["res-1"]
    assert result["severity"] == "high"
