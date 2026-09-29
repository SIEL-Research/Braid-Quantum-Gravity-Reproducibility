#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from access_guard import AccessDenied, guarded_read
from exact_witness_constructor import run
from validate_retention import validate


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


frozen = json.loads((HERE / "WITNESS_RESULT.json").read_text())
fresh = run()
assert fresh == frozen
assert fresh["all_expected_separations"] is True
assert all(fresh["decision"].values())

schema = json.loads((HERE / "RAW_ROW_SCHEMA.json").read_text())
retention_frozen = json.loads((HERE / "RETENTION_VALIDATION_RESULT.json").read_text())
assert validate(fresh, schema) == retention_frozen

allowlist = json.loads((HERE / "INPUT_ALLOWLIST.json").read_text())
allowed = {row["path"]: row["sha256"] for row in allowlist["allowed"]}
denied = allowlist["deny_globs"]
for relative, expected in allowed.items():
    payload = guarded_read(REPO, relative, allowed, denied)
    assert hashlib.sha256(payload).hexdigest() == expected

for relative in [
    "records/BGCE443_SOURCE_REFINEMENT_LIMIT_UNBOUNDED_DERIVATION_THREE_PLANE_GATE_20260925/RESULT.json",
    "records/BGCE443_SOURCE_REFINEMENT_LIMIT_UNBOUNDED_DERIVATION_THREE_PLANE_GATE_20260925/REVISION_2/STATUS.json",
    "records/BGCE443_SOURCE_REFINEMENT_LIMIT_UNBOUNDED_DERIVATION_THREE_PLANE_GATE_20260925/REVISION_4/E0_RESULT.json",
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

suite = unittest.defaultTestLoader.discover(str(HERE), pattern="test_access_guard.py")
test_result = unittest.TextTestRunner(verbosity=0).run(suite)
assert test_result.wasSuccessful()

for name in [
    "RAW_ROW_SCHEMA.json",
    "RETENTION_VALIDATION_RESULT.json",
    "ACCESS_GUARD_RESULT.json",
    "WITNESS_BASELINE_GATE.json",
    "STATUS.json",
]:
    json.loads((HERE / name).read_text())

print(json.dumps({
    "status": "PASS",
    "witness_result_sha256": digest(HERE / "WITNESS_RESULT.json"),
    "exact_constructor_sha256": digest(HERE / "exact_witness_constructor.py"),
    "retention_validator_sha256": digest(HERE / "validate_retention.py"),
    "access_guard_sha256": digest(HERE / "access_guard.py"),
    "all_expected_separations": fresh["all_expected_separations"],
    "retention_validation": retention_frozen["status"],
    "access_guard_tests_run": test_result.testsRun,
    "allowed_source_hashes_verified": len(allowed),
    "focal_source_used": fresh["focal_source_used"],
}, sort_keys=True, indent=2))
