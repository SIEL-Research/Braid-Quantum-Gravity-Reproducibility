#!/usr/bin/env python3
"""Structural verifier for BGCE283 artifacts."""

from pathlib import Path
import json


HERE = Path(__file__).resolve().parent
raw = json.loads((HERE / "RAW_OUTPUT.json").read_text())
result = json.loads((HERE / "RESULT.json").read_text())

assert raw["candidate_id"] == "BGCE283"
assert raw["baseline_gate"] == "PASS_REVISION_MATCHED_BGCE137_268_280_281_282_AND_X21R1_EXACT_MATRIX_REPLAY"
assert raw["atlas_representation"] == {
    "ray_chart_count": 24,
    "carrier_transition_definition": "C_pi=U P_pi U^T",
    "all_carrier_transitions_clock_fixed_signed_monomial_orthogonal": True,
    "carrier_image_size": 24,
    "projector_label_action_definition": "S_pi=C_pi entrywise-square",
    "label_image_size": 6,
    "label_kernel_size": 4,
    "label_image": "S3 permutations of the three spatial theta/projector directions",
    "carrier_cocycle_checks": 576,
    "label_cocycle_checks": 576,
    "constant_overlap_transition_derivative": "zero",
}
assert raw["summary"] == {
    "sector_count": 8,
    "metric_chart_covariance_packets": 192,
    "tangent_nonmetricity_chart_covariance_packets": 576,
    "double_overlap_tangent_cocycle_packets": 13824,
    "all_chart_tangents_symmetric_exact_rank_two": True,
    "all_connections_remain_exact_zero": True,
    "source_event_atlas_tensor_gluing": True,
}
assert len(raw["sector_records"]) == 8
for sector in raw["sector_records"]:
    assert sector["metric_chart_covariance_packets"] == 24
    assert sector["tangent_and_nonmetricity_chart_covariance_packets"] == 72
    assert sector["double_overlap_tangent_cocycle_packets"] == 1728
    assert sector["all_chart_tangents_symmetric_rank_two"] is True
    assert sector["constant_transition_keeps_zero_connection"] is True
    assert sector["nonmetricity_equals_transformed_metric_tangent"] is True
assert raw["dependency_effect"]["S4_chart_independent_metric_tensor_bundle_on_source_event_atlas"] is True
assert raw["dependency_effect"]["S4_chart_independent_nonmetricity_tensor_bundle_on_source_event_atlas"] is True
assert raw["dependency_effect"]["continuous_first_order_source_event_tensor_field"] is True
assert raw["dependency_effect"]["arbitrary_smooth_diffeomorphism_covariance"] is False
assert raw["dependency_effect"]["empirical_natural_spacetime_identification_and_calibration"] is False
assert raw["dependency_effect"]["Einstein_dynamics"] is False
assert result["verification"] == raw["decision"]
assert result["source_event_atlas_metric_tensor_gluing"] == "PASS"
assert result["source_event_atlas_nonmetricity_tensor_gluing"] == "PASS"

print("PASS_BGCE283_VERIFICATION")
