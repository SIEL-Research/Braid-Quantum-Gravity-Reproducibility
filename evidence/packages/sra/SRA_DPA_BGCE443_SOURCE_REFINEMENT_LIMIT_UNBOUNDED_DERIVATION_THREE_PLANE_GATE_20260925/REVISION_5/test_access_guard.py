#!/usr/bin/env python3
from __future__ import annotations

import json
import hashlib
import tempfile
import unittest
from pathlib import Path

from access_guard import AccessDenied, guarded_read


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
R5_ALLOWLIST = HERE / "INPUT_ALLOWLIST.json"


class AccessGuardTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        packet = json.loads(R5_ALLOWLIST.read_text())
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

    def test_symlink_rejected_before_read(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            target = root / "target.bin"
            target.write_bytes(b"allowed payload")
            link = root / "link.bin"
            link.symlink_to(target)
            allowed = {"link.bin": hashlib.sha256(target.read_bytes()).hexdigest()}
            with self.assertRaisesRegex(AccessDenied, "SYMLINK_PATH"):
                guarded_read(root, "link.bin", allowed, [])

    def test_hash_mismatch_rejected_before_return(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            target = root / "payload.bin"
            target.write_bytes(b"actual payload")
            allowed = {"payload.bin": hashlib.sha256(b"different payload").hexdigest()}
            with self.assertRaisesRegex(AccessDenied, "HASH_MISMATCH"):
                guarded_read(root, "payload.bin", allowed, [])


if __name__ == "__main__":
    unittest.main()
