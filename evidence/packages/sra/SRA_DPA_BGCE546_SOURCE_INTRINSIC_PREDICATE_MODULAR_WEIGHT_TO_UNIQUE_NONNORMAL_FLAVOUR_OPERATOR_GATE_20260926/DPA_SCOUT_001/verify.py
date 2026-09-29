#!/usr/bin/env python3
"""Verify BGCE546 retained artifacts."""

from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def main() -> None:
    manifest = json.loads((HERE / "INPUT_MANIFEST.json").read_text())
    raw = json.loads((HERE / "RAW_OUTPUT.json").read_text())
    result = json.loads((HERE / "RESULT.json").read_text())
    certificate = json.loads((HERE / "CERTIFICATE.json").read_text())
    status = json.loads((HERE / "STATUS.json").read_text())
    assert raw["source_commit"] == manifest["source_commit"] == result["source_commit"]
    assert raw["forward_reverse_transpose_exact"] is True
    assert result["exact_results"]["pass_rule"] == raw["pass_rule"]
    assert certificate["raw_output_sha256"] == sha256((HERE / "RAW_OUTPUT.json").read_bytes()).hexdigest()
    assert certificate["result_sha256"] == sha256((HERE / "RESULT.json").read_bytes()).hexdigest()
    assert certificate["decision"] == result["decision"] == status["decision"]
    print("BGCE546 verification PASS")


if __name__ == "__main__":
    main()
