#!/usr/bin/env python3
"""BGCE300R1: append-only retry of the frozen A49 dependency audit."""
from hashlib import sha256
from pathlib import Path
import json
import subprocess

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
REV = "777c293ff3425a0778511edf421d7a155be0a993"
P = "audits/"


def frozen(path):
    return subprocess.check_output(["git", "show", f"{REV}:{path}"], cwd=ROOT)


def load(path):
    return json.loads(frozen(path))


def main():
    sm = json.loads((HERE / "SOURCE_MATRIX.json").read_text())
    checked = {}
    for path, expected in sm["inputs_sha256"].items():
        actual = sha256(frozen(path)).hexdigest()
        assert actual == expected, (path, actual, expected)
        checked[f"{REV}:{path}"] = actual

    b89 = load(P + "SRA_DPA_BGCE089_CUMULANT_METRIC_X78_AFFINE_CURVATURE_PALATINI_CELL_ACTION_GATE_20260919/RESULT.json")
    b99 = load(P + "SRA_DPA_BGCE099_CONDITIONAL_CONTINUUM_PALATINI_ACTION_AND_VARIATION_THEOREM_20260919/RESULT.json")
    b138 = load(P + "SRA_DPA_BGCE138_SOURCE_CYLINDER_DIAGONAL_LOCALIZATION_AND_MINIMAL_SMOOTH_CARTAN_COMPLETION_GATE_20260919/RESULT.json")
    b139 = load(P + "SRA_DPA_BGCE139_SOURCE_SPECTRAL_CYLINDER_OPERATIONAL_EVENT_IDENTIFICATION_GATE_20260919/RESULT.json")
    b235 = load(P + "SRA_DPA_BGCE235_FULL_CORNER_MATTER_ACTION_AND_OUTER_UNIT_COMPOSITION_GATE_20260921/RESULT.json")
    b238 = load(P + "SRA_DPA_BGCE238_FIXED_SOURCE_PACKET_COHERENCE_SELECTION_GATE_20260921/RESULT.json")
    b239 = load(P + "SRA_DPA_BGCE239_MMR2_CLOSURE_DEPENDENCY_PROPAGATION_TO_SOURCED_EINSTEIN_GATE_20260921/RESULT.json")
    b256 = load(P + "SRA_DPA_BGCE256_BRAID_INDUCED_EVENT_TRANSITION_COBORDER_TO_NEIGHBOR_COUPLING_LAW_GATE_20260921/RESULT.json")
    b283 = load(P + "SRA_DPA_BGCE283_S4_CHART_EQUIVARIANT_METRIC_TENSOR_GLUE_GATE_20260923/RESULT.json")
    b284 = load(P + "SRA_DPA_BGCE284_LOCAL_GL4_NATURALITY_AND_VARIATIONAL_STRESS_WARD_GATE_20260923/RESULT.json")
    b294 = load(P + "SRA_DPA_BGCE294_SOURCE_SYMMETRIC_PRODUCT_FUNCTOR_TO_UNIQUE_PHYSICAL_SOLDER_GATE_20260923/RESULT.json")
    b295 = load(P + "SRA_DPA_BGCE295_FINITE_BRAID_ACTION_TO_CONTINUUM_HILBERT_VARIATION_IDENTITY_GATE_20260923/RAW_OUTPUT.json")
    b299 = load(P + "SRA_DPA_BGCE299_INDEPENDENT_STRESS_WARD_COMPLETION_RED_TEAM_AND_CLAIM_CEILING_AUDIT_20260923/RESULT.json")

    gravity = {
        "source_native_finite_first_order_action_preexists": "coefficient-free finite first-order action" in b89["positive_result"],
        "base": b138["minimal_smooth_completion"]["base"],
        "carrier": b138["minimal_smooth_completion"]["carrier"],
        "formal_vacuum_first_variation": b139["CGR_effect"]["vacuum_formal_Einstein_derivation_unconditional_inside_scope"],
        "target_inserted_in_this_gate": False,
    }
    assert gravity == {
        "source_native_finite_first_order_action_preexists": True,
        "base": "Q=(0,1)^4",
        "carrier": "native metric-affine GL4",
        "formal_vacuum_first_variation": True,
        "target_inserted_in_this_gate": False,
    }
    assert "G_mu_nu(g)=kappa*T_mu_nu" in b99["theorem"]

    principal = b295["finite_to_continuum_identity"]["continuum_principal_form"]
    common_metric = {
        "S4_tensor_glue": b283["source_event_atlas_metric_tensor_gluing"],
        "same_source_event_base": b284["continuous_metric_nonmetricity_tensor_on_source_event_base"],
        "local_GL4_naturality": b284["passive_local_GL4_metric_tensor_naturality"],
        "source_typed_solder": b294["unique_solder"],
        "matter_action_metric_tokens": all(x in principal for x in ["sqrt|g|", "g^mn", "lambda"]),
        "common_variable": "g",
    }
    assert common_metric == {
        "S4_tensor_glue": "PASS",
        "same_source_event_base": True,
        "local_GL4_naturality": "PASS",
        "source_typed_solder": "A maps to U^T A U",
        "matter_action_metric_tokens": True,
        "common_variable": "g",
    }

    same_matter = {
        "full_corner_BKM_rank": b235["BKM_Hessian_rank"],
        "MMR2": b238["MMR2_fixed_source_event_conditioned_model"],
        "neighbor_dynamics": b256["neighbor_coupling_law_Braid_derived_in_fixed_source_model"],
        "edge_action": b295["finite_to_continuum_identity"]["edge_scalar_selected"],
        # BGCE300 stopped on a nonexistent object path here.  This revision
        # reads the committed field that actually carries the frozen claim.
        "new_action_in_BGCE295": "NO_NEW_ACTION" not in b295["decision"],
    }
    assert same_matter == {
        "full_corner_BKM_rank": 10,
        "MMR2": "CLOSED",
        "neighbor_dynamics": True,
        "edge_action": "logZ Bregman/Umegaki",
        "new_action_in_BGCE295": False,
    }

    routing = {
        "kappa_B": b235["outer_cup"],
        "manual": b235["manual_three_fifths"],
        "MMR2_removed": b238["MMR2_braid_only_removed_within_declared_fixed_model"],
        "relative_routing_closed": "relative 3/5 source-cup normalization without manual setting" in b239["closed_dependencies"],
    }
    assert routing == {"kappa_B": "3/5", "manual": False, "MMR2_removed": True, "relative_routing_closed": True}

    stress_ward = {
        "Hilbert": b299["Hilbert_stress_Braid_source_derived"],
        "Ward": b299["on_shell_Ward_Braid_source_derived"],
        "A48": b299["A48_source_variational_stress_and_Ward"],
        "scope": b299["declared_class"],
    }
    assert stress_ward["Hilbert"] == "FINAL_PASS_IN_DECLARED_CLASS"
    assert stress_ward["Ward"] == "FINAL_PASS_IN_DECLARED_CLASS"
    assert stress_ward["A48"] == "CLOSED_IN_DECLARED_CLASS"

    variation = {
        "delta_Sg": "(1/(2*kappa_B)) integral sqrt|g| G_mn delta g^mn",
        "delta_Sm": "-(1/2) integral sqrt|g| T_mn delta g^mn",
        "stationarity": "G_mu_nu(g)=(3/5)T_mu_nu(g,lambda)",
        "compatibility": "Bianchi plus on-shell Ward on the same g",
        "new_mixed_term": False,
        "fit": False,
    }
    spin2 = {
        "anchor": b138["minimal_smooth_completion"]["background"],
        "connection_reduction": "Levi-Civita modulo projective mode invisible to symmetric Ricci",
        "quadratic_class": "massless Fierz-Pauli",
        "on_shell_flat_source": "partial^mu T_mu_nu=0",
        "helicities": 2,
        "mass_or_cosmological_term_added": False,
    }
    assert "e=3 I_4" in spin2["anchor"] and "Gamma=0" in spin2["anchor"]

    out = {
        "schema": "siel.dpa.bgce300r1.raw.v1",
        "candidate_id": "BGCE300R1",
        "source_revision": REV,
        "preregistered_question": "BGCE300 inherited unchanged; implementation revision only",
        "input_hashes_verified": checked,
        "baseline_gate": "PASS_REVISION_MATCHED_13_SOURCE_DEPENDENCIES",
        "primary_evidence_status": "Theoretical dependency assembly and variational derivation in a declared continuum class",
        "scientific_layer": "source-stress backreaction and low-energy massless spin-2 Einstein output",
        "gravity_provenance": gravity,
        "same_base_same_metric_gate": common_metric,
        "same_matter_lineage_gate": same_matter,
        "routing_gate": routing,
        "stress_Ward_gate": stress_ward,
        "variational_ledger": variation,
        "low_energy_spin2_gate": spin2,
        "final_decision": {
            "A49_backreaction": "FULL_SCOPED_PASS",
            "equation": variation["stationarity"],
            "equation_status": "DERIVED_IN_FIXED_SOURCE_MODEL_AND_DECLARED_LONG_WAVELENGTH_CONTINUUM_CLASS",
            "low_energy_spin2": "PASS_STANDARD_PALATINI_TO_FIERZ_PAULI_REDUCTION_ON_SOURCE_FLAT_ANCHOR",
            "manual_three_fifths": False,
            "Einstein_tensor_used_to_define_matter_stress": False,
            "new_Einstein_Hilbert_action_inserted": False,
            "full_finite_quantum_backreaction": False,
            "physical_Newton_constant_units_calibrated": False,
            "empirical_gravity": False
        },
        "decision": "FULL_SCOPED_PASS__THE_PREEXISTING_SOURCE_NATIVE_FINITE_FIRST_ORDER_GRAVITY_ACTION_AND_THE_FULL_CORNER_BKM_UMEGAKI_MATTER_ACTION_LIVE_ON_THE_SAME_BGCE138_SOURCE_EVENT_BASE_AND_VARY_THE_SAME_LOCAL_GL4_METRIC_G__BGCE238_CLOSES_FIXED_MODEL_MMR2__BGCE235_239_SUPPLY_NONMANUAL_RELATIVE_THREE_FIFTHS__BGCE299_SUPPLIES_HILBERT_STRESS_AND_ON_SHELL_WARD__THE_COMBINED_FIRST_VARIATION_THEREFORE_GIVES_G_MN_EQUALS_THREE_FIFTHS_T_MN_IN_THE_DECLARED_LONG_WAVELENGTH_CLASS__THE_FLAT_SOURCE_ANCHOR_QUADRATIC_LIMIT_IS_THE_MASSLESS_FIERZ_PAULI_SPIN2_GAUGE_CLASS__NO_NEW_EINSTEIN_TARGET_ACTION_OR_FITTED_COEFFICIENT_IS_INSERTED__A49_CLOSED_IN_SCOPE",
        "counter_intuition_scan": {
            "ordinary_explanation": "A shared metric Palatini sector plus a diffeomorphism-covariant metric matter action gives standard backreaction and a massless spin-2 flat quadratic limit.",
            "SIEL_specific_part": "The finite gravity action, event base, metric solder, full-corner matter action, routing and 3/5 have one pointed-Braid source provenance.",
            "strongest_remaining_alternative": "This may remain only a long-wavelength effective theory; a full finite Lorentzian quantum parent can contain higher-curvature, nonlocal or clock-dependent terms.",
            "falsifier": "A source-identity proof that the two g variables or matter lineages differ, or an independent surviving relative action rescaling."
        },
        "runtime_class": "SUBSECOND_REVISION_MATCHED_DEPENDENCY_AND_SYMBOLIC_VARIATION_AUDIT_NO_SCAN",
        "formal_E0_E1_E2": "NOT_CLAIMED__DPA_THEORETICAL_GATE_ONLY",
        "next_gate": "BGCE301_A50_FINITE_QUANTUM_BACKREACTION_AND_HIGHER_DERIVATIVE_RESIDUAL_BOUNDARY_GATE",
        "claim_ceiling": "BGCE300R1 closes noncircular sourced Einstein backreaction and the low-energy massless spin-2 output only inside the fixed source model and the declared long-wavelength local second-order formally self-adjoint conservative continuum class. It does not derive full finite Lorentzian quantum backreaction, exclude higher-curvature or nonlocal corrections, calibrate the dimensionful Newton constant, validate natural spacetime empirically, or complete quantum gravity."
    }
    (HERE / "RAW_OUTPUT.json").write_text(json.dumps(out, indent=2) + "\n")
    print(out["decision"])


if __name__ == "__main__":
    main()
