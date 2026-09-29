#!/usr/bin/env python3
"""Run the canonical-source verification and compare with frozen output."""

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from bqg_v1 import verify_source_class


def main() -> None:
    actual = verify_source_class(ROOT / "data/canonical_source_class_v1.json")
    expected = json.loads((ROOT / "expected/source_verification_v1.json").read_text(encoding="utf-8"))
    if actual != expected:
        print(json.dumps({"status": "FAIL", "actual": actual, "expected": expected}, indent=2))
        raise SystemExit(1)
    print(json.dumps(actual, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
