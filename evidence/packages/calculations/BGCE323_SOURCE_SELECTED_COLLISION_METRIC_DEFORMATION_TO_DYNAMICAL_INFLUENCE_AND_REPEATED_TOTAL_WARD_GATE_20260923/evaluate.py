#!/usr/bin/env python3
"""BGCE323: strong collision intertwiner and temporal-alignment gate."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
REV = "575c571946ba4006377ce51c9d89d49f0c5170b4"

PATHS = {
    "r310": ROOT / "records/BGCE310_TORSOR_GAUGE_COVARIANT_ENVIRONMENT_CHARGE_AND_TOTAL_G1_BALANCE_GATE_20260923/RESULT.json",
    "r311": ROOT / "records/BGCE311_FOUR_SOURCE_CHARGE_ENVIRONMENT_BALANCES_TO_DISCRETE_TOTAL_WARD_GATE_20260923/RESULT.json",
    "r319": ROOT / "records/BGCE319_CANONICAL_MODULAR_TIME_REVERSAL_AND_CTP_METRIC_GATE_20260923/RESULT.json",
    "r321": ROOT / "records/BGCE321_BKM_RIESZ_ODD_SOURCE_LIFT_AND_CONTACT_TERM_GATE_20260923/RESULT.json",
    "r322": ROOT / "records/BGCE322_COLLISION_SUPPORT_INTERACTION_STRESS_AND_FOUR_COMPONENT_BALANCE_GATE_20260923/RESULT.json",
    "o14": ROOT / "public-inputs/formal_checks/ocbfh014_source_native_refinement_naturality_check.py",
    "e141": ROOT / "records/BGCE141_SOURCE_MARK_CHARGE_CYLINDER_CURRENT_TO_DOUBLED_METRIC_STRESS_FUNCTOR_GATE_20260919/evaluate.py",
    "e319": ROOT / "records/BGCE319_CANONICAL_MODULAR_TIME_REVERSAL_AND_CTP_METRIC_GATE_20260923/evaluate.py",
    "e320": ROOT / "records/BGCE320_THETA_ODD_RESPONSE_TO_SOURCE_METRIC_TANGENT_INTERTWINER_GATE_20260923/evaluate.py",
    "ub476": ROOT / "records/UB476_BRAID_CASIMIR_SECTION_FREE_SAME_ENERGY_C5_BACKREACTION_GATE/evaluate.py",
    "ub443": ROOT / "records/UB443_TYPED_SIGNED_SURVIVOR_GAUGE_OR_OBSERVABLE_GATE/evaluate.py",
    "helper": ROOT / "records/BGCE108_SOURCE_PARENT_ACTION_SECTOR_IDEMPOTENT_GATE_20260919/evaluate.py",
}

EXPECTED = {
    "r310": "cf2c04a8f32f8f5a2ffb2d2ff0c95600de10e2d467e830a0d5da65452a2988f0",
    "r311": "fb4a435034c5dfaa79864fd7c3dee0b3bc4c1d744e8763e6bb23b20b76c8d41d",
    "r319": "bb5d05194da43dd5a5755a96aafc51463120dbae335c490b3c4f053fbde986f7",
    "r321": "ea0de4f01e6975768445cb00acbd24fca25e1cb63f8126d0f8c00bd5b9e269a3",
    "r322": "8ae1776515657371834bd52f0f7e35d9cdd723e36ebf5931d0b3705f8ca61754",
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
    spec = importlib.util.spec_from_file_location(f"bgce323_{name}", PATHS[name])
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[f"bgce323_{name}"] = module
    spec.loader.exec_module(module)
    return module


@dataclass(frozen=True)
class Q3:
    """a+b*sqrt(3), used only for exact scalar coefficients."""

    a: Fraction = Fraction(0)
    b: Fraction = Fraction(0)

    def __add__(self, other):
        if not isinstance(other, Q3):
            other = Q3(Fraction(other), Fraction(0))
        return Q3(self.a + other.a, self.b + other.b)

    def __mul__(self, other):
        if not isinstance(other, Q3):
            other = Q3(Fraction(other), Fraction(0))
        return Q3(
            self.a * other.a + 3 * self.b * other.b,
            self.a * other.b + self.b * other.a,
        )

    __rmul__ = __mul__


def exact_rank(matrix: list[list[Fraction]]) -> int:
    rows = [[Fraction(value) for value in row] for row in matrix]
    pivot_row = 0
    for column in range(len(rows[0])):
        pivot = next((r for r in range(pivot_row, len(rows)) if rows[r][column]), None)
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        value = rows[pivot_row][column]
        rows[pivot_row] = [x / value for x in rows[pivot_row]]
        for r in range(len(rows)):
            if r != pivot_row and rows[r][column]:
                factor = rows[r][column]
                rows[r] = [x - factor * y for x, y in zip(rows[r], rows[pivot_row])]
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return pivot_row


def temporal_residual_norm(g_num, group) -> Fraction:
    # Each scalar coefficient is sqrt(2)*(a+b sqrt(3)); products contribute
    # the explicit factor two below.  B_gh=sqrt(p_g p_h) H_E,gh.
    coefficients = {
        (0, 1): -2,
        (0, 2): 1,
        (0, 5): 1,
        (1, 3): 1,
        (1, 4): 1,
        (2, 3): 1,
        (2, 4): -2,
        (3, 5): -2,
        (4, 5): 1,
    }
    b_matrix = [[Fraction(0) for _ in range(6)] for _ in range(6)]
    for (i, j), value in coefficients.items():
        b_matrix[i][j] = b_matrix[j][i] = Fraction(value, 48)

    total = Q3()
    for g in range(6):
        commutator = group[g] @ g_num - g_num @ group[g]
        terms = [
            (Q3(Fraction(0), Fraction(1, 24)) if g == 0 else Q3(Fraction(1, 24)), commutator)
        ]
        for h in range(6):
            if not b_matrix[g][h]:
                continue
            coefficient = (
                Q3(Fraction(0), -Fraction(2, 3) * b_matrix[g][h])
                if g == 0
                else Q3(-2 * b_matrix[g][h])
            )
            terms.append((coefficient, group[h]))
        for left_coefficient, left in terms:
            for right_coefficient, right in terms:
                inner = int(np.sum(left * right))
                total = total + 2 * inner * left_coefficient * right_coefficient
    assert total.b == 0
    return total.a


def spatial_residual_norm(g_num, group, projector_num, projector_den) -> Fraction:
    lifted = np.kron(projector_num, np.eye(5, dtype=np.int64))
    commutator = g_num @ lifted - lifted @ g_num
    probabilities = [Fraction(3, 8)] + [Fraction(1, 8)] * 5
    denominator = 6 * projector_den
    total = Fraction(0)
    for probability, unitary in zip(probabilities, group):
        residual_num = unitary @ commutator - commutator @ unitary
        total += probability * int(np.sum(residual_num * residual_num)) / denominator**2
    return total


def main():
    r310 = load_json("r310")
    r311 = load_json("r311")
    r319 = load_json("r319")
    r321 = load_json("r321")
    r322 = load_json("r322")
    assert r310["total_G1_balance"]["discrete_total_G1_conserved"] is True
    assert r311["spatial_environment_only_balance"]["defect_HS_norm_squared"] == ["24", "14", "14"]
    assert r319["internal_source_level_result"]["antiunitary_time_reversal_involution"] is True
    assert r321["single_doubled_operator"]["rank_all_sectors"] == [10] * 8
    assert r322["four_component_one_collision_balance"]["all_four_exact"] is True

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
    input_hashes = {str(PATHS[name].relative_to(ROOT)): EXPECTED[name] for name in PATHS}
    records = []

    for survivor in survivors:
        g_num, g_den, r1, r2 = o14.source_g1(survivor["R"].astype(np.int64))
        assert g_den == 6
        group = [identity125, r1, r2, r1 @ r2, r2 @ r1, r1 @ r2 @ r1]

        residual_norms = [temporal_residual_norm(g_num, group)]
        residual_norms.extend(
            spatial_residual_norm(g_num, group, projector_num, projector_den)
            for projector_num, projector_den in projectors
        )
        assert residual_norms == [Fraction(12), Fraction(64), Fraction(112, 3), Fraction(112, 3)]

        defect_norms = [Fraction(0), Fraction(24), Fraction(14), Fraction(14)]
        minimal_interaction_norms = [2 * r - d for r, d in zip(residual_norms, defect_norms)]
        assert minimal_interaction_norms == [
            Fraction(24), Fraction(104), Fraction(182, 3), Fraction(182, 3)
        ]

        # Exact temporal alignment test.  If the charge score were the G1
        # score, invertibility of K_omega would make these two tangents
        # proportional.  Their exact Gram rank is instead two.
        h_real = []
        for projector_num, _ in projectors:
            lifted = np.kron(projector_num, identity5)
            h_real.append(g_num @ lifted - lifted @ g_num)
        ordinary = e319.signed_system([r1, r2] + h_real, [])
        components, dimension, _ = e319.decomposition(ordinary)
        assert dimension == 633
        pointed_num = np.kron(identity25 + survivor["P"].astype(np.int64), identity5)
        omega_num, _, _ = e319.project(
            ordinary, components, pointed_num, 150, 450, certify_rowspace=False
        )
        omega = (omega_num, 450)
        g1 = (g_num, g_den)
        g1_mean = ub476.trace_product(omega, g1)
        omega_g1 = ub476.normalize(omega_num @ g_num, 450 * g_den)
        g1_tangent = ub476.combine([
            (Fraction(1), omega_g1),
            (-g1_mean, omega),
        ])
        bundle = e141.build_metric_bundle(ub476, survivor, projectors)
        charge_tangent = e320.centered_charge_tangent(
            survivor, endpoint_j, bundle["state"], identity5, ub443, helper, ub476
        )
        alignment_gram = e320.operator_gram([charge_tangent, g1_tangent], ub476)
        alignment_rank = exact_rank(alignment_gram)
        assert alignment_rank == 2
        assert alignment_gram == [
            [Fraction(4, 375), Fraction(3217, 3796875)],
            [Fraction(3217, 3796875), Fraction(598699, 34171875)],
        ]

        records.append({
            "mask": survivor["mask"],
            "strong_residual_HS_norm_squared": [str(value) for value in residual_norms],
            "compressed_defect_HS_norm_squared": [str(value) for value in defect_norms],
            "minimal_strong_interaction_HS_norm_squared": [str(value) for value in minimal_interaction_norms],
            "charge_vs_G1_tangent_Gram": [[str(value) for value in row] for row in alignment_gram],
            "charge_vs_G1_tangent_rank": alignment_rank,
        })

    assert len(records) == 8
    common = [{k: v for k, v in row.items() if k != "mask"} for row in records]
    assert all(row == common[0] for row in common)

    d_system = 125
    d_output = 750
    complement_dimension = (d_output - d_system) ** 2
    doubled_complement_dimension = (2 * d_output - 2 * d_system) ** 2
    assert complement_dimension == 390625
    assert doubled_complement_dimension == 1562500

    out = {
        "schema": "siel.public-calculation.bgce323.result.v1",
        "candidate_id": "BGCE323",
        "date": "2026-09-23",
        "fixed_source_revision": REV,
        "input_hashes": input_hashes,
        "primary_evidence_status": "Speculative interpretation",
        "qualifier": "exact all-sector finite isometry theorem with temporal typing obstruction",
        "status": "SPLIT_PASS_EXACT_STRONG_ONE_COLLISION_FOUR_GENERATOR_INTERTWINER_AND_FINITE_NOETHER_COVARIANCE__SPATIAL_METRIC_DIRECTIONS_ALIGN__TEMPORAL_CHARGE_SCORE_INDEPENDENT_OF_G1__FULL_VARIATIONAL_STRESS_DYNAMICAL_INFLUENCE_LOCAL_REPEATED_WARD_AND_CONTINUUM_IDENTIFICATION_OPEN",
        "strong_intertwiner": {
            "input_generators": ["G1", "H1", "H2", "H3"],
            "bare_output_generator": "Y0_alpha=X_alpha tensor I + I tensor E_alpha",
            "residual": "R_alpha=V X_alpha-Y0_alpha V",
            "compressed_defect": "D_alpha=V*R_alpha",
            "minimal_Hermitian_interaction": "J_alpha=R_alpha V*+V R_alpha*-V D_alpha V*",
            "identity": "(Y0_alpha+J_alpha)V=V X_alpha",
            "Hermitian": True,
            "all_four_nonzero_strong_residuals": True,
            "all_eight_actual_sectors": True,
            "strong_residual_HS_norm_squared": ["12", "64", "112/3", "112/3"],
            "minimal_interaction_HS_norm_squared": ["24", "104", "182/3", "182/3"],
            "exponentiated_covariance": "exp(-it(Y0+J)) V = V exp(-itX) for every real t",
            "new_fit_or_coefficient": False,
            "q_one_quarter_collision_used": True,
        },
        "uniqueness_and_contact": {
            "selection": "unique Hermitian solution with zero complement-complement block, equivalently the minimum Hilbert-Schmidt/reachable-block representative",
            "general_solution": "J=J_min+C with C=C* and C V=0",
            "undetermined_complement_dimension": complement_dimension,
            "doubled_undetermined_complement_dimension": doubled_complement_dimension,
            "physical_intertwining_affected_by_C": False,
            "unrestricted_microscopic_contact_removed": False,
        },
        "metric_response_alignment": {
            "three_spatial_directions": "PASS: both use the same G1/P_chi_i commutators",
            "temporal_collision_generator": "G1",
            "temporal_BGCE321_score_source": "centered charge chemical-potential tangent",
            "charge_tangent_vs_omega_G1_tangent_rank_all_sectors": [2] * 8,
            "common_exact_Gram": [["4/375", "3217/3796875"], ["3217/3796875", "598699/34171875"]],
            "charge_score_proportional_to_G1_score": False,
            "full_one_plus_three_metric_Noether_identification": False,
        },
        "repeated_collision": {
            "global_n_step_support_covariance": "PASS_BY_ISOMETRY_COMPOSITION",
            "local_additive_interaction_telescoping": False,
            "reason": "The spatial J_i acts jointly on the continuing system and emitted block, so later collisions dress earlier interaction terms; it is not an emitted environment-only charge.",
        },
        "scope_boundary": {
            "strong_finite_one_collision_Ward_Noether_candidate": True,
            "physical_full_four_component_metric_variational_stress": False,
            "source_selected_full_ten_metric_collision_deformation": False,
            "standard_dynamical_Feynman_Vernon_or_SK_influence_action": False,
            "local_repeated_total_Ward": False,
            "finite_to_continuum_Hilbert_stress_identity": False,
            "continuum_total_Ward_from_collision_parent": False,
            "full_finite_Lorentzian_Einstein_backreaction": False,
        },
        "records": records,
        "decision": "The BGCE322 compression balance upgrades exactly to a strong one-collision intertwiner.  The unique reachable-block Hermitian completion J_alpha makes (Y0_alpha+J_alpha)V=V X_alpha and therefore exponentiates to a finite Noether covariance in all eight sectors without a fitted coefficient.  This is stronger than expectation or compression conservation.  The three spatial generators are the same G1/P_chi_i directions used by the BGCE321 mixed scores.  The remaining temporal direction does not align: the BGCE321 centered-charge tangent and the omega_can G1 tangent have exact rank two in every sector, so their BKM scores are independent.  Consequently the strong G1+H_i quartet cannot yet be identified with the full charge+mixed metric-response quartet.  Global repeated support transport follows by composition, but local additive interaction telescoping, a full metric-dependent collision deformation, a standard dynamical influence action, physical four-component variational stress, and collision-derived continuum total Ward remain open.",
        "counter_intuition_scan": {
            "ordinary_explanation": "A Hermitian strong completion can be built for any finite isometry once a generator is chosen; the formula is general dilation geometry.",
            "SIEL_specific_part": "The actual Braid source fixes V, G1, the three H_i, the exact residual norms, the common all-sector result, and the independent charge-plus-mixed BKM metric packet.",
            "strongest_counterpattern": "The temporal metric score is not the conserved G1 generator, and arbitrary complement-only operators remain invisible to the physical intertwining relation.",
            "falsifier": "Failure of the exact residual norms, non-Hermiticity or failure of the strong identity, or rank one rather than rank two for the charge/G1 tangent pair.",
        },
        "next_gate": "BGCE324_CENTERED_CHARGE_SCORE_TO_COLLISION_NOETHER_TIME_OR_MODULAR_ENERGY_GATE",
        "runtime_class": "SHORT_EXACT_ALL_SECTOR_LINEAR_ALGEBRA_NO_PARAMETER_SCAN",
        "formal_E0_E1_E2": "NOT_CLAIMED__PUBLIC_THEORETICAL_GATE_ONLY",
        "claim_ceiling": "BGCE323 derives an exact strong one-collision four-generator intertwiner and finite exponentiated Noether covariance, and proves a temporal typing obstruction between the conserved G1 direction and the BGCE321 centered-charge metric score.  It does not derive a full four-component physical variational stress, a full ten-component metric deformation of the collision, a standard causal influence action, local repeated Ward conservation, equality with continuum Hilbert stress, collision-derived continuum Einstein backreaction, empirical gravity, or completed quantum gravity.",
    }
    (HERE / "RESULT.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({
        "candidate_id": out["candidate_id"],
        "status": out["status"],
        "strong_residual_norms": out["strong_intertwiner"]["strong_residual_HS_norm_squared"],
        "minimal_interaction_norms": out["strong_intertwiner"]["minimal_interaction_HS_norm_squared"],
        "temporal_charge_G1_rank": out["metric_response_alignment"]["charge_tangent_vs_omega_G1_tangent_rank_all_sectors"],
        "full_metric_Noether_identification": out["metric_response_alignment"]["full_one_plus_three_metric_Noether_identification"],
    }, indent=2))


if __name__ == "__main__":
    main()
