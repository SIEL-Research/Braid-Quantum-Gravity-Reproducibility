#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
raw = HERE / "RAW_OUTPUT.json"
result = subprocess.run([sys.executable, "-B", str(HERE / "evaluate.py")], capture_output=True, text=True)
if result.returncode:
    raise SystemExit(result.stderr or result.stdout)
fresh = json.loads(raw.read_text())

assert fresh["decision"].startswith("CONDITIONAL_PASS_EXACT_S4_EQUIVARIANT")
factor = fresh["graded_factorization_gate"]
assert factor["factorization_pass"] is True
assert factor["orientation_grade"]["S4_gauge_orbits"] == 1
assert factor["orientation_grade"]["A4_orientation_orbits"] == 2
cell = fresh["five_adic_null_cell_gate"]
assert cell["children_per_parent"] == 625
assert cell["parent_to_five_child_link_checks"] == 20
assert cell["parent_to_twenty_five_grandchild_link_checks"] == 20
assert cell["cell_volume_ratio_per_epoch"] == "1/625"
assert cell["ambient_R4_assumed"] is False
utc = fresh["UTC_anchor_gate"]
assert utc["UTC1_identity_log_branch"] == "PASS"
assert utc["UTC2_uniform_first_second_differences"].startswith("PASS")
assert utc["UTC3_projective_source_anchor"].startswith("PASS")
assert fresh["remaining_boundary"]["open_C2_AffV4_or_GL4_field_neighborhood_source_derived"] is False
assert fresh["CGR_effect"]["CGR_removed"] is False
print("BGCE137 VERIFY PASS")
