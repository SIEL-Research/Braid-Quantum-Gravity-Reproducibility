#!/usr/bin/env python3
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
raw = json.loads((HERE / "RAW_OUTPUT.json").read_text())
crossing = json.loads((HERE / "CROSSING_OUTPUT.json").read_text())
result = json.loads((HERE / "RESULT.json").read_text())

assert raw["rank_profile"] == {"60": 1, "64": 12, "65": 12, "66": 600}
assert raw["sector_count"] == 625
assert raw["exact_orbit_count"] == 45
assert raw["decision_inputs_are_floating_point"] is False
assert [item["crossing_rank_numeric"] for item in crossing["records"]] == [2, 1]
assert result["status"].startswith("SCOPED_SPLIT_PASS_EXACT_RANK_LOSS")
print("BQGSTRAT-010 VERIFY PASS")
