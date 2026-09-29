#!/usr/bin/env python3
"""Non-focal exact semantic witness harness for BGCE443 Revision 3."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def exact_rank(rows: list[list[int]]) -> int:
    matrix = [[Fraction(value) for value in row] for row in rows]
    if not matrix:
        return 0
    rank = 0
    column = 0
    while rank < len(matrix) and column < len(matrix[0]):
        pivot = next((r for r in range(rank, len(matrix)) if matrix[r][column]), None)
        if pivot is None:
            column += 1
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        scale = matrix[rank][column]
        matrix[rank] = [value / scale for value in matrix[rank]]
        for r in range(len(matrix)):
            if r != rank and matrix[r][column]:
                factor = matrix[r][column]
                matrix[r] = [a - factor * b for a, b in zip(matrix[r], matrix[rank])]
        rank += 1
        column += 1
    return rank


def evaluate(case: dict) -> dict:
    rank = exact_rank(case["derivation_rows"])
    endpoint = {
        "stabilization": all(value == 0 for value in case["stabilization_residuals"]),
        "implementer_growth": all(value > 0 for value in case["growth_slopes"]),
        "rank_three": rank == 3,
        "bounded_inner_exclusion": all(value > 0 for value in case["action_growth_slopes"]),
        "closability": case["closability_defect"] == 0,
        "word_independence": case["word_independence_residual"] == 0,
    }
    full_pass = all(endpoint.values())
    if case["role"] in {"positive", "comparator_pass"}:
        expected_separation = full_pass
    elif case["role"] == "single_direction":
        expected_separation = rank == 1 and not full_pass
    else:
        expected_separation = not full_pass
    return {
        "id": case["id"],
        "role": case["role"],
        "exact_rank": rank,
        "endpoint": endpoint,
        "full_pass": full_pass,
        "expected_separation": expected_separation,
        "raw": case,
    }


def main() -> None:
    packet = json.loads((ROOT / "WITNESS_CASES.json").read_text())
    rows = [evaluate(case) for case in packet["cases"]]
    result = {
        "schema": "siel.public-calculation.bgce443.r3.witness-output.v1",
        "all_expected_separations": all(row["expected_separation"] for row in rows),
        "positive_dynamic_range": any(row["full_pass"] for row in rows)
        and any(not row["full_pass"] for row in rows),
        "rows": rows,
    }
    frozen = json.loads((ROOT / "WITNESS_RESULT.json").read_text())
    compact = {
        "schema": "siel.public-calculation.bgce443.r3.witness-result.v1",
        "all_expected_separations": result["all_expected_separations"],
        "positive_dynamic_range": result["positive_dynamic_range"],
        "rows": [
            {
                "id": row["id"],
                "role": row["role"],
                "exact_rank": row["exact_rank"],
                "full_pass": row["full_pass"],
                "expected_separation": row["expected_separation"],
            }
            for row in rows
        ],
        "raw_rows_path": "WITNESS_CASES.json",
        "harness_path": "witness_harness.py",
        "focal_source_used": False,
    }
    if compact != frozen:
        raise SystemExit("WITNESS_RESULT_MISMATCH")
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
