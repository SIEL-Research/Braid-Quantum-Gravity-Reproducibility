#!/usr/bin/env python3
from __future__ import annotations

import json
import unittest
from pathlib import Path

from access_guard import AccessDenied, guarded_read


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
R4_ALLOWLIST = HERE / "INPUT_ALLOWLIST.json"


class AccessGuardTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        packet = json.loads(R4_ALLOWLIST.read_text())
        cls.allowed = {row["path"]: row["sha256"] for row in packet["allowed"]}
        cls.denied = packet["deny_globs"]

    def test_allowed_hash_bound_source(self) -> None:
        path = "audits/SRA_DPA_BGCE075_MIXED_BRACKET_TO_TEMPORAL_METRIC_VECTOR_RANK_GATE_20260919/RESULT.json"
        self.assertTrue(guarded_read(REPO, path, self.allowed, self.denied))

    def test_denied_r1_result(self) -> None:
        path = "audits/SRA_DPA_BGCE443_SOURCE_REFINEMENT_LIMIT_UNBOUNDED_DERIVATION_THREE_PLANE_GATE_20260925/RESULT.json"
        with self.assertRaises(AccessDenied):
            guarded_read(REPO, path, self.allowed, self.denied)

    def test_denied_r2_glob(self) -> None:
        path = "audits/SRA_DPA_BGCE443_SOURCE_REFINEMENT_LIMIT_UNBOUNDED_DERIVATION_THREE_PLANE_GATE_20260925/REVISION_2/STATUS.json"
        with self.assertRaises(AccessDenied):
            guarded_read(REPO, path, self.allowed, self.denied)

    def test_absolute_and_traversal_rejected(self) -> None:
        for path in ["/etc/passwd", "../RESULT.json"]:
            with self.assertRaises(AccessDenied):
                guarded_read(REPO, path, self.allowed, self.denied)

    def test_unlisted_source_rejected(self) -> None:
        with self.assertRaises(AccessDenied):
            guarded_read(REPO, "AGENTS.md", self.allowed, self.denied)


if __name__ == "__main__":
    unittest.main()
