#!/usr/bin/env python3
"""Fail unless every v0.99 theorem-like statement has public evidence."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ALLOWED = {"PUBLIC_PROOF", "PUBLIC_CODE", "EXTERNAL_THEOREM_REDUCTION"}


def main() -> None:
    inventory = json.loads((ROOT / "theorems/theorem_inventory_v099.json").read_text(encoding="utf-8"))
    ledger = json.loads((ROOT / "theorems/theorem_evidence_v099.json").read_text(encoding="utf-8"))
    expected = {record["id"] for record in inventory["records"]}
    entries = ledger["entries"]
    actual = {entry["id"] for entry in entries}
    failures = []
    if expected != actual:
        failures.append(
            {
                "error": "inventory_mismatch",
                "missing": sorted(expected - actual),
                "extra": sorted(actual - expected),
            }
        )
    for entry in entries:
        if entry["status"] not in ALLOWED:
            failures.append({"id": entry["id"], "error": "unclosed_status", "status": entry["status"]})
        for relative in entry.get("evidence_files", []):
            if not (ROOT / relative).is_file():
                failures.append({"id": entry["id"], "error": "missing_evidence_file", "path": relative})
        if not entry.get("verification_command") and entry["status"] == "PUBLIC_CODE":
            failures.append({"id": entry["id"], "error": "missing_verification_command"})
        if not entry.get("claim_ceiling"):
            failures.append({"id": entry["id"], "error": "missing_claim_ceiling"})
    result = {
        "status": "PASS" if not failures else "FAIL",
        "inventory_total": len(expected),
        "closed_entries": sum(entry["status"] in ALLOWED for entry in entries),
        "failures": failures,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
