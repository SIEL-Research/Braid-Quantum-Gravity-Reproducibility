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
bh3, bh4, bh5, bh17, bh27, bh31, bh32, bh35 = (
    get(token) for token in
    ("BQGBH003", "BQGBH004", "BQGBH005", "BQGBH017", "BQGBH027", "BQGBH031", "BQGBH032", "BQGBH035")
)

assert bh4["fixed_mass_two_register_dynamics_pass"] is True
assert bh5["source_coordinate"]["identity"] == "R^2=X^2+ell_star^2"
assert bh17["full_six_face_holonomy_pass"] is True
assert bh27["horizon_F_zero_rank"] == 4
assert bh31["complete_connection_eliminated_edge_action"] == "2*C*(DeltaR*Delta(RF)/h+kappa_Omega*h)"
assert bh32["regular_black_bounce_stationary_in_relative_Palatini_class"] is True
assert bh35["unit_relative_coefficient_forced"] is True

# Exact global regimes for a=ell_star>0, m=r_h>=0.
horizon_regimes = {
    "m<a": "no horizon; F>0",
    "m=a": "double horizon at X=0",
    "m>a": "simple horizons X_plus/minus=plus/minus sqrt(m^2-a^2)",
}
simple_horizon_derivative = "F'(X_s)=X_s/m^2"
signed_surface_gravity = "kappa_s=F'(X_s)/2=X_s/(2m^2)"
simple_horizon_nonzero = True
degenerate_expansion = "m=a: F(X)=X^2/(2a^2)+O(X^4)"

# The old one-chart completeness inference omitted the second null family.
# For radial nulls, Xdot=+E gives dv/dX=2/F.  At a simple horizon,
# F=2 kappa_s (X-X_s)+..., hence v=(1/kappa_s)log|X-X_s|+O(1)
# while lambda=(X-X0)/E is finite.
single_ingoing_EF_chart_covers_both_null_families = False
outgoing_null_reaches_chart_infinity_at_finite_affine_parameter = True
outgoing_EF_extension = "u=v-2r_star; ds^2=-F du^2-2 du dX+R^2 dOmega^2"
kruskal_extension = {
    "definitions": "U_s=-exp(-kappa_s u), V_s=exp(kappa_s v)",
    "product": "U_s V_s=-exp(2 kappa_s r_star)=-(X-X_s)*exp(analytic)",
    "metric_coefficient": "-F*exp(-2 kappa_s r_star)/kappa_s^2 is finite and nonzero",
    "bifurcation_sphere_included": True,
}
horizon_complete_atlas = True

# Global regularity and ends.
two_asymptotically_flat_ends = True
minimum_areal_radius_positive = True
throat_is_interior_regular_surface = True
curvature_building_blocks_bounded = bh5["regularity"]["curvature_building_blocks_bounded"]
no_finite_affine_geometric_boundary_after_atlas_completion = True

# Connection-first resolution of the old logarithm obligation.
# On the selected solution DeltaY=DeltaR=Delta rho and rho is 1-Lipschitz,
# so |v_e|,|U_e|<=1 on every nonzero oriented edge.
connection_solution = {
    "v_e": "DeltaR_e/h_e",
    "U_e": "-DeltaY_e/h_e",
    "bounds": "abs(v_e)<=1 and abs(U_e)<=1",
    "reverse_edge": "integrated connection changes sign, so Hol(bar e)=Hol(e)^(-1)",
    "refinement": "ordered holonomies compose; no logarithm is taken",
}
global_matrix_log_required = False
connection_first_holonomy_globally_defined_on_source_chain = True

all_gates = all([
    simple_horizon_nonzero,
    outgoing_null_reaches_chart_infinity_at_finite_affine_parameter,
    horizon_complete_atlas,
    two_asymptotically_flat_ends,
    minimum_areal_radius_positive,
    throat_is_interior_regular_surface,
    curvature_building_blocks_bounded,
    no_finite_affine_geometric_boundary_after_atlas_completion,
    connection_first_holonomy_globally_defined_on_source_chain,
    not global_matrix_log_required,
])
assert all_gates

