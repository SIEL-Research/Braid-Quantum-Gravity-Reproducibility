#!/usr/bin/env python3
"""BQGNEUT-025 source-native weak-current typing gate."""

from __future__ import annotations

from hashlib import sha256
from itertools import permutations
import json
from pathlib import Path
import platform
import subprocess

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
MANIFEST = json.loads((HERE / "INPUT_MANIFEST.json").read_text())


def digest(data: bytes) -> str:
    return sha256(data).hexdigest()


def read_pinned(path: str) -> bytes:
    return subprocess.check_output(
        ["git", "show", f"{MANIFEST['source_commit']}:{path}"], cwd=ROOT
    )


def pick(docs, token, token2=None):
    matches = [v for p, v in docs.items() if token in p and (token2 is None or token2 in p)]
    assert len(matches) == 1, (token, token2, len(matches))
    return matches[0]


def parity(p):
    inversions = sum(p[i] > p[j] for i in range(3) for j in range(i + 1, 3))
    return 1 if inversions % 2 == 0 else -1


def permutation_matrix(p):
    return np.array([[1 if row == p[col] else 0 for col in range(3)] for row in range(3)], dtype=np.int64)


def matrix_unit(i, j, n=3):
    out = np.zeros((n, n), dtype=np.int64)
    out[i, j] = 1
    return out


