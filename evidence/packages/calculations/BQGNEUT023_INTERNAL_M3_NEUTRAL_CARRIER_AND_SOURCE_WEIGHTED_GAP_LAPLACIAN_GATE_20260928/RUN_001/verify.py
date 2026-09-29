#!/usr/bin/env python3
"""Verify BQGNEUT-023 retained hashes and exact decision."""

from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
cert = json.loads((HERE / "CERTIFICATE.json").read_text())
result = json.loads((HERE / "RESULT.json").read_text())
assert sha256((HERE / "RAW_OUTPUT.json").read_bytes()).hexdigest() == cert["raw_output_sha256"]
assert sha256((HERE / "RESULT.json").read_bytes()).hexdigest() == cert["result_sha256"]
assert result["decision"] == cert["decision"]
assert result["operational_carrier_pass"] is True
assert result["gap_shape_pass"] is True
assert result["simultaneous_physical_PMNS_pass"] is False
assert result["internal_neutral_carrier"]["generated_complex_dimension"] == 9
assert result["internal_neutral_carrier"]["commutant_dimension"] == 1
assert result["source_weighted_gap_generator"]["dimensionless_spectrum"] == ["0", "4/5", "6/5"]
assert result["source_weighted_gap_generator"]["coordinate_frame_Jarlskog"] == "0"
print("PASS_VERIFY_BQGNEUT_023_X1")
