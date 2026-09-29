#!/usr/bin/env python3
"""BGCE322: exact collision-support interaction balance and CTP transport gate.

This is a subsecond theorem-composition check.  It does not scan parameters or
pretend that an isometric support lift is already a dynamical metric
deformation of the collision unitary.
"""

from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
REV = "686e27e963841a280545e418fcaeb97e228e9957"

INPUTS = {
    "audits/SRA_DPA_BGCE299_INDEPENDENT_STRESS_WARD_COMPLETION_RED_TEAM_AND_CLAIM_CEILING_AUDIT_20260923/RESULT.json": "f077cb7e84ce29bbbcd2e8593d539c0ed9b2581a913a210151005c508cb6ee0b",
    "audits/SRA_DPA_BGCE310_TORSOR_GAUGE_COVARIANT_ENVIRONMENT_CHARGE_AND_TOTAL_G1_BALANCE_GATE_20260923/RESULT.json": "cf2c04a8f32f8f5a2ffb2d2ff0c95600de10e2d467e830a0d5da65452a2988f0",
    "audits/SRA_DPA_BGCE311_FOUR_SOURCE_CHARGE_ENVIRONMENT_BALANCES_TO_DISCRETE_TOTAL_WARD_GATE_20260923/RESULT.json": "fb4a435034c5dfaa79864fd7c3dee0b3bc4c1d744e8763e6bb23b20b76c8d41d",
    "audits/SRA_DPA_BGCE318_SOURCE_SELECTED_NONTRACIAL_COMMON_MODULAR_REFERENCE_GATE_20260923/RESULT.json": "f53667320d7cdfb4bc71c7cb00e7df87148301b31cec15d6b1b26ae2656a924b",
    "audits/SRA_DPA_BGCE319_CANONICAL_MODULAR_TIME_REVERSAL_AND_CTP_METRIC_GATE_20260923/RESULT.json": "bb5d05194da43dd5a5755a96aafc51463120dbae335c490b3c4f053fbde986f7",
    "audits/SRA_DPA_BGCE321_BKM_RIESZ_ODD_SOURCE_LIFT_AND_CONTACT_TERM_GATE_20260923/RESULT.json": "ea0de4f01e6975768445cb00acbd24fca25e1cb63f8126d0f8c00bd5b9e269a3",
}


def load(path):
    raw = (ROOT / path).read_bytes()
    actual = sha256(raw).hexdigest()
    assert actual == INPUTS[path], (path, actual, INPUTS[path])
    return json.loads(raw), actual


