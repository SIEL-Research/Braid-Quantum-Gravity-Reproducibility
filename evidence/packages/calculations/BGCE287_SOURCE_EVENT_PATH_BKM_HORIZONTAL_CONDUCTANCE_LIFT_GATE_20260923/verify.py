#!/usr/bin/env python3
"""Independent artifact assertions for BGCE287."""

from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
raw = json.loads((HERE / "RAW_OUTPUT.json").read_text())
result = json.loads((HERE / "RESULT.json").read_text())

assert raw["candidate_id"] == "BGCE287"
assert raw["baseline_gate"].startswith("PASS_")
source = raw["source_event_path_geometry"]
assert source["microscopic_rate_tangent_dimension"] == 48
assert source["new_fitted_coefficient"] is False
micro = raw["microscopic_horizontal_gate"]
assert micro["moment_map_rank"] == 10
assert micro["kernel_dimension"] == 38
assert micro["BKM_rank_on_kernel"] == 38
assert micro["right_inverse_exact"] is True
assert micro["kernel_BKM_orthogonality_exact"] is True
assert micro["S4_equivariance_checks"] == 24
quotient = raw["BGCE286_quotient_gate"]
assert quotient["old_kernel_dimension"] == 2
assert quotient["BKM_rank_on_old_kernel"] == 2
assert quotient["old_kernel_removed_by_horizontal_condition"] is True
assert quotient["weight_ratio_common_to_relative"] == "18:1"
actual = raw["actual_X21R1_gate"]
assert actual["tangent_count"] == 24
assert actual["all_reproduced_exactly"] is True
assert actual["all_BKM_horizontal"] is True
assert len(actual["records"]) == 24
assert all(row["reproduced_exactly"] and row["BKM_horizontal"] for row in actual["records"])

assert result["verification"].startswith("FULL_PASS_")
assert result["first_order_curved_conductance_lift_uniqueness"] == "PASS_IN_SOURCE_EVENT_PATH_BKM_HORIZONTAL_CLASS"
assert result["Hilbert_stress_source_derived"] is False
assert result["Ward_source_derived"] is False
assert result["full_nonlinear_integrability"] == "OPEN"
print("PASS_BGCE287_VERIFICATION")
