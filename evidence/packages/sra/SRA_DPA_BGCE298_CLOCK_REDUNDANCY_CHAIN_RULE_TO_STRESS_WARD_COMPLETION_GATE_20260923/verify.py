#!/usr/bin/env python3
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
raw=json.loads((HERE/"RAW_OUTPUT.json").read_text())
result=json.loads((HERE/"RESULT.json").read_text())
f=raw["tangent_factorization"]
assert f["D_Q_K_rank"] == 10
assert f["D_tau_K_rank"] == 3
assert f["D_tau_K_times_tau_zero"] is True
assert f["exact_C_exists_with_D_tau_K_equals_D_Q_K_times_C"] is True
assert f["cotangent_E_tau_equals_C_transpose_E_Q"] is True
assert raw["interpretation"]["tau_is_independent_continuum_coupling"] is False
assert raw["stress_Ward"]["full_rank_Hilbert_stress_source_derived_in_declared_class"] is True
assert raw["stress_Ward"]["on_shell_Braid_only_Ward_in_declared_class"] is True
assert result["Einstein_dynamics"] is False
print("PASS_BGCE298_STRESS_WARD_SCOPED_COMPLETION_VERIFICATION")
