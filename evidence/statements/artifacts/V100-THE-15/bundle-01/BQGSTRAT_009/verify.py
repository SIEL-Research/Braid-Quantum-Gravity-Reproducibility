#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
subprocess.run(["python3", str(ROOT / "evaluate.py")], check=True)
d = json.loads((ROOT / "RAW_OUTPUT.json").read_text())
assert d["decision"] == "BGCE094_TEMPORAL_PROMOTIONS_RECLASSIFIED_AS_SOURCE_DERIVED_AUXILIARY_GAUGE_COMPLETION_CLOSED_SCOPED"
assert all(d["gates"].values())
assert d["lorentz_invariance"]["residual"] == "0"
assert d["exact_temporal_split"]["counts"] == {"e0_times_spatial_curvature": 12, "spatial_coframe_times_F0i": 12}
print("BQGSTRAT-009 VERIFY PASS")