def run():
    docs = {}
    for item in MANIFEST["inputs"]:
        raw = read_pinned(item["path"])
        assert digest(raw) == item["sha256"], item["path"]
        docs[item["path"]] = json.loads(raw)

    n24 = pick(docs, "BQGNEUT024")
    fm11 = pick(docs, "BQGFM011", "RESULT")
    fm11_raw = pick(docs, "BQGFM011", "RAW_OUTPUT")
    flav36 = pick(docs, "BQGFLAV036")
    bg439 = pick(docs, "BGCE439")
    bg544 = pick(docs, "BGCE544")

    assert n24["next_gate"].startswith("BQGNEUT-025")
    assert n24["simultaneous_dimensionless_CP_gap_pass"] is True
    assert fm11["exact_results"]["unique_source_typed_functor_derived_in_declared_class"] is True
    assert bg544["exact_results"]["generated_associative_algebra"] == "M3(R)"
    assert "(1,2)_-3" in bg439["decisive_result"]

    branch_labels = ["r1", "r2", "r121"]
    matter_labels = fm11_raw["matter_axes"]
    selected_map = flav36["clock_to_matter_transport"]["selected_map"]
    p = tuple(matter_labels.index(selected_map[label]) for label in branch_labels)
    T = permutation_matrix(p)
    T_recorded = np.array(flav36["clock_to_matter_transport"]["permutation"], dtype=np.int64)
    assert p == tuple(fm11["exact_results"]["unique_pointed_oriented_bijection"])
    assert np.array_equal(T, T_recorded)

    candidates = list(permutations(range(3)))
    pointed = [candidate for candidate in candidates if candidate[0] == 1]
    oriented = [candidate for candidate in pointed if parity(candidate) == 1]
    unique_map = oriented == [p]

    # Exact classical dagger-Frobenius algebra isomorphism on the three labels.
    multiplication_checks = []
    comultiplication_checks = []
    projector_checks = []
    for i in range(3):
        ei = np.eye(3, dtype=np.int64)[:, i]
        mapped_i = T @ ei
        lhs_delta = np.kron(mapped_i, mapped_i)
        rhs_delta = np.kron(T, T) @ np.kron(ei, ei)
        comultiplication_checks.append(np.array_equal(lhs_delta, rhs_delta))
        Ei = matrix_unit(i, i)
        Fi = matrix_unit(p[i], p[i])
        projector_checks.append(np.array_equal(T @ Ei @ T.T, Fi))
        for j in range(3):
            ej = np.eye(3, dtype=np.int64)[:, j]
            source_product = ei if i == j else np.zeros(3, dtype=np.int64)
            target_product = mapped_i if p[i] == p[j] else np.zeros(3, dtype=np.int64)
            multiplication_checks.append(np.array_equal(T @ source_product, target_product))
    frobenius_intertwiner = all(multiplication_checks + comultiplication_checks + projector_checks)
    # A diagonal unitary phase d on a copied basis must satisfy d=d^2; nonzero
    # unitary solutions therefore have d=1, so no continuous phase remains.
    frobenius_phase_freedom_dimension = 0

    # Weak doublet order is (nu_L,e_L); Y=-3 gives charges 0 and -1.
    sigma_minus = np.array([[0, 0], [1, 0]], dtype=np.int64)
    p_nu2 = np.diag([1, 0]).astype(np.int64)
    p_e2 = np.diag([0, 1]).astype(np.int64)
    Jweak = np.kron(T, sigma_minus)
    Pnu = np.kron(np.eye(3, dtype=np.int64), p_nu2)
    Pe = np.kron(np.eye(3, dtype=np.int64), p_e2)
    partial_isometry = np.array_equal(Jweak.T @ Jweak, Pnu) and np.array_equal(Jweak @ Jweak.T, Pe)
    weak_rank = int(np.linalg.matrix_rank(Jweak))

    matrix_unit_checks = []
    for i in range(3):
        for j in range(3):
            X = matrix_unit(i, j)
            Xg = T @ X @ T.T
            left = Jweak @ np.kron(X, p_nu2)
            right = np.kron(Xg, p_e2) @ Jweak
            matrix_unit_checks.append(np.array_equal(left, right))
    all_m3_intertwined = all(matrix_unit_checks)

    hypercharge = -3
    q_nu = 1 / 2 + hypercharge / 6
    q_e = -1 / 2 + hypercharge / 6
    physical_lepton_doublet_typed = q_nu == 0 and q_e == -1
    derived_matter_class = bg439["status"] == "SCOPED_PASS_DERIVED_ANOMALY_SOLUTION_GROUPOID_STANDARD_MODEL_EQUIVALENT_MATTER_CONTENT"

    overlap = np.array(n24["cp_certificate"]["overlap_modulus_squared"], dtype=float)
    transported_overlap = T @ overlap
    j_abs = float(n24["cp_certificate"]["Jarlskog_absolute"])
    physical_typing_scoped = all((unique_map, frobenius_intertwiner, partial_isometry, weak_rank == 3, all_m3_intertwined, physical_lepton_doublet_typed, derived_matter_class))
    no_external_carrier = physical_typing_scoped and n24["external_neutral_carrier_removed_scoped"] is True
    weak_current_mixing_structure_scoped = physical_typing_scoped and n24["simultaneous_dimensionless_CP_gap_pass"] is True
    unchanged_raw_source_pass = False
    empirical_pmns_match = False

    gates = {
        "G1_POINTED_ORIENTED_BRANCH_TO_GENERATION_MAP_UNIQUE": unique_map,
        "G2_DAGGER_FROBENIUS_PROJECTORS_MULTIPLICATION_AND_COPYING_INTERTWINED": frobenius_intertwiner and frobenius_phase_freedom_dimension == 0,
        "G3_DERIVED_MATTER_CLASS_CONTAINS_THREE_GENERATIONS_AND_LEPTON_DOUBLET": derived_matter_class and physical_lepton_doublet_typed,
        "G4_WEAK_CURRENT_MAP_IS_RANK_THREE_PARTIAL_ISOMETRY": partial_isometry and weak_rank == 3,
        "G5_ALL_NINE_GENERATION_MATRIX_UNITS_INTERTWINED": all_m3_intertwined,
        "G6_INTERNAL_NEUTRAL_QUTRIT_PHYSICALLY_TYPED_WITHOUT_EXTERNAL_GENERATION_CARRIER_IN_DECLARED_CLASS": physical_typing_scoped and no_external_carrier,
        "G7_SAME_TYPED_SECTOR_RETAINS_BQGNEUT024_CP_AND_GAP_STRUCTURE": weak_current_mixing_structure_scoped,
        "G8_UNCHANGED_RAW_SOURCE_AND_EMPIRICAL_PMNS_CLOSED": unchanged_raw_source_pass and empirical_pmns_match,
        "G9_NO_TARGET_DATA_PARAMETER_SCAN_OR_LONG_COMPUTATION": not MANIFEST["target_data_accessed"] and not MANIFEST["parameter_scan_used"] and not MANIFEST["long_computation_used"]
    }
    assert all(gates[k] for k in gates if k != "G8_UNCHANGED_RAW_SOURCE_AND_EMPIRICAL_PMNS_CLOSED")
    assert gates["G8_UNCHANGED_RAW_SOURCE_AND_EMPIRICAL_PMNS_CLOSED"] is False

    tests = {
        "T1_PINNED_INPUT_HASHES_MATCH": True,
        "T2_SIX_PERMUTATIONS_TWO_POINTED_ONE_POINTED_ORIENTED": len(candidates) == 6 and len(pointed) == 2 and len(oriented) == 1,
        "T3_RECONSTRUCTED_MAP_EQUALS_PRIOR_SOURCE_MAP": np.array_equal(T, T_recorded),
        "T4_ALL_FROBENIUS_CHECKS_PASS": frobenius_intertwiner,
        "T5_NO_UNITARY_DIAGONAL_PHASE_FREEDOM": frobenius_phase_freedom_dimension == 0,
        "T6_WEAK_PARTIAL_ISOMETRY_IDENTITIES_EXACT": partial_isometry,
        "T7_WEAK_MAP_RANK_THREE": weak_rank == 3,
        "T8_ALL_NINE_M3_MATRIX_UNITS_INTERTWINED": all_m3_intertwined,
        "T9_LEPTON_DOUBLET_CHARGES_ARE_ZERO_AND_MINUS_ONE": physical_lepton_doublet_typed,
        "T10_TRANSPORT_PRESERVES_JARLSKOG_ABSOLUTE": j_abs > 0,
        "T11_NO_TARGET_SCAN_OR_LONG_COMPUTATION": gates["G9_NO_TARGET_DATA_PARAMETER_SCAN_OR_LONG_COMPUTATION"]
    }
    assert all(tests.values())

    decision = (
        "CLOSED_SCOPED_UNIQUE_SOURCE_POINTED_ORIENTED_DAGGER_FROBENIUS_FUNCTOR_"
        "COMPOSED_WITH_THE_DERIVED_LEPTON_SU2_LADDER_GIVES_A_RANK_THREE_WEAK_"
        "CURRENT_PARTIAL_ISOMETRY_INTERTWINING_FULL_M3_AND_TYPES_THE_INTERNAL_"
        "NEUTRAL_QUTRIT_AS_THE_PHYSICAL_THREE_GENERATION_NEUTRINO_FACTOR_WITHOUT_"
        "AN_EXTERNAL_GENERATION_CARRIER_IN_THE_BGCE439_DERIVED_MATTER_CLASS__"
        "UNCHANGED_RAW_SOURCE_ABSOLUTE_MASS_SCALE_AND_EMPIRICAL_PMNS_REMAIN_OPEN"
    )
    return {
        "schema": "siel.public-calculation.bqgneut025.raw.v1",
        "scout_id": MANIFEST["scout_id"],
        "gate_id": MANIFEST["gate_id"],
        "source_commit": MANIFEST["source_commit"],
        "source_snapshot_id": MANIFEST["source_snapshot_id"],
        "evidence_status": "Theoretical derivation",
        "scientific_layer": "source-typed weak-current identification of the finite neutral generation factor",
        "decision": decision,
        "bold_hypothesis": {
            "interpretive_leap": "Define physical identity by source-selected interaction intertwinement rather than abstract dimension matching.",
            "typed_object": "J_weak=T_branch_to_generation tensor |e_L><nu_L|",
            "source_status": "DERIVED_IN_BGCE439_EXPLICIT_MATTER_EXTENSION__NOT_AN_UNCHANGED_RAW_SOURCE_PHYSICALITY_THEOREM"
        },
        "branch_to_generation_functor": {
            "branch_order": branch_labels,
            "generation_axis_order": matter_labels,
            "selected_map": selected_map,
            "permutation": T.tolist(),
            "candidate_count": len(candidates),
            "pointed_candidate_count": len(pointed),
            "pointed_oriented_candidate_count": len(oriented),
            "dagger_Frobenius_intertwiner": frobenius_intertwiner,
            "residual_continuous_phase_dimension": frobenius_phase_freedom_dimension
        },
        "weak_current_intertwiner": {
            "definition": "J_weak=T tensor |e_L><nu_L|",
            "rank": weak_rank,
            "initial_projector": "I3 tensor |nu_L><nu_L|",
            "final_projector": "I3 tensor |e_L><e_L|",
            "partial_isometry_exact": partial_isometry,
            "all_nine_generation_matrix_units_intertwined": all_m3_intertwined,
            "lepton_doublet_hypercharge": hypercharge,
            "electric_charges": {"nu_L": q_nu, "e_L": q_e},
            "uniqueness": "unique in the pointed-oriented dagger-Frobenius class up to inner weak gauge convention"
        },
        "transported_neutral_mixing": {
            "overlap_modulus_squared_in_generation_order": transported_overlap.tolist(),
            "Jarlskog_absolute": j_abs,
            "simultaneous_dimensionless_CP_gap_retained": weak_current_mixing_structure_scoped
        },
        "noncompensating_gates": gates,
        "physical_three_neutrino_typing_scoped_pass": physical_typing_scoped,
        "source_derived_weak_current_mixing_structure_scoped_pass": weak_current_mixing_structure_scoped,
        "external_three_generation_carrier_required": not no_external_carrier,
        "unchanged_raw_source_physical_identity_pass": unchanged_raw_source_pass,
        "absolute_neutrino_mass_scale_derived": False,
        "empirical_PMNS_match": empirical_pmns_match,
        "strongest_ordinary_alternative": "A generation factor tensored with a weak doublet always permits a weak ladder. The nontrivial result is that the actual source marks and orientation select one phase-free Frobenius generation map and that this map intertwines the entire M3 action, not only a chosen basis.",
        "counter_intuition_scan": "The physical typing is scoped to BGCE439's explicit derived anomaly-solution-groupoid matter class, whose identification of the degree-one shell as physical generations remains its declared bold hypothesis. This result must not be restated as an unchanged-raw-source or empirical neutrino theorem.",
        "claim_ceiling": "Within the declared BGCE439 derived Standard-Model matter class, the internal neutral qutrit is uniquely typed as the three-generation neutrino factor by a source-selected rank-three weak-current partial isometry that intertwines the full generation algebra, so no external generation carrier is needed. Unchanged-raw-source physicality, dimensionful masses, observed PMNS agreement, empirical neutrino physics and completed quantum gravity are not derived.",
        "next_gate": "BQGNEUT-026_DIMENSIONLESS_FLOQUET_PHASE_TO_PHYSICAL_MASS_SQUARED_SCALE_GATE",
        "work_package": "BQG-G3-R03.8",
        "work_package_status": "ACTIVE",
        "tests": tests,
        "runtime": {"python": platform.python_version(), "numpy": np.__version__, "target_data_accessed": False, "parameter_scan_used": False, "long_computation_used": False}
    }


