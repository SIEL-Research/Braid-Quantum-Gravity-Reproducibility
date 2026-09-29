#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from access_guard import AccessDenied, guarded_read
from exact_witness_constructor import run


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


frozen = json.loads((HERE / "WITNESS_RESULT.json").read_text())
fresh = run()
assert fresh == frozen
assert fresh["all_expected_separations"] is True
assert all(fresh["decision"].values())

allowlist = json.loads((HERE / "INPUT_ALLOWLIST.json").read_text())
allowed = {row["path"]: row["sha256"] for row in allowlist["allowed"]}
denied = allowlist["deny_globs"]
for relative, expected in allowed.items():
    payload = guarded_read(REPO, relative, allowed, denied)
    assert hashlib.sha256(payload).hexdigest() == expected

for relative in [
    "records/BGCE443_SOURCE_REFINEMENT_LIMIT_UNBOUNDED_DERIVATION_THREE_PLANE_GATE_20260925/RESULT.json",
    "records/BGCE443_SOURCE_REFINEMENT_LIMIT_UNBOUNDED_DERIVATION_THREE_PLANE_GATE_20260925/REVISION_2/STATUS.json",
    "/etc/passwd",
    "../RESULT.json",
    "AGENTS.md",
]:
    try:
        guarded_read(REPO, relative, allowed, denied)
    except AccessDenied:
        pass
    else:
        raise AssertionError(f"guard unexpectedly allowed {relative}")

for name in ["RETENTION_SCHEMA.json", "ACCESS_GUARD_RESULT.json", "WITNESS_BASELINE_GATE.json", "STATUS.json"]:
    json.loads((HERE / name).read_text())

print(json.dumps({
    "status": "PASS",
    "witness_result_sha256": digest(HERE / "WITNESS_RESULT.json"),
    "exact_constructor_sha256": digest(HERE / "exact_witness_constructor.py"),
    "access_guard_sha256": digest(HERE / "access_guard.py"),
    "all_expected_separations": fresh["all_expected_separations"],
    "allowed_source_hashes_verified": len(allowed),
    "focal_source_used": fresh["focal_source_used"],
}, sort_keys=True, indent=2))
