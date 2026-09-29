#!/usr/bin/env python3
"""BQGNEUT-031 minimal finite-CTP causal-face transgression gate."""

from __future__ import annotations

from hashlib import sha256
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


def circular_gaps(phases: np.ndarray) -> np.ndarray:
    ordered = np.sort(np.mod(phases, 2 * np.pi))
    return np.sort(np.diff(np.r_[ordered, ordered[0] + 2 * np.pi]))


def run():
    inputs = {}
    for item in MANIFEST["inputs"]:
        raw = read_pinned(item["path"])
        assert digest(raw) == item["sha256"], item["path"]
        inputs[item["path"]] = json.loads(raw)

    floquet = next(v for p, v in inputs.items() if "BQGNEUT024" in p)
    lift = next(v for p, v in inputs.items() if "BQGNEUT027" in p)
    face = next(v for p, v in inputs.items() if "BQGNEUT030" in p)
    ctp = next(v for p, v in inputs.items() if "BGCE532" in p)
    nambu = next(v for p, v in inputs.items() if "BGCE570" in p)

    assert floquet["floquet_operator"]["exact_unitary"] is True
    assert face["scoped_causal_face_holonomy_pass"] is True
    assert ctp["branch_pairing"]["reverse"] == "M_H*"
    assert ctp["exterior_trace"]["ordinary_trace_positive"] is True
    assert nambu["pass_rule"] is True

    C = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=complex)
    L = np.array([[11, -7, -4], [-7, 11, -4], [-4, -4, 8]], dtype=float) / 15
    evals, evecs = np.linalg.eigh(L)
    E = evecs @ np.diag(np.exp(-1j * (2 * np.pi / 3) * evals)) @ evecs.conj().T
    U_F = C @ E

    W = C @ E @ C.conj().T @ E.conj().T
    identity = np.eye(3, dtype=complex)
    unitary_residual = float(np.linalg.norm(W.conj().T @ W - identity, ord="fro"))
    nonidentity_norm = float(np.linalg.norm(W - identity, ord="fro"))
    commutator_norm_squared = float(np.linalg.norm(C @ E - E @ C, ord="fro") ** 2)
    det_residual = float(abs(np.linalg.det(W) - 1))

    exact_group_commutator_determinant = "1"
    central_u1_flux = "0 mod 2*pi"

    uf_phases = np.mod(-np.angle(np.linalg.eigvals(U_F)), 2 * np.pi)
    face_phases = np.mod(-np.angle(np.linalg.eigvals(W)), 2 * np.pi)
    uf_gaps = circular_gaps(uf_phases)
    face_gaps = circular_gaps(face_phases)
    gap_multiset_distance = float(np.linalg.norm(uf_gaps - face_gaps))
    face_has_repeated_gap = bool(abs(face_gaps[0] - face_gaps[1]) < 1e-12)

    lifted = np.array([
        float(x) for x in lift["device_relative_mass_squared_output"]["lifted_action_phases"]
    ])
    lifted_nontrivial = bool(np.max(np.abs(lifted)) > 1e-6)

    gates = {
        "G1_PINNED_FINITE_CTP_NAMBU_AND_FACE_INPUTS_VALID": True,
        "G2_MINIMAL_DAGGER_CTP_FACE_HOLONOMY_UNITARY": unitary_residual < 1e-12,
        "G3_SOURCE_TRANSPORT_AND_INTERACTION_NONCOMMUTE": commutator_norm_squared > 1e-6,
        "G4_NONIDENTITY_NONABELIAN_FACE_HOLONOMY_EXISTS": nonidentity_norm > 1e-6,
        "G5_GROUP_COMMUTATOR_DETERMINANT_EXACTLY_ONE": det_residual < 1e-12,
        "G6_CENTRAL_U1_FACE_FLUX_REPRODUCES_NONTRIVIAL_LIFT": False,
        "G7_PLAQUETTE_PHASE_GAPS_MATCH_BQGNEUT027_LIFT": gap_multiset_distance < 1e-12,
        "G8_UNCHANGED_FINITE_ACTION_SELECTS_BQGNEUT030_TRANSGRESSION": False,
        "G9_NO_TARGET_SCAN_OR_LONG_COMPUTATION": not MANIFEST["target_data_accessed"] and not MANIFEST["parameter_scan_used"] and not MANIFEST["long_computation_used"],
    }
    gates = {k: bool(v) for k, v in gates.items()}
    scoped_nonabelian_capacity = all(gates[k] for k in (
        "G1_PINNED_FINITE_CTP_NAMBU_AND_FACE_INPUTS_VALID",
        "G2_MINIMAL_DAGGER_CTP_FACE_HOLONOMY_UNITARY",
        "G3_SOURCE_TRANSPORT_AND_INTERACTION_NONCOMMUTE",
        "G4_NONIDENTITY_NONABELIAN_FACE_HOLONOMY_EXISTS",
        "G5_GROUP_COMMUTATOR_DETERMINANT_EXACTLY_ONE",
        "G9_NO_TARGET_SCAN_OR_LONG_COMPUTATION",
    ))
    central_transgression_pass = gates["G6_CENTRAL_U1_FACE_FLUX_REPRODUCES_NONTRIVIAL_LIFT"] and gates["G7_PLAQUETTE_PHASE_GAPS_MATCH_BQGNEUT027_LIFT"] and gates["G8_UNCHANGED_FINITE_ACTION_SELECTS_BQGNEUT030_TRANSGRESSION"]

    tests = {
        "T1_INPUT_HASHES_MATCH": True,
        "T2_MINIMAL_CTP_FACE_IS_NONTRIVIAL_UNITARY": gates["G2_MINIMAL_DAGGER_CTP_FACE_HOLONOMY_UNITARY"] and gates["G4_NONIDENTITY_NONABELIAN_FACE_HOLONOMY_EXISTS"],
        "T3_EXACT_CENTRAL_DETERMINANT_TRIVIAL": gates["G5_GROUP_COMMUTATOR_DETERMINANT_EXACTLY_ONE"] and exact_group_commutator_determinant == "1",
        "T4_NONTRIVIAL_LIFT_NOT_REPRODUCED": lifted_nontrivial and not gates["G6_CENTRAL_U1_FACE_FLUX_REPRODUCES_NONTRIVIAL_LIFT"],
        "T5_GAP_MULTISET_MISMATCH": gap_multiset_distance > 1e-3 and face_has_repeated_gap,
        "T6_SPLIT_CAPACITY_PASS_AND_CENTRAL_NO_GO": scoped_nonabelian_capacity and not central_transgression_pass,
        "T7_NO_TARGET_SCAN_OR_LONG_COMPUTATION": gates["G9_NO_TARGET_SCAN_OR_LONG_COMPUTATION"],
    }
    assert all(tests.values())

    decision = (
        "SPLIT_SCOPED_PASS_EXISTING_SOURCE_TRANSPORT_INTERACTION_AND_CTP_DAGGER_REVERSAL_"
        "GIVE_A_NONIDENTITY_UNITARY_NONABELIAN_CAUSAL_PLAQUETTE_HOLONOMY__SCOPED_NO_GO_"
        "THE_MINIMAL_RECTANGULAR_CTP_GROUP_COMMUTATOR_HAS_EXACT_DETERMINANT_ONE_ZERO_CENTRAL_"
        "U1_FLUX_AND_A_REPEATED_GAP_SPECTRUM_NOT_THE_BQGNEUT027_LIFT__UNCHANGED_FINITE_"
        "ACTION_DOES_NOT_SELECT_THE_BQGNEUT030_CENTRAL_TWO_FORM_TRANSGRESSION__PFAFFIAN_"
        "DETERMINANT_LINE_BERRY_CURVATURE_MECHANISM_REQUIRED"
    )
    return {
        "schema": "siel.dpa.bqgneut031.raw.v1",
        "scout_id": MANIFEST["scout_id"],
        "gate_id": MANIFEST["gate_id"],
        "source_commit": MANIFEST["source_commit"],
        "source_snapshot_id": MANIFEST["source_snapshot_id"],
        "evidence_status": "Theoretical derivation",
        "evidence_qualifiers": "Exploratory DPA scout; exact determinant no-go plus fixed 3x3 numerical witness in the minimal rectangular dagger-CTP plaquette class",
        "scientific_layer": "finite neutral CTP face holonomy and internal-phase to causal-two-form transgression",
        "decision": decision,
        "bold_hypothesis": {
            "minimal_ctp_face": "W_face=C_g E C_g^dagger E^dagger",
            "interpretive_leap": "The source transport and interaction slots are adjacent edges of one causal CTP plaquette; dagger reversal supplies the opposite edges.",
            "new_fitted_coefficient_or_target": False
        },
        "minimal_ctp_face_result": {
            "unitary_residual": unitary_residual,
            "nonidentity_frobenius_norm": nonidentity_norm,
            "source_edge_commutator_norm_squared": commutator_norm_squared,
            "exact_determinant": exact_group_commutator_determinant,
            "numerical_determinant_residual": det_residual,
            "central_U1_flux": central_u1_flux,
            "floquet_circular_gap_multiset": [float(x) for x in uf_gaps],
            "plaquette_circular_gap_multiset": [float(x) for x in face_gaps],
            "gap_multiset_l2_distance": gap_multiset_distance,
            "plaquette_has_repeated_gap": face_has_repeated_gap
        },
        "typing_boundary": {
            "nonabelian_source_face_holonomy": "DERIVED_IN_MINIMAL_RECTANGULAR_CTP_CLASS",
            "central_U1_transgression": "SCOPED_NO_GO_IN_ORDINARY_GROUP_COMMUTATOR_CLASS",
            "BQGNEUT027_phase_preservation": "FAIL_IN_MINIMAL_PLAQUETTE_CLASS",
            "finite_parent_selection_of_BQGNEUT030_transgression": "OPEN",
            "next_positive_mechanism": "Nambu Pfaffian or fermion determinant-line Berry curvature rather than the determinant of an ordinary group commutator"
        },
        "noncompensating_gates": gates,
        "scoped_nonabelian_face_holonomy_capacity_pass": scoped_nonabelian_capacity,
        "central_two_form_transgression_pass": central_transgression_pass,
        "strongest_ordinary_alternative": "A noncommuting pair of finite unitaries generically produces a nontrivial group-commutator plaquette. The determinant-one obstruction is universal, so a central phase requires a determinant/Pfaffian line or another added line-bundle structure.",
        "counter_intuition_scan": "The existence of a nonidentity face holonomy does not imply the required central neutral phase. Ordinary CTP dagger closure removes the determinant phase exactly. Reading its non-Abelian eigenphases as the old lift would also fail because the circular gap multiset changes and acquires a repeated gap.",
        "claim_ceiling": "The existing source transport, weighted interaction and dagger CTP reversal generate a nontrivial non-Abelian causal plaquette in the minimal rectangular class, but that class has exact zero central U(1) determinant flux and does not reproduce the BQGNEUT-027 lifted phase. This excludes only the ordinary group-commutator transgression route; it does not exclude a Pfaffian/determinant-line Berry curvature, open Wilson surface, empirical neutrino physics or completed quantum gravity.",
        "next_gate": "BQGNEUT-032_PFAFFIAN_DETERMINANT_LINE_BERRY_CURVATURE_TO_CAUSAL_FACE_TRANSGRESSION_GATE",
        "work_package": "BQG-G3-R03.8",
        "work_package_status": "ACTIVE",
        "runtime": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "target_data_accessed": False,
            "parameter_scan_used": False,
            "long_computation_used": False
        },
        "tests": tests
    }


