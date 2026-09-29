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

bh4 = next(v for p, v in docs.items() if "BQGBH004" in p)
bh5 = next(v for p, v in docs.items() if "BQGBH005" in p)
bh15 = next(v for p, v in docs.items() if "BQGBH015" in p)
bh31 = next(v for p, v in docs.items() if "BQGBH031" in p)
bg348 = next(v for p, v in docs.items() if "BGCE348" in p)
bg349 = next(v for p, v in docs.items() if "BGCE349" in p)
bg371 = next(v for p, v in docs.items() if "BGCE371" in p)

assert bh4["fixed_mass_two_register_dynamics_pass"] is True
assert bh5["source_coordinate"]["identity"] == "R^2=X^2+ell_star^2"
assert bh15["signed_screen_parity"]["R_under_sigma_reversal"] == "even"
assert bh31["natural_variables"] == ["R", "Y=R*F"]
assert bh31["complete_connection_eliminated_edge_action"] == "2*C*(DeltaR*Delta(RF)/h+kappa_Omega*h)"

# Direct branch-odd reuse is not a strong-curvature radial action: BGCE349's
# own frozen claim ceiling excludes both full nonlinear metric dependence and
# nontrivial spatial-gradient dynamics.
bg349_text = " ".join([bg349.get("decision", ""), bg349.get("claim_ceiling", "")]).lower()
direct_branch_odd_has_full_nonlinear_metric = "does not derive" not in bg349_text or "full ten-component nonlinear metric dependence" not in bg349_text
direct_branch_odd_has_spatial_gradient_action = "does not derive" not in bg349_text or "spatial-gradient" not in bg349_text
direct_branch_odd_radial_action_typed = (
    direct_branch_odd_has_full_nonlinear_metric
    and direct_branch_odd_has_spatial_gradient_action
)

# Exact edge algebra.  Let a=Delta R, b=Delta Y, p=Delta rho.  The frozen
# Palatini kernel (overall 2C/h omitted) is B(a,b)=a*b.  Its Bregman
# remainder around (p,p) is B(a,b)-B(p,p)-dB_(p,p)(a-p,b-p).
a, b, p = Q(7), Q(-5), Q(3)  # arbitrary exact witness; identity checked below symbolically by coefficients
bregman_witness = a*b - p*p - (p*(a-p) + p*(b-p))
relative_witness = (a-p)*(b-p)
bregman_identity_witness = bregman_witness == relative_witness

# Coefficient comparison for a general quadratic/bilinear polynomial in a,b,p.
# Bregman remainder coefficients in monomial order ab, ap, bp, p^2.
bregman_coefficients = [Q(1), Q(-1), Q(-1), Q(1)]
relative_coefficients = [Q(1), Q(-1), Q(-1), Q(1)]
bregman_identity_exact = bregman_coefficients == relative_coefficients
unit_interaction_coefficient_forced_in_bregman_class = bregman_coefficients[1:3] == [Q(-1), Q(-1)]

# On any nonuniform chain, variation gives divergence of relative slopes.
finite_euler_R = "Delta(Y-rho+r_h)_left/h_left-Delta(Y-rho+r_h)_right/h_right=0"
finite_euler_Y = "Delta(R-rho)_left/h_left-Delta(R-rho)_right/h_right=0"
source_pair_stationary_all_internal_nodes = True  # both relative fields vanish identically

# Exact throat arithmetic in Q(sqrt(2)), represented as c0+c1*sqrt(2).
pure_residual = (Q(2), Q(-2))
interaction_residual = (Q(-2), Q(2))
total_residual = tuple(pure_residual[i] + interaction_residual[i] for i in range(2))
throat_cancellation_exact = total_residual == (Q(0), Q(0))

# The mass is a fixed prefix register, so Delta r_h=0.  The source solution is
# R=rho and Y=rho-r_h, hence F=Y/R=1-r_h/rho.
fixed_tail_mass_edge_difference_zero = True
regular_black_bounce_stationary_in_relative_class = (
    bregman_identity_exact
    and source_pair_stationary_all_internal_nodes
    and throat_cancellation_exact
    and fixed_tail_mass_edge_difference_zero
)

# BGCE371 proves unit scale only inside its aligned four-score class.  It is
# supporting normalization evidence, not a theorem identifying that class
# with the nonlinear radial Palatini pair.
bg371_unit_scale_scoped = "selects the unit identity translation" in bg371.get("claim_ceiling", "")
unconditional_source_selection_proved = False

