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
freeze = json.loads((HERE / "SCOUT_FREEZE.json").read_text())

for name, expected in freeze["artifacts"].items():
    if name == "ITERATION_LEDGER.md":
        continue
    assert digest(name) == expected
assert freeze["outcome_accessed"] is False
iteration_text = (HERE / "ITERATION_LEDGER.md").read_text()
assert "FROZEN_NOT_EXECUTED" in iteration_text
assert "PASS_SCOPED" in iteration_text
assert digest("RAW_OUTPUT.json") == status["raw_output_sha256"]
assert digest("RESULT.json") == status["result_sha256"]
assert digest("REPORT.md") == status["report_sha256"]
assert raw["scout_id"] == result["scout_id"] == status["scout_id"] == "PUBLIC-RUN-BGCE459-001"
assert raw["attempt"] == status["successful_attempt"] == "0001"
assert raw["forbidden_inputs_used"] == []
assert raw["complex_carrier"]["complex_dimension"] == 36
assert raw["exact_two_orbit_witness"]["closure_numerator"] == 2
assert raw["exact_two_orbit_witness"]["closure_denominator"] == 10
assert raw["exact_two_orbit_witness"]["probability"] == "1/5"
assert raw["power_law_controls"]["r1"]["probability"] == "1/3"
assert raw["power_law_controls"]["r2"]["probability"] == "1/5"
assert raw["power_law_controls"]["r4"]["probability"] == "1/17"
assert raw["power_law_controls"]["r1"]["parallelogram"]["passes"] is False
assert raw["power_law_controls"]["r2"]["parallelogram"]["passes"] is True
assert raw["power_law_controls"]["r4"]["parallelogram"]["passes"] is False
assert result["decision"] == status["decision"] == "CLOSED_SCOPED"
assert result["all_noncompensating_gates_pass"] is True
assert all(result["gates"].values())

print(json.dumps({
    "status": "PASS",
    "scout_id": raw["scout_id"],
    "complex_dimension": raw["complex_carrier"]["complex_dimension"],
    "born_witness": raw["exact_two_orbit_witness"]["probability"],
    "raw_sha256": digest("RAW_OUTPUT.json"),
    "result_sha256": digest("RESULT.json")
}, indent=2, sort_keys=True))
