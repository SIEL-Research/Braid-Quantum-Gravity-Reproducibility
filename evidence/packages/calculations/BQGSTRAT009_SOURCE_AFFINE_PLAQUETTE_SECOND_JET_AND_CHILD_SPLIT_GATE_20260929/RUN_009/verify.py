#!/usr/bin/env python3
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
raw = json.loads((HERE / "RAW_OUTPUT.json").read_text())

assert all(raw["source_checks"].values())
assert all(raw["plaquette_checks"].values())
assert all(raw["incidence_checks"].values())
assert raw["stationarity_checks"]["coframe_gradient_zero_at_flat_anchor"]
assert raw["stationarity_checks"]["interior_connection_gradient_zero_by_incidence"]
assert raw["stationarity_checks"]["raw_K_blocks_well_defined"]
assert raw["stationarity_checks"]["rank_or_crossing_evaluated"] is False
assert raw["stationarity_checks"]["component_selection_proved"] is False
assert raw["construction_passed"] is True
assert raw["actual_caustic_closed"] is False
print("BQGSTRAT-009 VERIFY PASS")
