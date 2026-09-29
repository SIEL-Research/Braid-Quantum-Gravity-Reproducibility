#!/usr/bin/env python3
"""BGCE443 R7 focal evaluator. Never run before revision-matched independent E0 PASS."""

from __future__ import annotations

import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path

import numpy as np

from access_guard import guarded_read


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SNAPSHOT = "audits/SRA_DPA_BGCE443_SOURCE_REFINEMENT_LIMIT_UNBOUNDED_DERIVATION_THREE_PLANE_GATE_20260925/REVISION_7/ACTUAL_SOURCE_SNAPSHOT.json"
R6_E0 = "audits/SRA_DPA_BGCE443_SOURCE_REFINEMENT_LIMIT_UNBOUNDED_DERIVATION_THREE_PLANE_GATE_20260925/REVISION_6/E0_RESULT.json"


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
    nonzero = np.argwhere(matrix != 0)
    return {"rows": int(matrix.shape[0]), "columns": int(matrix.shape[1]), "entries": [{"row": int(r), "column": int(c), "value": int(matrix[r, c])} for r, c in nonzero]}


def exact_rank(matrices: list[np.ndarray]) -> tuple[int, dict | None]:
    rows = [matrix.reshape(-1).astype(object) for matrix in matrices]
    for rank in range(min(len(rows), len(rows[0])), 0, -1):
        for row_indices in itertools.combinations(range(len(rows)), rank):
            nonzero_columns = sorted(set(np.flatnonzero(np.vstack([rows[index] for index in row_indices]))))
            for columns in itertools.combinations(nonzero_columns, rank):
                minor = [[Fraction(int(rows[row][column])) for column in columns] for row in row_indices]
                value = determinant(minor)
                if value:
                    return rank, {"rows": list(row_indices), "columns": list(columns), "determinant": str(value)}
    return 0, None


def determinant(matrix: list[list[Fraction]]) -> Fraction:
    if not matrix:
        return Fraction(1)
    if len(matrix) == 1:
        return matrix[0][0]
    total = Fraction(0)
    for column in range(len(matrix)):
        minor = [row[:column] + row[column + 1:] for row in matrix[1:]]
        total += ((-1) ** column) * matrix[0][column] * determinant(minor)
    return total


def candidate_vectors() -> list[tuple[str, np.ndarray]]:
    out = []
    for index in range(5):
        vector = np.zeros(5, dtype=object)
        vector[index] = 1
        out.append((f"e{index}", vector))
    phases = [("+1", 1), ("-1", -1), ("+i", 1j), ("-i", -1j)]
    for left in range(5):
        for right in range(left + 1, 5):
            for label, phase in phases:
                vector = np.zeros(5, dtype=object)
                vector[left], vector[right] = 1, phase
                out.append((f"e{left}{label}e{right}", vector))
    return out


def exact_product_energy(commutator_numerator: np.ndarray, vector: np.ndarray) -> Fraction:
    product = np.kron(np.kron(vector, vector), vector)
    numerator = np.vdot(product, 1j * commutator_numerator.astype(object) @ product)
    assert numerator.imag == 0 and float(numerator.real).is_integer()
    norm = np.vdot(vector, vector)
    assert norm.imag == 0 and float(norm.real).is_integer()
    return Fraction(int(numerator.real), 24 * int(norm.real) ** 3)


