#!/usr/bin/env python3
import json
from pathlib import Path

p = json.loads(Path(__file__).with_name("RESULT.json").read_text())
assert p["candidate_id"] == "BGCE456"
assert p["status"].startswith("SCOPED_PASS_")
g = p["gate_decision"]
assert g["actual_metric_nonnegative_conductance"] == "PASS_STRICTLY_POSITIVE"
assert g["exact_BGCE452_isotropic_limit"] == "PASS"
assert g["all_depth_refinement_intertwining"] == "PASS"
assert g["same_operator_UCP_heat"] == "PASS"
assert g["same_operator_positive_selfadjoint_wave"] == "PASS"
assert g["anisotropic_spectral_dimension_three"].startswith("PASS_")
assert g["conductance_uniqueness_from_source_axioms"] == "OPEN"
assert g["smooth_spacetime_principal_symbol_equal_to_A"] == "OPEN"
assert g["general_physical_UV_completion"] == "OPEN"
assert len(p["all_eight_sector_inheritance"]) == 8
assert not any([
    g["MMR_CGR_used"],
    g["target_Einstein_equation_used"],
    g["Einstein_Hilbert_or_Fierz_Pauli_action_used"],
    g["manual_three_fifths_used"],
    g["fitted_coefficient_used"],
])
print("BGCE456_VERIFY_PASS")
