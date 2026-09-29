#!/usr/bin/env python3
"""Attempt-0002 path-only wrapper for the frozen BGCE458 evaluator."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
FROZEN = HERE / "evaluate_scout.py"
SPEC = importlib.util.spec_from_file_location("bgce458_frozen_attempt_0001", FROZEN)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

# Path-only correction.  All scientific code, endpoints, controls, thresholds,
# source rows, and claim boundaries remain those of the frozen evaluator.
MODULE.REPO = HERE.parents[2]
MODULE.SOURCE = MODULE.REPO / "records/BGCE139_SOURCE_SPECTRAL_CYLINDER_OPERATIONAL_EVENT_IDENTIFICATION_GATE_20260919/RAW_OUTPUT.json"

print(json.dumps(MODULE.run(), indent=2, sort_keys=True))