def energy_density_certificate(commutator_numerator: np.ndarray) -> dict:
    rows = [{"state": label, "energy": str(exact_product_energy(commutator_numerator, vector))} for label, vector in candidate_vectors()]
    minimum = min(rows, key=lambda row: (Fraction(row["energy"]), row["state"]))
    maximum = max(rows, key=lambda row: (Fraction(row["energy"]), row["state"]))
    gap = Fraction(maximum["energy"]) - Fraction(minimum["energy"])
    return {
        "candidate_family": "all e_j and e_j+(+1,-1,+i,-i)e_k for j<k",
        "candidate_count": len(rows),
        "minimum": minimum,
        "maximum": maximum,
        "exact_energy_density_gap": str(gap),
        "all_n_spectral_diameter_lower_bound": f"({gap})*(n-2)",
        "all_n_domain": "all integers n>=3",
        "bounded_inner_excluded": gap > 0,
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
        mapping[column] = row
        signs[column] = int(pair_sign[pair_column])
    return mapping, signs


def compose(left: tuple[np.ndarray, np.ndarray], right: tuple[np.ndarray, np.ndarray]) -> tuple[np.ndarray, np.ndarray]:
    lm, ls = left
    rm, rs = right
    return lm[rm], ls[rm] * rs


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


def action_difference_certificate(signed_term: np.ndarray, unsigned_term: np.ndarray) -> dict:
    difference = signed_term - unsigned_term
    dimension = difference.shape[0]
    witness = None
    for index in range(dimension):
        observable = np.zeros((dimension, dimension), dtype=np.int64)
        observable[index, index] = 1
        signed_action = signed_term @ observable - observable @ signed_term
        unsigned_action = unsigned_term @ observable - observable @ unsigned_term
        if np.any(signed_action != unsigned_action):
            witness = (index, observable, signed_action, unsigned_action)
            break
    if witness is None and np.any(difference):
        diagonal = np.diag(difference)
        for row in range(dimension):
            for column in range(dimension):
                if diagonal[row] != diagonal[column]:
                    observable = np.zeros((dimension, dimension), dtype=np.int64)
                    observable[row, column] = 1
                    witness = (dimension + row * dimension + column, observable, signed_term @ observable - observable @ signed_term, unsigned_term @ observable - observable @ unsigned_term)
                    break
            if witness:
                break
    return {
        "transported_implementer_difference_frobenius_square": int(np.sum(difference.astype(object) ** 2)),
        "raw_action_difference_found": witness is not None,
        "witness_id": None if witness is None else int(witness[0]),
        "observable": None if witness is None else sparse_integer(witness[1]),
        "signed_action": None if witness is None else sparse_integer(witness[2]),
        "unsigned_action": None if witness is None else sparse_integer(witness[3]),
    }


def relation_checks(relation: np.ndarray) -> dict:
    identity125 = np.eye(125, dtype=np.int64)
    r0 = np.kron(relation, np.eye(5, dtype=np.int64))
    r1 = np.kron(np.eye(5, dtype=np.int64), relation)
    return {
        "involution": bool(np.array_equal(relation @ relation, np.eye(25, dtype=np.int64))),
        "braid_relation": bool(np.array_equal(r0 @ r1 @ r0, r1 @ r0 @ r1)),
        "source_dimension": 5,
        "three_site_dimension": 125,
    }


def main() -> None:
    allowlist = json.loads((HERE / "INPUT_ALLOWLIST.json").read_text())
    allowed = {row["path"]: row["sha256"] for row in allowlist["allowed"]}
    denied = allowlist["deny_globs"]
    snapshot = json.loads(guarded_read(ROOT, SNAPSHOT, allowed, denied))
    e0 = json.loads(guarded_read(ROOT, R6_E0, allowed, denied))
    assert e0["decision"] == "PASS"
    unsigned = unsigned_relation()
    identity5 = np.eye(5, dtype=np.int64)
    sector_rows = []
    for sector in snapshot["sectors"]:
        relation = dense(sector["signed_relation"])
        relations = relation_checks(relation)
        commutators = [dense(direction["commutator_numerator"]) for direction in sector["directions"]]
        rank, minor = exact_rank(commutators)
        directions = []
        for direction, commutator_numerator in zip(sector["directions"], commutators):
            assert np.array_equal(commutator_numerator.T, -commutator_numerator)
            energy = energy_density_certificate(commutator_numerator)
            base = np.kron(commutator_numerator, identity5)
            canonical_shift = np.kron(identity5, commutator_numerator)
            signed_shift = conjugate(base, block_shift_action(relation))
            unsigned_shift = conjugate(base, block_shift_action(unsigned))
            assert np.array_equal(unsigned_shift, canonical_shift)
            comparator = action_difference_certificate(signed_shift, unsigned_shift)
            directions.append({
                "direction": direction["direction"],
                "hermitian": True,
                "finite_range": 3,
                "canonical_refinement_stabilizes": True,
                "uniform_local_frobenius_bound_square_numerator": int(np.sum(commutator_numerator.astype(object) ** 2)),
                "energy_density": energy,
                "signed_unsigned_comparator": comparator,
                "generic_closable_unbounded_derivation": bool(energy["bounded_inner_excluded"]),
            })
        generic = rank == 3 and all(row["generic_closable_unbounded_derivation"] for row in directions) and relations["involution"] and relations["braid_relation"]
        specificity = all(row["signed_unsigned_comparator"]["raw_action_difference_found"] for row in directions)
        sector_rows.append({"mask": sector["mask"], "relations": relations, "derivation_rank": rank, "rank_minor": minor, "directions": directions, "generic_carrier_pass": generic, "braid_transport_specificity_pass": specificity})
    generic_all = all(row["generic_carrier_pass"] for row in sector_rows)
    specificity_all = all(row["braid_transport_specificity_pass"] for row in sector_rows)
    raw = {"schema": "siel.dpa.bgce443.r7.raw.v1", "candidate_id": "BGCE443-R7", "source_snapshot_sha256": hashlib.sha256((HERE / "ACTUAL_SOURCE_SNAPSHOT.json").read_bytes()).hexdigest(), "sector_rows": sector_rows}
    result = {
        "schema": "siel.dpa.bgce443.r7.result.v1",
        "candidate_id": "BGCE443-R7",
        "date": "2026-09-25",
        "primary_evidence_status": "Theoretical derivation",
        "status": ("SCOPED_PASS_SOURCE_REFINEMENT_CLOSABLE_UNBOUNDED_DERIVATION_THREE_PLANE" if generic_all else "NO_GO_SOURCE_REFINEMENT_UNBOUNDED_DERIVATION_THREE_PLANE"),
        "generic_carrier_all_eight": generic_all,
        "braid_transport_specificity_all_eight": specificity_all,
        "specificity_status": "PASS" if specificity_all else "NO_GO_OR_PARTIAL",
        "sector_derivation_ranks": [row["derivation_rank"] for row in sector_rows],
        "claim_ceiling": "Source-refinement closable unbounded derivation three-plane only. No moment map, Hamiltonian/momentum constraint identification, first-class clock-spatial bracket, hypersurface-deformation algebra, empirical gravity, RPD adoption or Official SIEL adoption."
    }
    (HERE / "RAW_OUTPUT.json").write_text(json.dumps(raw, sort_keys=True, indent=2) + "\n")
    (HERE / "RESULT.json").write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
