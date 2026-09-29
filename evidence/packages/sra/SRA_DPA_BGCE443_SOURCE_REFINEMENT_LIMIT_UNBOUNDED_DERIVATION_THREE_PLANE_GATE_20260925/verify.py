#!/usr/bin/env python3
import json
from pathlib import Path

p = json.loads(Path(__file__).with_name("RESULT.json").read_text())
assert p["candidate_id"] == "BGCE443"
assert p["status"].startswith("SCOPED_PASS_")
assert p["independence_certificate"]["rank"] == 3
g = p["gate_decision"]
assert g["source_refinement_intertwining"] == "PASS_EXACT"
assert g["three_independent_spatial_derivations"] == "PASS_ALL_EIGHT"
assert g["closable_unbounded_limit"] == "PASS"
assert g["spatial_derivation_common_core_closure"] == "PASS_ABELIAN_NO_ANOMALY"
assert g["typed_cotangent_moment_maps"] == "OPEN"
assert g["clock_spatial_mixed_brackets"] == "OPEN"
assert g["full_finite_anomaly_free_constraint_algebra"] == "OPEN"
assert len(p["all_eight_sector_inheritance"]) == 8
assert not any([
    g["MMR_CGR_used"],
    g["target_Einstein_equation_used"],
    g["Einstein_Hilbert_or_Fierz_Pauli_action_used"],
    g["manual_three_fifths_used"],
    g["fitted_coefficient_used"],
])
print("BGCE443_VERIFY_PASS")