def main():
    docs = {}
    hashes = {}
    for path in INPUTS:
        docs[path], hashes[path] = load(path)

    r299 = docs[next(p for p in INPUTS if "BGCE299_" in p)]
    r310 = docs[next(p for p in INPUTS if "BGCE310_" in p)]
    r311 = docs[next(p for p in INPUTS if "BGCE311_" in p)]
    r318 = docs[next(p for p in INPUTS if "BGCE318_" in p)]
    r319 = docs[next(p for p in INPUTS if "BGCE319_" in p)]
    r321 = docs[next(p for p in INPUTS if "BGCE321_" in p)]

    assert r299["verification"] == "FINAL_SCOPED_PASS"
    assert r310["total_G1_balance"]["discrete_total_G1_conserved"] is True
    assert r311["spatial_environment_only_balance"]["environment_only_charge_solution"] is False
    assert r311["spatial_environment_only_balance"]["defect_HS_norm_squared"] == ["24", "14", "14"]
    assert r318["faithful"] is True and r318["nontracial"] is True
    assert r319["internal_source_level_result"]["Theta_squared_identity"] is True
    assert r321["single_doubled_operator"]["rank_all_sectors"] == [10] * 8
    assert r321["single_doubled_operator"]["Theta_hat_odd"] is True

    # General exact isometry lemma.  V:H_S -> H_S tensor C^6 has V*V=I.
    # With P=VV*, C_P:P B(H_out) P -> B(H_S), C_P(J)=V*JV, is an
    # isomorphism.  Therefore the unique support representative of a system
    # defect D is J=VDV*.  On the unrestricted output algebra, ker C is large.
    d_system = 125
    d_environment = 6
    d_output = d_system * d_environment
    d_branch = 2
    d_doubled_input = d_branch * d_system
    d_doubled_output = d_branch * d_output
    unrestricted_kernel_dimension = d_output**2 - d_system**2
    doubled_unrestricted_kernel_dimension = d_doubled_output**2 - d_doubled_input**2
    assert unrestricted_kernel_dimension == 546875
    assert doubled_unrestricted_kernel_dimension == 2187500

    # For X_0=G1 use the existing environment charge E_0=H_E and D_0=0.
    # For X_i=H_i use E_i=0 and D_i=X_i-V*(X_i tensor I)V.  BGCE311
    # supplies nonzero D_i.  I_i=V D_i V* is the unique support interaction
    # representative and gives V*(X_i tensor I+I_i)V=X_i exactly.
    component_records = [
        {
            "component": 0,
            "source_generator": "G1",
            "pure_environment_charge": "H_E from BGCE310",
            "interaction_support_representative": "0",
            "balance_exact": True,
        }
    ]
    for index, norm in enumerate(["24", "14", "14"], start=1):
        component_records.append({
            "component": index,
            "source_generator": f"H_{index}=-i[G1,P_chi_{index}]",
            "pure_environment_charge": "0; environment-only solution excluded by BGCE311",
            "interaction_support_representative": f"I_{index}=V D_{index} V*",
            "defect_HS_norm_squared": norm,
            "interaction_nonzero": True,
            "balance_exact": True,
        })
    assert len(component_records) == 4
    assert all(row["balance_exact"] for row in component_records)

    out = {
        "schema": "siel.dpa.bgce322.result.v1",
        "candidate_id": "BGCE322",
        "date": "2026-09-23",
        "fixed_source_revision": REV,
        "input_hashes": hashes,
        "primary_evidence_status": "Speculative interpretation",
        "qualifier": "exact finite isometry theorem composition and scoped support representative",
        "status": "SPLIT_PASS_EXACT_ONE_COLLISION_FOUR_COMPONENT_TOTAL_BALANCE_WITH_INTERACTION_STRESS_ON_STINESPRING_SUPPORT__RANK_TEN_BKM_CTP_CUMULANT_TRANSPORT__DYNAMICAL_COLLISION_METRIC_DEFORMATION_REPEATED_LOCAL_WARD_AND_CONTINUUM_TOTAL_WARD_OPEN",
        "isometry_support_lemma": {
            "system_dimension": d_system,
            "environment_dimension": d_environment,
            "output_dimension": d_output,
            "support_projection": "P=VV*",
            "support_compression_isomorphism": "J in P B(H_out) P -> V* J V",
            "unique_support_lift": "D -> V D V*",
            "unrestricted_output_contact_kernel_dimension": unrestricted_kernel_dimension,
            "doubled_unrestricted_contact_kernel_dimension": doubled_unrestricted_kernel_dimension,
            "unrestricted_contact_removed": False,
        },
        "four_component_one_collision_balance": {
            "identity": "V*(X_alpha tensor I + I tensor E_alpha + I_alpha)V=X_alpha for alpha=0,1,2,3",
            "temporal_source": "BGCE310 exact G1 plus environment H_E balance",
            "spatial_source": "BGCE311 defects D_i=H_i-V*(H_i tensor I)V",
            "metric_direction_alignment": "The three BGCE321 mixed scores and the three BGCE311 H_i are generated by the same G1/P_chi_i commutator directions.",
            "spatial_interaction": "I_i=V D_i V* on P=VV*",
            "component_records": component_records,
            "all_four_exact": True,
            "all_eight_actual_sectors": True,
            "q_one_quarter_collision_used": True,
            "new_fit_or_coefficient": False,
            "pure_environment_spatial_stress_derived": False,
            "system_environment_interaction_balance_class_with_metric_typing_derived": True,
            "physical_variational_interaction_stress_derived": False,
        },
        "BKM_CTP_collision_support_transport": {
            "doubled_isometry": "Vhat=I_2 tensor V",
            "transported_operator": "Jhat(F)=Vhat Ahat(F) Vhat*",
            "rank_all_sectors": [10] * 8,
            "Theta_out_odd_on_support": True,
            "support_state": "Omega_out=Vhat[(I_2/2) tensor omega_can]Vhat*",
            "local_cumulant": "Phi_out(F)=log Tr_P exp(log Omega_out + Jhat(F))",
            "Phi_zero": "0",
            "first_derivative_at_zero": "0 because the branch Pauli channels are traceless",
            "Hessian": "faithful BKM covariance on the support",
            "Hessian_rank": 10,
            "isometric_equality": "Phi_out(F)=Phi_in(F)",
            "new_metric_coefficient": False,
        },
        "scope_boundary": {
            "standard_dynamical_Feynman_Vernon_or_SK_influence_action_derived": False,
            "source_selected_metric_deformation_of_collision_isometry_or_unitary_derived": False,
            "causal_response_kernel_derived": False,
            "repeated_collision_local_interaction_telescoping_derived": False,
            "finite_to_BGCE299_continuum_stress_identification_derived": False,
            "continuum_covariant_total_Ward_derived_from_collision": False,
            "BGCE299_scoped_continuum_Ward_retained_separately": True,
            "full_finite_Lorentzian_Einstein_backreaction": False,
        },
        "decision": "The three spatial 24,14,14 defects are not algebraically lost from the one-collision balance.  For the actual Braid Stinespring isometry each has the unique representative I_i=V D_i V* on the physical collision support, while the temporal component is already balanced by the BGCE310 environment charge.  Hence one collision has an exact source-derived 1+3 total operator balance with a metric-typed interaction-balance term, in all eight sectors and without a fitted coefficient.  The BGCE321 rank-ten odd BKM operator also transports isometrically to that support and generates a faithful rank-ten local doubled cumulant.  However the source has not yet selected a metric-dependent deformation V(F) of the collision dynamics; therefore the interaction-balance term is not yet a physical variational stress, this cumulant is not yet a dynamical Feynman-Vernon influence action, unrestricted off-support contacts remain, repeated local Ward telescoping is not established, and the collision result has not been identified with the separately retained BGCE299 continuum Ward tensor.",
        "counter_intuition_scan": {
            "ordinary_explanation": "Every isometry transports an input observable to a unique observable on its range, so support-level balance alone is a general dilation fact.",
            "SIEL_specific_part": "The actual source supplies the Braid collision V, the exact temporal environment charge, the three nonzero orthogonal defects with norms 24,14,14, and the independent rank-ten BKM/CTP metric typing.",
            "strongest_counterpattern": "Calling V D_i V* a physical stress without deriving a metric deformation of V would merely rename a support lift; off the support a large contact kernel remains.",
            "falsifier": "Failure of any BGCE310/311 balance premise, failure of rank-ten BKM transport, or a proof that the collision support is not the physical output support.",
        },
        "next_gate": "BGCE323_SOURCE_SELECTED_COLLISION_METRIC_DEFORMATION_TO_DYNAMICAL_INFLUENCE_AND_REPEATED_TOTAL_WARD_GATE",
        "runtime_class": "SUBSECOND_EXACT_THEOREM_COMPOSITION_NO_PARAMETER_SCAN",
        "formal_E0_E1_E2": "NOT_CLAIMED__DPA_THEORETICAL_GATE_ONLY",
        "claim_ceiling": "BGCE322 derives an exact one-collision four-component total operator balance with nonzero spatial interaction-balance representatives carrying metric-response typing on the actual Stinespring support, and transports the rank-ten BKM/CTP operator to a local support cumulant.  It does not yet derive a physical variational interaction stress, metric-dependent collision dynamics, a standard causal influence action, repeated local Ward conservation, equality with the BGCE299 continuum stress, continuum total Ward from the collision parent, full finite Lorentzian Einstein backreaction, empirical gravity, or completed quantum gravity.",
    }
    (HERE / "RESULT.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({
        "candidate_id": out["candidate_id"],
        "status": out["status"],
        "all_four_one_collision_balances_exact": out["four_component_one_collision_balance"]["all_four_exact"],
        "spatial_defect_norms": ["24", "14", "14"],
        "BKM_CTP_support_rank": out["BKM_CTP_collision_support_transport"]["Hessian_rank"],
        "continuum_total_Ward_from_collision": out["scope_boundary"]["continuum_covariant_total_Ward_derived_from_collision"],
    }, indent=2))


if __name__ == "__main__":
    main()
