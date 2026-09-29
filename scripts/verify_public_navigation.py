#!/usr/bin/env python3
"""Fail unless all reader-facing v1 evidence endpoints are public and English."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CJK = re.compile(r"[\u3040-\u30ff\u3400-\u9fff]")
LOCAL_LINK = re.compile(r"\[[^\]]+\]\((?!https?://)([^)#]+)(?:#[^)]+)?\)")


def main() -> None:
    inventory = json.loads((ROOT / "theorems/theorem_inventory_v1.json").read_text())
    expected = [record["id"] for record in inventory["records"]]
    failures = []
    index = (ROOT / "THEOREM_EVIDENCE_INDEX_v1.0.md").read_text(encoding="utf-8")

    if "SRA_DPA_" in index or "REPORT_JA" in index or "SIEL-Research-Agent" in index:
        failures.append("master index exposes an internal or Japanese-only endpoint")

    for identifier in expected:
        relative = f"evidence/statements/{identifier}.md"
        page = ROOT / relative
        manifest = ROOT / f"evidence/statements/manifests/{identifier}.json"
        if f"]({relative})" not in index:
            failures.append(f"{identifier}: missing English-page link in index")
        if not page.is_file():
            failures.append(f"{identifier}: missing English evidence page")
            continue
        text = page.read_text(encoding="utf-8")
        if CJK.search(text):
            failures.append(f"{identifier}: reader page contains Japanese/CJK text")
        for required in (
            identifier,
            "## Statement in the paper",
            "## What the evidence establishes",
            "## Public verification",
            "## Direct evidence",
            "Machine-readable evidence manifest",
        ):
            if required not in text:
                failures.append(f"{identifier}: missing {required!r}")
        if "SIEL-Research-Agent" in text or "REPORT_JA" in text or "SRA_DPA_" in text:
            failures.append(f"{identifier}: points to private/Japanese-only evidence")
        if "## Navigation" in text or "THEOREM_EVIDENCE_INDEX" in text:
            failures.append(f"{identifier}: bounces back to an index instead of direct evidence")
        for target in LOCAL_LINK.findall(text):
            resolved = (page.parent / target).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                failures.append(f"{identifier}: local link escapes repository: {target}")
                continue
            if not resolved.exists():
                failures.append(f"{identifier}: broken local link: {target}")
        if not manifest.is_file():
            failures.append(f"{identifier}: missing machine manifest")
            continue
        payload = json.loads(manifest.read_text(encoding="utf-8"))
        if payload.get("id") != identifier:
            failures.append(f"{identifier}: manifest ID mismatch")
        direct_artifacts = payload.get("direct_artifacts", [])
        if not direct_artifacts and not payload.get("public_urls"):
            failures.append(f"{identifier}: no direct evidence artifact or public record")
        for artifact in direct_artifacts:
            artifact_path = ROOT / artifact["path"]
            try:
                artifact_text = artifact_path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError) as exc:
                failures.append(f"{identifier}: unreadable direct artifact: {exc}")
                continue
            if CJK.search(artifact_text):
                failures.append(f"{identifier}: direct artifact is not English-readable")

    pages = sorted((ROOT / "evidence/statements").glob("V100-*.md"))
    manifests = sorted((ROOT / "evidence/statements/manifests").glob("V100-*.json"))
    artifact_dirs = sorted(
        path for path in (ROOT / "evidence/statements/artifacts").iterdir() if path.is_dir()
    )
    if len(pages) != 53 or len(manifests) != 53 or len(artifact_dirs) != 53:
        failures.append(
            "unexpected endpoint count: "
            f"pages={len(pages)}, manifests={len(manifests)}, artifacts={len(artifact_dirs)}"
        )

    result = {
        "status": "PASS" if not failures else "FAIL",
        "english_statement_pages": len(pages),
        "machine_manifests": len(manifests),
        "direct_artifact_sets": len(artifact_dirs),
        "failures": failures,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
