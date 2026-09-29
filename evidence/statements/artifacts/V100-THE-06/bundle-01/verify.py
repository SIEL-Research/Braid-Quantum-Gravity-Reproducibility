#!/usr/bin/env python3
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
raw=json.loads((HERE/"RAW_OUTPUT.json").read_text()); result=json.loads((HERE/"RESULT.json").read_text())
assert raw["unrestricted"]["S4_equivariant_commutant_dimension"]==9
assert raw["unrestricted"]["clock_grading_event_spectral_residual_dimension"]==5
assert raw["source_typed_functor"]["spanning_rank"]==10
assert raw["source_typed_functor"]["residual_affine_dimension"]==0
assert raw["source_typed_functor"]["new_coefficient"] is False
assert result["finite_to_continuum_action_variation_identity"]=="OPEN"
print("PASS_BGCE294_VERIFICATION")
