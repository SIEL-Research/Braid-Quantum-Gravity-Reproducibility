#!/usr/bin/env python3
"""Run the complete public v1 verification suite."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMMANDS = [
    [sys.executable, "scripts/verify_manifest.py"],
    [sys.executable, "scripts/verify_source.py"],
    [sys.executable, "scripts/verify_theorem_coverage_v1.py"],
    [sys.executable, "scripts/verify_public_navigation.py"],
    [sys.executable, "scripts/verify_version_cleanliness.py"],
    [sys.executable, "scripts/verify_evidence_integrity.py"],
    [sys.executable, "scripts/verify_vendored_packages.py"],
    [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
]


def main() -> None:
    for command in COMMANDS:
        print("+", " ".join(command), flush=True)
        subprocess.run(command, cwd=ROOT, check=True)
    print("PUBLIC V1 VERIFICATION: PASS")


if __name__ == "__main__":
    main()
