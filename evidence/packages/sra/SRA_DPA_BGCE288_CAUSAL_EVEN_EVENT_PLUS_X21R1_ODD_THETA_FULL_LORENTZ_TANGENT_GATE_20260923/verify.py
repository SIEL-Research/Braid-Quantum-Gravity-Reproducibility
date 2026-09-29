#!/usr/bin/env python3
"""Independent artifact assertions for BGCE288."""

from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
raw = json.loads((HERE / "RAW_OUTPUT.json").read_text())
result = json.loads((HERE / "RESULT.json").read_text())

assert raw["candidate_id"] == "BGCE288"
assert raw["baseline_gate"].startswith("PASS_")
cone = raw["positive_event_moment_cone"]
assert cone["sector_count"] == 8
assert cone["X21R1_Gram_feasible_count"] == 0
assert cone["X21R1_inverse_Gram_feasible_count"] == 0
assert all(not row["Gram_in_positive_actual_event_moment_cone"] for row in cone["records"])
assert all(not row["inverse_Gram_in_positive_actual_event_moment_cone"] for row in cone["records"])

base = raw["source_physical_base"]
assert base["uniform_event_weight"] == "1/25"
assert base["uniform_weight_moment_equals_Q4"] is True
assert base["source_time_reflection_times_Q4_equals_K_evt"] is True

split = raw["causal_representation_split"]
assert split["J_even_symmetric_dimension"] == 7
assert split["J_odd_symmetric_dimension"] == 3
assert split["event_even_response_rank"] == 7
assert split["theta_odd_response_rank_each_sector"] == 3
assert split["direct_sum_dimension"] == 10
assert split["combined_full_rank_each_sector"] is True
assert len(raw["sector_records"]) == 8
assert all(row["J_odd_clock_spatial_rank"] == 3 for row in raw["sector_records"])
assert all(row["event_even_plus_theta_odd_combined_rank"] == 10 for row in raw["sector_records"])
assert raw["atlas_gate"]["even_odd_split_glues"] is True

assert result["verification"].startswith("PARTIAL_PASS_")
assert result["new_fitted_coefficient"] is False
assert result["finite_nonlinear_odd_integrability"] == "OPEN"
assert result["Hilbert_stress_source_derived"] is False
assert result["Ward_source_derived"] is False
print("PASS_BGCE288_VERIFICATION")
