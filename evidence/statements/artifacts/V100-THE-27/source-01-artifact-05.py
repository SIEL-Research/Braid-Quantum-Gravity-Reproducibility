#!/usr/bin/env python3
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
r = json.loads((HERE / "RESULT.json").read_text())
raw = json.loads((HERE / "RAW_OUTPUT.json").read_text())
assert r["decision"].startswith("CLOSED_SCOPED_POINTED_HODGE_POLAR_GINSPARG_WILSON_REGULATOR")
assert all(r["checks"].values())
assert raw["one_cube"]["GW_index"] == "1"
assert raw["one_cube"]["kernel_dimension"] == 1
assert all(float(x["rescaled_gap_numeric"]) > 1 for x in raw["five_adic_gap"]["stages"])
print("BQGQBV-002 verification PASS")

