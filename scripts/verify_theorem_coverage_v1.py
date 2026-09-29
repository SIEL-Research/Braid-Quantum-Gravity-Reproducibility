#!/usr/bin/env python3
"""Fail unless every v1.0 theorem-like statement has reachable evidence."""

import json
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
ALLOWED = {"PUBLIC_PROOF", "PUBLIC_CODE", "EXTERNAL_THEOREM_REDUCTION"}
RESULT_NAMES = {"RESULT.json", "CERTIFICATE.json", "PROOF_CERTIFICATE.json"}


def valid_https_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def directory_has_executable_and_result(path: Path) -> tuple[bool, bool]:
    files = [item for item in path.rglob("*") if item.is_file()]
    has_executable = any(
        item.suffix == ".py" and item.name != "__init__.py" for item in files
    )
    has_result = any(item.name in RESULT_NAMES for item in files)
    return has_executable, has_result


def main() -> None:
    inventory = json.loads(
        (ROOT / "theorems/theorem_inventory_v1.json").read_text(encoding="utf-8")
    )
    ledger = json.loads(
        (ROOT / "theorems/theorem_evidence_v1.json").read_text(encoding="utf-8")
    )
    locators = json.loads(
        (ROOT / "theorems/paper_locator_v1.json").read_text(encoding="utf-8")
    )
    expected = {record["id"] for record in inventory["records"]}
    entries = ledger["entries"]
    actual = {entry["id"] for entry in entries}
    locator_entries = locators["entries"]
    locator_ids = {entry["id"] for entry in locator_entries}
    failures: list[dict] = []

    if inventory["counts"]["total"] != 53:
        failures.append(
            {
                "error": "unexpected_inventory_total",
                "expected": 53,
                "actual": inventory["counts"]["total"],
            }
        )
    if len(actual) != len(entries):
        failures.append({"error": "duplicate_evidence_id"})
    if expected != actual:
        failures.append(
            {
                "error": "inventory_mismatch",
                "missing": sorted(expected - actual),
                "extra": sorted(actual - expected),
            }
        )
    if len(locator_ids) != len(locator_entries):
        failures.append({"error": "duplicate_paper_locator_id"})
    if expected != locator_ids:
        failures.append(
            {
                "error": "paper_locator_inventory_mismatch",
                "missing": sorted(expected - locator_ids),
                "extra": sorted(locator_ids - expected),
            }
        )
    paper_numbers = [entry.get("paper_number") for entry in locator_entries]
    if len(set(paper_numbers)) != len(paper_numbers):
        failures.append({"error": "duplicate_paper_number"})
    for locator in locator_entries:
        if not locator.get("paper_number") or not isinstance(locator.get("pdf_page"), int):
            failures.append({"id": locator.get("id"), "error": "invalid_paper_locator"})

    proof_text = (ROOT / "theorems/analytic_proofs_v1.md").read_text(encoding="utf-8")

    for entry in entries:
        evidence_paths = entry.get("evidence_paths", [])
        public_urls = entry.get("public_urls", [])
        status = entry.get("status")

        if status not in ALLOWED:
            failures.append({"id": entry["id"], "error": "unclosed_status", "status": status})
        if not evidence_paths and not public_urls:
            failures.append({"id": entry["id"], "error": "no_evidence_locator"})
        if not entry.get("claim_ceiling"):
            failures.append({"id": entry["id"], "error": "missing_claim_ceiling"})

        local_code = False
        package_code = False
        package_result = False
        for relative in evidence_paths:
            path = ROOT / relative
            if not path.exists():
                failures.append({"id": entry["id"], "error": "missing_evidence_path", "path": relative})
                continue
            if path.is_file() and path.suffix == ".py":
                local_code = True
            if path.is_dir():
                has_code, has_result = directory_has_executable_and_result(path)
                package_code = package_code or has_code
                package_result = package_result or has_result

        for url in public_urls:
            if not valid_https_url(url):
                failures.append({"id": entry["id"], "error": "invalid_public_url", "url": url})

        if status == "PUBLIC_CODE":
            local_runner = bool(entry.get("verification_command")) and local_code
            vendored_package = package_code and package_result
            external_runner = bool(entry.get("verification_command")) and bool(public_urls)
            if not (local_runner or vendored_package or external_runner):
                failures.append(
                    {
                        "id": entry["id"],
                        "error": "public_code_lacks_runner_or_complete_package",
                    }
                )
        elif status in {"PUBLIC_PROOF", "EXTERNAL_THEOREM_REDUCTION"}:
            if entry["id"] not in proof_text:
                failures.append({"id": entry["id"], "error": "proof_heading_missing"})
            if status == "EXTERNAL_THEOREM_REDUCTION" and not public_urls:
                failures.append({"id": entry["id"], "error": "external_reduction_lacks_public_source"})

    result = {
        "status": "PASS" if not failures else "FAIL",
        "inventory_total": len(expected),
        "paper_locators": len(locator_ids),
        "closed_entries": sum(entry.get("status") in ALLOWED for entry in entries),
        "public_code": sum(entry.get("status") == "PUBLIC_CODE" for entry in entries),
        "public_proof": sum(entry.get("status") == "PUBLIC_PROOF" for entry in entries),
        "external_theorem_reduction": sum(
            entry.get("status") == "EXTERNAL_THEOREM_REDUCTION" for entry in entries
        ),
        "failures": failures,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
