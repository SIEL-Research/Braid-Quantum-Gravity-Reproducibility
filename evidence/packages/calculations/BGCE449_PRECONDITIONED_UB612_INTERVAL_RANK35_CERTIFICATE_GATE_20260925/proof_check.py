#!/usr/bin/env python3
"""BGCE449 exact preconditioned interval regularity certificate."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from decimal import Decimal as D, getcontext
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BGCE448_PROOF = ROOT / "records/BGCE448_ACTUAL_UB612_U4_JETS_TO_SOURCE_CYLINDER_FIFTY_FIVE_COLUMN_HESSIAN_GATE_20260925/proof_check.py"
BGCE448_RESULT = ROOT / "records/BGCE448_ACTUAL_UB612_U4_JETS_TO_SOURCE_CYLINDER_FIFTY_FIVE_COLUMN_HESSIAN_GATE_20260925/RESULT.json"
SELECTED_COLUMNS = [15, 45, 35, 12, 41, 34, 28, 36, 3, 25, 1, 14, 50, 47, 27, 11, 40, 24, 54, 23, 48, 38, 37, 42, 26, 29, 10, 52, 16, 46, 18, 32, 19, 20, 49]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_bgce448():
    spec = importlib.util.spec_from_file_location("bgce448_for_bgce449", BGCE448_PROOF)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def decimal(value: Fraction) -> D:
    return D(value.numerator) / D(value.denominator)


def decimal_inverse(matrix):
    n = len(matrix)
    augmented = [matrix[i][:] + [D(int(i == j)) for j in range(n)] for i in range(n)]
    for column in range(n):
        pivot = max(range(column, n), key=lambda row: abs(augmented[row][column]))
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        value = augmented[column][column]
        assert value
        augmented[column] = [x / value for x in augmented[column]]
        for row in range(n):
            if row != column and augmented[row][column]:
                value = augmented[row][column]
                augmented[row] = [
                    augmented[row][j] - value * augmented[column][j]
                    for j in range(2 * n)
                ]
    return [row[n:] for row in augmented]


def build_interval_matrix(module):
    source = json.loads(module.UB612.read_text())
    u4 = source["van_vleck"]["U4_total"]
    midpoint, radius = [], []
    for alpha in module.MONS:
        lo, hi = map(Fraction, u4[",".join(map(str, alpha))]["value"])
        midpoint.append((lo + hi) / 2)
        radius.append((hi - lo) / 2)
    midpoint_columns, pairs = module.columns(midpoint)
    matrix = [[midpoint_columns[column][row] for column in range(55)] for row in range(35)]

    generators = module.source_generators()
    error_columns = []
    for a, left in enumerate(generators):
        for b in range(a, 10):
            right = generators[b]
            operator_columns = []
            for k in range(35):
                unit = [Fraction(int(i == k)) for i in range(35)]
                lr = module.rho(left, module.rho(right, unit))
                image = lr if a == b else [
                    x + y for x, y in zip(lr, module.rho(right, module.rho(left, unit)))
                ]
                operator_columns.append(image)
            error_columns.append([
                sum(abs(operator_columns[k][row]) * radius[k] for k in range(35))
                for row in range(35)
            ])
    error = [[error_columns[column][row] for column in range(55)] for row in range(35)]
    return matrix, error, pairs


def main():
    module = load_bgce448()
    prior = json.loads(BGCE448_RESULT.read_text())
    assert prior["gate_decision"]["actual_U4_fifty_five_columns"] == "PASS_CONSTRUCTED"
    matrix, error, pairs = build_interval_matrix(module)
    assert len(SELECTED_COLUMNS) == len(set(SELECTED_COLUMNS)) == 35
    center = [[matrix[i][j] for j in SELECTED_COLUMNS] for i in range(35)]
    radius = [[error[i][j] for j in SELECTED_COLUMNS] for i in range(35)]

    # The decimal inverse only proposes a rational preconditioner.  Converting
    # its entries back to Fraction makes the final residual and interval bound
    # exact rational arithmetic.
    getcontext().prec = 220
    approximate_inverse = decimal_inverse([[decimal(x) for x in row] for row in center])
    preconditioner = [[Fraction(str(x)) for x in row] for row in approximate_inverse]

    comparison = []
    residual_row_sums = []
    for i in range(35):
        row = []
        residual_sum = Fraction(0)
        for j in range(35):
            residual = Fraction(int(i == j)) - sum(
                preconditioner[i][k] * center[k][j] for k in range(35)
            )
            uncertainty = sum(
                abs(preconditioner[i][k]) * radius[k][j] for k in range(35)
            )
            row.append(abs(residual) + uncertainty)
            residual_sum += abs(residual)
        comparison.append(row)
        residual_row_sums.append(residual_sum)

    # A positive diagonal scaling is obtained by power iteration, then frozen
    # as exact decimal rationals.  The final Collatz row ratios are exact.
    vector = [D(1) for _ in range(35)]
    for _ in range(500):
        image = [
            sum(decimal(comparison[i][j]) * vector[j] for j in range(35))
            for i in range(35)
        ]
        scale = max(image)
        vector = [value / scale for value in image]
    rational_vector = [Fraction(str(value)) for value in vector]
    exact_ratios = [
        sum(comparison[i][j] * rational_vector[j] for j in range(35)) / rational_vector[i]
        for i in range(35)
    ]
    exact_upper = max(exact_ratios)
    assert exact_upper < 1

    out = {
        "schema": "siel.public-calculation.bgce449.interval-rank-certificate.v1",
        "candidate_id": "BGCE449",
        "date": "2026-09-25",
        "status": "PASS_EXACT_PRECONDITIONED_INTERVAL_RANK35_FOR_ACTUAL_UB612_U4_SOURCE_RESPONSE",
        "source_hashes": {
            str(module.UB612.relative_to(ROOT)): sha(module.UB612),
            str(BGCE448_RESULT.relative_to(ROOT)): sha(BGCE448_RESULT),
            str(BGCE448_PROOF.relative_to(ROOT)): sha(BGCE448_PROOF),
        },
        "selected_columns_zero_based": SELECTED_COLUMNS,
        "selected_source_pairs": [pairs[index] for index in SELECTED_COLUMNS],
        "minor_shape": [35, 35],
        "preconditioner_decimal_precision": 220,
        "exact_Krawczyk_Beeck_Collatz_upper": {
            "numerator": str(exact_upper.numerator),
            "denominator": str(exact_upper.denominator),
            "decimal": format(decimal(exact_upper), ".18E"),
            "strictly_less_than_one": True,
        },
        "max_exact_preconditioner_residual_row_sum_decimal": format(
            decimal(max(residual_row_sums)), ".18E"
        ),
        "theorem": "For every coefficient tensor in the saved componentwise UB612 U4 interval box, the selected preconditioned 35-by-35 source-response minor is nonsingular. Therefore every admissible 35-by-55 response matrix has row rank 35.",
        "correlation_requirement": "NOT_NEEDED_THE_INDEPENDENT_SAVED_INTERVAL_BOX_ALREADY_PASSES_AFTER_SOURCE_COLUMN_PRECONDITIONING",
    }
    (HERE / "PROOF_CERTIFICATE.json").write_text(json.dumps(out, indent=2) + "\n")
    print(out["status"])


if __name__ == "__main__":
    main()
