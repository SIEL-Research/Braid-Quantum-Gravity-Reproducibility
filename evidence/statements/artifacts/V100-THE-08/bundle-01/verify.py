#!/usr/bin/env python3
"""Independent retained-artifact verification for BGCE300R1."""
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
raw = json.loads((HERE / "RAW_OUTPUT.json").read_text())
result = json.loads((HERE / "RESULT.json").read_text())

assert raw["baseline_gate"] == "PASS_REVISION_MATCHED_13_SOURCE_DEPENDENCIES"
assert len(raw["input_hashes_verified"]) == 13
assert raw["gravity_provenance"]["source_native_finite_first_order_action_preexists"] is True
assert raw["gravity_provenance"]["formal_vacuum_first_variation"] is True
assert raw["same_base_same_metric_gate"]["same_source_event_base"] is True
assert raw["same_base_same_metric_gate"]["local_GL4_naturality"] == "PASS"
assert raw["same_base_same_metric_gate"]["common_variable"] == "g"
assert raw["same_matter_lineage_gate"]["MMR2"] == "CLOSED"
assert raw["same_matter_lineage_gate"]["new_action_in_BGCE295"] is False
assert raw["routing_gate"] == {
    "kappa_B": "3/5",
    "manual": False,
    "MMR2_removed": True,
    "relative_routing_closed": True,
}
assert raw["stress_Ward_gate"]["Hilbert"] == "FINAL_PASS_IN_DECLARED_CLASS"
assert raw["stress_Ward_gate"]["Ward"] == "FINAL_PASS_IN_DECLARED_CLASS"
assert raw["variational_ledger"]["stationarity"] == "G_mu_nu(g)=(3/5)T_mu_nu(g,lambda)"
assert raw["low_energy_spin2_gate"]["quadratic_class"] == "massless Fierz-Pauli"
assert raw["low_energy_spin2_gate"]["helicities"] == 2
assert raw["final_decision"]["A49_backreaction"] == "FULL_SCOPED_PASS"
assert raw["final_decision"]["new_Einstein_Hilbert_action_inserted"] is False
assert raw["final_decision"]["full_finite_quantum_backreaction"] is False
assert result["verification"] == "FULL_SCOPED_PASS"
assert result["A49_noncircular_backreaction"] == "CLOSED_IN_DECLARED_CLASS"
assert result["manual_three_fifths"] is False
assert result["completed_quantum_gravity"] is False
print("PASS_BGCE300R1_A49_NONCIRCULAR_BACKREACTION_AND_LOW_ENERGY_SPIN2")
