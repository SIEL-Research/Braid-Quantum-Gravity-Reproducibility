#!/usr/bin/env python3
"""Lightweight stored-result verification for BGCE259."""

from pathlib import Path
import hashlib
import json


here = Path(__file__).resolve().parent
root = here.parents[1]
raw = json.loads((here / "RAW_OUTPUT.json").read_text())
result = json.loads((here / "RESULT.json").read_text())

assert raw["candidate_id"] == result["candidate_id"] == "BGCE259"
assert raw["decision"] == result["verification"]
assert raw["forward_reverse_gate"]["actual_event_map_involutive"] is True
assert raw["forward_reverse_gate"]["orientation_odd_second_rank"] == 0
assert raw["chart_parity_gate"]["Q_even_equals_Q_odd_equals_Q4"] is True
assert raw["chart_parity_gate"]["parity_signed_rank"] == 0
assert raw["principal_action_gate"]["orientation_generates_J_ray_insertion"] is False
assert raw["dependency_effect"]["BGCE258_algebraic_Lorentz_carrier_retained"] is True
assert raw["dependency_effect"]["SDPC_complete"] is False

cert = json.loads((here / "CERTIFICATE.json").read_text())
for filename, expected in cert["artifact_sha256"].items():
    assert hashlib.sha256((here / filename).read_bytes()).hexdigest() == expected, filename
report = cert["output_report"]
assert hashlib.sha256((root / report["path"]).read_bytes()).hexdigest() == report["sha256"]

print("BGCE259 STORED VERIFY PASS")
