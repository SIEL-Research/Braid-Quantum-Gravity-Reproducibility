#!/usr/bin/env python3
"""Render the v1.0 theorem-to-evidence ledger as a reader-facing index."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "THEOREM_EVIDENCE_INDEX_v1.0.md"


def link(path: str) -> str:
    label = Path(path).name
    return f"[`{label}`]({path})"


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
    evidence = {entry["id"]: entry for entry in ledger["entries"]}
    paper_locator = {entry["id"]: entry for entry in locators["entries"]}

    lines = [
        "# v1.0 Theorem Evidence Index",
        "",
        "This is the public navigation layer for all 53 theorem-like statements in the",
        "v1.0 manuscript. Each row points to repository-local proof or executable",
        "evidence, or to a checked external theorem reduction. `PASS` here means that",
        "the evidence path is complete and addressable; it does not enlarge the claim",
        "ceiling printed in the final column.",
        "",
        "Run `python3 scripts/verify_theorem_coverage_v1.py` to check inventory",
        "completeness and every local locator. Run `python3 scripts/verify_source.py`",
        "for the canonical-source exact reconstruction. Run",
        "`python3 scripts/verify_vendored_packages.py` for the canonical vendored",
        "verifiers and public adapters; supporting inputs are hash-bound separately.",
        "",
        "The paper locator gives the printed theorem, proposition or corollary",
        "number and the physical PDF page in the fixed v1 manuscript.",
        "",
        "| ID | Paper locator | Statement | Evidence class | Evidence | Claim ceiling |",
        "|---|---|---|---|---|---|",
    ]

    for record in inventory["records"]:
        entry = evidence[record["id"]]
        locator = paper_locator[record["id"]]
        locators = [link(path) for path in entry.get("evidence_paths", [])]
        locators.extend(f"[external source]({url})" for url in entry.get("public_urls", []))
        ceiling = entry["claim_ceiling"].replace("|", "\\|")
        title = record["title"].replace("|", "\\|")
        anchored_id = f'<a id="{record["id"]}"></a>`{record["id"]}`'
        lines.append(
            f"| {anchored_id} | {locator['paper_number']}, PDF p. {locator['pdf_page']} | "
            f"{title} | `{entry['status']}` | "
            f"{'<br>'.join(locators)} | {ceiling} |"
        )

    lines.extend(
        [
            "",
            "## What this gate does and does not establish",
            "",
            "The index removes the former evidence-screening defect: no theorem-like",
            "statement terminates at a private path, mutable task ledger or unexplained",
            "internal identifier. The vendored packages retain the calculation code,",
            "frozen inputs where used, raw output, adjudicated result and audit report.",
            "",
            "The gate is an evidence-reachability result, not an independent replication",
            "of all 53 statements. Scientific validity remains bounded by each theorem's",
            "hypotheses and claim ceiling. The CKM entries remain a retrospective",
            "registered reproducibility confirmation, not a prospective prediction.",
            "",
        ]
    )
    OUT.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
