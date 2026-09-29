#!/usr/bin/env python3
"""Lightweight verification for PUBLIC-RUN-BGCE499-001."""

import json
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
raw = json.loads((HERE / "RAW_OUTPUT.json").read_text())
result = json.loads((HERE / "RESULT.json").read_text())

assert all(raw["input_hash_checks"].values())
assert all(raw["noncompensating_gates"].values())
assert Fraction(raw["exact_rational_result"]["internal_fisher_gain"]) == 1
assert Fraction(raw["exact_rational_result"]["external_relative_weight"]) == Fraction(3, 5)
assert result["same_scalar_referent"] is False
assert result["asymmetric_score_hessian_map_used"] is False
assert result["work_item_decision"] == "CLOSED_SCOPED"
print("PASS_VERIFY_RUN_BGCE499_001")
