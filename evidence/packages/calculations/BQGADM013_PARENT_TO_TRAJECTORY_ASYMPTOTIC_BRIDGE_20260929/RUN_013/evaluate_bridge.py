#!/usr/bin/env python3
"""Deterministic source audit for the BQGADM-013 parent/trajectory bridge."""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
MATRIX_PATH = HERE / "SOURCE_MATRIX.json"


def git_bytes(commit: str, path: str) -> bytes:
    return subprocess.check_output(
        ["git", "show", f"{commit}:{path}"], cwd=REPO
    )


def load_pinned(commit: str, path: str) -> dict:
    return json.loads(git_bytes(commit, path))


matrix = json.loads(MATRIX_PATH.read_text())
commit = matrix["source_commit"]

source_hashes = {}
source_records = {}
for source in matrix["sources"]:
    raw = git_bytes(commit, source["path"])
    digest = hashlib.sha256(raw).hexdigest()
    source_hashes[source["path"]] = {
        "expected": source["sha256"],
        "actual": digest,
        "pass": digest == source["sha256"],
    }
    source_records[source["path"]] = json.loads(raw)


def record(suffix: str) -> dict:
    matches = [
        value for path, value in source_records.items() if path.endswith(suffix)
    ]
    assert len(matches) == 1, (suffix, len(matches))
    return matches[0]


bgce099 = record("BGCE099_CONDITIONAL_CONTINUUM_PALATINI_ACTION_AND_VARIATION_THEOREM_20260919/RESULT.json")
bgce294 = record("BGCE294_SOURCE_SYMMETRIC_PRODUCT_FUNCTOR_TO_UNIQUE_PHYSICAL_SOLDER_GATE_20260923/RESULT.json")
bgce295 = record("BGCE295_FINITE_BRAID_ACTION_TO_CONTINUUM_HILBERT_VARIATION_IDENTITY_GATE_20260923/RESULT.json")
bgce300 = record("BGCE300R1_A49_NONCIRCULAR_BACKREACTION_TO_LOW_ENERGY_SPIN2_EINSTEIN_GATE_20260923/RESULT.json")
bgce446 = record("BGCE446_SOURCE_625_CHILD_FOURTH_JET_TO_PBM_U4_GATE_20260925/RESULT.json")
bgce447 = record("BGCE447_SOURCE_CYLINDER_TO_UB612_PBM_METRIC_SAME_CARRIER_INTERTWINER_GATE_20260925/RESULT.json")
adm006 = record("SOURCE_INCIDENCE_TORSION_ADM_CONSTRAINT_SYMBOL_GATE_20260926/RUN_006/RESULT.json")
adm012 = record("SOURCE_PERFECT_HISTORY_GROUPOID_ADM_HDA_CLOSURE_20260926/RUN_012/RESULT.json")
euler004 = record("LINEAR_TWO_MODE_FINITE_TIME_STRONG_CONVERGENCE_GATE_20260926/RUN_004/RESULT.json")
euler006 = record("ENTROPIC_POSITIVE_MOMENT_CLOSURE_GATE_20260926/RUN_006/RESULT_ATTEMPT_006.json")
euler007 = record("BKM_HORIZONTAL_SELECTION_AND_LOCAL_NONLINEAR_CONVERGENCE_CLOSURE_20260926/RUN_007/RESULT.json")
euler010 = record("NORMALIZED_SYM2_TEN_COMPONENT_STRONG_CONVERGENCE_CLOSURE_20260926/RUN_010/RESULT.json")

