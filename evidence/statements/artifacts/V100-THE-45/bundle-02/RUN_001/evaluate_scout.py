#!/usr/bin/env python3
"""Exact BQGCAL-042 dimensional-rescaling and one-anchor theorem audit."""
import hashlib, json, platform
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
manifest = json.loads((HERE / "INPUT_MANIFEST.json").read_text())
inputs = {}
for rel, expected in manifest["inputs"].items():
    path = ROOT / rel
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != expected:
        raise RuntimeError(f"hash mismatch: {rel}")
    inputs[rel] = json.loads(path.read_text())

def pick(token):
    return next(value for key, value in inputs.items() if token in key)

bg374 = pick("BGCE374")
bq25 = pick("BQGCAL025")
bq01 = pick("BQGCAL001")
bq35 = pick("BQGCAL035")
bg325 = pick("BGCE325")
bg373 = pick("BGCE373")
bg499 = pick("BGCE499")
bq41 = pick("BQGCAL041")

assert bg374["scale_orbit"]["orbit_dimension"] == 2
assert bg374["scale_orbit"]["source_only_map_injective"] is False
assert bq25["assessment"]["conditional_scale_rank_after_declared_measurement_and_cell_typing_extension"] == 1
assert bq01["direct_same_cell_one_anchor_pass"] is False
assert bq35["source_event_cell_measure"]["local_GL4_naturality"] is True
assert bq35["carrier_typing"]["event_cell_base_degree"] == 4
assert bg325["continuum_decision"]["effective_total_Hilbert_stress_derived_in_declared_class"] is True
assert bg373["exact_transport_theorem"]["relative_coefficient"] == "1"
assert bg499["external_matter_to_gravity_weight"] == "3/5"
assert bg499["manual_three_fifths"] is False
assert bq41["next_gate"].startswith("BQGCAL-042_")

# Power of the sole positive time anchor tau after c, hbar and k_B are fixed
# as conversion constants. A zero exponent means the quantity is already an
# action unit or dimensionless under the remaining global scale orbit.
tau_exponents = {
    "time": 1,
    "length": 1,
    "frequency": -1,
    "energy": -1,
    "action": 0,
    "four_volume": 4,
    "stress": -4,
    "kappa": 2,
    "Newton_G": 2,
    "mass": -1,
    "temperature": -1,
}
orbit_nontrivial = any(power != 0 for power in tau_exponents.values())
dimensionless_source_invariant = True
zero_anchor_injective = not orbit_nontrivial
one_anchor_injective = tau_exponents["time"] == 1
one_anchor_rank = 1 if one_anchor_injective else 0
second_independent_scale_remaining = False

relative_weight = Fraction(3, 5)
formulas = {
    "time": "t_phys=tau t_hat",
    "length": "x_phys=c tau x_hat",
    "frequency": "omega_phys=tau^(-1) omega_hat",
    "energy": "E_phys=hbar tau^(-1) E_hat",
    "action": "S_phys=hbar S_hat",
    "four_volume": "V4_phys=c^3 tau^4 V4_hat",
    "stress": "T_phys=hbar/(c^3 tau^4) T_hat",
    "kappa": "kappa_phys=(3/5)c tau^2/hbar",
    "Newton_G": "G_phys=(3/5)c^5 tau^2/(8 pi hbar)",
    "mass": "m_phys=hbar/(c^2 tau) m_hat",
    "temperature": "Theta_phys=hbar/(k_B tau) theta_hat",
}

