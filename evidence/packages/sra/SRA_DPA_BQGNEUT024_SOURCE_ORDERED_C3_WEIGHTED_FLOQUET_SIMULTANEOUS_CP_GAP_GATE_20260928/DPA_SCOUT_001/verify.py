#!/usr/bin/env python3
"""Verify BQGNEUT-024 retained hashes and decision."""

from hashlib import sha256
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
cert = json.loads((HERE / "CERTIFICATE.json").read_text())
result = json.loads((HERE / "RESULT.json").read_text())
assert sha256((HERE / "RAW_OUTPUT.json").read_bytes()).hexdigest() == cert["raw_output_sha256"]
assert sha256((HERE / "RESULT.json").read_bytes()).hexdigest() == cert["result_sha256"]
assert result["decision"] == cert["decision"]
assert result["floquet_operator"]["exact_unitary"] is True
assert result["floquet_operator"]["quadratic_discriminant_exact_nonzero"] is True
assert result["cp_certificate"]["exact_nonzero"] is True
assert result["simultaneous_dimensionless_CP_gap_pass"] is True
assert result["external_neutral_carrier_removed_scoped"] is True
assert result["physical_PMNS_pass"] is False
assert result["runtime"]["target_data_accessed"] is False
assert result["runtime"]["parameter_scan_used"] is False
print("PASS_VERIFY_BQGNEUT_024_X1")
