#!/usr/bin/env python3
"""Exact proof checker for BGCE444.

The scientific result is the finite-dimensional algebraic proof recorded in
AUDIT.md.  This script checks its rational matrices and the committed source
inventory; it is not an empirical endpoint and does not issue E0/E1/E2.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations_with_replacement
from pathlib import Path
import hashlib
import json
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE_REVISION = "bff28ef1c5a1860780f0d4f3d594c7dbb09783a4"

INPUTS = {
    "records/BGCE290_INDEPENDENT_DOUBLED_A_SOURCE_TO_CAUSAL_METRIC_HILBERT_WARD_GATE_20260923/RESULT.json": "fe7000b5c16f8b3225ca18799170b25d98307208cada544b605675f483e0be8b",
    "records/BGCE290_INDEPENDENT_DOUBLED_A_SOURCE_TO_CAUSAL_METRIC_HILBERT_WARD_GATE_20260923/RAW_OUTPUT.json": "f4661c8007524532a5da1ceb8a97a29e98bd2fa9af968ef8730453868e8aa724",
    "records/BGCE291_STRESS_WARD_INDEPENDENT_REDERIVATION_AND_SCOPE_RED_TEAM_GATE_20260923/RESULT.json": "a931435e39aefcd1e77c2aa2f61868a590a2d1d0c1c984799aad9d2f00e9dc99",
    "records/BGCE288_CAUSAL_EVEN_EVENT_PLUS_X21R1_ODD_THETA_FULL_LORENTZ_TANGENT_GATE_20260923/RAW_OUTPUT.json": "dbe19c46ca6a2e4225b16d84c03946e584a7cb03b2d42b4035ea58426d509e93",
    "records/UB612_PBM_COVARIANT_SIGMA6_U4_V0_2_PARALLEL4_FOUR_ROOT_GENERATOR_GATE/RESULT.json": "45cf6192289655b8626dfbba77dc829fd69f85e34d1e17359c56b2c1ffe99c7c",
    "records/UB612_PBM_COVARIANT_SIGMA6_U4_V0_2_PARALLEL4_FOUR_ROOT_GENERATOR_GATE/PBM_COVARIANT_TRANSPORT_JETS_PARTIAL_v1.json": "a17ed6e96ddf5a191daf58f099d5ecbaac2d610e22645af646b1f6e03fa3a5db",
}

PAIRS = list(combinations_with_replacement(range(4), 2))
PAIR_PAIRS = list(combinations_with_replacement(range(10), 2))
QUARTICS = list(combinations_with_replacement(range(4), 4))


def load_pinned(relative: str) -> dict:
    data = subprocess.check_output(
        ["git", "show", f"{SOURCE_REVISION}:{relative}"], cwd=ROOT
    )
    assert hashlib.sha256(data).hexdigest() == INPUTS[relative]
    assert data == (ROOT / relative).read_bytes()
    return json.loads(data)


def mmul(a, b):
    return [
        [sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def transpose(a):
    return [list(row) for row in zip(*a)]


def matrix_rank(matrix):
    a = [row[:] for row in matrix]
    rows, cols = len(a), len(a[0])
    rank = 0
    for col in range(cols):
        pivot = next((r for r in range(rank, rows) if a[r][col]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        p = a[rank][col]
        a[rank] = [x / p for x in a[rank]]
        for r in range(rows):
            if r != rank and a[r][col]:
                q = a[r][col]
                a[r] = [a[r][c] - q * a[rank][c] for c in range(cols)]
        rank += 1
    return rank


def basis_matrix(pair):
    i, j = pair
    out = [[Fraction(0) for _ in range(4)] for _ in range(4)]
    out[i][j] = out[j][i] = Fraction(1 if i == j else 1, 1 if i == j else 2)
    return out


def quadratic_coefficients(matrix):
    # Coefficients of x^T matrix x in the ten monomial basis x_i x_j.
    return [matrix[i][j] if i == j else 2 * matrix[i][j] for i, j in PAIRS]


def polynomial_product(q1, q2):
    out = [Fraction(0) for _ in QUARTICS]
    index = {monomial: i for i, monomial in enumerate(QUARTICS)}
    for a, c1 in zip(PAIRS, q1):
        for b, c2 in zip(PAIRS, q2):
            out[index[tuple(sorted(a + b))]] += c1 * c2
    return out


def main():
    sources = {path: load_pinned(path) for path in INPUTS}
    bgce290 = sources[next(path for path in INPUTS if path.endswith("BGCE290_INDEPENDENT_DOUBLED_A_SOURCE_TO_CAUSAL_METRIC_HILBERT_WARD_GATE_20260923/RESULT.json"))]
    bgce291 = sources[next(path for path in INPUTS if path.endswith("BGCE291_STRESS_WARD_INDEPENDENT_REDERIVATION_AND_SCOPE_RED_TEAM_GATE_20260923/RESULT.json"))]
    bgce288 = sources[next(path for path in INPUTS if path.endswith("BGCE288_CAUSAL_EVEN_EVENT_PLUS_X21R1_ODD_THETA_FULL_LORENTZ_TANGENT_GATE_20260923/RAW_OUTPUT.json"))]
    ub612_result = sources[next(path for path in INPUTS if path.endswith("UB612_PBM_COVARIANT_SIGMA6_U4_V0_2_PARALLEL4_FOUR_ROOT_GENERATOR_GATE/RESULT.json"))]
    ub612_packet = sources[next(path for path in INPUTS if path.endswith("PBM_COVARIANT_TRANSPORT_JETS_PARTIAL_v1.json"))]

    assert bgce290["source_to_causal_Sym2_rank"] == 10
    assert bgce291["algebraic_rank10_Hadamard_Sym2_solder"] == "PASS_CANONICAL_CANDIDATE"
    assert bgce288["causal_representation_split"]["combined_full_rank_each_sector"] is True
    assert len(bgce288["sector_records"]) == 8
    assert all(
        record["event_even_plus_theta_odd_combined_rank"] == 10
        for record in bgce288["sector_records"]
    )

    U = [[Fraction(x, 2) for x in row] for row in [
        [1, 1, 1, 1],
        [1, -1, -1, 1],
        [1, -1, 1, -1],
        [1, 1, -1, -1],
    ]]
    images = []
    for pair in PAIRS:
        A = basis_matrix(pair)
        images.append(quadratic_coefficients(mmul(mmul(transpose(U), A), U)))
    solder_matrix = [[images[col][row] for col in range(10)] for row in range(10)]
    solder_rank = matrix_rank(solder_matrix)
    assert solder_rank == 10

    columns = []
    for a, b in PAIR_PAIRS:
        columns.append(polynomial_product(images[a], images[b]))
    second_response = [[columns[col][row] for col in range(55)] for row in range(35)]
    second_response_rank = matrix_rank(second_response)
    kernel_dimension = 55 - second_response_rank
    assert second_response_rank == 35
    assert kernel_dimension == 20

    assert ub612_result["actual_output"]["coefficient_counts"]["U4"] == 35
    assert len(ub612_result["actual_output"]["root_direction_order"]) == 4
    assert len(ub612_packet["van_vleck"]["U4_total"]) == 35
    assert all(
        len(record["derivatives"]) == 4
        for record in ub612_packet["van_vleck"]["U4_total"].values()
    )
    assert "second_metric_source_response" not in ub612_packet

    print(json.dumps({
        "source_revision": SOURCE_REVISION,
        "source_dimension": 10,
        "symmetric_source_pair_dimension": len(PAIR_PAIRS),
        "quartic_dimension": len(QUARTICS),
        "source_solder_rank": solder_rank,
        "second_response_rank": second_response_rank,
        "kernel_dimension": kernel_dimension,
        "sector_count_checked": len(bgce288["sector_records"]),
        "sector_masks": [record["mask"] for record in bgce288["sector_records"]],
        "ub612_U4_coefficient_count": len(ub612_packet["van_vleck"]["U4_total"]),
        "ub612_available_derivative_directions": 4,
        "ub612_ten_source_second_response_present": False,
    }, indent=2))


if __name__ == "__main__":
    main()
