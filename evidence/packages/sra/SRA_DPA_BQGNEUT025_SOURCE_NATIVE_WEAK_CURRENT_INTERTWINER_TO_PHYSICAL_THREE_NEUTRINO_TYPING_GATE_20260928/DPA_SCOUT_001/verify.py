#!/usr/bin/env python3
"""Verify BQGNEUT-025 retained hashes and decision."""

from hashlib import sha256
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
cert = json.loads((HERE / "CERTIFICATE.json").read_text())
result = json.loads((HERE / "RESULT.json").read_text())
assert sha256((HERE / "RAW_OUTPUT.json").read_bytes()).hexdigest() == cert["raw_output_sha256"]
assert sha256((HERE / "RESULT.json").read_bytes()).hexdigest() == cert["result_sha256"]
assert result["decision"] == cert["decision"]
assert result["weak_current_intertwiner"]["rank"] == 3
assert result["weak_current_intertwiner"]["all_nine_generation_matrix_units_intertwined"] is True
assert result["physical_three_neutrino_typing_scoped_pass"] is True
assert result["external_three_generation_carrier_required"] is False
assert result["unchanged_raw_source_physical_identity_pass"] is False
assert result["empirical_PMNS_match"] is False
print("PASS_VERIFY_BQGNEUT_025_X1")
