#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
FILES = [
    "AUDIT_JA.md",
    "PBM_COVARIANT_TRANSPORT_JETS_PARTIAL_v1.json",
    "RESULT.json",
    "evaluate.py",
    "finalize.py",
    "make_manifest.py",
    "verify.py",
]


def main():
    rows = []
    for name in FILES:
        p = HERE / name
        rows.append({"path": str(p.relative_to(HERE.parents[1])),
                     "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
                     "bytes": p.stat().st_size})
    (HERE / "MANIFEST.json").write_text(json.dumps({
        "schema": "siel.audit.manifest.v1", "date": "2026-09-13", "files": rows
    }, indent=2) + "\n")


if __name__ == "__main__":
    main()
