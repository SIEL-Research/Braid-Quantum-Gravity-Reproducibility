#!/usr/bin/env python3
"""Independent result-shape verifier for BQGSTRAT-012."""

from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
raw = json.loads((HERE / "RAW_OUTPUT.json").read_text())
result = json.loads((HERE / "RESULT.json").read_text())

assert raw["type_gate"]["same_operator"] is False
assert raw["type_gate"]["commuting_factors"] is True
assert raw["exact_internal_hodge"]["J_squared_equals_minus_identity"] is True
assert raw["completion_theorem"]["equal_dagger_completion"] == "J P_plus + J P_minus = J"
assert raw["completion_theorem"]["source_selects_relative_holst_phase"] is False
assert raw["rank_consequence"]["passed"] is False
assert raw["rank_consequence"]["equal_weight_profile"] == {"60": 1, "64": 12, "65": 12, "66": 600}
assert result["status"].startswith("NO_GO_SOURCE_DAGGER_CHIRAL_EQUAL_WEIGHT_COMPLETION")
assert result["next_gate"] == "BQGSTRAT-013_SOURCE_PERFECT_BFV_SCHUR_COMPLEMENT_GATE"
print("BQGSTRAT-012 VERIFY PASS")

