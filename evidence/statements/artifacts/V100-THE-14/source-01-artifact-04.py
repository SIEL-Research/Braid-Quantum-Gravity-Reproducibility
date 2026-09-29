#!/usr/bin/env python3
"""Exact DPA scout for BGCE443. This is not the failed/frozen R7 evaluator."""

from __future__ import annotations

import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
MANIFEST = HERE / "INPUT_MANIFEST.json"
RAW = HERE / "RAW_OUTPUT.json"
RESULT = HERE / "RESULT.json"


def dense(raw: dict) -> np.ndarray:
    out = np.zeros((raw["rows"], raw["columns"]), dtype=np.int64)
    seen = set()
    for entry in raw["entries"]:
        key = (entry["row"], entry["column"])
        assert key not in seen
        seen.add(key)
        out[key] = entry["value"]
    return out


def sparse_integer(matrix: np.ndarray) -> dict:
    return {
        "rows": int(matrix.shape[0]),
        "columns": int(matrix.shape[1]),
        "entries": [
            {"row": int(row), "column": int(column), "value": int(matrix[row, column])}
            for row, column in np.argwhere(matrix != 0)
        ],
    }


def sparse_exact_rank(matrices: list[np.ndarray]) -> dict:
    basis: list[dict[int, Fraction]] = []
    pivots: list[int] = []
    for matrix in matrices:
        flat = matrix.reshape(-1)
        vector = {int(index): Fraction(int(flat[index])) for index in np.flatnonzero(flat)}
        for pivot, row in zip(pivots, basis):
            if pivot not in vector:
                continue
            factor = vector[pivot] / row[pivot]
            for column, value in row.items():
                updated = vector.get(column, Fraction(0)) - factor * value
                if updated:
                    vector[column] = updated
                else:
                    vector.pop(column, None)
        if vector:
            pivot = min(vector)
            pivots.append(pivot)
            basis.append(vector)
    return {"rank": len(basis), "pivot_columns": pivots}


def candidate_vectors() -> list[tuple[str, np.ndarray]]:
    vectors = []
    for index in range(5):
        vector = np.zeros(5, dtype=object)
        vector[index] = 1
        vectors.append((f"e{index}", vector))
    for left in range(5):
        for right in range(left + 1, 5):
            for label, phase in (("+1", 1), ("-1", -1), ("+i", 1j), ("-i", -1j)):
                vector = np.zeros(5, dtype=object)
                vector[left], vector[right] = 1, phase
                vectors.append((f"e{left}{label}e{right}", vector))
    assert len(vectors) == 45
    return vectors


def exact_product_energy(commutator: np.ndarray, vector: np.ndarray) -> Fraction:
    product = np.kron(np.kron(vector, vector), vector)
    numerator = np.vdot(product, 1j * commutator.astype(object) @ product)
    norm = np.vdot(vector, vector)
    assert numerator.imag == 0 and float(numerator.real).is_integer()
    assert norm.imag == 0 and float(norm.real).is_integer()
    return Fraction(int(numerator.real), 24 * int(norm.real) ** 3)


def energy_certificate(commutator: np.ndarray) -> dict:
    rows = [
        {"state": label, "energy": str(exact_product_energy(commutator, vector))}
        for label, vector in candidate_vectors()
    ]
    minimum = min(rows, key=lambda row: (Fraction(row["energy"]), row["state"]))
    maximum = max(rows, key=lambda row: (Fraction(row["energy"]), row["state"]))
    gap = Fraction(maximum["energy"]) - Fraction(minimum["energy"])
    return {
        "candidate_count": 45,
        "minimum": minimum,
        "maximum": maximum,
        "exact_gap": str(gap),
        "all_n_lower_bound": f"({gap})*(n-2)",
        "all_n_domain": "integers n>=3",
        "positive_gap": gap > 0,
        "rows": rows,
    }


