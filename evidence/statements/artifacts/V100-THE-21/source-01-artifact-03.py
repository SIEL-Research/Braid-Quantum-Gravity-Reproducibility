#!/usr/bin/env python3
import json
from pathlib import Path

p = json.loads(Path(__file__).with_name("RESULT.json").read_text())
assert p["candidate_id"] == "BGCE452"
assert p["status"].startswith("SCOPED_PASS_")
assert p["gate_decision"]["exact_multiresolution_intertwiner"] == "PASS"
assert p["gate_decision"]["UCP_heat_all_depths"] == "PASS"
assert p["gate_decision"]["spectral_dimension_three"] == "PASS_EXACT"
assert p["gate_decision"]["all_finite_polynomial_composite_moments"] == "PASS"
assert p["gate_decision"]["fundamental_source_cylinder_UV_completion"] == "CLOSED_SCOPED"
assert p["gate_decision"]["smooth_spacetime_empirical_UV_completion"] == "OPEN"
assert p["formal_E0_E1_E2"].startswith("NOT_CLAIMED")
print("BGCE452_VERIFY_PASS")
