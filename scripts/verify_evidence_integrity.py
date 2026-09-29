#!/usr/bin/env python3
"""Build or verify deterministic digests for every v1.0 local evidence path."""

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "theorems/theorem_evidence_v1.json"
MANIFEST = ROOT / "evidence/evidence_integrity_v1.json"


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evidence_record(relative: str) -> dict:
    path = ROOT / relative
    if path.is_file():
        return {
            "path": relative,
            "kind": "file",
            "file_count": 1,
            "size_bytes": path.stat().st_size,
            "sha256": file_digest(path),
        }

    files = sorted(item for item in path.rglob("*") if item.is_file())
    tree = hashlib.sha256()
    total = 0
    for item in files:
        inside = item.relative_to(path).as_posix()
        size = item.stat().st_size
        digest = file_digest(item)
        total += size
        tree.update(inside.encode("utf-8"))
        tree.update(b"\0")
        tree.update(str(size).encode("ascii"))
        tree.update(b"\0")
        tree.update(digest.encode("ascii"))
        tree.update(b"\n")
    return {
        "path": relative,
        "kind": "directory",
        "file_count": len(files),
        "size_bytes": total,
        "sha256_tree": tree.hexdigest(),
    }


def current_manifest() -> dict:
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    paths = sorted(
        {
            *ledger.get("supporting_evidence_paths", []),
            *(
                relative
                for entry in ledger["entries"]
                for relative in entry.get("evidence_paths", [])
            ),
        }
    )
    records = [evidence_record(relative) for relative in paths]
    return {
        "schema": "siel.bqg.evidence-integrity.v1",
        "manuscript_version": "v1.0",
        "algorithm": "sha256; directory digest over sorted path\\0size\\0file_sha256\\n records",
        "records": records,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    current = current_manifest()
    if args.write:
        MANIFEST.parent.mkdir(parents=True, exist_ok=True)
        MANIFEST.write_text(json.dumps(current, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps({"status": "WROTE", "records": len(current["records"])}))
        return

    expected = json.loads(MANIFEST.read_text(encoding="utf-8"))
    status = "PASS" if current == expected else "FAIL"
    print(
        json.dumps(
            {
                "status": status,
                "records": len(current["records"]),
                "expected_matches_current": current == expected,
            },
            indent=2,
            sort_keys=True,
        )
    )
    if status != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
