#!/usr/bin/env python3
"""Verify sizes and SHA-256 hashes declared in MANIFEST.json."""

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    manifest = json.loads((ROOT / "MANIFEST.json").read_text(encoding="utf-8"))
    failures = []
    for record in manifest["files"]:
        path = ROOT / record["path"]
        if not path.is_file():
            failures.append({"path": record["path"], "error": "missing"})
            continue
        payload = path.read_bytes()
        actual_size = len(payload)
        actual_hash = hashlib.sha256(payload).hexdigest()
        if actual_size != record["size_bytes"] or actual_hash != record["sha256"]:
            failures.append(
                {
                    "path": record["path"],
                    "expected_size": record["size_bytes"],
                    "actual_size": actual_size,
                    "expected_sha256": record["sha256"],
                    "actual_sha256": actual_hash,
                }
            )
    result = {"status": "PASS" if not failures else "FAIL", "files_checked": len(manifest["files"]), "failures": failures}
    print(json.dumps(result, indent=2, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
