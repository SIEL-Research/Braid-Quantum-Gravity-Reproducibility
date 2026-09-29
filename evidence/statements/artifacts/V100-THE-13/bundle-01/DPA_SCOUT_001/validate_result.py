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

assert digest("SCOUT_PLAN.md") == freeze["scout_plan_sha256"]
assert digest("INPUT_MANIFEST.json") == freeze["input_manifest_sha256"]
assert digest("evaluate_scout.py") == freeze["evaluator_sha256"]
assert digest("RAW_OUTPUT.json") == result["raw_output_sha256"] == status["raw_output_sha256"]
assert digest("RESULT.json") == status["result_sha256"]
assert raw["scout_id"] == result["scout_id"] == status["scout_id"] == "DPA-SCOUT-BGCE457-001"
assert [row["mask"] for row in raw["sector_rows"]] == [0, 5, 8, 13, 16, 21, 24, 29]
assert all(row["defect_gram_rank"] == 4 for row in raw["sector_rows"])
assert min(row["defect_gram_minimum_eigenvalue"] for row in raw["sector_rows"]) > 13.0
assert all(value == "0" for row in raw["exact_fraction_Ward_witness_residuals"] for value in row)
assert raw["all_finite_registers_give_prior_summed_CPTP_instruments"] is True
assert raw["all_finite_n_theorem"] is True
assert raw["nonlinear_feedback"] is True
assert result["decision"] == "CLOSED_SCOPED"
assert result["all_noncompensating_gates_pass"] is True
assert all(result["gates"].values())

print(json.dumps({
    "status": "PASS",
    "scout_id": raw["scout_id"],
    "sectors": len(raw["sector_rows"]),
    "minimum_gram_eigenvalue": min(row["defect_gram_minimum_eigenvalue"] for row in raw["sector_rows"]),
    "raw_sha256": digest("RAW_OUTPUT.json"),
    "result_sha256": digest("RESULT.json"),
}, indent=2, sort_keys=True))
