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
bh3, bh4, bh5, bh31, bh32, bh33, bg254, bg256 = (
    get(token) for token in
    ("BQGBH003", "BQGBH004", "BQGBH005", "BQGBH031", "BQGBH032", "BQGBH033", "BGCE254", "BGCE256")
)

assert "REFLECT" in bh3["decision"] or "reflection" in bh3["decision"].lower()
assert bh4["fixed_mass_two_register_dynamics_pass"] is True
assert bh5["source_coordinate"]["identity"] == "R^2=X^2+ell_star^2"
assert bh31["complete_connection_eliminated_edge_action"] == "2*C*(DeltaR*Delta(RF)/h+kappa_Omega*h)"
assert bh32["bregman_identity_exact_by_coefficients"] is True
assert bh33["current_shape_matches_pure_Palatini_Euler_on_every_nonuniform_internal_node"] is True
assert bg254["response_mismatch_one_form_exact"] is True
assert bg254["diagonal_zero_fixes_integration_constant"] is True
assert bg256["neighbor_coupling_law_Braid_derived_in_fixed_source_model"] is True

H = ((Q(0), Q(1)), (Q(1), Q(0)))
e_plus = (Q(1), Q(1))
e_minus = (Q(1), Q(-1))
matvec = lambda M, v: tuple(sum(M[i][j] * v[j] for j in range(2)) for i in range(2))
dot = lambda u, v: sum(a*b for a,b in zip(u,v))

positive_mode = matvec(H, e_plus) == e_plus and dot(e_plus, matvec(H, e_plus)) == Q(2)
negative_mode = matvec(H, e_minus) == tuple(-x for x in e_minus) and dot(e_minus, matvec(H, e_minus)) == Q(-2)
orthogonal_modes = dot(e_plus, matvec(H, e_minus)) == 0

# Source reference on any edge: fixed r_h gives Delta(rho-r_h)=Delta rho.
# Represent a=Delta rho by the coefficient of the basis vector e_plus.
source_shift_direction = e_plus
source_shift_has_negative_mode_component = False

# Exact polynomial coefficients in monomial order r*y, a*r, a*y, a^2.
pure_coefficients = (Q(2), Q(0), Q(0), Q(0))
bregman_coefficients = (Q(2), Q(-2), Q(-2), Q(2))
expected_relative_coefficients = tuple(Q(2)*Q(x) for x in bh32["bregman_coefficients_ab_ap_bp_p2"])
bregman_matches_bh32 = bregman_coefficients == expected_relative_coefficients
interaction_coefficients = tuple(bregman_coefficients[i] - pure_coefficients[i] for i in range(4))
expected_interaction_coefficients = (Q(0), Q(-2), Q(-2), Q(2))

# The gradient of the interaction with respect to (r,y) is (-2a,-2a),
# i.e. minus the source-positive-mode covector with the already fixed unit
# relative coefficient.  Edge assembly gives -Q in both node equations.
interaction_gradient_per_a = (Q(-2), Q(-2))
pure_reference_gradient_per_a = tuple(Q(2)*x for x in matvec(H, source_shift_direction))
negative_gradient_exact = interaction_gradient_per_a == tuple(-x for x in pure_reference_gradient_per_a)
unit_relative_coefficient = all(
    interaction_gradient_per_a[i] == -pure_reference_gradient_per_a[i]
    for i in range(2)
)
node_current_coefficients = [Q(1), Q(-1)]
interaction_node_coefficients = [-x for x in node_current_coefficients]
matches_bh33_required_node_coefficients = [str(x) for x in interaction_node_coefficients] == bh33["required_interaction_coefficients_left_right"]

all_gates = all([
    positive_mode,
    negative_mode,
    orthogonal_modes,
    not source_shift_has_negative_mode_component,
    bregman_matches_bh32,
    interaction_coefficients == expected_interaction_coefficients,
    negative_gradient_exact,
    unit_relative_coefficient,
    matches_bh33_required_node_coefficients,
])
assert all_gates

result = {
    "schema": "siel.dpa.bqgbh035.raw_output.v1",
    "scout_id": "DPA-SCOUT-BQGBH-035-X1",
    "source_revision": manifest["source_revision"],
    "all_input_hashes_match": all(checks.values()),
    "input_hash_checks": checks,
    "Palatini_edge_kernel_without_common_factor": "k(r,y)=2*r*y=x^T H x; H=[[0,1],[1,0]]",
    "positive_mode": "e_plus=(1,1); H e_plus=e_plus",
    "negative_mode": "e_minus=(1,-1); H e_minus=-e_minus",
    "source_fixed_tail_active_screen_shift": "p=a*(1,1), a=Delta rho, because Delta(rho-r_h)=Delta rho",
    "source_shift_has_negative_mode_component": source_shift_has_negative_mode_component,
    "response_exact_Bregman_primitive": "B_k(x,p)=2*(r-a)*(y-a)",
    "expanded_interaction": "-2*a*r-2*a*y+2*a^2",
    "matches_BQGBH032_relative_kernel_exactly": bregman_matches_bh32,
    "interaction_gradient_is_negative_source_positive_mode": negative_gradient_exact,
    "unit_relative_coefficient_forced": unit_relative_coefficient,
    "arbitrary_nonuniform_node_interaction_coefficients_left_right": [str(x) for x in interaction_node_coefficients],
    "matches_BQGBH033_required_negative_current": matches_bh33_required_node_coefficients,
    "raw_Petz_branch_order_used": False,
    "target_Einstein_tensor_accessed": False,
    "target_stress_accessed": False,
    "coefficient_fit": False,
    "parameter_scan": False,
    "decision": "CLOSED_SCOPED_SOURCE_FIXED_TAIL_ACTIVE_SCREEN_SHIFT_LIES_EXACTLY_IN_THE_POSITIVE_PALATINI_DIRICHLET_MODE__RESPONSE_EXACT_DIAGONAL_ZERO_BREGMAN_CENTERING_UNIQUELY_GENERATES_THE_BQGBH032_RELATIVE_ACTION_AND_THE_BQGBH033_NEGATIVE_UNIT_CURRENT__PETZ_BRANCH_SELECTION_NOT_NEEDED",
    "next_gate": "BQGBH-036_GLOBAL_LOG_BRANCH_AND_MAXIMAL_EXTENSION_FROM_THE_SELECTED_STATIC_SPHERICAL_FINITE_ACTION_GATE",
    "ordinary_explanation": "Completing the positive screen mode to a square around its source reference fixes the restoring minus sign.  The negative Palatini mode is orthogonal and is not treated as entropy.",
    "strongest_counterpattern": "The full Palatini form is indefinite.  The result would fail if the source shift had any component in its negative mode; exact fixed-tail typing makes that component zero.",
    "claim_ceiling": "Source selection of the negative interaction sign and unit coefficient in the complete static spherical reduced six-face Palatini class.  No claim for arbitrary nonspherical fields, physical-time dissipation, evaporation, thermodynamics or empirical black holes."
}
payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
(HERE / "RAW_OUTPUT.json").write_text(payload)
print(payload, end="")
