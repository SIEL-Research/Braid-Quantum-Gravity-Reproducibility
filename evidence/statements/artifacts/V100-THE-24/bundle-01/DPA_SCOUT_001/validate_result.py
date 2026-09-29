#!/usr/bin/env python3
from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def digest(name: str) -> str:
    return sha256((HERE / name).read_bytes()).hexdigest()


raw = json.loads((HERE / "RAW_OUTPUT.json").read_text())
result = json.loads((HERE / "RESULT.json").read_text())
status = json.loads((HERE / "STATUS.json").read_text())
freeze1 = json.loads((HERE / "SCOUT_FREEZE.json").read_text())
freeze2 = json.loads((HERE / "SCOUT_FREEZE_R2.json").read_text())
freeze3 = json.loads((HERE / "SCOUT_FREEZE_R3.json").read_text())
fail1 = json.loads((HERE / "ATTEMPT_0001_FAILURE.json").read_text())
fail2 = json.loads((HERE / "ATTEMPT_0002_FAILURE.json").read_text())

assert digest("SCOUT_PLAN.md") == freeze1["scout_plan_sha256"]
assert digest("INPUT_MANIFEST.json") == freeze1["input_manifest_sha256"]
assert digest("evaluate_scout.py") == freeze1["evaluator_sha256"] == freeze2["frozen_scientific_evaluator_sha256"] == freeze3["frozen_scientific_evaluator_sha256"]
assert digest("evaluate_scout_r2.py") == freeze2["path_only_wrapper_sha256"]
assert digest("ATTEMPT_0001_FAILURE.json") == freeze2["attempt_0001_failure_sha256"]
assert digest("evaluate_scout_r3.py") == freeze3["attempt_0003_runner_sha256"]
assert digest("ATTEMPT_0002_FAILURE.json") == freeze3["attempt_0002_failure_sha256"]
assert fail1["incident_class"] == fail2["incident_class"] == "IMPLEMENTATION_PROVENANCE_FAILURE"
assert digest("RAW_OUTPUT.json") == result["raw_output_sha256"] == status["raw_output_sha256"]
assert digest("RESULT.json") == status["result_sha256"]
assert digest("REPORT_JA.md") == status["report_sha256"]
assert raw["scout_id"] == result["scout_id"] == status["scout_id"] == "DPA-SCOUT-BGCE458-001"
assert raw["attempt"] == status["successful_attempt"] == "0003"
rows = {row["name"]: row for row in raw["rows"]}
focal = rows["actual_pointed_braid_event"]
assert focal["yang_baxter_failures"] == 0
assert focal["C_order_three"] is True
assert focal["A_squared_plus_3P_basis_failures"] == 0
assert focal["P_real_rank"] == 72
assert focal["reconstructed_complex_dimension"] == 36
assert focal["R1_reverses_J"] is True
assert rows["identity_control"]["reconstructed_complex_dimension"] == 0
assert rows["ordinary_flip_control"]["P_real_rank"] == 80
assert rows["ordinary_flip_control"]["reconstructed_complex_dimension"] == 40
assert rows["deterministic_involutive_yang_baxter_broken_control"]["yang_baxter_failures"] == 18
assert raw["forbidden_quantum_inputs_used"] == []
assert result["decision"] == status["decision"] == "CLOSED_SCOPED"
assert result["all_noncompensating_gates_pass"] is True
assert all(result["gates"].values())
assert result["born_rule"].startswith("OPEN_")
assert result["controls"]["specificity"] == "NOT_ESTABLISHED"

print(json.dumps({
    "status": "PASS",
    "scout_id": raw["scout_id"],
    "attempts_retained": status["attempts_retained"],
    "actual_real_rank": focal["P_real_rank"],
    "actual_complex_dimension": focal["reconstructed_complex_dimension"],
    "identity_complex_dimension": rows["identity_control"]["reconstructed_complex_dimension"],
    "flip_complex_dimension": rows["ordinary_flip_control"]["reconstructed_complex_dimension"],
    "raw_sha256": digest("RAW_OUTPUT.json"),
    "result_sha256": digest("RESULT.json")
}, indent=2, sort_keys=True))
