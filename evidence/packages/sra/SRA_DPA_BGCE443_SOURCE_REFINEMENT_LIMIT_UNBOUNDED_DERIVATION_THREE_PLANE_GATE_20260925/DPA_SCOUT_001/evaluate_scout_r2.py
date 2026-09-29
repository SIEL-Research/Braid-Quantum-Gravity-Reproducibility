#!/usr/bin/env python3
"""Attempt 0003: exact nonhomogeneous product witness and signed-sector comparator."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RAW = HERE / "RAW_OUTPUT_R2.json"
RESULT = HERE / "RESULT_R2.json"
BASE_PATH = HERE / "evaluate_scout.py"
spec = importlib.util.spec_from_file_location("bgce443_scout_base", BASE_PATH)
base = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = base
spec.loader.exec_module(base)


def digits(index: int) -> tuple[int, int, int]:
    return index // 25, (index // 5) % 5, index % 5


def product_energy(commutator: np.ndarray, local_vectors: list[np.ndarray]) -> Fraction:
    product = np.kron(np.kron(local_vectors[0], local_vectors[1]), local_vectors[2])
    numerator = np.vdot(product, 1j * commutator.astype(object) @ product)
    norm = np.vdot(product, product)
    assert numerator.imag == 0 and float(numerator.real).is_integer()
    assert norm.imag == 0 and float(norm.real).is_integer()
    return Fraction(int(numerator.real), 24 * int(norm.real))


def entry_product_witness(commutator: np.ndarray) -> dict:
    phases = (("+1", 1), ("-1", -1), ("+i", 1j), ("-i", -1j))
    for left, right in np.argwhere(np.triu(commutator != 0, 1)):
        left_digits, right_digits = digits(int(left)), digits(int(right))
        differing = [site for site in range(3) if left_digits[site] != right_digits[site]]
        for choices in itertools.product(phases, repeat=len(differing)):
            vectors = []
            labels = []
            choice_index = 0
            for site in range(3):
                vector = np.zeros(5, dtype=object)
                vector[left_digits[site]] = 1
                if site in differing:
                    label, phase = choices[choice_index]
                    choice_index += 1
                    vector[right_digits[site]] = phase
                    labels.append(f"e{left_digits[site]}{label}e{right_digits[site]}")
                else:
                    labels.append(f"e{left_digits[site]}")
                vectors.append(vector)
            energy = product_energy(commutator, vectors)
            if energy:
                conjugates = [np.conjugate(vector) for vector in vectors]
                conjugate_energy = product_energy(commutator, conjugates)
                assert conjugate_energy == -energy
                low, high = sorted((energy, conjugate_energy))
                return {
                    "found": True,
                    "source_matrix_entry": [int(left), int(right), int(commutator[left, right])],
                    "state": labels,
                    "energy": str(energy),
                    "conjugate_energy": str(conjugate_energy),
                    "exact_gap": str(high - low),
                    "all_n_lower_bound": f"({high - low})*(n-2)",
                    "all_n_domain": "integers n>=3",
                }
    return {"found": False, "exact_gap": "0"}


def main() -> None:
    assert not RAW.exists() and not RESULT.exists(), "NO_OVERWRITE"
    manifest = json.loads((HERE / "INPUT_MANIFEST.json").read_text())
    source = ROOT / manifest["input"]["path"]
    payload = source.read_bytes()
    assert hashlib.sha256(payload).hexdigest() == manifest["input"]["sha256"]
    snapshot = json.loads(payload)
    sectors = snapshot["sectors"]
    assert [row["mask"] for row in sectors] == manifest["expected_sector_masks"]
    reference = [base.dense(direction["commutator_numerator"]) for direction in sectors[0]["directions"]]
    rows = []
    for sector in sectors:
        relation = base.dense(sector["signed_relation"])
        generators = [base.dense(direction["commutator_numerator"]) for direction in sector["directions"]]
        rank = base.sparse_exact_rank(generators)
        directions = []
        for index, (direction, generator) in enumerate(zip(sector["directions"], generators)):
            product_witness = entry_product_witness(generator)
            comparator = (
                {"reference": True, "found": True}
                if sector["mask"] == 0
                else base.action_difference_witness(generator, reference[index])
            )
            directions.append({
                "direction": direction["direction"],
                "product_witness": product_witness,
                "signed_sector_vs_unsigned_reference": comparator,
            })
        rows.append({
            "mask": sector["mask"],
            "relation_checks": base.relation_checks(relation),
            "seed_rank": rank,
            "matrix_commutator_jacobi_zero": base.jacobi_zero(generators),
            "directions": directions,
        })
    all_relations = all(row["relation_checks"]["involution"] and row["relation_checks"]["braid_relation"] for row in rows)
    all_rank3 = all(row["seed_rank"]["rank"] == 3 for row in rows)
    all_gaps = all(direction["product_witness"]["found"] for row in rows for direction in row["directions"])
    all_specific = all(direction["signed_sector_vs_unsigned_reference"]["found"] for row in rows if row["mask"] != 0 for direction in row["directions"])
    all_jacobi = all(row["matrix_commutator_jacobi_zero"] for row in rows)
    passed = all_relations and all_rank3 and all_gaps and all_specific and all_jacobi
    raw = {
        "schema": "siel.dpa.scout.bgce443.raw-r2.v1",
        "scout_id": manifest["scout_id"],
        "attempt": 3,
        "input_sha256": manifest["input"]["sha256"],
        "retained_attempt_2_transport_covariance_raw_sha256": hashlib.sha256((HERE / "RAW_OUTPUT.json").read_bytes()).hexdigest(),
        "sector_rows": rows,
    }
    result = {
        "schema": "siel.dpa.scout.bgce443.result-r2.v1",
        "scout_id": manifest["scout_id"],
        "attempt": 3,
        "date": "2026-09-25",
        "primary_evidence_status": "Theoretical derivation",
        "decision": "CLOSED_SCOPED" if passed else "OPEN",
        "all_eight_relation_checks": all_relations,
        "all_eight_rank_three": all_rank3,
        "all_24_constructive_positive_gap_witnesses": all_gaps,
        "all_21_signed_sector_action_witnesses_vs_unsigned_reference": all_specific,
        "all_eight_exact_jacobi_checks": all_jacobi,
        "generated_lie_closure": passed,
        "anomaly_status": "NO_CENTRAL_ANOMALY_IN_DERIVATION_REPRESENTATION" if passed else "UNRESOLVED",
        "attempt_2_transport_comparator_interpretation": "SIGNED_AND_UNSIGNED_SUPPORT_TRANSPORT_ACTIONS_MATCH; RETAINED AS COVARIANCE, NOT USED AS SPECIFICITY",
        "claim_ceiling": "Source-generated all-eight-sector Braid-specific closable unbounded local derivation constraint algebra with exact finite-order Lie/Jacobi closure only. No moment-map identification, Hamiltonian/momentum typing, hypersurface-deformation algebra, continuum quantum gravity, empirical gravity, RPD result, confirmation, Level 3 or Official SIEL adoption."
    }
    RAW.write_text(json.dumps(raw, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    RESULT.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
