#!/usr/bin/env python3
import json
from pathlib import Path

here = Path(__file__).resolve().parent
result = json.loads((here / "RESULT.json").read_text())
raw = json.loads((here / "RAW_OUTPUT.json").read_text())
assert result == raw
assert result["global_rescaling_orbit"]["orbit_dimension_after_typed_action_stress_composition"] == 1
assert result["necessity_theorem"]["zero_anchor_map_injective"] is False
assert result["necessity_theorem"]["minimal_anchor_lower_bound"] == 1
assert result["sufficiency_theorem"]["one_anchor_map_injective"] is True
assert result["sufficiency_theorem"]["second_independent_scale_remaining_in_frozen_class"] is False
assert result["sufficiency_theorem"]["minimal_anchor_upper_bound"] == 1
assert result["sufficiency_theorem"]["minimal_anchor_count_exact"] == 1
assert result["assessment"]["scale_rank_after_typed_composition"] == 1
assert result["counterexample_control"]["existing_device_clock_as_universal_anchor"].startswith("SCOPED_NO_GO")
print("BQGCAL-042 verification: PASS")