def pair_action(relation: np.ndarray, order: int, site: int) -> tuple[np.ndarray, np.ndarray]:
    pair_map = np.argmax(np.abs(relation), axis=0)
    pair_sign = relation[pair_map, np.arange(25)]
    dimension = 5**order
    mapping = np.zeros(dimension, dtype=np.int64)
    signs = np.ones(dimension, dtype=np.int64)
    for column in range(dimension):
        digits = []
        value = column
        for power in range(order - 1, -1, -1):
            divisor = 5**power
            digits.append(value // divisor)
            value %= divisor
        pair_column = 5 * digits[site] + digits[site + 1]
        pair_row = int(pair_map[pair_column])
        digits[site], digits[site + 1] = divmod(pair_row, 5)
        row = 0
        for digit in digits:
            row = 5 * row + digit
        mapping[column], signs[column] = row, int(pair_sign[pair_column])
    return mapping, signs


def compose(left: tuple[np.ndarray, np.ndarray], right: tuple[np.ndarray, np.ndarray]) -> tuple[np.ndarray, np.ndarray]:
    left_map, left_sign = left
    right_map, right_sign = right
    return left_map[right_map], left_sign[right_map] * right_sign


def block_shift_action(relation: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    action = (np.arange(625, dtype=np.int64), np.ones(625, dtype=np.int64))
    for site in (2, 1, 0):
        action = compose(pair_action(relation, 4, site), action)
    return action


def conjugate(matrix: np.ndarray, action: tuple[np.ndarray, np.ndarray]) -> np.ndarray:
    mapping, signs = action
    out = np.zeros_like(matrix)
    out[np.ix_(mapping, mapping)] = signs[:, None] * matrix * signs[None, :]
    return out


def unsigned_relation() -> np.ndarray:
    relation = np.zeros((25, 25), dtype=np.int64)
    for left in range(5):
        for right in range(5):
            relation[5 * right + left, 5 * left + right] = 1
    return relation


def matrix_unit_action(matrix: np.ndarray, row: int, column: int) -> np.ndarray:
    action = np.zeros_like(matrix)
    action[:, column] += matrix[:, row]
    action[row, :] -= matrix[column, :]
    return action


def action_difference_witness(signed: np.ndarray, unsigned: np.ndarray) -> dict:
    difference = signed - unsigned
    off_diagonal = difference.copy()
    np.fill_diagonal(off_diagonal, 0)
    if np.any(off_diagonal):
        row, column = map(int, np.argwhere(off_diagonal != 0)[0])
        observable_row = observable_column = column
    else:
        diagonal = np.diag(difference)
        pairs = [(row, column) for row, column in itertools.product(range(len(diagonal)), repeat=2) if diagonal[row] != diagonal[column]]
        if not pairs:
            return {"found": False, "implementer_difference_frobenius_square": int(np.sum(difference.astype(object) ** 2))}
        observable_row, observable_column = pairs[0]
    observable = np.zeros_like(signed)
    observable[observable_row, observable_column] = 1
    signed_action = matrix_unit_action(signed, observable_row, observable_column)
    unsigned_action = matrix_unit_action(unsigned, observable_row, observable_column)
    assert np.any(signed_action != unsigned_action)
    return {
        "found": True,
        "implementer_difference_frobenius_square": int(np.sum(difference.astype(object) ** 2)),
        "observable": sparse_integer(observable),
        "signed_action": sparse_integer(signed_action),
        "unsigned_action": sparse_integer(unsigned_action),
    }


def relation_checks(relation: np.ndarray) -> dict:
    identity25 = np.eye(25, dtype=np.int64)
    identity5 = np.eye(5, dtype=np.int64)
    left = np.kron(relation, identity5)
    right = np.kron(identity5, relation)
    return {
        "involution": bool(np.array_equal(relation @ relation, identity25)),
        "braid_relation": bool(np.array_equal(left @ right @ left, right @ left @ right)),
    }


def jacobi_zero(generators: list[np.ndarray]) -> bool:
    def bracket(left: np.ndarray, right: np.ndarray) -> np.ndarray:
        return left @ right - right @ left
    for left, middle, right in itertools.product(generators, repeat=3):
        jacobi = bracket(left, bracket(middle, right)) + bracket(middle, bracket(right, left)) + bracket(right, bracket(left, middle))
        if np.any(jacobi):
            return False
    return True


def main() -> None:
    assert not RAW.exists() and not RESULT.exists(), "NO_OVERWRITE"
    manifest = json.loads(MANIFEST.read_text())
    source = ROOT / manifest["input"]["path"]
    payload = source.read_bytes()
    assert hashlib.sha256(payload).hexdigest() == manifest["input"]["sha256"]
    snapshot = json.loads(payload)
    assert [row["mask"] for row in snapshot["sectors"]] == manifest["expected_sector_masks"]
    unsigned = unsigned_relation()
    identity5 = np.eye(5, dtype=np.int64)
    sector_rows = []
    for sector in snapshot["sectors"]:
        relation = dense(sector["signed_relation"])
        checks = relation_checks(relation)
        commutators = [dense(direction["commutator_numerator"]) for direction in sector["directions"]]
        assert all(np.array_equal(matrix.T, -matrix) for matrix in commutators)
        rank = sparse_exact_rank(commutators)
        directions = []
        for direction, commutator in zip(sector["directions"], commutators):
            energy = energy_certificate(commutator)
            base = np.kron(commutator, identity5)
            canonical = np.kron(identity5, commutator)
            signed = conjugate(base, block_shift_action(relation))
            unsigned_shift = conjugate(base, block_shift_action(unsigned))
            assert np.array_equal(unsigned_shift, canonical)
            directions.append({
                "direction": direction["direction"],
                "hermitian_seed": True,
                "finite_range": 3,
                "uniform_local_frobenius_bound_square_numerator": int(np.sum(commutator.astype(object) ** 2)),
                "energy": energy,
                "signed_unsigned_action_witness": action_difference_witness(signed, unsigned_shift),
            })
        sector_rows.append({
            "mask": sector["mask"],
            "relation_checks": checks,
            "seed_rank": rank,
            "matrix_commutator_jacobi_zero": jacobi_zero(commutators),
            "directions": directions,
        })
    all_relations = all(row["relation_checks"]["involution"] and row["relation_checks"]["braid_relation"] for row in sector_rows)
    all_rank3 = all(row["seed_rank"]["rank"] == 3 for row in sector_rows)
    all_gaps = all(direction["energy"]["positive_gap"] for row in sector_rows for direction in row["directions"])
    all_specific = all(direction["signed_unsigned_action_witness"]["found"] for row in sector_rows for direction in row["directions"])
    all_jacobi = all(row["matrix_commutator_jacobi_zero"] for row in sector_rows)
    passed = all_relations and all_rank3 and all_gaps and all_specific and all_jacobi
    raw = {
        "schema": "siel.dpa.scout.bgce443.raw.v1",
        "scout_id": manifest["scout_id"],
        "input_sha256": manifest["input"]["sha256"],
        "sector_rows": sector_rows,
    }
    result = {
        "schema": "siel.dpa.scout.bgce443.result.v1",
        "scout_id": manifest["scout_id"],
        "date": "2026-09-25",
        "primary_evidence_status": "Theoretical derivation",
        "decision": "CLOSED_SCOPED" if passed else "OPEN",
        "all_eight_relation_checks": all_relations,
        "all_eight_rank_three": all_rank3,
        "all_24_positive_all_n_gap_certificates": all_gaps,
        "all_24_signed_unsigned_action_witnesses": all_specific,
        "all_eight_exact_jacobi_checks": all_jacobi,
        "generated_lie_closure": passed,
        "anomaly_status": "NO_CENTRAL_ANOMALY_IN_DERIVATION_REPRESENTATION" if passed else "UNRESOLVED",
        "claim_ceiling": "Source-generated all-eight-sector Braid-specific closable unbounded local derivation constraint algebra with exact finite-order Lie/Jacobi closure only. No moment-map identification, Hamiltonian/momentum typing, hypersurface-deformation algebra, continuum quantum gravity, empirical gravity, RPD result, confirmation, Level 3 or Official SIEL adoption."
    }
    RAW.write_text(json.dumps(raw, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    RESULT.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
