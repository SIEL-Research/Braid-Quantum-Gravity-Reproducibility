#!/usr/bin/env python3
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
manifest = json.loads((HERE / "INPUT_MANIFEST.json").read_text())
checks = {
    path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest
    for path, digest in manifest["inputs"].items()
}
assert all(checks.values())
docs = {path: json.loads((ROOT / path).read_text()) for path in manifest["inputs"]}
get = lambda token: next(v for p, v in docs.items() if token in p)
bh3, bh4, bh5, bh15, bh31, bh32, bg348 = (
    get(token) for token in ("BQGBH003", "BQGBH004", "BQGBH005", "BQGBH015", "BQGBH031", "BQGBH032", "BGCE348")
)

assert "reflection" in bh3["decision"].lower() or "REFLECT" in bh3["decision"]
assert bh4["fixed_mass_two_register_dynamics_pass"] is True
assert bh5["source_coordinate"]["identity"] == "R^2=X^2+ell_star^2"
assert bh15["signed_screen_parity"]["X_under_sigma_reversal"] == "odd"
assert bh31["finite_Euler_Y"] == "DeltaR_left/h_left-DeltaR_right/h_right=0"
assert bh32["regular_black_bounce_stationary_in_relative_Palatini_class"] is True

# Exact arbitrary-chain identity.  Treat left and right screen slopes as two
# independent symbols.  The source current divergence and the pure Palatini
# Euler covector have the same coefficient vector (+1,-1).
source_divergence_coefficients = [Q(1), Q(-1)]
palatini_euler_coefficients = [Q(1), Q(-1)]
current_shape_match_all_nonuniform_nodes = source_divergence_coefficients == palatini_euler_coefficients
required_interaction_coefficients = [-x for x in source_divergence_coefficients]

# Exact throat in Q(sqrt(2)): left slope=1-sqrt(2), right=sqrt(2)-1.
left = (Q(1), Q(-1))
right = (Q(-1), Q(1))
source_divergence = (left[0]-right[0], left[1]-right[1])
required_interaction = (-source_divergence[0], -source_divergence[1])
total = (source_divergence[0]+required_interaction[0], source_divergence[1]+required_interaction[1])
throat_exact = source_divergence == (Q(2),Q(-2)) and required_interaction == (Q(-2),Q(2)) and total == (Q(0),Q(0))

# BGCE348 fixes the branch tangents and their unconditioned cancellation.
branch = bg348["branch_resolved_identity"]
raw = branch["raw_effect_tangent"]
petz = branch["Petz_effect_tangent"]
contrast = branch["branch_contrast"]
average = branch["unconditioned_cancellation"]
assert "D_alpha/2" in raw
assert "-D_alpha/2" in petz
assert "=D_alpha" in contrast
assert "=0" in average

available_branch_coefficients = {
    "raw": "plus one-half",
    "Petz": "minus one-half",
    "raw_minus_Petz": "plus one",
    "Petz_minus_raw": "minus one",
    "unconditioned_average": "zero",
}
negative_unit_contrast_available = available_branch_coefficients["Petz_minus_raw"] == "minus one"
unconditioned_interaction_nonzero = available_branch_coefficients["unconditioned_average"] != "zero"

# The frozen BGCE348 source record defines raw-minus-Petz as its metric
# contrast.  It does not state that the reversed Petz-minus-raw ordering is
# the physical radial backreaction coupling.  Availability is not selection.
negative_coupling_uniquely_selected = False

result = {
    "schema": "siel.public-calculation.bqgbh033.raw_output.v1",
    "scout_id": "PUBLIC-RUN-BQGBH-033-X1",
    "source_revision": manifest["source_revision"],
    "all_input_hashes_match": all(checks.values()),
    "input_hash_checks": checks,
    "source_screen_current": "j_e=Delta rho_e/Delta X_e",
    "source_screen_current_as_walk_coboundary": "rho-rho_after_step, normalized by the signed source edge length",
    "node_current_divergence": "Q_k=j_left-j_right",
    "source_divergence_coefficients_left_right": [str(x) for x in source_divergence_coefficients],
    "pure_Palatini_Euler_coefficients_left_right": [str(x) for x in palatini_euler_coefficients],
    "current_shape_matches_pure_Palatini_Euler_on_every_nonuniform_internal_node": current_shape_match_all_nonuniform_nodes,
    "required_interaction_coefficients_left_right": [str(x) for x in required_interaction_coefficients],
    "throat_source_divergence_Qsqrt2": [str(x) for x in source_divergence],
    "throat_required_interaction_Qsqrt2": [str(x) for x in required_interaction],
    "throat_total_Qsqrt2": [str(x) for x in total],
    "throat_exact_cancellation": throat_exact,
    "raw_Petz_available_branch_coefficients": available_branch_coefficients,
    "negative_unit_Petz_minus_raw_contrast_available": negative_unit_contrast_available,
    "unconditioned_branch_average_supplies_nonzero_interaction": unconditioned_interaction_nonzero,
    "negative_radial_backreaction_coupling_uniquely_selected_by_existing_source_record": negative_coupling_uniquely_selected,
    "target_Einstein_tensor_accessed": False,
    "target_stress_accessed": False,
    "coefficient_fit": False,
    "parameter_scan": False,
    "decision": "SPLIT_SCOPED_PASS_ACTUAL_REFLECTED_SOURCE_SCREEN_WALK_GENERATES_THE_EXACT_NONUNIFORM_PALATINI_EULER_CURRENT_SHAPE_AND_THROAT_MAGNITUDE__SCOPED_NO_GO_UNCONDITIONED_RAW_PETZ_AVERAGE_IS_ZERO_AND_EXISTING_RECORDS_DO_NOT_SELECT_PETZ_MINUS_RAW_AS_THE_PHYSICAL_NEGATIVE_RADIAL_COUPLING__SIGN_SELECTION_REMAINS_OPEN",
    "next_gate": "BQGBH-034_PETZ_RECOVERY_ORIENTATION_TO_NEGATIVE_SCREEN_CURRENT_COUPLING_GATE",
    "ordinary_explanation": "A scalar field on a chain always has a gradient and divergence; the remaining physical question is why the source current enters the Palatini equation with the cancelling sign.",
    "strongest_counterpattern": "Both plus-one and minus-one branch contrasts are algebraically available by reversing the contrast order, while the prior-summed instrument has zero first variation. Availability does not select the physical sign.",
    "claim_ceiling": "Exact derivation of the required radial current shape and magnitude from the reflected source screen walk. No unique physical sign or unconditional interaction action, and no collapse, evaporation, thermodynamics, astrophysical or empirical claim."
}
payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
(HERE / "RAW_OUTPUT.json").write_text(payload)
print(payload, end="")
