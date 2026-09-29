#!/usr/bin/env python3
"""Reject internal research labels, private-repository references, and CJK text."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CJK = re.compile(r"[\u3040-\u30ff\u3400-\u9fff]")
FORBIDDEN = (
    "S" + "RA",
    "D" + "PA",
    "D" + "PA_SCOUT",
    "SIEL-" + "Research-Agent",
    "REPORT_" + "JA",
    "AUDIT_" + "JA",
)
SKIP_PARTS = {".git", "__pycache__"}


def public_files():
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in SKIP_PARTS for part in path.parts):
            continue
        yield path


def main() -> None:
    failures = []
    scanned = 0
    for path in public_files():
        relative = path.relative_to(ROOT).as_posix()
        if any(token in relative for token in FORBIDDEN):
            failures.append(f"forbidden internal label in path: {relative}")
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        scanned += 1
        for token in FORBIDDEN:
            if token in text:
                failures.append(f"forbidden internal label in content: {relative}")
                break
        if CJK.search(text):
            failures.append(f"CJK text in public repository: {relative}")

    result = {
        "status": "PASS" if not failures else "FAIL",
        "utf8_files_scanned": scanned,
        "failures": failures,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
