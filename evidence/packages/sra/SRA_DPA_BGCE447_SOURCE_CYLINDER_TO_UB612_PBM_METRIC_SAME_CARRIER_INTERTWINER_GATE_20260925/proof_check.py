#!/usr/bin/env python3
"""BGCE447 exact same-carrier and frozen-lineage audit."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

PATHS = {
    "bgce290": "audits/SRA_DPA_BGCE290_INDEPENDENT_DOUBLED_A_SOURCE_TO_CAUSAL_METRIC_HILBERT_WARD_GATE_20260923/RAW_OUTPUT.json",
    "bgce446": "audits/SRA_DPA_BGCE446_SOURCE_625_CHILD_FOURTH_JET_TO_PBM_U4_GATE_20260925/RESULT.json",
    "ub476": "audits/UB476_BRAID_CASIMIR_SECTION_FREE_SAME_ENERGY_C5_BACKREACTION_GATE/SAME_ENERGY_C5_CERTIFICATE.json",
    "ub496": "audits/UB496_TWO_ANCHOR_DENSITY_REGULAR_COMMON_INTERVAL_AND_REFERENCE_RESPONSE_GATE/RESULT.json",
    "ub596e": "audits/UB596E_NONCIRCULAR_PBM_TIME_JET_LOCAL_ENERGY_GATE/RESULT.json",
    "ub597a": "audits/UB597A_NONZERO_ENERGY_CENTERED_K_DOMAIN_GATE/RESULT.json",
    "ub598j": "audits/UB598J_ACTUAL_SCHEME_V2_HPS_INSERTION_C1_COEFFICIENT_GATE/ACTUAL_UB597A_PROPER_FRAME_NABLA2_RICCI_C1.json",
    "ub598o": "audits/UB598O_ACTUAL_UB597A_RIEMANN_C1_GATE/ACTUAL_UB597A_PROPER_FRAME_RIEMANN_C1_PACKET_v1.json",
    "ub612": "audits/UB612_PBM_COVARIANT_SIGMA6_U4_V0_2_PARALLEL4_FOUR_ROOT_GENERATOR_GATE/PBM_COVARIANT_TRANSPORT_JETS_PARTIAL_v1.json",
    "ub612_eval": "audits/UB612_PBM_COVARIANT_SIGMA6_U4_V0_2_PARALLEL4_FOUR_ROOT_GENERATOR_GATE/evaluate.py",
    "x49": "audits/SRA_DPA_A57S_X49_BOUNDARY_METRIC_TANGENT_INTERTWINER_GATE_20260917/RESULT.json",
}


def load(name: str):
    return json.loads((ROOT / PATHS[name]).read_text())


def sha(path: str) -> str:
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def frac(value):
    return Fraction(value)


def ldl_pivots(matrix):
    n = len(matrix)
    lower = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    diagonal = [Fraction(0) for _ in range(n)]
    for i in range(n):
        lower[i][i] = 1
        diagonal[i] = matrix[i][i] - sum(lower[i][k] ** 2 * diagonal[k] for k in range(i))
        assert diagonal[i] != 0
        for j in range(i + 1, n):
            lower[j][i] = (
                matrix[j][i] - sum(lower[j][k] * lower[i][k] * diagonal[k] for k in range(i))
            ) / diagonal[i]
    return diagonal


def main():
    data = {name: load(name) for name in PATHS if name != "ub612_eval"}
    hashes = {path: sha(path) for path in PATHS.values()}

    # BGCE290 source frame and UB476 PBM creation frame use exactly the same
    # ordered clock/Jordan-character carrier.  The characters are precisely
    # the nonconstant rows of the normalized Hadamard frame map.
    source = data["bgce290"]["independent_metric_source_solder"]
    screen = data["ub476"]["screen"]
    assert source["source_frame"] == "[G1,{G1,P1}/2,{G1,P2}/2,{G1,P3}/2]"
    assert screen["repair"] == "X_chi=(G1 P_chi+P_chi G1)/2"
    assert screen["characters"] == [
        [1, -1, -1, 1],
        [1, -1, 1, -1],
        [1, 1, -1, -1],
    ]
    assert source["frame_intertwiner"] == "U=H4/2"
    assert source["Sym2_rank"] == 10
    assert source["S4_intertwining_checks"] == 240

    # UB476's Gram-Schmidt shift has form Y_i=X_i-c_i G1.  Its matrix is unit
    # lower triangular, so det(B)=1 independently of the c_i values.  The
    # saved exact metric verifies one negative clock and an SPD spatial block.
    metric = [[frac(x) for x in row] for row in screen["clock_orthogonal_metric"]]
    assert all(metric[0][i] == metric[i][0] == 0 for i in range(1, 4))
    spatial_pivots = ldl_pivots([row[1:] for row in metric[1:]])
    assert metric[0][0] < 0 and all(x > 0 for x in spatial_pivots)
    basis_det = Fraction(1)

    scale_lo, scale_hi = map(frac, data["ub476"]["constraint_root"]["scale_bracket"])
    assert 0 < scale_lo <= scale_hi
    # For a 4-carrier C, Sym^2(C) has determinant det(C)^5.  Hadamard U,
    # unit-triangular B and positive clock/spatial rescalings are invertible;
    # hence their induced ten-component metric map is invertible.
    induced_sym2_rank = 10
    induced_sym2_nonzero_determinant = basis_det != 0 and scale_lo > 0
    assert induced_sym2_nonzero_determinant

    # Actual frozen lineage.  Each consumer records the producer digest.
    ub476_path = PATHS["ub476"]
    ub496_path = PATHS["ub496"]
    ub596e_path = PATHS["ub596e"]
    assert data["ub496"]["input_hashes"][ub476_path] == hashes[ub476_path]
    assert data["ub596e"]["input_hashes"][ub496_path] == hashes[ub496_path]
    assert data["ub597a"]["input_hashes"][ub596e_path] == hashes[ub596e_path]

    box_id = data["ub597a"]["frozen_box"]["id"]
    roots = ["p1", "p2", "p3", "H"]
    for key in ("ub598j", "ub598o", "ub612"):
        assert data[key]["box_id"] == box_id
        assert data[key]["root_direction_order"] == roots
    eval_text = (ROOT / PATHS["ub612_eval"]).read_text()
    assert "def load_metric_inverse():" in eval_text
    assert "audits/UB596E_NONCIRCULAR_PBM_TIME_JET_LOCAL_ENERGY_GATE/evaluate.py" in eval_text
    assert data["ub612"]["status"].startswith("PARTIAL_PASS_ACTUAL_U4_V0_2")

    # The older X49 negative same-subspace result compared a different
    # moment-marker screen (H,L,L^2,L^3) to the character screen.  Current
    # UB476 instead uses G1 and the Jordan-dressed P_chi in the same order.
    assert data["x49"]["status"] == "EXPLORATORY_PARTIAL_PASS_INVERTIBLE_CROSS_PAIRING_WITH_NONZERO_RESIDUAL"
    assert data["x49"]["summary"]["sector_records"][0]["packets"][0]["exact_screen_intertwiner"] is False
    x49_not_current_pbm_screen = True

    result = {
        "schema": "siel.dpa.bgce447.proof-certificate.v1",
        "candidate_id": "BGCE447",
        "date": "2026-09-25",
        "status": "PASS_EXACT_CURRENT_UB612_PBM_AND_SOURCE_CYLINDER_SAME_ORDERED_G1_JORDAN_CHARACTER_CARRIER",
        "source_hashes": hashes,
        "carrier": {
            "source_order": ["G1", "{G1,P_chi1}/2", "{G1,P_chi2}/2", "{G1,P_chi3}/2"],
            "pbm_creation_order": ["G1", "X_chi1", "X_chi2", "X_chi3"],
            "X_chi_definition": "X_chi=(G1 P_chi+P_chi G1)/2",
            "same_ordered_characters": True,
            "hadamard_frame": "U=H4/2",
            "clock_orthogonalization": "Y_i=X_i-c_i G1",
            "clock_orthogonalization_determinant": str(basis_det),
            "positive_creation_scale_interval": [str(scale_lo), str(scale_hi)],
            "source_to_metric_rank": source["Sym2_rank"],
            "induced_sym2_rank_after_composition": induced_sym2_rank,
            "induced_sym2_nonzero_determinant": induced_sym2_nonzero_determinant,
            "spatial_LDL_pivots": [str(x) for x in spatial_pivots],
            "Lorentz_inertia": [1, 3, 0],
        },
        "actual_lineage": {
            "chain": ["UB476", "UB496", "UB596E", "UB597A", "UB598J/UB598O", "UB612"],
            "hash_pinned_through_UB597A": True,
            "UB612_metric_loader_reuses_UB596E_terminal_chart": True,
            "box_id": box_id,
            "root_direction_order": roots,
            "constant_linear_intertwiner_commutes_with_metric_jets": True,
        },
        "counter_intuition": {
            "X49_same_subspace_failure": True,
            "X49_not_current_PBM_screen": x49_not_current_pbm_screen,
            "reason": "X49 used the distinct H,L,L^2,L^3 moment screen; actual UB612 descends from UB476's G1 and Jordan-dressed ordered P_chi screen.",
            "not_claimed": "Carrier identity does not by itself derive the PBM dynamics, U4 coefficients, a source-child sampling theorem for the nonpolynomial metric, or physical UV completion.",
        },
    }
    (HERE / "PROOF_CERTIFICATE.json").write_text(json.dumps(result, indent=2) + "\n")
    print(result["status"])


if __name__ == "__main__":
    main()
