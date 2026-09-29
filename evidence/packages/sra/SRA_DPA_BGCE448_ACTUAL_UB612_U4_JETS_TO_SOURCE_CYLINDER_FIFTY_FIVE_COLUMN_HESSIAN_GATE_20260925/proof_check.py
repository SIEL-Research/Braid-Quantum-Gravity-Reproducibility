#!/usr/bin/env python3
"""BGCE448 actual UB612 U4 55-column osculating response audit."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
UB612 = ROOT / "audits/UB612_PBM_COVARIANT_SIGMA6_U4_V0_2_PARALLEL4_FOUR_ROOT_GENERATOR_GATE/PBM_COVARIANT_TRANSPORT_JETS_PARTIAL_v1.json"
BGCE447 = ROOT / "audits/SRA_DPA_BGCE447_SOURCE_CYLINDER_TO_UB612_PBM_METRIC_SAME_CARRIER_INTERTWINER_GATE_20260925/RESULT.json"
PRIMES = (1000003, 1000033, 1000037)
K = (Fraction(-12, 25), Fraction(52, 25), Fraction(52, 25), Fraction(52, 25))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def monomials():
    out = []
    for a in range(4, -1, -1):
        for b in range(4 - a, -1, -1):
            for c in range(4 - a - b, -1, -1):
                out.append((a, b, c, 4 - a - b - c))
    assert len(out) == 35
    return out


MONS = monomials()
INDEX = {a: i for i, a in enumerate(MONS)}


def rho(generator, vector):
    out = [Fraction(0) for _ in MONS]
    for alpha, coefficient in zip(MONS, vector):
        for i in range(4):
            for j in range(4):
                if alpha[i] and generator[i][j]:
                    beta = list(alpha)
                    beta[i] -= 1
                    beta[j] += 1
                    out[INDEX[tuple(beta)]] += coefficient * alpha[i] * generator[i][j]
    return out


def source_generators():
    out = []
    for i in range(4):
        for j in range(i, 4):
            h = Fraction(1) if i == j else Fraction(1, 2)
            generator = [[Fraction(0) for _ in range(4)] for _ in range(4)]
            generator[i][j] = h / (2 * K[i])
            if i != j:
                generator[j][i] = h / (2 * K[j])
            out.append(generator)
    assert len(out) == 10
    return out


def columns(vector):
    generators = source_generators()
    out = []
    pairs = []
    for a, left in enumerate(generators):
        for b in range(a, 10):
            right = generators[b]
            lr = rho(left, rho(right, vector))
            value = lr if a == b else [x + y for x, y in zip(lr, rho(right, rho(left, vector)))]
            out.append(value)
            pairs.append((a, b))
    assert len(out) == 55
    return out, pairs


def modular_rank(rows, prime):
    a = [[int(x.numerator % prime) * pow(int(x.denominator % prime), -1, prime) % prime for x in row] for row in rows]
    rank = 0
    for column in range(len(a[0])):
        pivot = next((r for r in range(rank, len(a)) if a[r][column]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        inverse = pow(a[rank][column], -1, prime)
        a[rank] = [x * inverse % prime for x in a[rank]]
        for r in range(len(a)):
            if r != rank and a[r][column]:
                q = a[r][column]
                a[r] = [(a[r][c] - q * a[rank][c]) % prime for c in range(len(a[0]))]
        rank += 1
        if rank == len(a):
            break
    return rank


def float_interval_screen(u4):
    midpoint, radius = [], []
    for alpha in MONS:
        lo, hi = map(float, u4[",".join(map(str, alpha))]["value"])
        midpoint.append((lo + hi) / 2)
        radius.append((hi - lo) / 2)
    midpoint = np.array(midpoint)
    radius = np.array(radius)

    # Build each response operator on coefficient space.  This is a diagnostic
    # enclosure screen, not the exact correlated interval endpoint.
    generators = source_generators()
    operators = []
    for generator in generators:
        op = np.zeros((35, 35))
        for column in range(35):
            unit = [Fraction(int(i == column)) for i in range(35)]
            image = rho(generator, unit)
            op[:, column] = [float(x) for x in image]
        operators.append(op)
    mids, radii = [], []
    for a, left in enumerate(operators):
        for b in range(a, 10):
            right = operators[b]
            op = left @ right if a == b else left @ right + right @ left
            mids.append(op @ midpoint)
            radii.append(np.abs(op) @ radius)
    matrix = np.array(mids).T
    error = np.array(radii).T
    scale = np.maximum(np.max(np.abs(matrix), axis=1), 1e-300)
    normalized = matrix / scale[:, None]
    normalized_error = error / scale[:, None]
    singular = np.linalg.svd(normalized, compute_uv=False)

    # Fixed 34x34 witness selected once from the midpoint QR scout.
    rows = [13, 25, 23, 15, 32, 9, 17, 24, 14, 7, 1, 27, 8, 34, 30, 20, 28, 0, 10, 2, 18, 33, 3, 31, 11, 22, 19, 4, 26, 16, 6, 29, 21, 12]
    cols = [1, 2, 11, 12, 20, 35, 33, 36, 53, 49, 54, 17, 13, 50, 24, 34, 10, 51, 16, 48, 42, 30, 37, 39, 3, 14, 19, 32, 41, 27, 15, 47, 43, 25]
    minor = normalized[np.ix_(rows, cols)]
    minor_error = normalized_error[np.ix_(rows, cols)]
    beeck_screen = float(np.max(np.sum(np.abs(np.linalg.inv(minor)) @ minor_error, axis=1)))
    error_norm_upper = float(np.sqrt(np.linalg.norm(normalized_error, 1) * np.linalg.norm(normalized_error, np.inf)))
    return {
        "midpoint_float_rank": int(np.linalg.matrix_rank(normalized)),
        "smallest_singular_value": float(singular[-1]),
        "second_smallest_singular_value": float(singular[-2]),
        "independent_interval_error_norm_upper": error_norm_upper,
        "fixed_34_minor_Beeck_screen": beeck_screen,
        "stable_rank_at_least_34_screen": bool(beeck_screen < 1),
        "rank35_not_certified_by_independent_interval_screen": bool(singular[-1] <= error_norm_upper),
        "diagnostic_only": True,
    }


def main():
    source = json.loads(UB612.read_text())
    carrier = json.loads(BGCE447.read_text())
    assert source["status"].startswith("PARTIAL_PASS_ACTUAL_U4_V0_2")
    assert source["coefficient_counts"]["U4"] == 35
    assert carrier["gate_decision"]["source_to_actual_UB612_metric_intertwiner"] == "PASS_EXACT_INVERTIBLE"
    u4 = source["van_vleck"]["U4_total"]
    midpoint = []
    for alpha in MONS:
        lo, hi = u4[",".join(map(str, alpha))]["value"]
        midpoint.append((Fraction(lo) + Fraction(hi)) / 2)
    cols, pairs = columns(midpoint)
    matrix_rows = [[cols[column][row] for column in range(55)] for row in range(35)]
    ranks = {str(prime): modular_rank(matrix_rows, prime) for prime in PRIMES}
    assert set(ranks.values()) == {35}
    screen = float_interval_screen(u4)
    assert screen["stable_rank_at_least_34_screen"]
    assert screen["rank35_not_certified_by_independent_interval_screen"]
    out = {
        "schema": "siel.dpa.bgce448.proof-certificate.v1",
        "candidate_id": "BGCE448",
        "date": "2026-09-25",
        "status": "SCOPED_PASS_ACTUAL_U4_FIFTY_FIVE_COLUMNS_AND_EXACT_MIDPOINT_RANK35__OPEN_CORRELATED_INTERVAL_RANK35",
        "source_hashes": {str(UB612.relative_to(ROOT)): sha(UB612), str(BGCE447.relative_to(ROOT)): sha(BGCE447)},
        "column_construction": {
            "quartic_slots": 35,
            "source_metric_directions": 10,
            "unordered_second_response_columns": 55,
            "source_pair_order": pairs,
            "formula": "D_ab U4 = rho(S_a)rho(S_b)U4 for a=b and the symmetrized two-order sum for a<b",
            "fitted_lift": False,
        },
        "exact_midpoint_modular_ranks": ranks,
        "interval_screen": screen,
        "decision": {
            "actual_U4_55_column_construction": "PASS",
            "exact_saved_midpoint_rank35": "PASS_THREE_PRIMES",
            "stable_rank_at_least_34": "PASS_DIAGNOSTIC_ENCLOSURE_SCREEN",
            "actual_correlated_interval_rank35": "OPEN_NOT_CERTIFIED",
            "full_metric_Frechet_Hessian": "OPEN_OSCULATING_FRAME_RESPONSE_ONLY",
        },
    }
    (HERE / "PROOF_CERTIFICATE.json").write_text(json.dumps(out, indent=2) + "\n")
    print(out["status"])


if __name__ == "__main__":
    main()
