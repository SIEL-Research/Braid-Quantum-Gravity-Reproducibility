#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent


def digest(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


raw = json.loads((HERE / "RAW_OUTPUT_R2.json").read_text())
result = json.loads((HERE / "RESULT_R2.json").read_text())
freeze = json.loads((HERE / "SCOUT_FREEZE_R2.json").read_text())
assert digest("evaluate_scout_r2.py") == freeze["evaluate_scout_r2_sha256"]
assert digest("SCOUT_PLAN_R2.md") == freeze["scout_plan_r2_sha256"]
assert digest("RAW_OUTPUT.json") == freeze["retained_attempt_2_raw_sha256"]
assert digest("RESULT.json") == freeze["retained_attempt_2_result_sha256"]
assert [row["mask"] for row in raw["sector_rows"]] == [0, 5, 8, 13, 16, 21, 24, 29]
assert len(raw["sector_rows"]) == 8
assert sum(len(row["directions"]) for row in raw["sector_rows"]) == 24
for row in raw["sector_rows"]:
    assert row["relation_checks"] == {"braid_relation": True, "involution": True}
    assert row["seed_rank"]["rank"] == 3
    assert row["matrix_commutator_jacobi_zero"] is True
    for direction in row["directions"]:
        witness = direction["product_witness"]
        assert witness["found"] is True
        assert Fraction(witness["exact_gap"]) == Fraction(2, 3)
        comparator = direction["signed_sector_vs_unsigned_reference"]
        assert comparator["found"] is True
        if row["mask"] != 0:
            assert comparator["signed_action"] != comparator["unsigned_action"]
assert result["decision"] == "CLOSED_SCOPED"
for key in (
    "all_eight_relation_checks",
    "all_eight_rank_three",
    "all_24_constructive_positive_gap_witnesses",
    "all_21_signed_sector_action_witnesses_vs_unsigned_reference",
    "all_eight_exact_jacobi_checks",
    "generated_lie_closure",
):
    assert result[key] is True
print(json.dumps({
    "status": "PASS",
    "raw_sha256": digest("RAW_OUTPUT_R2.json"),
    "result_sha256": digest("RESULT_R2.json"),
    "sectors": 8,
    "directions": 24,
    "signed_comparisons": 21,
    "exact_gap": "2/3"
}, indent=2, sort_keys=True))