gates = {
    "pinned_source_hashes": all(row["pass"] for row in source_hashes.values()),
    "same_rank_ten_metric_carrier": (
        bgce294["verification"].startswith("FULL_PASS_UNIQUE_SOLDER")
        and bgce294["source_product_spanning_rank"] == 10
        and bgce447["gate_decision"]["source_to_actual_UB612_metric_intertwiner"]
        == "PASS_EXACT_INVERTIBLE"
        and bgce446["gate_decision"]["commutes_with_ten_component_metric_solder"]
        == "PASS"
    ),
    "same_continuum_metric_euler_target": (
        "G_mu_nu(g)=kappa*T_mu_nu" in bgce099["theorem"]
        and bgce295["finite_Braid_edge_to_continuum_variation_identity"] == "PASS"
        and bgce300["same_local_GL4_metric_g"] is True
        and bgce300["A49_noncircular_backreaction"] == "CLOSED_IN_DECLARED_CLASS"
    ),
    "unique_positive_bkm_exact_moment_member": (
        euler006["gates"]["feature_rank_six"]
        and euler006["gates"]["exact_strict_positive_feasible_witness"]
        and euler006["gates"]["dual_hessian_positive"]
        and euler006["gates"]["all_entropy_rates_positive"]
        and euler007["typing_identity"]["new_functional_form"] is False
        and euler007["typing_identity"]["new_target_equation_fit"] is False
        and euler010["gate_results"]["exact_actual_metric_principal_moment"].startswith("PASS")
    ),
    "strong_on_shell_euler_defect_vanishes": (
        "h^2+tau_h^2" in euler010["proved_bounds"]["strong_local_truncation"]
    ),
    "subsidiary_defect_vanishes_for_tau_order_h": (
        "h+tau_h^2/h" in euler010["proved_bounds"]["subsidiary_residual"]
        and "tau_h=O(h)" in euler010["proved_bounds"]["trajectory"]
    ),
    "strong_common_interval_trajectory_convergence": (
        "-> 0" in euler010["proved_bounds"]["trajectory"]
        and euler010["work_package_status_after_gate"] == "CLOSED_SCOPED"
    ),
    "perfect_parent_exact_noether_and_refinement": (
        adm012["gate_results"]["off_shell_noether_identity"].startswith("PASS_EXACT")
        and adm012["gate_results"]["refinement_naturality"].startswith("PASS_EXACT")
    ),
    "finite_local_update_exact_constraint_preservation": (
        "exact finite-mesh HDA/BFV and exact zero constraint preservation"
        not in euler010["remaining_open"]
    ),
    "physical_dimension_and_flat_helicity_compatible": (
        adm012["proof"]["physical_quotient"].endswith("two configuration modes")
        and adm006["decisive_result"].find("rank-four") >= 0
        and bgce300["physical_helicities_in_4D"] == 2
    ),
    "explicit_source_physical_projector_present": (
        euler004["physical_ADM_two_mode_strong_convergence"]
        != "OPEN_SOURCE_IDENTIFICATION_REQUIRED"
    ),
    "no_new_coefficient_action_or_target_fit": (
        euler010["gate_results"]["no_new_physical_coefficient_or_target_fit"]
        == "PASS"
        and bgce300["new_Einstein_Hilbert_action_inserted"] is False
        and bgce300["fitted_coefficient"] is False
    ),
}

asymptotic_gate_names = [
    "pinned_source_hashes",
    "same_rank_ten_metric_carrier",
    "same_continuum_metric_euler_target",
    "unique_positive_bkm_exact_moment_member",
    "strong_on_shell_euler_defect_vanishes",
    "subsidiary_defect_vanishes_for_tau_order_h",
    "strong_common_interval_trajectory_convergence",
    "perfect_parent_exact_noether_and_refinement",
    "physical_dimension_and_flat_helicity_compatible",
    "no_new_coefficient_action_or_target_fit",
]

literal_exact_identity = (
    gates["perfect_parent_exact_noether_and_refinement"]
    and gates["finite_local_update_exact_constraint_preservation"]
    and gates["explicit_source_physical_projector_present"]
)
asymptotic_bridge = all(gates[name] for name in asymptotic_gate_names)

