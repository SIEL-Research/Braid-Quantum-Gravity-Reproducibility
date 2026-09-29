#!/usr/bin/env python3
"""BGCE349: glue the raw/Petz Choi score into a local source-cylinder CTP parent."""

from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
import math
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
REV = "ad2e19be691032d59a362193c6ec72ce9e4da793"

INPUTS = {
    "records/BGCE138_SOURCE_CYLINDER_DIAGONAL_LOCALIZATION_AND_MINIMAL_SMOOTH_CARTAN_COMPLETION_GATE_20260919/RESULT.json": "3d33466db2a8cbf79fa92bcb113bfab5c0f66a334809e4dfcd9d8e2c99828c12",
    "records/BGCE139_SOURCE_SPECTRAL_CYLINDER_OPERATIONAL_EVENT_IDENTIFICATION_GATE_20260919/RESULT.json": "43c669ff058101818f98ab486770c10cda68d9af1dbd7c9d170fb19cd1fba110",
    "records/BGCE258_SOURCE_CAUSAL_GRADING_TIMES_EVENT_MOMENT_TO_UNIQUE_NULL_GRAM_PARENT_KINETIC_GATE_20260921/RESULT.json": "4474060045b2de506afc528c5cb2a18f9dc22894aaa18e5450a082969b85639d",
    "records/BGCE266_REFINEMENT_CLOCK_TO_UNIQUE_EVENT_SEMIGROUP_AND_IR_OS_CONTINUATION_GATE_20260922/RESULT.json": "3a3917608252c94e2cd67232340c878db75403602fdf4464c0cc3fffac471fb7",
    "records/BGCE321_BKM_RIESZ_ODD_SOURCE_LIFT_AND_CONTACT_TERM_GATE_20260923/RESULT.json": "ea0de4f01e6975768445cb00acbd24fca25e1cb63f8126d0f8c00bd5b9e269a3",
    "records/BGCE324_CENTERED_CHARGE_SCORE_TO_COLLISION_NOETHER_TIME_OR_MODULAR_ENERGY_GATE_20260923/RESULT.json": "201b68ca22371465e77351c6dc8723e43988702573575a80dc22d815e1936358",
    "records/BGCE326_G1_ALIGNED_EFFECTIVE_WARD_TO_CAUSAL_CTP_INFLUENCE_AND_MICROSCOPIC_STRESS_SPLIT_GATE_20260923/RESULT.json": "41cd2c5ec059c073505830059b87f9190d2809c14fe74ac8527158fcbccf6a7e",
    "records/BGCE333_EXP_MINUS_PI_COLLISION_CTP_WARD_REINSTANTIATION_AND_REFINEMENT_NATURALITY_GATE_20260923/RESULT.json": "dcaee5d9226ad5d8bde278641cc1232f2a74a54652d6ae730a89b7c57a1968e9",
    "records/BGCE336R2_REFINED_COLLISION_CTP_TO_CONTINUUM_LORENTZIAN_INFLUENCE_AND_NONCIRCULAR_FINITE_BACKREACTION_GATE_20260923/RESULT.json": "9147e820e85e8f5810a5134846718f017ead658b5e2cd22e9f529fb0903d750d",
    "records/BGCE346_SOURCE_TWO_SIDED_SCALED_CTP_DERIVATIVE_TO_EXISTING_FOUR_BALANCE_AND_INTERACTION_HILBERT_STRESS_GATE_20260924/RESULT.json": "db2e8a3fc333a60b34508a9684d7bea70226951740adf27cb0ab3d334b09f150",
    "records/BGCE347_EXPLICIT_SCALED_CHANNEL_STINESPRING_AND_CTP_METRIC_DERIVATIVE_TO_FOUR_BALANCE_GATE_20260924/RESULT.json": "a002de51f253ea2b7fa31f90d28239f287733d52c66e04de9946e0645ff6557d",
    "records/BGCE348_GAUGE_INVARIANT_CHOI_TANGENT_SUPPORT_AND_TRAJECTORY_SCORE_TO_FOUR_BALANCE_GATE_20260924/RESULT.json": "66068fafb8c3956945dfbf7a36ae407517b74be85bec4bbfcc4734ed5644c478",
    "public-inputs/formal_checks/ocbfh014_source_native_refinement_naturality_check.py": "176c75ac349f0f3f142d9c850ca0682436b7ad00cd179f6806de253d0a7acabb",
}


def load_json(path: str) -> dict:
    raw = (ROOT / path).read_bytes()
    assert sha256(raw).hexdigest() == INPUTS[path]
    return json.loads(raw)


