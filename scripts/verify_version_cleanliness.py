#!/usr/bin/env python3
"""Fail if a pre-v1 manuscript identifier remains in the current release tree."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {
    ".cff",
    ".json",
    ".md",
    ".py",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}
FORBIDDEN = (
    "v0" + ".99",
    "V0" + ".99",
    "v" + "099",
    "V" + "099",
)


def main() -> None:
    failures: list[dict[str, str]] = []
    for path in sorted(ROOT.rglob("*")):
        relative = path.relative_to(ROOT)
        if ".git" in relative.parts or "__pycache__" in relative.parts:
            continue

        relative_text = relative.as_posix()
        for token in FORBIDDEN:
            if token in relative_text:
                failures.append(
                    {"kind": "path", "path": relative_text, "token": token}
                )

        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for token in FORBIDDEN:
            if token in text:
                failures.append(
                    {"kind": "content", "path": relative_text, "token": token}
                )

    result = {
        "status": "PASS" if not failures else "FAIL",
        "release": "v1.0",
        "failures": failures,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
