#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


subprocess.run([sys.executable, str(HERE / "evaluate.py")], cwd=ROOT, check=True)
subprocess.run([sys.executable, str(HERE / "finalize.py")], cwd=ROOT, check=True)
r = json.loads((HERE / "RESULT.json").read_text())
p = json.loads((HERE / "PBM_COVARIANT_TRANSPORT_JETS_PARTIAL_v1.json").read_text())
assert r["status"].startswith("PARTIAL_PASS_ACTUAL_U4_V0_2")
assert r["executed"]["actual_sigma_through_degree_6_in_frozen_gamma0_spatial_frame"] is False
assert r["executed"]["actual_U_through_degree_4_center_and_four_roots"] is True
assert r["executed"]["actual_v0_through_degree_2_center_and_four_roots"] is True
assert r["executed"]["parallel_horizontal_operator_through_degree_4"] is False
assert p["coefficient_counts"] == {"U2": 10, "U3": 20, "U4": 35, "v01": 4, "v02": 10}
for sector in ("U2", "U3", "U4_total"):
    assert all(len(v["derivatives"]) == 4 for v in p["van_vleck"][sector].values())
assert all(len(v["derivatives"]) == 4 for v in p["v0"]["v02"].values())
assert p["v0"]["recurrence_interval_residual_contains_zero_all_coefficients_and_roots"] is True
assert p["parallel4"] is None
assert p["world_function"]["frames_identical"] is False
fx = p["sigma6_parallel4_first_fail"]["fixture_detects_omission"]
assert fx["raw_without_parallel_is_nonzero"] is True and fx["exact_sum"] == "0"
for rel, expected in p["input_hashes"].items():
    assert sha(ROOT / rel) == expected
# Independent saved coincidence value must overlap the newly generated v00.
hps = json.loads((ROOT / "records/UB598J_ACTUAL_SCHEME_V2_HPS_INSERTION_C1_COEFFICIENT_GATE/HPS_INSERTION_C1_COEFFICIENT_PACKET.json").read_text())
a = list(map(float, p["v0"]["v00"]["value"]))
b = list(map(float, hps["derivation"]["hps_coincidences"]["actual_V0_interval"]))
assert not (a[1] < b[0] or b[1] < a[0])
print("UB612_VERIFY_PASS_PARTIAL_FIRST_FAIL_PRESERVED")
