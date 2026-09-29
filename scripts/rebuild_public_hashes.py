#!/usr/bin/env python3
"""Rebuild hash metadata after deterministic public-package normalization."""

from __future__ import annotations

from hashlib import sha256
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGES = ROOT / "evidence/packages/calculations"
HEX = re.compile(r"^[0-9a-f]{64}$")
PYTHON_PATH_HASH = re.compile(
    r'(?P<prefix>["\'](?P<path>records/[^"\']+)["\']\s*:\s*["\'])'
    r'(?P<digest>[0-9a-f]{64})(?P<suffix>["\'])'
)


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def resolve(base: Path, raw: str) -> Path | None:
    value = raw.split(":", 1)[1] if re.match(r"^[0-9a-f]{7,64}:", raw) else raw
    candidates = []
    if value.startswith("records/"):
        candidates.append(PACKAGES / value.removeprefix("records/"))
    if value.startswith("evidence/"):
        candidates.append(ROOT / value)
    candidates.extend((base / value, ROOT / value, PACKAGES / value))
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return None


def inferred_file(base: Path, key: str) -> Path | None:
    normalized = key.lower()
    exact = {
        "raw_output_sha256": "RAW_OUTPUT.json",
        "raw_sha256": "RAW_OUTPUT.json",
        "result_sha256": "RESULT.json",
        "input_manifest_sha256": "INPUT_MANIFEST.json",
        "source_matrix_sha256": "SOURCE_MATRIX.json",
        "scout_plan_sha256": "SCOUT_PLAN.md",
        "execution_log_sha256": "EXECUTION_LOG.json",
        "status_sha256": "STATUS.json",
        "report_sha256": "REPORT.md",
        "audit_sha256": "AUDIT.md",
        "evaluate_scout_r2_sha256": "evaluate_scout_r2.py",
        "scout_plan_r2_sha256": "SCOUT_PLAN_R2.md",
        "retained_attempt_2_raw_sha256": "RAW_OUTPUT.json",
        "retained_attempt_2_result_sha256": "RESULT.json",
        "frozen_scientific_evaluator_sha256": "evaluate_scout.py",
        "path_only_wrapper_sha256": "evaluate_scout_r2.py",
        "attempt_0001_failure_sha256": "ATTEMPT_0001_FAILURE.json",
        "attempt_0003_runner_sha256": "evaluate_scout_r3.py",
        "attempt_0002_failure_sha256": "ATTEMPT_0002_FAILURE.json",
    }
    filename = exact.get(normalized)
    if filename:
        path = base / filename
        return path if path.is_file() else None
    if normalized == "evaluator_sha256":
        for name in (
            "evaluate_scout.py",
            "evaluate.py",
            "evaluate_exact.py",
            "evaluate_theorem.py",
            "proof_check.py",
        ):
            path = base / name
            if path.is_file():
                return path
    return None


def update_hashes(value, base: Path):
    changed = False
    if isinstance(value, dict):
        path_value = value.get("path")
        if isinstance(path_value, str) and isinstance(value.get("sha256"), str):
            path = resolve(base, path_value)
            if path:
                new = digest(path)
                if value["sha256"] != new:
                    value["sha256"] = new
                    changed = True
        for key, item in list(value.items()):
            if isinstance(item, str) and HEX.fullmatch(item):
                path = None
                if any(key.endswith(suffix) for suffix in (".json", ".py", ".md")):
                    path = resolve(base, key)
                elif key.endswith("_sha256"):
                    path = inferred_file(base, key)
                if path:
                    new = digest(path)
                    if item != new:
                        value[key] = new
                        changed = True
            nested_changed = update_hashes(value[key], base)
            changed = changed or nested_changed
    elif isinstance(value, list):
        for item in value:
            changed = update_hashes(item, base) or changed
    return changed


def main() -> None:
    files = sorted(PACKAGES.rglob("*.json"))
    total_writes = 0
    for _ in range(8):
        writes = 0
        for path in files:
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue
            cleaned = payload
            changed = update_hashes(cleaned, path.parent)
            if changed:
                path.write_text(
                    json.dumps(cleaned, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
                    encoding="utf-8",
                )
                writes += 1
        total_writes += writes
        if writes == 0:
            break
    python_writes = 0
    for path in sorted(PACKAGES.rglob("*.py")):
        text = path.read_text(encoding="utf-8")

        def replacement(match: re.Match[str]) -> str:
            target = resolve(path.parent, match.group("path"))
            if target is None:
                return match.group(0)
            return match.group("prefix") + digest(target) + match.group("suffix")

        updated = PYTHON_PATH_HASH.sub(replacement, text)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            python_writes += 1
    print(json.dumps({
        "status": "PASS",
        "json_files": len(files),
        "json_writes": total_writes,
        "python_writes": python_writes,
    }))


if __name__ == "__main__":
    main()
