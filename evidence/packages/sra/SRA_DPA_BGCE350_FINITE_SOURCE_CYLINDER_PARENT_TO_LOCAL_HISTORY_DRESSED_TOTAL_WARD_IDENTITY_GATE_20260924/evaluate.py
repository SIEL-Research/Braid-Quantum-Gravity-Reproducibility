#!/usr/bin/env python3
"""BGCE350: local history-dressed Ward identity from the BGCE349 parent."""

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
REV = "dfdb0494b841e4c85f0caff145a9e5acb4ec27ed"

INPUTS = {
    "audits/SRA_DPA_BGCE310_TORSOR_GAUGE_COVARIANT_ENVIRONMENT_CHARGE_AND_TOTAL_G1_BALANCE_GATE_20260923/RESULT.json": "cf2c04a8f32f8f5a2ffb2d2ff0c95600de10e2d467e830a0d5da65452a2988f0",
    "audits/SRA_DPA_BGCE311_FOUR_SOURCE_CHARGE_ENVIRONMENT_BALANCES_TO_DISCRETE_TOTAL_WARD_GATE_20260923/RESULT.json": "fb4a435034c5dfaa79864fd7c3dee0b3bc4c1d744e8763e6bb23b20b76c8d41d",
    "audits/SRA_DPA_BGCE322_COLLISION_SUPPORT_INTERACTION_STRESS_AND_FOUR_COMPONENT_BALANCE_GATE_20260923/RESULT.json": "8ae1776515657371834bd52f0f7e35d9cdd723e36ebf5931d0b3705f8ca61754",
    "audits/SRA_DPA_BGCE323_SOURCE_SELECTED_COLLISION_METRIC_DEFORMATION_TO_DYNAMICAL_INFLUENCE_AND_REPEATED_TOTAL_WARD_GATE_20260923/RESULT.json": "7b7585a2fdddf35046a8098d137ecba54996a9258e7b4f67d848c22bc7925aaf",
    "audits/SRA_DPA_BGCE325_G1_ALIGNED_STRONG_CTP_GENERATOR_TO_REPEATED_LOCAL_WARD_AND_CONTINUUM_STRESS_IDENTIFICATION_GATE_20260923/RESULT.json": "cec850cff6f08ec3bc980f87d89e3c4dfcf5ed6730ed56eb48895d8a8479cbd2",
    "audits/SRA_DPA_BGCE333_EXP_MINUS_PI_COLLISION_CTP_WARD_REINSTANTIATION_AND_REFINEMENT_NATURALITY_GATE_20260923/RESULT.json": "dcaee5d9226ad5d8bde278641cc1232f2a74a54652d6ae730a89b7c57a1968e9",
    "audits/SRA_DPA_BGCE336R2_REFINED_COLLISION_CTP_TO_CONTINUUM_LORENTZIAN_INFLUENCE_AND_NONCIRCULAR_FINITE_BACKREACTION_GATE_20260923/RESULT.json": "c1ddd9d8451cfe68dae8a134706fbf589375fe3e35da665a8e4cbb70f3519875",
    "audits/SRA_DPA_BGCE348_GAUGE_INVARIANT_CHOI_TANGENT_SUPPORT_AND_TRAJECTORY_SCORE_TO_FOUR_BALANCE_GATE_20260924/RESULT.json": "66068fafb8c3956945dfbf7a36ae407517b74be85bec4bbfcc4734ed5644c478",
    "audits/SRA_DPA_BGCE349_BRANCH_RESOLVED_CHOI_TRANSFER_TO_LOCAL_3PLUS1_DOUBLED_METRIC_LORENTZIAN_PARENT_GATE_20260924/RESULT.json": "2385486c5c3f8016d64e831e72859b55371cd542468333b8b928536c2d56de65",
    "projects/active/discovery_partner/formal_checks/ocbfh014_source_native_refinement_naturality_check.py": "176c75ac349f0f3f142d9c850ca0682436b7ad00cd179f6806de253d0a7acabb",
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
    r310, r311, r322, r323, r325, r333, r336, r348, r349 = (
        get(f"BGCE{number}_") for number in (310, 311, 322, 323, 325, 333, "336R2", 348, 349)
    )

    assert r310["total_G1_balance"]["discrete_total_G1_conserved"] is True
    assert r311["spatial_environment_only_balance"]["environment_only_charge_solution"] is False
    assert r322["four_component_one_collision_balance"]["all_four_exact"] is True
    assert r323["strong_intertwiner"]["all_eight_actual_sectors"] is True
    assert r323["repeated_collision"]["global_n_step_support_covariance"] == "PASS_BY_ISOMETRY_COMPOSITION"
    assert r323["repeated_collision"]["local_additive_interaction_telescoping"] is False
    assert r325["strict_repeated_collision_gate"]["strict_local_additive_four_component_Ward"] is False
    assert r325["strict_repeated_collision_gate"]["global_n_step_history_dressed_covariance"] is True
    assert r333["balance_and_strong_intertwiner"]["all_refinement_stages"] is True
    assert r336["continuum_total_balance_density"]["reduced_four_component_balance_density_finite"] is True
    assert r348["gate_decision"]["existing_reduced_four_balance_match"] is True
    assert r349["gate_decision"]["BQG_G1_R02_4"] == "CLOSED_SCOPED"
    assert r349["gluing_and_refinement"]["address_and_collision_refinement_commute"] is True

    q = math.exp(-math.pi)
    probabilities = [(1.0 + 5.0 * q) / 6.0] + [(1.0 - q) / 6.0] * 5
    o14_path = next(path for path in INPUTS if path.endswith("ocbfh014_source_native_refinement_naturality_check.py"))
    o14 = load_module("bgce350_o14", o14_path)
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
            # For Phi=E+qQ, D=(I-Phi)S belongs to Q and Phi(D)=qD.
            eigen_residual = hs_squared(phi(defect) - q * defect)
            assert eigen_residual < 1e-24

            histories = []
            running = np.zeros_like(defect, dtype=complex)
            propagated = defect.copy()
            for steps in range(1, 6):
                running += propagated
                endpoint = score.copy()
                for _ in range(steps):
                    endpoint = phi(endpoint)
                telescoping_residual = hs_squared(running - (score - endpoint))
                closed_formula_residual = hs_squared(running - ((1.0 - q**steps) / (1.0 - q)) * defect)
                assert telescoping_residual < 1e-23
                assert closed_formula_residual < 1e-23
                histories.append({
                    "steps": steps,
                    "history_dressed_telescoping_residual_HS_squared": telescoping_residual,
                    "closed_geometric_formula_residual_HS_squared": closed_formula_residual,
                })
                propagated = phi(propagated)

            components.append({
                "component": component,
                "Phi_D_equals_q_D_residual_HS_squared": eigen_residual,
                "histories": histories,
            })
        records.append({"mask": survivor["mask"], "components": components})

    assert len(records) == 8

    refinement_records = []
    for level in range(6):
        h_parent = 5.0 ** (-level)
        h_child = h_parent / 5.0
        q_parent = math.exp(-math.pi * h_parent)
        q_child = math.exp(-math.pi * h_child)
        temporal_residual = abs((1.0 - q_parent) - sum(q_child**k * (1.0 - q_child) for k in range(5)))
        address_parent = Fraction(1, 625**level)
        address_child = Fraction(1, 625 ** (level + 1))
        assert temporal_residual < 1e-14
        assert 625 * address_child == address_parent
        refinement_records.append({
            "level": level,
            "five_child_history_dressed_transfer_residual": temporal_residual,
            "625_child_address_measure_exact": True,
            "local_vertex_Ward_refinement_natural": True,
        })

    result = {
        "schema": "siel.dpa.bgce350.result.v1",
        "candidate_id": "BGCE350",
        "date": "2026-09-24",
        "fixed_source_revision": REV,
        "dpa_snapshot": {
            "id": "DPA-SNAPSHOT-dfdb0494b841",
            "record_count": 105,
            "last_event_id": "RPD-EVENT-0451",
            "reservoir_sha256": "7adc9570fdf2e0ee9020045c475350882d5d61b0d5ae8b879d90dcd4f807eaac",
            "source_inventory_sha256": "d7313547ad937300f375bc5ced5070be83deb43aaf98046c5d87f887795c9352",
        },
        "input_hashes": {path: sha256((ROOT / path).read_bytes()).hexdigest() for path in INPUTS},
        "primary_evidence_status": "Theoretical derivation",
        "qualifier": "exact strong-vertex and reduced telescoping Ward identity with all-eight-sector and refinement witnesses",
        "status": "SCOPED_PASS_BGCE349_FINITE_PARENT_HAS_AN_EXACT_LOCAL_STRONG_VERTEX_WARD_AND_CAUSAL_HISTORY_DRESSED_REDUCED_TOTAL_WARD__STRICT_EMITTED_BLOCK_ADDITIVE_SPATIAL_CURRENT_NO_GO_RETAINED__FIVE_WAY_TIME_AND_625_CHILD_ADDRESS_REFINEMENT_NATURAL__WEAK_CONTINUUM_WARD_IN_REFINEMENT_COMPATIBLE_ALIGNED_CLASS__BQG_G1_R01_5_CLOSED_SCOPED",
        "local_strong_vertex_Ward": {
            "input_generator": "X_alpha in {G1,H1,H2,H3}",
            "bare_output": "Y0_alpha=X_alpha tensor I+I tensor E_alpha",
            "interaction": "J_alpha=R_alpha V*+V R_alpha*-V D_alpha V*",
            "identity": "(Y0_alpha+J_alpha)V=V X_alpha",
            "physical_support_compression": "V*J_alpha V=D_alpha",
            "metric_variation_identity": "BGCE349 conditional log-score derivative=D_alpha",
            "same_interaction_stress": True,
            "new_conservation_term_added": False,
        },
        "history_dressed_total_Ward": {
            "reduced_one_step": "D_alpha=(I-Phi)S_alpha",
            "history_current": "I_alpha^(k)=Phi^k(D_alpha)",
            "n_step_identity": "sum_(k=0)^(n-1) Phi^k(D_alpha)=S_alpha-Phi^n(S_alpha)",
            "Reynolds_closed_form": "Phi^k(D_alpha)=q^k D_alpha and sum=[(1-q^n)/(1-q)]D_alpha",
            "operator_level_origin": "future collisions dress each local J_alpha insertion; strong isometry composition gives the same endpoint identity on the reachable support",
            "strict_fresh_block_additive_current": False,
            "why_history_dressing_is_required": "spatial J_i acts on the continuing system and emitted block and is transformed by later collisions",
            "all_four_components": True,
            "all_eight_actual_sectors": True,
            "records": records,
        },
        "locality_and_refinement": {
            "source_causal_path_local": True,
            "future_dependence": "only descendants in the source causal order, not spacelike unrelated cells",
            "five_way_time_refinement": "sum_(r=0)^4 q_child^r(1-q_child)=1-q_parent",
            "625_child_address_refinement": "625 child volumes sum exactly to one parent volume",
            "address_and_time_refinement_commute": True,
            "records": refinement_records,
        },
        "continuum_boundary": {
            "mesh": "h_m=5^(-m)",
            "q_h": "exp(-gamma h)",
            "local_transfer_density": "D_alpha(h)/h -> gamma Q S_alpha",
            "weak_refinement_compatible_Ward": "the exact finite-stage telescoping identity descends against child-constant compactly supported cylinder test fields; interior terms cancel and only causal-boundary flux remains",
            "effective_on_shell_Ward_consistent_with_BGCE325": True,
            "arbitrary_smooth_diffeomorphism_Ward_derived": False,
            "full_ten_component_Ward_derived": False,
        },
        "gate_decision": {
            "BQG_G1_R01_5": "CLOSED_SCOPED",
            "BQG_G1": "CLOSED_SCOPED_IN_ALIGNED_BLOCK_LOCAL_PARENT_AND_WARD_CLASS",
            "BQG_G2_R01_1": "ACTIVE",
            "strict_environment_only_spatial_Ward": False,
            "history_dressed_local_total_Ward": True,
            "MMR_CGR_used": False,
            "Einstein_target_used": False,
            "Einstein_Hilbert_or_Fierz_Pauli_used": False,
            "manual_three_fifths_used": False,
            "fitted_coefficient_used": False,
            "direct_finite_backreaction": False,
        },
        "decision": "The BGCE349 parent has an exact local total Ward identity when the interaction current is typed correctly. At each source vertex the BGCE323 strong intertwiner equates the incoming generator with the bare outgoing plus interaction generator, and BGCE349 identifies the same support compression D_alpha as the local metric derivative. Later collisions dress the interaction insertion. On the reduced algebra this gives the exact causal telescoping identity sum Phi^k(D_alpha)=S_alpha-Phi^n(S_alpha), with Phi^k(D_alpha)=q^kD_alpha for the source Reynolds channel. The identity is local along causal descendants, holds for all four components and all eight sectors, and is natural under five-way event-time and 625-child address refinement. The strict emitted-block-only spatial current remains excluded, so no prior NO-GO is reversed. The exact finite-stage identity yields a weak continuum Ward law only for refinement-compatible aligned cylinder test fields. It does not establish arbitrary smooth diffeomorphism Ward, full ten-component metric response, or direct backreaction.",
        "counter_intuition_scan": {
            "ordinary_explanation": "For any Markov channel, D=(I-Phi)S is a coboundary and its propagated sum telescopes. Strong Stinespring intertwining is a standard dilation form of the same conservation identity.",
            "SIEL_specific_part": "The four scores, their interaction defects, raw/Petz metric variation, source causal routing, exp(-pi) Reynolds channel and refinement system are fixed by the pointed-Braid lineage.",
            "strongest_counterpattern": "The Ward identity is history-dressed and aligned-class scoped. It is not an emitted-bath additive current and does not by itself yield a metric equation of motion or prove general spacetime diffeomorphism invariance.",
            "falsifier": "Any sector/component failing the coboundary telescope, a refinement stage with unequal parent and five-child transfer, failure of the strong vertex identity, or a metric derivative different from D_alpha.",
        },
        "DPA_reporting": {
            "Observed_Evidence": "BGCE323 supplies exact strong vertex covariance and composed support covariance; BGCE325 proves strict emitted-block spatial additivity impossible; BGCE348/349 identify D_alpha as the local metric variation inside a local causal parent.",
            "Pattern": "The conserved local object is a causal coboundary with history-dressed interaction current, not a sum of autonomous emitted-block charges.",
            "Interpretive_Leap": "This finite aligned-class Ward identity is the microscopic conservation law of physical gravity.",
            "Alternative_Explanations": "It is the standard telescoping identity of a Markov channel, instantiated by the Braid source but not yet empirically distinguished.",
            "Novel_Hypothesis": "Varying the same finite parent jointly in its source Lorentz geometry and recorded collision instrument yields a noncircular finite geometry-matter backreaction equation.",
            "Falsifier": "The geometry variation remains kinematically independent of the collision state/current or requires inserting a target Einstein tensor or free coupling.",
            "Required_Prospective_Test": "BGCE351 direct finite noncircular backreaction from the completed aligned source-cylinder parent.",
            "Confidence_in_Pattern": "VERY_HIGH_IN_THE_DECLARED_FINITE_REYNOLDS_AND_REFINEMENT_CLASS",
            "Confidence_in_Interpretation": "MEDIUM_LOW",
            "standard_explanation": "Markov coboundary telescoping and strong Stinespring covariance.",
            "SIEL_specific_interpretation": "The source-derived operational geometry and collision transfer share one exact local conservation complex.",
            "novelty_question": "Whether the combined source geometry/instrument variation forces a coupled equation not equivalent to a generic controlled Markov process.",
            "distinguishing_prediction": "A valid next equation must follow from the finite parent variation with no MMR/CGR, Einstein target, EH/FP action, manual 3/5 or fitted coefficient.",
            "SIEL_generation_classification": "SIEL_GUIDED_STANDARD_COMPATIBLE",
            "nearest_claim_ceiling": "Local history-dressed total Ward identity in the aligned block-local source-cylinder parent class.",
        },
        "next_gate": "BGCE351_COMPLETED_FINITE_SOURCE_CYLINDER_PARENT_TO_DIRECT_NONCIRCULAR_BACKREACTION_GATE",
        "runtime_class": "SUBSECOND_EXACT_COBBOUNDARY_IDENTITIES_PLUS_FIVE_STEP_HISTORY_AND_SIX_REFINEMENT_LEVELS_ALL_EIGHT_SECTORS_NO_SCAN",
        "formal_E0_E1_E2": "NOT_CLAIMED__DPA_THEORETICAL_GATE_ONLY",
        "claim_ceiling": "BGCE350 derives an exact local strong-vertex and history-dressed reduced total Ward identity only in the BGCE349 aligned four-score, block-local source-cylinder parent class. It retains the NO-GO for strict emitted-block-only spatial additivity and yields only a refinement-compatible weak continuum Ward statement. It does not derive arbitrary smooth diffeomorphism Ward, full ten-component nonlinear metric dynamics, direct finite backreaction, an unconditional Einstein equation, empirical gravity or completed quantum gravity.",
    }
    (HERE / "RESULT.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({
        "candidate_id": result["candidate_id"],
        "status": result["status"],
        "all_four": result["history_dressed_total_Ward"]["all_four_components"],
        "all_eight": result["history_dressed_total_Ward"]["all_eight_actual_sectors"],
        "R01_5": result["gate_decision"]["BQG_G1_R01_5"],
        "next_gate": result["next_gate"],
    }, indent=2))


if __name__ == "__main__":
    main()