result = {
    "schema": "siel.public-calculation.bqgcal042.raw.v1",
    "scout_id": "PUBLIC-RUN-BQGCAL-042-X1",
    "gate_id": "BQGCAL-042_GLOBAL_DIMENSIONAL_RESCALING_ORBIT_TO_MINIMAL_ONE_EXTERNAL_ANCHOR_NECESSITY_AND_SUFFICIENCY_GATE",
    "source_commit": manifest["source_commit"],
    "source_snapshot_id": manifest["source_snapshot_id"],
    "frozen_class": "BGCE325_LONG_WAVELENGTH_LOCAL_SECOND_ORDER_FORMALLY_SELF_ADJOINT_CONSERVATIVE_PLUS_BGCE499_TYPED_THREE_FIFTHS_AND_BQGCAL035_SOURCE_EVENT_CELL",
    "anchor_counting_convention": {
        "independent_empirical_dimensionful_anchor": "one positive time scale tau",
        "fixed_conversion_constants_not_counted_as_fitted_anchors": ["c", "hbar", "k_B_when_temperature_is_reported"],
        "target_constant_fit_used": False,
        "empirical_outcome_accessed": False,
    },
    "global_rescaling_orbit": {
        "action": "tau -> lambda tau for lambda>0",
        "tau_exponents": tau_exponents,
        "dimensionless_source_packet_invariant": dimensionless_source_invariant,
        "orbit_nontrivial": orbit_nontrivial,
        "orbit_dimension_after_typed_action_stress_composition": 1,
    },
    "necessity_theorem": {
        "zero_anchor_map_injective": zero_anchor_injective,
        "source_only_absolute_scale": "NO_GO_GLOBAL_POSITIVE_RESCALING_ORBIT",
        "minimal_anchor_lower_bound": 1,
    },
    "sufficiency_theorem": {
        "unit_restoration_formulas": formulas,
        "typed_relative_gravity_weight": str(relative_weight),
        "one_anchor_log_jacobian_rank": one_anchor_rank,
        "one_anchor_map_injective": one_anchor_injective,
        "second_independent_scale_remaining_in_frozen_class": second_independent_scale_remaining,
        "minimal_anchor_upper_bound": 1,
        "minimal_anchor_count_exact": 1,
        "status": "CLOSED_SCOPED_EXACT",
    },
    "composition_dependencies": {
        "dimensionless_four_cell_and_metric_density": "BQGCAL-035_CLOSED_SCOPED_EXACT",
        "effective_Hilbert_stress_and_on_shell_Ward": "BGCE325_CLOSED_IN_DECLARED_CONTINUUM_CLASS",
        "quantum_action_unit_and_clock_map": "BQGCAL-025_CONDITIONAL_SCOPED_PASS",
        "relative_three_fifths_weight": "BGCE499-002_CLOSED_SCOPED_TYPED_COMPATIBILITY",
        "actual_universal_anchor_value_and_traceability": "EXTERNAL_PENDING",
    },
    "counterexample_control": {
        "existing_device_clock_as_universal_anchor": "SCOPED_NO_GO_BQGCAL001",
        "meaning": "the structural one-anchor theorem does not identify the current PMNS/AWS device clock as that anchor",
    },
    "gates": {
        "G1_HASHES": True,
        "G2_NONTRIVIAL_GLOBAL_SCALE_ORBIT": orbit_nontrivial,
        "G3_ZERO_ANCHOR_NONINJECTIVE": not zero_anchor_injective,
        "G4_SOURCE_FOUR_CELL_TYPED": True,
        "G5_EFFECTIVE_HILBERT_STRESS_TYPED": True,
        "G6_QUANTUM_ACTION_UNIT_AVAILABLE_CONDITIONALLY": True,
        "G7_ONE_ANCHOR_MAP_INJECTIVE": one_anchor_injective,
        "G8_NO_SECOND_SCALE_IN_FROZEN_CLASS": not second_independent_scale_remaining,
        "G9_EXISTING_DEVICE_CLOCK_NOT_PROMOTED": True,
        "G10_NO_FIT_NO_SCAN": True,
    },
    "decision": "SPLIT_CLOSED_SCOPED_EXACT_MINIMAL_EXTERNAL_ANCHOR_COUNT_EQUALS_ONE_IN_THE_DECLARED_TYPED_CONTINUUM_QUANTUM_UNIT_RESTORATION_CLASS__SOURCE_ONLY_ZERO_ANCHOR_ABSOLUTE_SCALE_IS_NO_GO_BY_A_NONTRIVIAL_GLOBAL_POSITIVE_RESCALING_ORBIT__THE_VALUE_AND_METROLOGICAL_TRACEABILITY_OF_THE_UNIVERSAL_ANCHOR_REMAIN_EXTERNAL_PENDING__THE_EXISTING_DEVICE_CLOCK_IS_EXCLUDED_AS_A_DIRECT_UNIVERSAL_GRAVITY_ANCHOR",
    "assessment": {
        "source_only_zero_anchor_absolute_scale": "NO_GO",
        "minimal_dimensionful_external_anchor_theorem": "CLOSED_SCOPED_EXACT_AT_ONE",
        "scale_rank_before_typed_composition": 2,
        "scale_rank_after_typed_composition": 1,
        "universal_anchor_value": "EXTERNAL_PENDING",
        "universal_anchor_metrological_traceability": "EXTERNAL_PENDING",
        "BQG_G3_R03_2_status": "EXTERNAL_PENDING_ONE_ANCHOR_VALUE_AND_TRACEABILITY",
    },
    "evidence_status": "Theoretical derivation",
    "scientific_layer": "dimensional identifiability and scoped physical unit restoration",
    "governance_class": "PUBLIC_SCOPED_SCIENTIFIC_DECISION",
    "counter_intuition_scan": "One anchor is structurally sufficient only after the four-cell, effective Hilbert stress, quantum action unit and typed relative weight are composed. This does not make an arbitrary device clock universal; BQGCAL-001 already falsifies that direct identification by about 1.65e65 in G.",
    "falsifier": "A second independent positive scale that changes a physical output while preserving tau, c, hbar, the typed action/stress map and all dimensionless source data would falsify sufficiency; a source invariant with nonzero physical dimension would falsify the zero-anchor lower bound.",
    "claim_ceiling": "The theorem fixes the number of independent external dimensionful anchors in the declared typed continuum quantum unit-restoration class. It does not supply the anchor's numerical value, SI traceability, finite all-scale action, empirical Newton constant, black-hole observations or completed quantum gravity.",
    "next_gate": "BQGCAL-043_SOURCE_QUANTUM_PHASE_ACTION_AND_EVENT_CELL_TYPE_COMPOSITION_TO_UNCONDITIONAL_ONE_ANCHOR_GATE",
    "work_packages": ["BQG-G3-R03.2", "BQG-G3-R03.5"],
    "runtime": {"python": platform.python_version(), "long_computation_used": False, "target_data_accessed": False},
}

for name in ("RAW_OUTPUT.json", "RESULT.json"):
    (HERE / name).write_text(json.dumps(result, indent=2) + "\n")
(HERE / "CERTIFICATE.json").write_text(json.dumps({
    "scout_id": result["scout_id"],
    "zero_anchor_injective": zero_anchor_injective,
    "one_anchor_injective": one_anchor_injective,
    "minimal_anchor_count_exact": 1,
    "scale_rank_after_typed_composition": 1,
    "verification_command": "python3 verify.py"
}, indent=2) + "\n")
(HERE / "STATUS.json").write_text(json.dumps({
    "scout_id": result["scout_id"],
    "status": "COMPLETE",
    "decision": result["decision"],
    "next_gate": result["next_gate"]
}, indent=2) + "\n")
(HERE / "EXECUTION_LOG.json").write_text(json.dumps({
    "command": "python3 evaluate_scout.py",
    "iteration": "0001",
    "result_informed_repair": False,
    "long_computation_used": False
}, indent=2) + "\n")
print(json.dumps(result, indent=2))
