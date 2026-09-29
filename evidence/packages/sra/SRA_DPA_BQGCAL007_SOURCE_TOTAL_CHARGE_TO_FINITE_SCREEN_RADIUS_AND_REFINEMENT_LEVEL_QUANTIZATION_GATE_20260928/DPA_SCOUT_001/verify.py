#!/usr/bin/env python3
from hashlib import sha256
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
cert = json.loads((HERE / "CERTIFICATE.json").read_text())
raw = json.loads((HERE / "RAW_OUTPUT.json").read_text())
result = json.loads((HERE / "RESULT.json").read_text())
status = json.loads((HERE / "STATUS.json").read_text())

assert cert["evaluator_sha256"] == sha256((HERE / "evaluate_scout.py").read_bytes()).hexdigest()
assert cert["raw_output_sha256"] == sha256((HERE / "RAW_OUTPUT.json").read_bytes()).hexdigest()
assert cert["result_sha256"] == sha256((HERE / "RESULT.json").read_bytes()).hexdigest()
assert all(cert["tests"].values())
assert raw["decision"] == result["decision"] == status["decision"]
assert raw["unique_refinement_level_from_existing_total_charge_pass"] is False
assert raw["refinement_invariant_composite_screen_pass"] is True
assert raw["positive_source_screen_number_operator_pass"] is False
assert raw["composite_screen"]["total_area"] == "A_total(K,m)=N_m*A_m=K*A_0"
print("PASS_VERIFY_BQGCAL_007_X1")
