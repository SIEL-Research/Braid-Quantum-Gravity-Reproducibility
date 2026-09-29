#!/usr/bin/env python3
"""BGCE324: centered-charge no-go and conserved-G1 BKM replacement gate."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
REV = "02701a2dd739790e573c31a71f68c0e235fe7b12"

PATHS = {
    "r318": ROOT / "records/BGCE318_SOURCE_SELECTED_NONTRACIAL_COMMON_MODULAR_REFERENCE_GATE_20260923/RESULT.json",
    "r321": ROOT / "records/BGCE321_BKM_RIESZ_ODD_SOURCE_LIFT_AND_CONTACT_TERM_GATE_20260923/RESULT.json",
    "r323": ROOT / "records/BGCE323_SOURCE_SELECTED_COLLISION_METRIC_DEFORMATION_TO_DYNAMICAL_INFLUENCE_AND_REPEATED_TOTAL_WARD_GATE_20260923/RESULT.json",
    "o14": ROOT / "public-inputs/formal_checks/ocbfh014_source_native_refinement_naturality_check.py",
    "e141": ROOT / "records/BGCE141_SOURCE_MARK_CHARGE_CYLINDER_CURRENT_TO_DOUBLED_METRIC_STRESS_FUNCTOR_GATE_20260919/evaluate.py",
    "e319": ROOT / "records/BGCE319_CANONICAL_MODULAR_TIME_REVERSAL_AND_CTP_METRIC_GATE_20260923/evaluate.py",
    "e320": ROOT / "records/BGCE320_THETA_ODD_RESPONSE_TO_SOURCE_METRIC_TANGENT_INTERTWINER_GATE_20260923/evaluate.py",
    "ub476": ROOT / "records/UB476_BRAID_CASIMIR_SECTION_FREE_SAME_ENERGY_C5_BACKREACTION_GATE/evaluate.py",
    "ub443": ROOT / "records/UB443_TYPED_SIGNED_SURVIVOR_GAUGE_OR_OBSERVABLE_GATE/evaluate.py",
    "helper": ROOT / "records/BGCE108_SOURCE_PARENT_ACTION_SECTOR_IDEMPOTENT_GATE_20260919/evaluate.py",
}

EXPECTED = {
    "r318": "f53667320d7cdfb4bc71c7cb00e7df87148301b31cec15d6b1b26ae2656a924b",
    "r321": "ea0de4f01e6975768445cb00acbd24fca25e1cb63f8126d0f8c00bd5b9e269a3",
    "r323": "7b7585a2fdddf35046a8098d137ecba54996a9258e7b4f67d848c22bc7925aaf",
    "o14": "176c75ac349f0f3f142d9c850ca0682436b7ad00cd179f6806de253d0a7acabb",
    "e141": "be872bba4a2b6da1ed0aeb20a443714d6984086c5d5ae8f584e0dad4a12da3c1",
    "e319": "0be77a8650115667ae14be1c07adb168449372924d02ca6fe3131a10cb30c3e3",
    "e320": "433abba77f16fe239a07034bb390bb3808ce013aef0f03e95f6d06314efa805e",
    "ub476": "1a97f11de4a3024a4839fc99f54574ca148ac59c7026bb24bb16ba8e6e5f2ad6",
    "ub443": "ad53908146ba65d9de71994c0b297fac759a05c4938378f6cc962bbf9eae8c9e",
    "helper": "cdaabce1dd356cd67505463baff2d9963c1dc598aa888982d046ae93910f3ea7",
}


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def load_json(name: str) -> dict:
    assert digest(PATHS[name]) == EXPECTED[name]
    return json.loads(PATHS[name].read_text())


def load_module(name: str):
    assert digest(PATHS[name]) == EXPECTED[name]
    module_name = f"bgce324_{name}"
    spec = importlib.util.spec_from_file_location(module_name, PATHS[name])
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def main():
    r318 = load_json("r318")
    r321 = load_json("r321")
    r323 = load_json("r323")
    assert r318["faithful"] is True and r318["commutes_with_all_Hi"] is True
    assert r321["single_doubled_operator"]["rank_all_sectors"] == [10] * 8
    assert r323["strong_intertwiner"]["all_eight_actual_sectors"] is True
    assert r323["metric_response_alignment"]["charge_score_proportional_to_G1_score"] is False

    o14 = load_module("o14")
    e141 = load_module("e141")
    e319 = load_module("e319")
    e320 = load_module("e320")
    ub476 = load_module("ub476")
    ub443 = load_module("ub443")
    helper = load_module("helper")

    survivors, projectors, _, _ = o14.reconstruct_actual_source()
    _, endpoint_j = ub443.build_survivors()
    identity5 = np.eye(5, dtype=np.int64)
    identity25 = np.eye(25, dtype=np.int64)
    identity125 = np.eye(125, dtype=np.int64)
    records = []

    for survivor in survivors:
        g_num, g_den, r1, r2 = o14.source_g1(survivor["R"].astype(np.int64))
        assert g_den == 6
        group = [identity125, r1, r2, r1 @ r2, r2 @ r1, r1 @ r2 @ r1]
        h_real = []
        for projector_num, _ in projectors:
            lifted = np.kron(projector_num, identity5)
            h_real.append(g_num @ lifted - lifted @ g_num)

        ordinary = e319.signed_system([r1, r2] + h_real, [])
        ordinary_components, ordinary_dimension, _ = e319.decomposition(ordinary)
        assert ordinary_dimension == 633
        pointed_num = np.kron(identity25 + survivor["P"].astype(np.int64), identity5)
        omega_num, _, _ = e319.project(
            ordinary,
            ordinary_components,
            pointed_num,
            150,
            450,
            certify_rowspace=False,
        )
        omega = (omega_num, 450)
        assert np.array_equal(omega_num @ g_num, g_num @ omega_num)

        bundle = e141.build_metric_bundle(ub476, survivor, projectors)
        state = bundle["state"]
        charge_tangent = e320.centered_charge_tangent(
            survivor, endpoint_j, state, identity5, ub443, helper, ub476
        )

        # A commutator tangent of the pointed projector state has zero support
        # and kernel diagonal blocks.  The charge tangent has both nonzero.
        support_num = state[0]
        support_den = 2
        complement_num = 2 * identity125 - support_num
        pp_num = support_num @ charge_tangent[0] @ support_num
        qq_num = complement_num @ charge_tangent[0] @ complement_num
        block_den = support_den * support_den * charge_tangent[1]
        pp_norm = Fraction(int(np.sum(pp_num * pp_num)), block_den**2)
        qq_norm = Fraction(int(np.sum(qq_num * qq_num)), block_den**2)
        assert (pp_norm, qq_norm) == (Fraction(67, 400), Fraction(217, 6000))

        # Nonzero commutator with omega excludes the modular centralizer and
        # therefore any score that is a function of modular energy alone.
        comm_num = charge_tangent[0] @ omega_num - omega_num @ charge_tangent[0]
        comm_den = charge_tangent[1] * 450
        comm_norm = Fraction(int(np.sum(comm_num * comm_num)), comm_den**2)
        assert comm_norm == Fraction(13129, 28476562500)

        # The actual q=1/4 collision channel does not fix the charge tangent.
        defect_num = 5 * charge_tangent[0] - sum(
            (u @ charge_tangent[0] @ u.T for u in group[1:]),
            start=np.zeros_like(charge_tangent[0]),
        )
        defect_den = 8 * charge_tangent[1]
        defect_num, defect_den = ub476.normalize(defect_num, defect_den)
        collision_defect_norm = Fraction(int(np.sum(defect_num * defect_num)), defect_den**2)
        assert collision_defect_norm == Fraction(313, 250000)

        # Conserved-energy replacement.  Since [omega,G1]=0,
        # K_omega(G1-<G1>)=omega(G1-<G1>) exactly.
        g1 = (g_num, g_den)
        g1_mean = ub476.trace_product(omega, g1)
        omega_g1 = ub476.normalize(omega_num @ g_num, 450 * g_den)
        g1_tangent = ub476.combine([
            (Fraction(1), omega_g1),
            (-g1_mean, omega),
        ])

        twisted = e319.signed_system([r1, r2], h_real)
        twisted_components, twisted_dimension, _ = e319.decomposition(twisted)
        assert twisted_dimension == 633
        seed_num, _, _ = e319.project(
            twisted,
            twisted_components,
            identity125,
            1,
            9,
            certify_rowspace=False,
        )
        v_num = 117 * seed_num - seed_num @ seed_num @ seed_num
        v_den = 324
        assert np.array_equal(v_num @ g_num @ v_num, v_den**2 * g_num)

        metric = [
            bundle["transformed"][row][column]
            for row in range(4)
            for column in range(row, 4)
        ]
        odd = [e320.theta_split(item, v_num, v_den, ub476)[0] for item in metric]
        odd_gram = e320.operator_gram(odd, ub476)
        mixed_response = [
            [ub476.trace_product(tangent, functional) for tangent in bundle["mixed_tangents"]]
            for functional in metric
        ]
        g1_response = [[ub476.trace_product(g1_tangent, functional)] for functional in metric]
        four_response = [mixed_response[index] + g1_response[index] for index in range(10)]
        response_rank = e320.exact_rank(four_response)
        odd_plus_mixed_rank = e320.exact_rank(e320.add_response_gram(odd_gram, mixed_response))
        full_rank = e320.exact_rank(
            e320.add_response_gram(
                e320.add_response_gram(odd_gram, mixed_response),
                g1_response,
            )
        )
        assert (response_rank, odd_plus_mixed_rank, full_rank) == (4, 9, 10)

        records.append({
            "mask": survivor["mask"],
            "charge_unitary_support_block_HS_norm_squared": str(pp_norm),
            "charge_unitary_kernel_block_HS_norm_squared": str(qq_norm),
            "charge_omega_commutator_HS_norm_squared": str(comm_norm),
            "charge_collision_defect_HS_norm_squared": str(collision_defect_norm),
            "Theta_G1_Theta_inverse_equals_G1": True,
            "mixed_plus_G1_response_rank": response_rank,
            "odd_plus_mixed_rank": odd_plus_mixed_rank,
            "odd_plus_mixed_plus_G1_rank": full_rank,
        })

    assert len(records) == 8
    common = [{k: v for k, v in row.items() if k != "mask"} for row in records]
    assert all(row == common[0] for row in common)

    input_hashes = {str(PATHS[name].relative_to(ROOT)): EXPECTED[name] for name in PATHS}
    out = {
        "schema": "siel.public-calculation.bgce324.result.v1",
        "candidate_id": "BGCE324",
        "date": "2026-09-23",
        "fixed_source_revision": REV,
        "input_hashes": input_hashes,
        "primary_evidence_status": "Speculative interpretation",
        "qualifier": "exact all-sector no-go plus coefficient-free conserved-score replacement",
        "status": "SCOPED_FULL_PASS_G1_BKM_SCORE_REPLACES_CENTERED_CHARGE__FOUR_RESPONSE_RANK_FOUR_AND_SINGLE_CTP_RANK_TEN_ALL_EIGHT__EXACT_ALIGNMENT_WITH_STRONG_CONSERVED_QUARTET__CENTERED_CHARGE_NOETHER_AND_MODULAR_TIME_ROUTES_NO_GO__LOCAL_REPEATED_AND_CONTINUUM_WARD_OPEN",
        "centered_charge_gate": {
            "unitary_Noether_orbit": False,
            "reason_unitary": "Both diagonal blocks relative to the pointed-state support are nonzero; a commutator tangent has zero diagonal blocks.",
            "support_block_HS_norm_squared": "67/400",
            "kernel_block_HS_norm_squared": "217/6000",
            "modular_centralizer_energy": False,
            "omega_commutator_HS_norm_squared": "13129/28476562500",
            "fixed_by_actual_q_one_quarter_collision": False,
            "collision_defect_HS_norm_squared": "313/250000",
            "all_eight_actual_sectors": True,
        },
        "G1_replacement": {
            "tangent": "delta_0 omega=omega_can(G1-Tr(omega_can G1)I)",
            "BKM_score": "S_0=G1-Tr(omega_can G1)I",
            "why_exact": "omega_can commutes with G1, so K_omega(S_0)=omega_can S_0",
            "Theta_even": True,
            "mixed_plus_G1_response_rank_all_sectors": [4] * 8,
            "Theta_odd_plus_mixed_rank_all_sectors": [9] * 8,
            "full_single_CTP_rank_all_sectors": [10] * 8,
            "minimal_four_score_contact_kernel_dimension_all_sectors": [0] * 8,
            "centered_charge_required_for_rank_ten": False,
            "A55_used": False,
            "centered_charge_three_fifths_used": False,
            "new_fit_or_coefficient": False,
        },
        "metric_Noether_alignment": {
            "metric_score_quartet": ["centered G1", "mixed H1", "mixed H2", "mixed H3"],
            "strong_conserved_quartet": ["G1", "H1", "H2", "H3"],
            "identity_shift_physical_effect": "none on commutators or normalized BKM response",
            "full_one_plus_three_finite_alignment": True,
            "BGCE323_strong_one_collision_intertwiner_reused": True,
            "finite_four_component_metric_Noether_candidate": True,
        },
        "CTP_update": {
            "definition": "Ahat_G1(F)=tau_z tensor P_minus(F)+tau_x tensor S_minus(R_G1(F))+tau_y tensor S_plus(R_G1(F))",
            "rank": 10,
            "Theta_hat_odd": True,
            "BKM_cumulant_exists_on_collision_support": True,
            "standard_dynamical_Feynman_Vernon_or_SK_action_derived": False,
        },
        "MMR_and_three_fifths_effect": {
            "finite_metric_Ward_packet_uses_centered_charge": False,
            "finite_metric_Ward_packet_uses_three_fifths": False,
            "MMR2_relative_gravity_matter_action_routing_removed": False,
            "unconditional_Einstein_relative_three_fifths_derived": False,
        },
        "scope_boundary": {
            "local_additive_repeated_collision_Ward": False,
            "finite_interaction_to_BGCE299_continuum_stress_identity": False,
            "continuum_covariant_total_Ward_from_collision_parent": False,
            "standard_causal_influence_action": False,
            "full_finite_Lorentzian_Einstein_backreaction": False,
        },
        "records": records,
        "decision": "The centered-charge score cannot itself be the collision Noether time or a modular-centralizer energy: its pointed-state support and kernel diagonal blocks are nonzero, it does not commute with omega_can, and it is not fixed by the actual q=1/4 collision channel.  The obstruction is bypassed without a new law.  Replacing the charge tangent by delta_0 omega=omega_can(G1-<G1>) gives the exact BKM score G1-<G1>, which is Theta-even and aligned with the BGCE323 conserved temporal generator.  Together with the three existing mixed directions, the response matrix has rank four and the single CTP packet has rank ten in every sector; the minimal four-score contact kernel remains zero.  Thus the finite 1+3 metric-response quartet and strong conserved quartet now coincide up to the irrelevant identity shift.  The centered charge and its three-fifths are no longer needed for this finite metric-Ward chain.  Local repeated interaction Ward, a standard dynamical influence action, identification with the BGCE299 continuum Hilbert stress, continuum total Ward from the collision parent, and MMR2 action routing remain open.",
        "counter_intuition_scan": {
            "ordinary_explanation": "For a faithful stationary state, a conserved observable commuting with the state supplies its own BKM exponential-family score; replacing a nonconserved chemical-potential direction by that energy score is standard information geometry.",
            "SIEL_specific_part": "The actual Braid source fixes omega_can, G1, the three H_i, Theta, the rank-ten metric functionals, and the strong collision intertwiner, and the replacement passes identically in all eight sectors without fitting.",
            "strongest_counterpattern": "This is still a fixed finite model.  Rank-ten response plus a four-generator Noether identity does not by itself prove a causal continuum stress tensor or Einstein dynamics.",
            "falsifier": "Any sector with mixed-plus-G1 response rank below four, full packet rank below ten, nonzero Theta-odd failure for G1, or a nonzero minimal four-score kernel.",
        },
        "next_gate": "BGCE325_G1_ALIGNED_STRONG_CTP_GENERATOR_TO_REPEATED_LOCAL_WARD_AND_CONTINUUM_STRESS_IDENTIFICATION_GATE",
        "runtime_class": "SHORT_EXACT_ALL_SECTOR_LINEAR_ALGEBRA_NO_PARAMETER_SCAN",
        "formal_E0_E1_E2": "NOT_CLAIMED__PUBLIC_THEORETICAL_GATE_ONLY",
        "claim_ceiling": "BGCE324 derives a coefficient-free replacement of the centered-charge score by the conserved centered-G1 BKM score, preserving rank-four source response, rank-ten single-CTP response, zero minimal contact kernel, and exact alignment with the BGCE323 strong conserved quartet in all eight finite sectors.  It does not derive local repeated Ward conservation, a standard causal influence action, equality with continuum Hilbert stress, collision-derived continuum Einstein backreaction, MMR2 removal, empirical gravity, or completed quantum gravity.",
    }
    (HERE / "RESULT.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({
        "candidate_id": out["candidate_id"],
        "status": out["status"],
        "charge_Noether_time": out["centered_charge_gate"]["unitary_Noether_orbit"],
        "G1_response_ranks": out["G1_replacement"]["mixed_plus_G1_response_rank_all_sectors"],
        "full_CTP_ranks": out["G1_replacement"]["full_single_CTP_rank_all_sectors"],
        "finite_one_plus_three_alignment": out["metric_Noether_alignment"]["full_one_plus_three_finite_alignment"],
    }, indent=2))


if __name__ == "__main__":
    main()