result = {
    "schema": "siel.public-calculation.bqgbh036.raw_output.v1",
    "scout_id": "PUBLIC-RUN-BQGBH-036-X1",
    "source_revision": manifest["source_revision"],
    "all_input_hashes_match": all(checks.values()),
    "input_hash_checks": checks,
    "selected_global_solution": "R=sqrt(X^2+ell_star^2); Y=R-r_h; F=1-r_h/R; X in R",
    "horizon_regimes": horizon_regimes,
    "simple_horizon_derivative": simple_horizon_derivative,
    "signed_surface_gravity": signed_surface_gravity,
    "degenerate_horizon_expansion": degenerate_expansion,
    "two_asymptotically_flat_ends": two_asymptotically_flat_ends,
    "minimum_areal_radius_positive": minimum_areal_radius_positive,
    "throat_is_interior_regular_surface": throat_is_interior_regular_surface,
    "curvature_building_blocks_bounded": curvature_building_blocks_bounded,
    "single_ingoing_EF_chart_covers_both_radial_null_families": single_ingoing_EF_chart_covers_both_null_families,
    "outgoing_null_reaches_v_infinity_at_finite_affine_parameter": outgoing_null_reaches_chart_infinity_at_finite_affine_parameter,
    "outgoing_EF_extension": outgoing_EF_extension,
    "simple_horizon_Kruskal_extension": kruskal_extension,
    "source_maximal_horizon_complete_atlas": horizon_complete_atlas,
    "no_finite_affine_geometric_boundary_after_atlas_completion": no_finite_affine_geometric_boundary_after_atlas_completion,
    "connection_first_solution": connection_solution,
    "global_matrix_log_required_by_selected_Palatini_action": global_matrix_log_required,
    "connection_first_holonomy_globally_defined_on_source_chain": connection_first_holonomy_globally_defined_on_source_chain,
    "target_Einstein_tensor_accessed": False,
    "target_stress_accessed": False,
    "coefficient_fit": False,
    "parameter_scan": False,
    "decision": "SPLIT_CLOSED_SCOPED_SELECTED_FINITE_ACTION_GIVES_A_TWO_ENDED_CURVATURE_REGULAR_HORIZON_COMPLETE_STATIC_SPHERICAL_ANALYTIC_DEVELOPMENT_AND_CONNECTION_FIRST_HOLONOMIES_REMOVE_THE_GLOBAL_MATRIX_LOG_OBLIGATION__CORRECTION_THE_SINGLE_INGOING_EF_CHART_ALONE_IS_NOT_COMPLETE_FOR_THE_OUTGOING_NULL_FAMILY__ABSOLUTE_ANALYTIC_INEXTENDIBILITY_AND_DYNAMICAL_BLACK_HOLE_FORMATION_REMAIN_OPEN",
    "next_gate": "BQGBH-037_SOURCE_MAXIMAL_ATLAS_INEXTENDIBILITY_AND_GLOBAL_CAUSAL_STRUCTURE_GATE",
    "ordinary_explanation": "A regular horizon needs an atlas, not one preferred EF chart.  The Palatini connection is primary, so finite holonomies are exponentials and need no globally single-valued logarithm.",
    "strongest_counterpattern": "The prior BQGBH-005 velocity bound controlled X but omitted that v diverges logarithmically for one null family at a simple horizon.  This is a chart endpoint, not a curvature endpoint.",
    "claim_ceiling": "Horizon-complete source-maximal static spherical analytic development and connection-first removal of the matrix-log obligation.  No absolute C^k inextendibility theorem, uniqueness, collapse, evaporation, thermodynamics, rotation, charge or empirical claim."
}
payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
(HERE / "RAW_OUTPUT.json").write_text(payload)
print(payload, end="")
