#!/usr/bin/env python3
import json
from pathlib import Path
r=json.loads((Path(__file__).resolve().parent/"RESULT.json").read_text())
assert r["all_input_hashes_match"] is True
assert r["remaining_contractions_match_exact_pattern"] is True
assert r["midpoint_identity_verified"] is True
assert r["gauge_zero_mode_decouples_exactly"] is True
assert r["complete_connection_eliminated_edge_action"]=="2*C*(DeltaR*Delta(RF)/h+kappa_Omega*h)"
assert r["intrinsic_screen_term_independent_of_R_and_RF"] is True
assert r["affine_solution_exact_on_arbitrary_nonuniform_mesh"] is True
assert r["finite_Schwarzschild_family_stationary"] is True
assert r["horizon_F_zero_regular"] is True
assert r["source_regular_bounce_throat_Euler_residual_Qsqrt2"]==["2","-2"]
assert r["pure_Palatini_regular_bounce_stationary"] is False
assert r["source_interaction_stress_required_for_positive_throat"] is True
assert r["coefficient_fit"] is False
assert r["decision"].startswith("SPLIT_SCOPED_PASS")
print("BQGBH-031 verification PASS")