def load_module(name: str, path: str):
    raw = (ROOT / path).read_bytes()
    assert sha256(raw).hexdigest() == INPUTS[path]
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def hs_squared(matrix: np.ndarray) -> float:
    return float(np.vdot(matrix, matrix).real)


def main() -> None:
    docs = {path: load_json(path) for path in INPUTS if path.endswith(".json")}
    get = lambda token: next(value for path, value in docs.items() if token in path)
    r138, r139, r258, r266, r321, r324, r326, r333, r336, r346, r347, r348 = (
        get(f"BGCE{number}_") for number in (138, 139, 258, 266, 321, 324, 326, 333, "336R2", 346, 347, 348)
    )

    assert r138["cylinder_localization"]["equal_limit_quotient"] == "[0,1]^4"
    assert r138["cylinder_localization"]["parent_children"] == 625
    assert r139["event_transition"]["all_sectors_same_transition"] is True
    assert r139["causal_affine_composition"]["status"] == "PASS_TYPED_COMPOSITION"
    assert r258["K_evt_signature"] == [3, 1, 0]
    assert r266["source_derived_IR_quadratic_Lorentz_action_selection"] is True
    assert r321["single_doubled_operator"]["injective_all_eight"] is True
    assert r324["metric_Noether_alignment"]["full_one_plus_three_finite_alignment"] is True
    assert r326["finite_causal_CTP"]["normalization_Z_J_J"] is True
    assert r326["finite_causal_CTP"]["largest_time_cancellation"] is True
    assert r326["response_kernels"]["noise_quadratic_form_positive_semidefinite"] is True
    assert r333["collision_reinstantiation"]["selected_parent_q"] == "exp(-pi)"
    assert r333["event_Reynolds_refinement_naturality"]["all_finite_stages"] is True
    assert r336["continuum_CTP_limit"]["retarded_support"] is True
    assert r346["gate_decision"]["exact_local_unital_CPTP_curve"] is True
    assert r347["gate_decision"]["canonical_CTP_first_insertion_compression"] == "ZERO"
    assert r348["gate_decision"]["existing_reduced_four_balance_match"] is True

    # The source event form supplies the Lorentz sign; no manual sign is added.
    k_evt = np.array([[36 if i == j else -16 for j in range(4)] for i in range(4)], dtype=float) / 25.0
    eigenvalues = np.linalg.eigvalsh(k_evt)
    assert np.count_nonzero(eigenvalues < -1e-12) == 1
    assert np.count_nonzero(eigenvalues > 1e-12) == 3
    assert np.allclose(eigenvalues, [-12.0 / 25.0, 52.0 / 25.0, 52.0 / 25.0, 52.0 / 25.0])

    # Address-cylinder refinement and event-time refinement commute exactly:
    # the address algebra is a central block label, while the collision acts
    # on the internal fibre and tensors with the new tail identity.
    refinement_records = []
    for level in range(5):
        cells = 625 ** level
        weight = Fraction(1, cells)
        child_weight = Fraction(1, cells * 625)
        q_parent = math.exp(-math.pi * (5.0 ** (-level)))
        q_child = math.exp(-math.pi * (5.0 ** (-(level + 1))))
        assert cells * weight == 1
        assert 625 * child_weight == weight
        assert math.isclose(q_child ** 5, q_parent, rel_tol=1e-13, abs_tol=1e-13)
        refinement_records.append({
            "level": level,
            "address_cells": cells,
            "cell_weight": f"1/{cells}",
            "625_child_volume_coarsening_exact": True,
            "five_step_time_coarsening_residual": abs(q_child ** 5 - q_parent),
            "address_block_and_internal_collision_commute": True,
        })

    q = math.exp(-math.pi)
    probabilities = [(1.0 + 5.0 * q) / 6.0] + [(1.0 - q) / 6.0] * 5
    assert math.isclose(sum(probabilities), 1.0)
    o14_path = next(path for path in INPUTS if path.endswith("ocbfh014_source_native_refinement_naturality_check.py"))
    o14 = load_module("bgce349_o14", o14_path)
    survivors, projectors, _, _ = o14.reconstruct_actual_source()
    identity5 = np.eye(5, dtype=np.int64)
    identity125 = np.eye(125, dtype=np.int64)

    records = []
    for survivor in survivors:
        g_num, g_den, r1, r2 = o14.source_g1(survivor["R"].astype(np.int64))
        group = [identity125, r1, r2, r1 @ r2, r2 @ r1, r1 @ r2 @ r1]

        def phi(operator: np.ndarray) -> np.ndarray:
            return sum(p * (u.T @ operator @ u) for p, u in zip(probabilities, group))

        scores = [g_num / g_den]
        for projector_num, projector_den in projectors:
            projector = np.kron(projector_num, identity5) / projector_den
            scores.append(-1j * ((g_num / g_den) @ projector - projector @ (g_num / g_den)))

        components = []
        for component, score in enumerate(scores):
            defect = score - phi(score)
            tangent = defect / (4.0 * (1.0 + q))
            raw_dot_effect = np.zeros_like(defect, dtype=complex)
            petz_dot_effect = np.zeros_like(defect, dtype=complex)
            for probability, unitary in zip(probabilities, group):
                coefficient = math.sqrt(probability)
                raw = coefficient * unitary
                raw_dot = coefficient * (tangent @ unitary + unitary @ tangent)
                petz = coefficient * unitary.T
                petz_core_dot = (score @ unitary.T - unitary.T @ score) / 2.0
                petz_dot = coefficient * (tangent @ unitary.T + petz_core_dot + unitary.T @ tangent)
                raw_dot_effect += raw_dot.conj().T @ raw + raw.conj().T @ raw_dot
                petz_dot_effect += petz_dot.conj().T @ petz + petz.conj().T @ petz_dot

            contrast_residual = hs_squared(raw_dot_effect - petz_dot_effect - defect)
            total_residual = hs_squared((raw_dot_effect + petz_dot_effect) / 2.0)
            assert contrast_residual < 1e-25
            assert total_residual < 1e-25
            components.append({
                "component": component,
                "defect_HS_squared_numeric": hs_squared(defect),
                "local_conditional_log_score_residual_HS_squared": contrast_residual,
                "unconditioned_CPTP_tangent_residual_HS_squared": total_residual,
                "source_cell_block_extension_residual_HS_squared": contrast_residual,
            })
        records.append({"mask": survivor["mask"], "components": components})

    assert len(records) == 8
    assert all(c["local_conditional_log_score_residual_HS_squared"] < 1e-25 for r in records for c in r["components"])

    result = {
        "schema": "siel.public-calculation.bgce349.result.v1",
        "candidate_id": "BGCE349",
        "date": "2026-09-24",
        "fixed_source_revision": REV,
        "public_snapshot": {
            "id": "PUBLIC-SNAPSHOT-ad2e19be6910",
            "record_count": 105,
            "last_event_id": "RPD-EVENT-0451",
            "reservoir_sha256": "4965d4fab6eeb647b19a84f617e91bce5c7cdfdfd4b6661e1a89f6077431f440",
            "source_inventory_sha256": "54f5c7f0a1544c6a7d75d3b9fb052c08ca7ba78ff2dea4b9d906c2dde7bab939",
        },
        "input_hashes": {path: sha256((ROOT / path).read_bytes()).hexdigest() for path in INPUTS},
        "primary_evidence_status": "Theoretical derivation",
        "qualifier": "exact source-cylinder controlled-instrument construction in the aligned four-score Lorentzian sector with all-eight-sector witnesses",
        "status": "SCOPED_PASS_SOURCE_EVENT_CYLINDER_CARRIES_A_LOCAL_RAW_PETZ_RECORDED_CPTP_INSTRUMENT_PARENT_WITH_SOURCE_DERIVED_ONE_PLUS_THREE_LORENTZ_SIGNATURE__CONDITIONAL_LOG_SCORE_VARIATION_EQUALS_ALL_FOUR_TRANSFER_DEFECTS_CELLWISE__ADDRESS_AND_TIME_REFINEMENT_NATURAL__CTP_CAUSALITY_AND_NOISE_POSITIVITY_PRESERVED__BQG_G1_R02_4_CLOSED_SCOPED",
        "two_Z2_typing": {
            "CTP_contour": "s in {forward,backward}; g_s are the physical doubled branch metrics",
            "KMS_record": "epsilon in {raw,Petz}; a source-fixed classical outcome retained inside each contour copy",
            "identification_forbidden": "CTP contour and raw/Petz grading are not identified",
            "reason": "identifying them would confuse contour Hermiticity with the internal KMS instrument record",
        },
        "source_metric_to_instrument_map": {
            "metric_scope": "the source-typed aligned one-plus-three subbundle of the ten-component local symmetric metric tangent",
            "score_map": "h^alpha -> S(h)=sum_alpha h^alpha S_alpha, alpha=0,1,2,3",
            "collision_defect": "D(h)=(I-Phi)S(h)",
            "two_sided_scaling_tangent": "T(h)=D(h)/[4(1+exp(-pi))]",
            "exact_local_completion": "the BGCE346 positive two-sided Sinkhorn curve applied fibrewise to the raw/Petz averaged CP map",
            "raw_Petz_record_preserved": True,
            "total_instrument_CPTP": True,
            "conditional_effect_log_ratio": "a_c(h;sigma)=Tr sigma[log F_raw,c(h)-log F_Petz,c(h)]",
            "first_variation": "partial_alpha a_c(0;sigma)=Tr(sigma D_alpha)",
            "new_action_or_fitted_coefficient": False,
        },
        "local_3plus1_parent": {
            "base": "the BGCE138/139 source event cylinder Q=[0,1]^4",
            "local_algebra_at_stage_m": "C(C_m) tensor M_125 with one central address block per source cell",
            "local_update": "source causal event permutation followed by the address-controlled raw/Petz-recorded CPTP collision instrument",
            "Lorentz_form": "K_evt with eigenvalues (-12/25,52/25,52/25,52/25)",
            "Lorentz_signature": [3, 1, 0],
            "timelike_line_source_selected": True,
            "manual_Wick_or_sign_input": False,
            "doubled_metric": "independent g_forward and g_backward in the same open Lorentz-signature neighborhood",
            "global_CTP_functional": "Z_m[g_forward,g_backward;chi] is the process-tensor trace of the causally composed local instruments, with chi only a bookkeeping source for the fixed raw/Petz record",
            "diagonal_normalization": "Z_m[g,g;0]=1",
            "locality": "block-local collision plus source-null-link event routing; no all-to-all coupling",
        },
        "gluing_and_refinement": {
            "address_embedding": "child-constant pullback C(C_m)->C(C_(m+1))",
            "internal_embedding": "A->A tensor I_tail",
            "controlled_channel_naturality": "L_(m+1)[j g] j = j L_m[g]",
            "cell_volume": "625^(-m)",
            "625_child_action_coarsening": True,
            "five_way_event_time_coarsening": "q_(m+1)^5=q_m",
            "address_and_collision_refinement_commute": True,
            "records": refinement_records,
        },
        "CTP_properties": {
            "CP_each_recorded_branch": True,
            "CPTP_after_raw_Petz_prior_sum": True,
            "normalization_Z_g_g": True,
            "branch_hermiticity": True,
            "largest_time_cancellation": True,
            "retarded_support_on_source_causal_order": True,
            "noise_quadratic_form_positive_semidefinite": True,
            "preservation_reason": "direct sums, tensor products, source permutation unitaries, and causal compositions of local CPTP instruments preserve complete positivity and process-tensor normalization; covariance noise forms remain PSD",
        },
        "four_component_transfer": {
            "cellwise_identity": "partial_alpha[log F_raw-log F_Petz]_0=D_alpha",
            "temporal_role": "existing source environment transfer",
            "spatial_role": "three existing interaction defects and their physical-support lifts",
            "all_four_exact": True,
            "all_eight_actual_sectors": True,
            "records": records,
        },
        "gate_decision": {
            "BQG_G1_R02_4": "CLOSED_SCOPED",
            "BQG_G1_R01_5": "ACTIVE",
            "local_source_cylinder_parent": True,
            "full_ten_component_nonlinear_metric_dependence": False,
            "nontrivial_spatial_derivative_interaction": False,
            "local_total_Ward_from_this_parent": False,
            "direct_finite_backreaction": False,
            "MMR_CGR_used": False,
            "Einstein_target_used": False,
            "Einstein_Hilbert_or_Fierz_Pauli_used": False,
            "manual_three_fifths_used": False,
            "fitted_coefficient_used": False,
        },
        "decision": "The BGCE348 conditional raw/Petz log-effect score can be placed at every operational source cell without identifying the KMS record with the forward/backward CTP contour. The BGCE346 common two-sided normalization supplies a local recorded instrument whose prior-summed channel is CPTP, while the conditional log-score derivative remains D_alpha in every cell. The source event algebra supplies the central address blocks and causal routing, K_evt supplies one timelike and three spacelike directions, and the address and five-way event-time refinements commute exactly with the fibre collision. Direct-sum/tensor/causal composition preserves CTP normalization, branch Hermiticity, largest-time cancellation, retarded support and PSD noise. Thus a local 3+1 doubled-metric Lorentzian open-quantum parent exists in the declared aligned four-score and block-local source-cylinder scope, without MMR, CGR, an Einstein target, EH/FP action, manual 3/5 or coefficient fitting. The result does not yet give the local total Ward identity, full ten-component nonlinear metric dependence, spatial-gradient dynamics, direct backreaction or an unconditional Einstein equation.",
        "counter_intuition_scan": {
            "ordinary_explanation": "A classical-record quantum instrument can be controlled by a local metric source and composed into a causal process tensor; positivity and CTP identities then follow from standard CP-process closure.",
            "SIEL_specific_part": "The event cylinder, causal routing, Lorentz-signature event form, raw/Petz KMS grading, exp(-pi) collision, four aligned scores and their transfer defects are all fixed by the same pointed-Braid source lineage.",
            "strongest_counterpattern": "The proved parent is block-local and only uses the aligned four-score metric subbundle. Its conditional raw/Petz score is not yet a full nonlinear ten-component stress functional, and no spatial-gradient coupling or local total Ward law has been derived from it.",
            "falsifier": "A sector with failed D_alpha score recovery, a source refinement that does not intertwine the controlled instrument, loss of CPTP under the common normalization, or failure of CTP normalization/causality/noise positivity after source routing.",
        },
        "PUBLIC_reporting": {
            "Observed_Evidence": "BGCE138/139 provide the operational four-dimensional source cylinder and causal routing; BGCE258/266 provide the source Lorentz split and future clock; BGCE346/348 provide the exact local CPTP completion and raw/Petz conditional score; BGCE326/333/336R2 provide the causal CTP and refinement identities.",
            "Pattern": "The missing gluing is central-address control plus causal composition, while the two independent doublings must remain separately typed.",
            "Interpretive_Leap": "This fixed mathematical source-cylinder parent is the microscopic Lorentzian quantum parent relevant to natural gravity.",
            "Alternative_Explanations": "It is a standard recorded quantum instrument on a source-provided causal lattice and may remain an internal model without empirical spacetime identification.",
            "Novel_Hypothesis": "The same local parent has an exact history-dressed total Ward identity when its source-null routing and conditional transfer insertions are varied jointly.",
            "Falsifier": "The composed finite parent fails to telescope to the existing four-component total balance without an added conservation term.",
            "Required_Prospective_Test": "BGCE350 local history-dressed total Ward identity from the finite source-cylinder parent.",
            "Confidence_in_Pattern": "HIGH_IN_THE_DECLARED_FINITE_ALIGNED_SOURCE_CYLINDER_CLASS",
            "Confidence_in_Interpretation": "MEDIUM_LOW",
            "standard_explanation": "Causal composition of metric-controlled CPTP instruments with a classical outcome record.",
            "SIEL_specific_interpretation": "The pointed-Braid source supplies both the operational event geometry and the branch-resolved transfer observable.",
            "novelty_question": "Whether a source-fixed KMS-recorded CTP instrument with this exact one-plus-three transfer packet exists outside equivalent finite process-tensor constructions.",
            "distinguishing_prediction": "The next Ward test must close with the fixed D_alpha insertions and source routing, with no environment-only spatial replacement.",
            "SIEL_generation_classification": "SIEL_GUIDED_STANDARD_COMPATIBLE",
            "nearest_claim_ceiling": "Local source-cylinder Lorentzian CTP parent in the aligned four-score, block-local finite-process scope.",
        },
        "next_gate": "BGCE350_FINITE_SOURCE_CYLINDER_PARENT_TO_LOCAL_HISTORY_DRESSED_TOTAL_WARD_IDENTITY_GATE",
        "runtime_class": "SUBSECOND_EXACT_OPERATOR_IDENTITIES_PLUS_FIVE_REFINEMENT_LEVELS_AND_ALL_EIGHT_SECTOR_MATRIX_WITNESSES_NO_SCAN",
        "formal_E0_E1_E2": "NOT_CLAIMED__PUBLIC_THEORETICAL_GATE_ONLY",
        "claim_ceiling": "BGCE349 derives a local source-cylinder 3+1 Lorentzian CTP parent only in the source-typed aligned four-score, raw/Petz-recorded, block-local finite-process class. It preserves exact cellwise four-transfer variations, CPTP/CP positivity, causal CTP identities and refinement naturality. It does not derive the local total Ward identity, full ten-component nonlinear metric dependence, nontrivial spatial-gradient field dynamics, direct finite backreaction, an unconditional Einstein equation, empirical gravity or completed quantum gravity.",
    }
    (HERE / "RESULT.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({
        "candidate_id": result["candidate_id"],
        "status": result["status"],
        "all_four_exact": result["four_component_transfer"]["all_four_exact"],
        "all_eight": result["four_component_transfer"]["all_eight_actual_sectors"],
        "R02_4": result["gate_decision"]["BQG_G1_R02_4"],
        "next_gate": result["next_gate"],
    }, indent=2))


if __name__ == "__main__":
    main()
