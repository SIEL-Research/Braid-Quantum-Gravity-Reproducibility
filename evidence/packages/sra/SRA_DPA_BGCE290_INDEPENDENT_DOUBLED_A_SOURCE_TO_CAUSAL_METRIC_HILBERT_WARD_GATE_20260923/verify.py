#!/usr/bin/env python3
"""Independent artifact assertions for BGCE290."""

from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
raw = json.loads((HERE / "RAW_OUTPUT.json").read_text())
result = json.loads((HERE / "RESULT.json").read_text())

assert raw["candidate_id"] == "BGCE290"
assert raw["baseline_gate"].startswith("PASS_")
solder = raw["independent_metric_source_solder"]
assert solder["Sym2_rank"] == 10
assert solder["causal_even_rank"] == 7
assert solder["causal_odd_rank"] == 3
assert solder["S4_intertwining_checks"] == 240
assert solder["matter_theta_independent"] is True
assert solder["fixed_matter_metric_variation_rank"] == 10

transport = raw["active_source_markov_transport"]
assert transport["coframe_strain_checks"] == 10
assert transport["full_rank10"] is True
assert transport["active_event_coframe_transport"] is True
assert transport["symmetric_conservative_refinement_preserved"] is True

parent = raw["source_selected_parent"]
assert parent["new_matter_action_added"] is False
assert parent["external_coefficient_fit"] is False

ward = raw["hilbert_ward"]
assert ward["Hilbert_stress_source_derived_in_declared_class"] is True
assert ward["Ward_source_derived_in_declared_class"] is True
assert result["verification"].startswith("FULL_PASS_")
assert result["Hilbert_stress_source_derived"] is True
assert result["on_shell_Ward_source_derived"] is True
assert result["unconditional_Einstein_dynamics"] is False
print("PASS_BGCE290_VERIFICATION")