raw_output = {
    "schema": "siel.public-calculation.bqgadm013.raw_output.v1",
    "scout_id": "PUBLIC-RUN-BQGADM-013",
    "source_commit": commit,
    "source_hashes": source_hashes,
    "gates": gates,
    "order_reduction_when_tau_equals_lambda_h": {
        "euler_defect": "O((1+lambda^2) h^2)",
        "subsidiary_defect": "O((1+lambda^2) h)",
        "both_vanish": True,
    },
    "literal_exact_finite_flow_identity": literal_exact_identity,
    "asymptotic_on_shell_bridge": asymptotic_bridge,
    "physical_projector_status": "OPEN_SOURCE_IDENTIFICATION_REQUIRED",
    "environment": {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "evaluator_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    },
}

if not asymptotic_bridge:
    decision = "NO_GO_ASYMPTOTIC_PARENT_TO_TRAJECTORY_BRIDGE"
elif literal_exact_identity:
    decision = "PASS_EXACT_FINITE_PARENT_TO_TRAJECTORY_IDENTITY"
else:
    decision = (
        "SCOPED_PASS_ASYMPTOTIC_ON_SHELL_PARENT_TO_TRAJECTORY_BRIDGE__"
        "NO_GO_LITERAL_EXACT_FINITE_FLOW_IDENTITY__"
        "OPEN_EXPLICIT_PHYSICAL_PROJECTOR"
    )

result = {
    "schema": "siel.public-calculation.bqgadm013.result.v1",
    "scout_id": "PUBLIC-RUN-BQGADM-013",
    "date": "2026-09-29",
    "work_packages": ["BQG-G3-R01.5", "BQG-G3-R02.5"],
    "primary_evidence_status": "Theoretical derivation",
    "decision": decision,
    "literal_bold_hypothesis": "NO_GO",
    "revised_bold_hypothesis": "SCOPED_PASS" if asymptotic_bridge else "NO_GO",
    "decisive_result": (
        "The perfect history-groupoid flow and the normalized local metric-Euler "
        "update are not the same finite map: the former has exact Noether and "
        "refinement constraint closure, whereas the latter has only a vanishing "
        "finite-mesh subsidiary defect. They nevertheless form an on-shell "
        "asymptotic commuting bridge on the common local regular branch. The "
        "same source metric carrier and continuum Euler equation are used, the "
        "positive exact-moment BKM member is unique inside the declared source "
        "leaf, the Euler defect is O(h^2+tau^2), the subsidiary defect is "
        "O(h+tau^2/h), and trajectories converge strongly for tau=O(h)."
    ),
    "bridge_relations": {
        "perfect_branch": "E(S_h^perf)=0 with R_h^dagger E(S_h^perf)=0 exactly",
        "local_shadow": "||E_h I_h U-I_h E(U)|| <= C(h^2+tau_h^2)",
        "constraint_commutator": "||B_h E_h I_h U|| <= C(h+tau_h^2/h)",
        "trajectory": "sup_[0,T] ||J_h U_h-U|| <= C_T(eta_h+h+tau_h^2/h) -> 0 for tau_h=O(h)",
        "uniqueness_scope": "source C5^3 directions plus positive BKM exponential leaf plus exact six metric moments plus source-forced 1/25 normalization",
    },
    "gate_results": gates,
    "physical_sector": {
        "dimension_and_flat_helicity_match": "PASS",
        "exact_finite_projector_intertwiner": "OPEN",
        "reason": "BQGEULER-004 explicitly retains OPEN_SOURCE_IDENTIFICATION_REQUIRED; dimension two plus a matching principal class does not construct a canonical projector."
    },
    "counter_intuition": {
        "strongest_counter_pattern": "Exact perfect-action constraint preservation and only asymptotic stencil preservation are incompatible with literal equality of the finite maps.",
        "ordinary_explanation": "A standard consistent stable discretization and an exact discrete Lagrangian can converge to the same continuum PDE without being variationally identical at finite resolution.",
        "braid_specific_input": "The Braid source fixes the common ten-metric carrier, one-plus-three chart, five-adic refinement, positive BKM leaf, exact metric moments, source clock and normalization.",
        "falsifier": "Carrier mismatch, different continuum Euler targets, loss of BKM uniqueness, nonvanishing residual under tau=O(h), failure of strong trajectory convergence, or an explicit finite physical projector contradicting the recorded OPEN boundary."
    },
    "remaining_open": [
        "an off-shell operator equality or an explicit variational derivation of the BQGEULER-010 stencil from S_h^perf",
        "a source-derived finite physical projector intertwining the four-dimensional quotient with the two-polarization carrier",
        "exact finite-mesh constraint preservation by the local update",
        "global or strong-curvature continuation, fully coupled matter and empirical gravity"
    ],
    "formal_E0_E1_E2": "NOT_CLAIMED__BOUNDED_PUBLIC_EXACT_THEORETICAL_SCOUT",
    "claim_ceiling": (
        "Local regular on-shell asymptotic commuting bridge and unique local "
        "shadow only within the source-typed positive-BKM exact-moment class. "
        "No literal exact finite-flow identity, explicit physical projector, "
        "off-shell variational equivalence, universal discretization theorem, "
        "global/strong-curvature result, empirical gravity, confirmation, RPD "
        "adoption, Level 3 or Official SIEL status."
    ),
}

(HERE / "RAW_OUTPUT.json").write_text(
    json.dumps(raw_output, indent=2, sort_keys=True) + "\n"
)
(HERE / "RESULT.json").write_text(
    json.dumps(result, indent=2, sort_keys=True) + "\n"
)
print(json.dumps({"decision": decision, "gates": gates}, indent=2, sort_keys=True))