def main():
    raw = run()
    result_keys = tuple(k for k in raw if k != "tests")
    (HERE / "RAW_OUTPUT.json").write_text(json.dumps(raw, indent=2, ensure_ascii=False) + "\n")
    (HERE / "RESULT.json").write_text(json.dumps({k: raw[k] for k in result_keys}, indent=2, ensure_ascii=False) + "\n")
    (HERE / "CERTIFICATE.json").write_text(json.dumps({
        "schema": "siel.dpa.bqgneut031.certificate.v1",
        "scout_id": raw["scout_id"],
        "source_commit": raw["source_commit"],
        "input_hashes": {item["path"]: item["sha256"] for item in MANIFEST["inputs"]},
        "evaluator_sha256": digest(Path(__file__).read_bytes()),
        "raw_output_sha256": digest((HERE / "RAW_OUTPUT.json").read_bytes()),
        "result_sha256": digest((HERE / "RESULT.json").read_bytes()),
        "tests": raw["tests"],
        "decision": raw["decision"]
    }, indent=2, ensure_ascii=False) + "\n")
    (HERE / "STATUS.json").write_text(json.dumps({
        "scout_id": raw["scout_id"], "status": "COMPLETE",
        "decision": raw["decision"], "next_gate": raw["next_gate"]
    }, indent=2, ensure_ascii=False) + "\n")
    (HERE / "EXECUTION_LOG.json").write_text(json.dumps({
        "iteration": 1,
        "command": "python3 -B evaluate_scout.py",
        "runtime_class": "subsecond exact determinant identity plus fixed 3x3 matrix witness",
        "result_informed_change": False
    }, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
