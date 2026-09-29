#!/usr/bin/env python3
"""Generate English, reader-facing evidence pages for every v1 statement."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence/statements"
MANIFESTS = OUT / "manifests"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_digest(path: Path) -> tuple[str, int]:
    digest = hashlib.sha256()
    files = sorted(item for item in path.rglob("*") if item.is_file())
    for item in files:
        relative = item.relative_to(path).as_posix().encode("utf-8")
        digest.update(len(relative).to_bytes(8, "big"))
        digest.update(relative)
        data = item.read_bytes()
        digest.update(len(data).to_bytes(8, "big"))
        digest.update(data)
    return digest.hexdigest(), len(files)


def main() -> None:
    inventory = json.loads((ROOT / "theorems/theorem_inventory_v1.json").read_text())
    evidence = json.loads((ROOT / "theorems/theorem_evidence_v1.json").read_text())
    locators = json.loads((ROOT / "theorems/paper_locator_v1.json").read_text())

    records = {record["id"]: record for record in inventory["records"]}
    entries = {entry["id"]: entry for entry in evidence["entries"]}
    paper = {entry["id"]: entry for entry in locators["entries"]}

    OUT.mkdir(parents=True, exist_ok=True)
    MANIFESTS.mkdir(parents=True, exist_ok=True)
    expected_pages: set[Path] = set()
    expected_manifests: set[Path] = set()

    index_lines = [
        "# v1.0 Theorem Evidence Index",
        "",
        "This is the public English navigation layer for all 53 theorem-like statements",
        "in the v1.0 manuscript. Each link opens a self-contained English evidence page",
        "inside this public reproducibility repository. The reader-facing links do not",
        "terminate in the private research repository or in Japanese-only audit reports.",
        "Legacy package names are retained only in machine manifests to preserve provenance.",
        "",
        "Run `python3 scripts/verify_public_navigation.py` to verify all 53 English pages",
        "and `python3 scripts/verify_all.py` to execute the complete public verification suite.",
        "",
        "| ID | Paper locator | Statement | Evidence class | English evidence | Claim ceiling |",
        "|---|---|---|---|---|---|",
    ]

    for identifier in [record["id"] for record in inventory["records"]]:
        record = records[identifier]
        entry = entries[identifier]
        locator = paper[identifier]
        page_path = OUT / f"{identifier}.md"
        manifest_path = MANIFESTS / f"{identifier}.json"
        expected_pages.add(page_path)
        expected_manifests.add(manifest_path)

        bundles = []
        public_files = []
        for relative in entry.get("evidence_paths", []):
            path = ROOT / relative
            if path.is_dir():
                digest, count = tree_digest(path)
                bundles.append(
                    {
                        "kind": "vendored_calculation_package",
                        "repository_path": relative,
                        "sha256_tree": digest,
                        "file_count": count,
                    }
                )
            else:
                public_files.append(
                    {
                        "kind": "public_file",
                        "repository_path": relative,
                        "sha256": sha256_file(path),
                    }
                )

        machine = {
            "schema": "siel.bqg.public-statement-evidence.v1",
            "id": identifier,
            "paper_number": locator["paper_number"],
            "pdf_page": locator["pdf_page"],
            "status": entry["status"],
            "claim_ceiling": entry["claim_ceiling"],
            "dependencies": entry.get("depends_on", []),
            "public_files": public_files,
            "vendored_bundles": bundles,
            "public_urls": entry.get("public_urls", []),
            "verification_command": entry.get(
                "verification_command", "python3 scripts/verify_all.py"
            ),
        }
        manifest_path.write_text(
            json.dumps(machine, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )

        lines = [
            f"# {identifier} — {record['title']}",
            "",
            f"**Paper location:** {locator['paper_number']}, physical PDF page {locator['pdf_page']}",
            "",
            f"**Evidence class:** `{entry['status']}`",
            "",
            "## Statement in the paper",
            "",
            "```latex",
            record["statement"],
            "```",
            "",
            "## What the evidence establishes",
            "",
            entry["claim_ceiling"],
            "",
            "## Public verification",
            "",
        ]

        command = entry.get("verification_command")
        if command and command.startswith("python3 "):
            lines.extend(
                [
                    "Run from the repository root:",
                    "",
                    "```bash",
                    command,
                    "```",
                ]
            )
        elif command:
            lines.append(command)
        else:
            lines.extend(
                [
                    "Run the complete public verification suite from the repository root:",
                    "",
                    "```bash",
                    "python3 scripts/verify_all.py",
                    "```",
                ]
            )

        lines.extend(
            [
                "",
                "The exact file and package identities, content hashes, external sources,",
                "and dependencies for this statement are recorded in the",
                f"[machine-readable evidence manifest](manifests/{identifier}.json).",
                "The complete suite checks the vendored code and result certificates without",
                "requiring access to the private research repository.",
                "",
            ]
        )

        if entry.get("public_urls"):
            lines.extend(["## External public sources", ""])
            for number, url in enumerate(entry["public_urls"], start=1):
                lines.append(f"- [External source {number}]({url})")
            lines.append("")

        if entry.get("depends_on"):
            lines.extend(["## Statement dependencies", ""])
            for dependency in entry["depends_on"]:
                lines.append(f"- [{dependency}]({dependency}.md)")
            lines.append("")

        lines.extend(
            [
                "## Navigation",
                "",
                "- [All 53 English evidence pages](README.md)",
                "- [Master theorem evidence index](../../THEOREM_EVIDENCE_INDEX_v1.0.md)",
                "- [Self-contained analytic proofs](../../theorems/analytic_proofs_v1.md)",
            ]
        )
        page_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

        index_lines.append(
            "| "
            + f"<a id=\"{identifier}\"></a>`{identifier}` | "
            + f"{locator['paper_number']}, PDF p. {locator['pdf_page']} | "
            + f"{record['title']} | `{entry['status']}` | "
            + f"[Open English evidence page](evidence/statements/{identifier}.md) | "
            + f"{entry['claim_ceiling']} |"
        )

    readme = [
        "# English evidence pages",
        "",
        "These 53 pages are the reader-facing evidence endpoints for the v1.0 paper.",
        "Every page states the printed claim, claim ceiling, verification route, external",
        "sources where applicable, and a hash-bound machine manifest. No page requires",
        "access to the private research repository or a Japanese-language audit report.",
        "",
        "| ID | Paper locator | Title |",
        "|---|---|---|",
    ]
    for identifier in [record["id"] for record in inventory["records"]]:
        record = records[identifier]
        locator = paper[identifier]
        readme.append(
            f"| [{identifier}]({identifier}.md) | {locator['paper_number']}, p. {locator['pdf_page']} | {record['title']} |"
        )
    (OUT / "README.md").write_text("\n".join(readme) + "\n", encoding="utf-8")
    (ROOT / "THEOREM_EVIDENCE_INDEX_v1.0.md").write_text(
        "\n".join(index_lines) + "\n", encoding="utf-8"
    )

    for old in OUT.glob("V100-*.md"):
        if old not in expected_pages:
            old.unlink()
    for old in MANIFESTS.glob("V100-*.json"):
        if old not in expected_manifests:
            old.unlink()


if __name__ == "__main__":
    main()
