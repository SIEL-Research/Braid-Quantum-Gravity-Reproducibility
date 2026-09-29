#!/usr/bin/env python3
"""Regenerate the release manifest for the v1.0 evidence package."""

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FILES = [
    ".github/workflows/verify.yml",
    "CITATION.cff",
    "CLAIM_TEST_MAP.md",
    "EVIDENCE_REACHABILITY_AUDIT_v1.0.md",
    "LICENSE",
    "PROVENANCE.md",
    "README.md",
    "THEOREM_EVIDENCE_INDEX_v1.0.md",
    "VERIFICATION_SCOPE.md",
    "data/canonical_source_class_v099.json",
    "evidence/IMPORT_PROVENANCE.md",
    "evidence/evidence_integrity_v1.json",
    "evidence/public_url_audit_v1.json",
    "expected/source_verification_v099.json",
    "pyproject.toml",
    "requirements.txt",
    "scripts/build_manifest.py",
    "scripts/extract_theorem_inventory.py",
    "scripts/render_theorem_evidence_index.py",
    "scripts/verify_evidence_integrity.py",
    "scripts/verify_manifest.py",
    "scripts/verify_source.py",
    "scripts/verify_theorem_coverage_v1.py",
    "scripts/verify_vendored_packages.py",
    "src/bqg_v099/__init__.py",
    "src/bqg_v099/source.py",
    "tests/test_source.py",
    "theorems/analytic_proofs_v1.md",
    "theorems/theorem_evidence_v1.json",
    "theorems/theorem_inventory_v1.json"
]


def main() -> None:
    records = []
    for relative in FILES:
        payload = (ROOT / relative).read_bytes()
        records.append(
            {
                "path": relative,
                "size_bytes": len(payload),
                "sha256": hashlib.sha256(payload).hexdigest(),
            }
        )
    manifest = {
        "schema": "siel.bqg.reproduction.manifest.v2",
        "package_version": "1.0.0",
        "prepared_at": "2026-09-30",
        "release_state": "PUBLIC_RELEASE_1_0_0",
        "repository": "https://github.com/SIEL-Research/Braid-Quantum-Gravity-Reproducibility",
        "test_entrypoints": [
            "scripts/verify_source.py",
            "scripts/verify_theorem_coverage_v1.py",
            "scripts/verify_evidence_integrity.py",
            "scripts/verify_vendored_packages.py"
        ],
        "expected_status": "PASS",
        "claim_boundary": {
            "source_reconstruction": "EXECUTABLE_EXACT_VERIFICATION",
            "representatives": 8,
            "real_typed_orbits": 8,
            "physical_sector_selection": "OPEN",
            "paper_wide_evidence_reachability": "PASS",
            "paper_wide_independent_replication": "NOT_CLAIMED"
        },
        "files": records,
    }
    (ROOT / "MANIFEST.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