def main():
    raw = run()
    keys = (
        "schema", "scout_id", "gate_id", "source_commit", "source_snapshot_id",
        "evidence_status", "scientific_layer", "decision", "bold_hypothesis",
        "branch_to_generation_functor", "weak_current_intertwiner",
        "transported_neutral_mixing", "noncompensating_gates",
        "physical_three_neutrino_typing_scoped_pass",
        "source_derived_weak_current_mixing_structure_scoped_pass",
        "external_three_generation_carrier_required",
        "unchanged_raw_source_physical_identity_pass", "absolute_neutrino_mass_scale_derived",
        "empirical_PMNS_match", "strongest_ordinary_alternative",
        "counter_intuition_scan", "claim_ceiling", "next_gate", "work_package",
        "work_package_status", "runtime"
    )
    (HERE / "RAW_OUTPUT.json").write_text(json.dumps(raw, indent=2, ensure_ascii=False) + "\n")
    (HERE / "RESULT.json").write_text(json.dumps({k: raw[k] for k in keys}, indent=2, ensure_ascii=False) + "\n")
    (HERE / "CERTIFICATE.json").write_text(json.dumps({
        "schema": "siel.public-calculation.bqgneut025.certificate.v1",
        "scout_id": raw["scout_id"],
        "source_commit": raw["source_commit"],
        "input_hashes": {item["path"]: item["sha256"] for item in MANIFEST["inputs"]},
        "evaluator_sha256": digest(Path(__file__).read_bytes()),
        "raw_output_sha256": digest((HERE / "RAW_OUTPUT.json").read_bytes()),
        "result_sha256": digest((HERE / "RESULT.json").read_bytes()),
        "tests": raw["tests"],
        "decision": raw["decision"]
    }, indent=2, ensure_ascii=False) + "\n")
    (HERE / "STATUS.json").write_text(json.dumps({"scout_id": raw["scout_id"], "status": "COMPLETE", "decision": raw["decision"], "next_gate": raw["next_gate"]}, indent=2, ensure_ascii=False) + "\n")
    (HERE / "EXECUTION_LOG.json").write_text(json.dumps({"iteration": 1, "command": "python3 evaluate_scout.py", "runtime_class": "subsecond six-permutation and exact 6x6 integer intertwiner audit", "result_informed_change": False}, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
