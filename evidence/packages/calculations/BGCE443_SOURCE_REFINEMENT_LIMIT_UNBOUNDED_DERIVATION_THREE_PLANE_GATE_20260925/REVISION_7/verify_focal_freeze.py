#!/usr/bin/env python3
from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path

from access_guard import AccessDenied, guarded_read


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


freeze = json.loads((HERE / "FOCAL_FREEZE.json").read_text())
assert digest(HERE / "evaluate.py") == freeze["evaluate_sha256"]
assert digest(HERE / "access_guard.py") == freeze["access_guard_sha256"]
assert digest(HERE / "INPUT_ALLOWLIST.json") == freeze["input_allowlist_sha256"]
ast.parse((HERE / "evaluate.py").read_text())
assert not (HERE / "RESULT.json").exists()
assert not (HERE / "RAW_OUTPUT.json").exists()

packet = json.loads((HERE / "INPUT_ALLOWLIST.json").read_text())
allowed = {row["path"]: row["sha256"] for row in packet["allowed"]}
denied = packet["deny_globs"]
for relative, expected in allowed.items():
    payload = guarded_read(ROOT, relative, allowed, denied)
    assert hashlib.sha256(payload).hexdigest() == expected
for relative in [
    "records/BGCE443_SOURCE_REFINEMENT_LIMIT_UNBOUNDED_DERIVATION_THREE_PLANE_GATE_20260925/REVISION_7/RESULT.json",
    "records/BGCE443_SOURCE_REFINEMENT_LIMIT_UNBOUNDED_DERIVATION_THREE_PLANE_GATE_20260925/REVISION_7/RAW_OUTPUT.json",
    "../RESULT.json",
    "/etc/passwd",
    "AGENTS.md",
]:
    try:
        guarded_read(ROOT, relative, allowed, denied)
    except AccessDenied:
        pass
    else:
        raise AssertionError(relative)

print(json.dumps({"status": "PASS", "allowed_inputs_verified": len(allowed), "focal_result_exists": False, "focal_raw_output_exists": False, "evaluate_sha256": freeze["evaluate_sha256"]}, sort_keys=True, indent=2))
