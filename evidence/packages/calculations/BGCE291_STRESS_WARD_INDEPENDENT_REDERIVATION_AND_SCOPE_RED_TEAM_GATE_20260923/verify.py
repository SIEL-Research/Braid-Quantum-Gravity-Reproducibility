#!/usr/bin/env python3
"""Independent artifact assertions for BGCE291."""

from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
raw = json.loads((HERE / "RAW_OUTPUT.json").read_text())
result = json.loads((HERE / "RESULT.json").read_text())

assert raw["candidate_id"] == "BGCE291"
assert raw["baseline_gate"].startswith("PASS_")
gates = raw["gate_results"]
assert gates["G1_independent_a_source_typing"].startswith("PASS_")
assert gates["G2_algebraic_Sym2_Hadamard_solder"].startswith("PASS_")
assert gates["G2_physical_solder_uniqueness"].startswith("FAIL_")
assert gates["G3_finite_nonlinear_active_Markov_transport"].startswith("FAIL_")
assert gates["G4_same_source_derived_off_shell_action"].startswith("FAIL_")
assert raw["exact_checks"]["Sym2_Hadamard_rank"] == 10
assert raw["exact_checks"]["S4_Sym2_commutant_dimension"] == 9
assert raw["reversal"]["BGCE290_FULL_PASS"] == "NOT_SUSTAINED"
assert result["physical_solder_uniquely_selected"] is False
assert result["finite_nonlinear_active_Markov_transport"] == "OPEN"
assert result["BGCE290_Hilbert_stress_promotion"] == "REVERSED_TO_CONDITIONAL"
assert result["unconditional_Einstein_dynamics"] is False
print("PASS_BGCE291_VERIFICATION")