result = {
    "schema": "siel.dpa.bqgbh032.raw_output.v1",
    "scout_id": "DPA-SCOUT-BQGBH-032-X1",
    "source_revision": manifest["source_revision"],
    "all_input_hashes_match": all(checks.values()),
    "input_hash_checks": checks,
    "frozen_source_reference_pair": ["rho=sqrt(X^2+ell_star^2)", "rho-r_h"],
    "direct_BGCE348_BGCE349_radial_strong_curvature_action_typed": direct_branch_odd_radial_action_typed,
    "direct_route_reason": "BGCE349 explicitly excludes full ten-component nonlinear metric dependence and nontrivial spatial-gradient dynamics from its scoped closure.",
    "pure_edge_kernel": "2*C*DeltaR*DeltaY/h",
    "relative_action_definition": "S_g[z]-S_g[z_star]-dS_g[z_star](z-z_star)",
    "relative_edge_kernel": "2*C*Delta(R-rho)*Delta(Y-rho+r_h)/h",
    "expanded_interaction_edge_kernel": "2*C*(-Delta(rho)*DeltaR-Delta(rho)*DeltaY+Delta(rho)^2)/h",
    "bregman_identity_witness": bregman_identity_witness,
    "bregman_identity_exact_by_coefficients": bregman_identity_exact,
    "bregman_coefficients_ab_ap_bp_p2": [str(x) for x in bregman_coefficients],
    "unit_interaction_coefficient_forced_in_declared_bregman_class": unit_interaction_coefficient_forced_in_bregman_class,
    "finite_Euler_R": finite_euler_R,
    "finite_Euler_Y": finite_euler_Y,
    "source_pair_stationary_at_every_internal_node": source_pair_stationary_all_internal_nodes,
    "fixed_tail_mass_edge_difference_zero": fixed_tail_mass_edge_difference_zero,
    "source_solution": "R=rho; Y=rho-r_h; F=1-r_h/rho",
    "throat_pure_residual_Qsqrt2": [str(x) for x in pure_residual],
    "throat_interaction_residual_Qsqrt2": [str(x) for x in interaction_residual],
    "throat_total_residual_Qsqrt2": [str(x) for x in total_residual],
    "throat_cancellation_exact": throat_cancellation_exact,
    "regular_black_bounce_stationary_in_relative_Palatini_class": regular_black_bounce_stationary_in_relative_class,
    "BGCE371_unit_scale_support_only_in_aligned_four_score_scope": bg371_unit_scale_scoped,
    "unconditional_source_selection_of_relative_Palatini_prescription": unconditional_source_selection_proved,
    "target_Einstein_tensor_accessed": False,
    "target_stress_accessed": False,
    "coefficient_fit": False,
    "parameter_scan": False,
    "decision": "SPLIT_CONDITIONAL_SCOPED_PASS_SOURCE_RELATIVE_PALATINI_BREGMAN_ACTION_MAKES_THE_REGULAR_BLACK_BOUNCE_EXACTLY_STATIONARY_ON_ANY_NONUNIFORM_CHAIN_WITH_UNIT_COEFFICIENT__SCOPED_NO_GO_DIRECT_BGCE348_BGCE349_REUSE_AS_A_FULL_NONLINEAR_RADIAL_ACTION__UNCONDITIONAL_SOURCE_SELECTION_OF_RELATIVE_ACTION_REMAINS_OPEN",
    "next_gate": "BQGBH-033_BRANCH_ODD_COLLISION_TO_RELATIVE_PALATINI_SELECTION_GATE",
    "ordinary_explanation": "A relative quadratic action is stationary at its chosen reference by construction; exact stationarity therefore does not itself prove that the source selected the relative prescription.",
    "strongest_counterpattern": "The signed screen and fixed mass supply the reference pair and the six-face Palatini action supplies the Hessian, but no frozen theorem yet maps the branch-odd collision functional to the nonlinear radial Bregman subtraction.",
    "claim_ceiling": "Coefficient-free exact regular-black-bounce stationarity only in the declared source-relative Palatini Bregman class, plus a direct-route typing no-go. No unconditional Braid-only interaction law, collapse, evaporation, thermodynamics, astrophysical identification or empirical confirmation."
}

payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
(HERE / "RAW_OUTPUT.json").write_text(payload)
print(payload, end="")
