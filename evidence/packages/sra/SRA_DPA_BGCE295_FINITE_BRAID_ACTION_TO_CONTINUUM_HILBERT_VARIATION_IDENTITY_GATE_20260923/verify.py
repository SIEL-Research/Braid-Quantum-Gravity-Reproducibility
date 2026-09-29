#!/usr/bin/env python3
from pathlib import Path
import json
H=Path(__file__).resolve().parent; r=json.loads((H/"RAW_OUTPUT.json").read_text()); q=json.loads((H/"RESULT.json").read_text())
assert r["finite_to_continuum_identity"]["variation_limit_commutes"].startswith("PASS_")
assert r["hilbert_ward"]["finite_Braid_edge_variation_equals_continuum_Hilbert_variation_in_declared_class"] is True
assert r["hilbert_ward"]["Hilbert_stress_source_derived_in_declared_class"] is True
assert r["hilbert_ward"]["Ward_source_derived_in_declared_class"] is True
assert q["full_finite_Lorentzian_Umegaki_action"] is False
print("PASS_BGCE295_VERIFICATION")
