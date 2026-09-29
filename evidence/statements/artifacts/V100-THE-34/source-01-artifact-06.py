#!/usr/bin/env python3
"""Verify BGCE552 retained exact variational-Yukawa artifacts."""

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
    assert raw["pass_rule"] is True
    assert all(raw["exact_tests"].values())
    assert result["exact_results"]["source_variation_equals_BGCE546_Y"] is True
    assert result["exact_results"]["mixed_Hstar_H_variation_equals_YtY"] is True
    assert result["closed_scope"].startswith("BGCE552 relative selector-to-variational-Yukawa")
    assert result["work_package_status"] == "ACTIVE"
    assert certificate["raw_output_sha256"] == sha256((HERE / "RAW_OUTPUT.json").read_bytes()).hexdigest()
    assert certificate["result_sha256"] == sha256((HERE / "RESULT.json").read_bytes()).hexdigest()
    assert certificate["decision"] == result["decision"] == status["decision"]
    print("BGCE552 verification PASS")


if __name__ == "__main__":
    main()
