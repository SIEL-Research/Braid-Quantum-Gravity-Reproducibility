#!/usr/bin/env python3
"""Generate English, reader-facing evidence pages for every v1 statement."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import shutil


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence/statements"
MANIFESTS = OUT / "manifests"
ARTIFACTS = OUT / "artifacts"
CJK = re.compile(r"[\u3040-\u30ff\u3400-\u9fff]")


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


def package_entrypoints(path: Path) -> list[Path]:
    preferred = {
        "verify.py",
        "validate_result.py",
        "proof_check.py",
        "evaluate.py",
        "evaluate_scout.py",
        "evaluate_exact.py",
        "evaluate_theorem.py",
        "RESULT.json",
        "CERTIFICATE.json",
        "PROOF_CERTIFICATE.json",
        "RAW_OUTPUT.json",
        "SOURCE_MATRIX.json",
        "INPUT_MANIFEST.json",
    }
    entries = []
    for item in path.rglob("*"):
        if not item.is_file() or item.name not in preferred:
            continue
        try:
            text = item.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if CJK.search(text):
            continue
        entries.append(item)
    return sorted(entries)


def artifact_kind(path: Path) -> str:
    if path.suffix == ".py":
        return "Verifier source"
    if path.name in {"RESULT.json", "RAW_OUTPUT.json"}:
        return "Machine result"
    if "CERTIFICATE" in path.name:
        return "Certificate"
    if "MANIFEST" in path.name or path.name == "SOURCE_MATRIX.json":
        return "Input provenance"
    if path.suffix == ".md":
        return "Analytic proof"
    return "Public evidence file"


def main() -> None:
    inventory = json.loads((ROOT / "theorems/theorem_inventory_v1.json").read_text())
    evidence = json.loads((ROOT / "theorems/theorem_evidence_v1.json").read_text())
    locators = json.loads((ROOT / "theorems/paper_locator_v1.json").read_text())

    records = {record["id"]: record for record in inventory["records"]}
    entries = {entry["id"]: entry for entry in evidence["entries"]}
    paper = {entry["id"]: entry for entry in locators["entries"]}

    OUT.mkdir(parents=True, exist_ok=True)
    MANIFESTS.mkdir(parents=True, exist_ok=True)
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
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
        artifact_dir = ARTIFACTS / identifier
        if artifact_dir.exists():
            shutil.rmtree(artifact_dir)
        artifact_dir.mkdir(parents=True)
        expected_pages.add(page_path)
        expected_manifests.add(manifest_path)

        bundles = []
        direct_artifacts = []
        for source_number, relative in enumerate(entry.get("evidence_paths", []), start=1):
            path = ROOT / relative
            if path.is_dir():
                digest, count = tree_digest(path)
                bundles.append(
                    {
                        "kind": "vendored_calculation_package",
                        "sha256_tree": digest,
                        "file_count": count,
                    }
                )
                selected = package_entrypoints(path)
            else:
                selected = [path]

            for file_number, source in enumerate(selected, start=1):
                alias = artifact_dir / (
                    f"source-{source_number:02d}-artifact-{file_number:02d}{source.suffix}"
                )
                shutil.copy2(source, alias)
                direct_artifacts.append(
                    {
                        "kind": artifact_kind(source),
                        "path": alias.relative_to(ROOT).as_posix(),
                        "sha256": sha256_file(alias),
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
            "direct_artifacts": direct_artifacts,
            "source_bundle_digests": bundles,
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

        lines.extend(["", "## Direct evidence", ""])
        labels: dict[str, int] = {}
        for artifact in direct_artifacts:
            labels[artifact["kind"]] = labels.get(artifact["kind"], 0) + 1
            filename = Path(artifact["path"]).name
            lines.append(
                f"- [{artifact['kind']} {labels[artifact['kind']]}]"
                f"(artifacts/{identifier}/{filename}) — SHA-256 `{artifact['sha256']}`"
            )
        for number, bundle in enumerate(bundles, start=1):
            lines.append(
                f"- Complete source bundle {number}: {bundle['file_count']} files; "
                f"tree SHA-256 `{bundle['sha256_tree']}`"
            )
        if not direct_artifacts and not bundles:
            for number, url in enumerate(entry.get("public_urls", []), start=1):
                lines.append(f"- [Archived evidence record {number}]({url})")
        lines.extend(
            [
                f"- [Machine-readable evidence manifest](manifests/{identifier}.json)",
                "",
                "These are the statement-specific public evidence endpoints. Local code,",
                "results and certificates are hash-bound where present; DOI-only records",
                "remain directly accessible without private-repository access.",
                "",
            ]
        )

        if entry.get("public_urls") and (direct_artifacts or bundles):
            lines.extend(["## External public sources", ""])
            for number, url in enumerate(entry["public_urls"], start=1):
                lines.append(f"- [External source {number}]({url})")
            lines.append("")

        if entry.get("depends_on"):
            lines.extend(["## Statement dependencies", ""])
            for dependency in entry["depends_on"]:
                lines.append(f"- [{dependency}]({dependency}.md)")
            lines.append("")

        page_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")

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
    expected_artifact_dirs = {record["id"] for record in inventory["records"]}
    for old in ARTIFACTS.iterdir():
        if old.is_dir() and old.name not in expected_artifact_dirs:
            shutil.rmtree(old)


if __name__ == "__main__":
    main()
