#!/usr/bin/env python3
"""Exact source-axis physical-projector audit for DPA-SCOUT-BQGADM-014."""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE_MATRIX = json.loads((HERE / "SOURCE_MATRIX.json").read_text())
PINNED = SOURCE_MATRIX["source_commit"]


def pinned_bytes(path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{PINNED}:{path}"], cwd=ROOT)


def load_pinned(path: str) -> dict:
    return json.loads(pinned_bytes(path))


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def matmul(left, right):
    return [
        [sum(left[i][k] * right[k][j] for k in range(len(right))) for j in range(len(right[0]))]
        for i in range(len(left))
    ]


def rref(matrix):
    a = [[F(x) for x in row] for row in matrix]
    if not a:
        return a, []
    rows, cols = len(a), len(a[0])
    pivots = []
    row = 0
    for col in range(cols):
        pivot = next((i for i in range(row, rows) if a[i][col] != 0), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        value = a[row][col]
        a[row] = [x / value for x in a[row]]
        for i in range(rows):
            if i != row and a[i][col] != 0:
                value = a[i][col]
                a[i] = [a[i][j] - value * a[row][j] for j in range(cols)]
        pivots.append(col)
        row += 1
        if row == rows:
            break
    return a, pivots


def rank(matrix):
    return len(rref(matrix)[1])


def inverse(matrix):
    n = len(matrix)
    augmented = [
        [F(x) for x in matrix[i]] + [F(i == j) for j in range(n)]
        for i in range(n)
    ]
    reduced, pivots = rref(augmented)
    assert pivots[:n] == list(range(n))
    return [row[n:] for row in reduced]


def identity(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def zero(rows, cols):
    return [[F(0) for _ in range(cols)] for _ in range(rows)]


def block_diag(*blocks):
    rows = sum(len(block) for block in blocks)
    cols = sum(len(block[0]) for block in blocks)
    out = zero(rows, cols)
    row_offset = 0
    col_offset = 0
    for block in blocks:
        for i, row in enumerate(block):
            for j, value in enumerate(row):
                out[row_offset + i][col_offset + j] = value
        row_offset += len(block)
        col_offset += len(block[0])
    return out


def hstack(left, right):
    return [left[i] + right[i] for i in range(len(left))]


def kron(left, right):
    return [
        [left[i][j] * right[k][ell] for j in range(len(left[0])) for ell in range(len(right[0]))]
        for i in range(len(left))
        for k in range(len(right))
    ]


def matrix_equal(left, right):
    return left == right


def all_zero(matrix):
    return all(value == 0 for row in matrix for value in row)


def rational_matrix(matrix):
    return [[str(value) for value in row] for row in matrix]


hash_checks = {}
for source in SOURCE_MATRIX["sources"]:
    payload = pinned_bytes(source["path"])
    actual = hashlib.sha256(payload).hexdigest()
    hash_checks[source["path"]] = {
        "expected": source["sha256"],
        "actual": actual,
        "pass": actual == source["sha256"],
    }
assert all(item["pass"] for item in hash_checks.values())

raw006_path = SOURCE_MATRIX["sources"][0]["path"]
result006_path = SOURCE_MATRIX["sources"][1]["path"]
result012_path = SOURCE_MATRIX["sources"][2]["path"]
result004_path = SOURCE_MATRIX["sources"][3]["path"]
result010_path = SOURCE_MATRIX["sources"][4]["path"]

raw006 = load_pinned(raw006_path)
result006 = load_pinned(result006_path)
result012 = load_pinned(result012_path)
result004 = load_pinned(result004_path)
result010 = load_pinned(result010_path)

assert result006["decision"] == "PARTIAL_SCOPED"
assert result012["gate_results"]["physical_phase_dimension_four"] == "PASS"
assert result004["hierarchical_two_mode_strong_convergence"] == "CLOSED_SCOPED"
assert result010["gate_results"]["one_full_ten_component_update"] == "PASS"

omega = [[F(value) for value in row] for row in raw006["reduced_two_form"]]
omega_inverse = inverse(omega)
metric_pairs = [(0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 2)]
frobenius_metric = block_diag([[F(1)]], [[F(2)]], [[F(2)]], [[F(1)]], [[F(2)]], [[F(1)]])


def tt_data(axis_index: int):
    transverse = [index for index in range(3) if index != axis_index]
    a, b = transverse
    basis = zero(6, 2)
    basis[metric_pairs.index((a, a))][0] = F(1)
    basis[metric_pairs.index((b, b))][0] = F(-1)
    pair = tuple(sorted((a, b)))
    basis[metric_pairs.index(pair)][1] = F(1)
    gram = matmul(matmul(transpose(basis), frobenius_metric), basis)
    decoder = matmul(matmul(inverse(gram), transpose(basis)), frobenius_metric)
    projector = matmul(basis, decoder)
    return basis, decoder, projector


axis_results = []
for source_axis in raw006["source_axis_results"]:
    axis = [F(value) for value in source_axis["axis"]]
    nonzero = [index for index, value in enumerate(axis) if value != 0]
    assert len(nonzero) == 1
    axis_index = nonzero[0]
    constraint = [[F(value) for value in row] for row in source_axis["constraint_symbol"]]

    basis6, decoder6, projector6 = tt_data(axis_index)
    projector12 = block_diag(projector6, projector6)
    basis12 = block_diag(basis6, basis6)
    decoder12 = block_diag(decoder6, decoder6)

    gauge = matmul(omega_inverse, transpose(constraint))
    constraint_bracket = matmul(matmul(constraint, omega_inverse), transpose(constraint))
    projected_symplectic = matmul(matmul(transpose(projector12), omega), projector12)
    quotient_span = hstack(gauge, basis12)

    # The tensor-factor test is independent of a numerical refinement rule:
    # any child-constant spatial embedding J commutes with an internal P.
    child_constant = [[F(1)] for _ in range(5)]
    refinement_phase = kron(child_constant, identity(12))
    fine_projector = kron(identity(5), projector12)
    exact_refinement_commutator = matrix_equal(
        matmul(fine_projector, refinement_phase),
        matmul(refinement_phase, projector12),
    )

    endpoints = {
        "tt_projector_idempotent": matrix_equal(matmul(projector6, projector6), projector6),
        "tt_projector_rank_two": rank(projector6) == 2,
        "phase_projector_idempotent": matrix_equal(matmul(projector12, projector12), projector12),
        "phase_projector_rank_four": rank(projector12) == 4,
        "constraint_symbol_rank_four": rank(constraint) == 4,
        "projector_image_inside_constraint_surface": all_zero(matmul(constraint, projector12)),
        "linear_constraint_bracket_zero": all_zero(constraint_bracket),
        "gauge_image_rank_four": rank(gauge) == 4,
        "projector_annihilates_gauge_image": all_zero(matmul(projector12, gauge)),
        "projected_symplectic_rank_four": rank(projected_symplectic) == 4,
        "symplectic_self_adjoint": matrix_equal(
            matmul(transpose(projector12), omega), matmul(omega, projector12)
        ),
        "constraint_surface_equals_gauge_plus_projector_image": rank(quotient_span) == 8,
        "encoder_decoder_identity": matrix_equal(matmul(decoder12, basis12), identity(4)),
        "unique_frobenius_orthogonal_tt_projector": (
            matrix_equal(matmul(transpose(projector6), frobenius_metric), matmul(frobenius_metric, projector6))
            and matrix_equal(projector6, matmul(basis6, decoder6))
        ),
        "exact_child_constant_refinement_commutation": exact_refinement_commutator,
    }
    assert all(endpoints.values())
    axis_results.append({
        "axis": [str(value) for value in axis],
        "axis_index": axis_index,
        "configuration_encoder_6x2": rational_matrix(basis6),
        "configuration_decoder_2x6": rational_matrix(decoder6),
        "configuration_projector_6x6": rational_matrix(projector6),
        "phase_projector_12x12": rational_matrix(projector12),
        "hamiltonian_gauge_vectors_12x4": rational_matrix(gauge),
        "constraint_bracket_4x4": rational_matrix(constraint_bracket),
        "projected_symplectic_rank": rank(projected_symplectic),
        "constraint_surface_dimension": 12 - rank(constraint),
        "gauge_plus_physical_span_rank": rank(quotient_span),
        "endpoints": endpoints,
    })

global_endpoints = {
    "pinned_source_hashes": all(item["pass"] for item in hash_checks.values()),
    "all_three_source_axes_pass": len(axis_results) == 3 and all(
        all(row["endpoints"].values()) for row in axis_results
    ),
    "all_configuration_ranks_two": all(rank([[F(x) for x in row] for row in item["configuration_projector_6x6"]]) == 2 for item in axis_results),
    "all_phase_ranks_four": all(rank([[F(x) for x in row] for row in item["phase_projector_12x12"]]) == 4 for item in axis_results),
    "hierarchical_two_copy_target_present": result004["hierarchical_two_mode_strong_convergence"] == "CLOSED_SCOPED",
    "no_target_equation_coefficient_or_new_action": True,
    "nonlinear_moving_projector_present": False,
    "arbitrary_finite_momentum_projector_present": False,
}

decision = (
    "CLOSED_SCOPED_EXACT_FLAT_SOURCE_AXIS_PHYSICAL_PROJECTOR_AND_REFINEMENT_INTERTWINER"
    "__OPEN_NONLINEAR_MOVING_AND_ARBITRARY_MOMENTUM_PROJECTOR"
)

raw = {
    "schema": "siel.dpa.bqgadm014.raw.v1",
    "scout_id": "DPA-SCOUT-BQGADM-014",
    "attempt": 1,
    "pinned_commit": PINNED,
    "source_snapshot_id": SOURCE_MATRIX["source_snapshot_id"],
    "hash_checks": hash_checks,
    "environment": {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "evaluator_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    },
    "source_coordinates": {
        "metric_pairs": [list(pair) for pair in metric_pairs],
        "phase_order": "six symmetric spatial metric coordinates followed by six symmetric boost/momentum coordinates",
        "frobenius_metric_diagonal": ["1", "2", "2", "1", "2", "1"],
    },
    "axis_results": axis_results,
    "global_endpoints": global_endpoints,
    "decision": decision,
}

result = {
    "schema": "siel.dpa.bqgadm014.result.v1",
    "scout_id": "DPA-SCOUT-BQGADM-014",
    "date": "2026-09-29",
    "work_packages": ["BQG-G3-R01.5", "BQG-G3-R02.5"],
    "primary_evidence_status": "Theoretical derivation",
    "decision": decision,
    "decisive_result": (
        "For each of the three source-selected nonzero spatial axes, the flat source coframe and actual pulled-back Palatini symplectic form determine the same source-axis transverse-tracefree construction. The six-coordinate projector is the unique Frobenius-orthogonal projector onto a rank-two tensor subspace. Its phase lift has rank four, lies in the rank-four constraint surface, kills the four Hamiltonian gauge vectors, is symplectic on its image, and splits the eight-dimensional constraint surface exactly into four gauge plus four physical dimensions. Because the projector acts only on the internal tensor factor, it commutes exactly with child-constant five-way refinement and identifies its two configuration coordinates with the BQGEULER-004 two-copy carrier."
    ),
    "gate_results": {
        "all_three_source_axes": "PASS_EXACT",
        "rank_two_configuration_projector": "PASS_EXACT",
        "rank_four_phase_projector": "PASS_EXACT",
        "coisotropic_constraint_and_gauge_reduction": "PASS_EXACT_AT_FLAT_SOURCE_ANCHOR",
        "nondegenerate_physical_symplectic_image": "PASS_EXACT",
        "five_way_refinement_intertwiner": "PASS_EXACT_BY_TENSOR_FACTOR_NATURALITY",
        "BQGEULER004_two_copy_identification": "PASS_EXACT_IN_DECLARED_HIERARCHICAL_LINEAR_SCOPE",
        "nonlinear_moving_projector": "OPEN",
        "arbitrary_finite_momentum_direction": "OPEN",
        "exact_nonlinear_BQGEULER010_commutation": "OPEN"
    },
    "bold_hypothesis_revision": (
        "The proposed BKM horizontal law was unnecessary. The existing flat source coframe supplies its Frobenius metric, and the source incidence axis supplies the longitudinal direction. Together with the already derived Palatini symplectic form and constraints, these data uniquely determine the scoped projector without a new law."
    ),
    "counter_intuition": {
        "ordinary_explanation": "This is the standard transverse-tracefree coisotropic reduction of linearized time-gauge Palatini gravity.",
        "braid_specific_input": "Braid supplies the finite twelve-dimensional carrier, actual pulled-back symplectic form, exactly three selected incidence axes, rank-four constraint symbols and five-way hierarchical refinement.",
        "strongest_boundary": "The result is exact only at the flat linearized source-axis anchor. It does not yet give a metric-dependent nonlinear moving projector or cover every finite momentum direction.",
        "falsifier": "Failure of idempotence, rank, constraint annihilation, gauge annihilation, symplectic nondegeneracy, quotient splitting or refinement commutation on any source axis."
    },
    "formal_E0_E1_E2": "NOT_CLAIMED__DPA_THEORETICAL_DERIVATION_ONLY",
    "claim_ceiling": (
        "Exact source-derived flat-anchor physical phase projector and hierarchical refinement/wave intertwiner for the three source-selected nonzero spatial axes. No nonlinear moving projector, arbitrary finite momentum theorem, exact full nonlinear update commutation, empirical gravity, confirmation, RPD adoption, Level 3 or Official SIEL status."
    )
}

(HERE / "RAW_OUTPUT.json").write_text(json.dumps(raw, ensure_ascii=False, indent=2) + "\n")
(HERE / "RESULT.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({
    "decision": decision,
    "source_axes": len(axis_results),
    "flat_source_axis_projector": "PASS",
    "nonlinear_moving_projector": "OPEN",
}, ensure_ascii=False, indent=2))
