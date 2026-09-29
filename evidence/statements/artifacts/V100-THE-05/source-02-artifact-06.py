#!/usr/bin/env python3
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
raw = json.loads((HERE / "RAW_OUTPUT.json").read_text())
result = json.loads((HERE / "RESULT.json").read_text())
gate = raw["curvature_gate"]
assert raw["candidate_id"] == "BGCE292"
assert gate["base_two_plane_count"] == 45
assert gate["nonzero_curvature_two_planes"] == 0
assert gate["curvature_span_rank_in_vertical_kernel"] == 0
assert gate["flat_at_source_anchor"] is True
assert gate["local_path_independence"] == "PASS"
assert result["Hilbert_stress_Braid_only"] == "OPEN_NOT_DERIVED"
print("PASS_BGCE292_VERIFICATION")
