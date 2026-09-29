#!/usr/bin/env python3
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
raw=json.loads((HERE/"RAW_OUTPUT.json").read_text())
result=json.loads((HERE/"RESULT.json").read_text())
inv=raw["independent_inverse_audit"]
scope=raw["action_scope_audit"]
final=raw["final_decision"]
assert inv["exact_inverse_checks"] == 11
assert inv["clock_sign_flip_checks"] == 11
assert inv["local_regular_full_rank"] == "PASS"
assert scope["independent_tau_P0_J_clock_token_present"] is False
assert scope["metric_volume_density_source_natural"] == "PASS"
assert scope["finite_C2_variation_limit"] == "PASS"
assert final["stress_Ward"] == "FINAL_SCOPED_PASS"
assert final["Hilbert_stress_source_derived"] is True
assert final["on_shell_Ward_source_derived"] is True
assert result["Einstein_backreaction"] is False
print("PASS_BGCE299_FINAL_SCOPED_STRESS_WARD_VERIFICATION")
