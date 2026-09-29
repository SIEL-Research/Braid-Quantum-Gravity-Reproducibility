#!/usr/bin/env python3
"""Fail-closed validator for DPA-SCOUT-BQGEULER-004."""

import json
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
raw = json.loads((HERE / "RAW_OUTPUT.json").read_text())
result = json.loads((HERE / "RESULT.json").read_text())

assert all(item["pass"] for item in raw["hash_checks"].values())
assert raw["intertwiner_witness"]["good_residual_norm_squared"] == "0"
assert raw["intertwiner_witness"]["bad_residual_norm_squared_on_unit_coarse_detail"] == "1"
assert raw["intertwiner_witness"]["endpoint_has_dynamic_range"] is True
tails = [F(row["two_polarization_isotropic_energy_error_squared"]) for row in raw["tail_witness"]]
assert all(tails[i + 1] < tails[i] for i in range(len(tails) - 1))
assert raw["endpoints"]["uniform_finite_time_strong_convergence"].startswith("PASS_EXACT")
assert raw["endpoints"]["physical_ADM_projector_refinement_intertwiner"] == "OPEN_SOURCE_NOT_PRESENT"
assert raw["endpoints"]["smooth_Fierz_Pauli_principal_symbol_identity"] == "OPEN_SOURCE_NOT_PRESENT"
assert result["hierarchical_two_mode_strong_convergence"] == "CLOSED_SCOPED"
assert result["physical_ADM_two_mode_strong_convergence"] == "OPEN_SOURCE_IDENTIFICATION_REQUIRED"
assert result["work_package_status_after_gate"] == "OPEN_SOURCE_CONSTRUCTION_REQUIRED"
print("VALIDATION_PASS")
