#!/usr/bin/env python3
from pathlib import Path
import json
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]

subprocess.run(["python3", "evaluate.py"], cwd=HERE, check=True)
raw = json.loads((HERE / "RAW_OUTPUT.json").read_text())
result = json.loads((HERE / "RESULT.json").read_text())

assert raw["target_gate"]["passed"] is False
assert raw["exact_free_associative_second_jet"]["log_reverse_equals_minus_log_forward"] is True
assert raw["exact_free_associative_second_jet"]["legal_reverse_action_factor"] == 1
assert raw["completion_family"]["inherited_rank_profiles"]["legal_equal_weight_orientation_pair"] == {"60": 1, "64": 12, "65": 12, "66": 600}
assert result["rank_consequence"]["passed"] is False
assert result["incident_class"] == "SCIENTIFIC_OUTCOME"
assert result["next_gate"] == "BQGSTRAT-012_SOURCE_DAGGER_CHIRAL_DOUBLE_COVER_GATE"
print("BQGSTRAT-011 verification PASS")
