#!/usr/bin/env python3
import json
from pathlib import Path

here = Path(__file__).resolve().parent
result = json.loads((here / "RESULT.json").read_text())
raw = json.loads((here / "RAW_OUTPUT.json").read_text())
assert result == raw
assert result["exact_first_variation_witness"]["fixed_collision_phase_metric_derivative"] == "0"
assert result["exact_first_variation_witness"]["BGCE325_T00"] == "1/2"
assert result["exact_first_variation_witness"]["match"] is False
assert result["required_maps"]["phase_operator_to_continuum_scalar_action_functional"] is False
assert result["required_maps"]["metric_dependent_source_unitary_family"] is False
assert result["assessment"]["direct_phase_event_cell_physical_action"].startswith("SCOPED_NO_GO")
assert result["assessment"]["minimal_external_anchor_count_in_declared_typed_class"] == 1
print("BQGCAL-043 verification: PASS")
