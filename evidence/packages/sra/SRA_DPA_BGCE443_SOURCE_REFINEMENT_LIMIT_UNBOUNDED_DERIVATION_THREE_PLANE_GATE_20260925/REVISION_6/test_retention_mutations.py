#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import unittest
from pathlib import Path

from validate_retention import dense, matrix_hash, validate


HERE = Path(__file__).resolve().parent


class RetentionMutationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = json.loads((HERE / "WITNESS_RESULT.json").read_text())
        cls.schema = json.loads((HERE / "RAW_ROW_SCHEMA.json").read_text())

    def rejected(self, mutated: dict) -> None:
        with self.assertRaises(AssertionError):
            validate(mutated, self.schema)

    def test_decision_mutation_rejected(self) -> None:
        mutated = copy.deepcopy(self.result)
        mutated["matched_comparator"]["generic_carrier_decision"] = "FAIL"
        mutated["matched_comparator"]["transport_specificity_decision"] = "NO_GO_IDENTICAL_RAW_ACTION"
        self.rejected(mutated)

    def test_relation_certificate_mutation_rejected(self) -> None:
        mutated = copy.deepcopy(self.result)
        for transport in ("signed", "unsigned"):
            for key in mutated["matched_comparator"][f"{transport}_relation_certificate"]["certificate"]:
                mutated["matched_comparator"][f"{transport}_relation_certificate"]["certificate"][key] = False
        self.rejected(mutated)

    def test_rank_determinant_mutation_rejected(self) -> None:
        mutated = copy.deepcopy(self.result)
        mutated["positive"]["rank"]["nonzero_minor"]["determinant"] = "999"
        self.rejected(mutated)

    def test_action_hash_mutation_rejected_even_with_aggregate_update(self) -> None:
        mutated = copy.deepcopy(self.result)
        rows = mutated["matched_comparator"]["raw_action_rows_retained"]["signed"]
        for index, row in enumerate(rows):
            row["action_sha256"] = hashlib.sha256(f"fabricated-{index}".encode()).hexdigest()
        payload = [row["action_sha256"] for row in rows]
        mutated["matched_comparator"]["signed_raw_action_sha256"] = hashlib.sha256(json.dumps(payload, separators=(",", ":")).encode()).hexdigest()
        mutated["matched_comparator"]["differing_raw_action_rows"] = 16
        self.rejected(mutated)

    def test_raw_action_mutation_rejected_even_with_hash_update(self) -> None:
        mutated = copy.deepcopy(self.result)
        rows = mutated["matched_comparator"]["raw_action_rows_retained"]["signed"]
        rows[0]["action_sparse"]["entries"][0]["value"] = "999"
        rows[0]["action_sha256"] = matrix_hash(dense(rows[0]["action_sparse"]))
        payload = [row["action_sha256"] for row in rows]
        mutated["matched_comparator"]["signed_raw_action_sha256"] = hashlib.sha256(json.dumps(payload, separators=(",", ":")).encode()).hexdigest()
        mutated["matched_comparator"]["differing_raw_action_rows"] = 16
        self.rejected(mutated)


if __name__ == "__main__":
    unittest.main()
