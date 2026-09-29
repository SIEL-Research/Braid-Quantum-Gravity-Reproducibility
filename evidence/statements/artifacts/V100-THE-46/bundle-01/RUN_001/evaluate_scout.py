#!/usr/bin/env python3
"""Exact BQGCAL-043 phase/action/event-cell typing audit."""
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

bq42 = pick("BQGCAL042")
bq25 = pick("BQGCAL025")
bq35 = pick("BQGCAL035")
bg325 = pick("BGCE325")
bg338 = pick("BGCE338")
bg499 = pick("BGCE499")

assert bq42["sufficiency_theorem"]["minimal_anchor_count_exact"] == 1
assert bq42["necessity_theorem"]["zero_anchor_map_injective"] is False
assert bq25["assessment"]["conditional_action_quantum_derived"] is True
assert bq25["assessment"]["source_native_noether_generator_derived"] is False
assert bq25["assessment"]["physical_gravitational_stress_derived"] is False
assert bq35["source_event_cell_measure"]["local_GL4_naturality"] is True
assert bq35["carrier_typing"]["event_cell_base_degree"] == 4
assert bq35["assessment"]["source_native_noether_action"] == "OPEN"
assert bg325["continuum_decision"]["effective_total_Hilbert_stress_derived_in_declared_class"] is True
assert bg338["two_fixed_conductance_readings"]["source_label_operational"]["generator_derivative"] == "delta L_alpha=0"
assert bg338["gate_decision"]["physical_metric_dependent_CPTP_generator"] is False
assert bg499["external_matter_to_gravity_weight"] == "3/5"

# Exact nonzero Hilbert-stress witness from the retained BGCE325 formula.
# Take one scalar score field with G_11=1 on Minkowski g=diag(-1,1,1,1)
# and lambda=t. Then d_0 lambda=1, g^rs d_r lambda d_s lambda=-1,
# so T_00 = 1 - (1/2)(-1)(-1) = 1/2.
continuum_T00 = Fraction(1, 1) - Fraction(1, 2)
fixed_collision_metric_derivative = Fraction(0, 1)
variation_match = fixed_collision_metric_derivative == continuum_T00

type_inventory = {
    "collision_phase_generator": "self_adjoint_operator_on_finite_dilation_Hilbert_space",
    "event_cell_measure": "scalar_four_density_on_source_derived_base",
    "continuum_action": "real_scalar_functional_of_fields_and_metric",
    "Hilbert_stress": "metric_variation_of_scalar_action_functional",
}
required_maps = {
    "phase_operator_to_continuum_scalar_action_functional": False,
    "metric_dependent_source_unitary_family": False,
    "equality_of_phase_and_Hilbert_metric_variations": variation_match,
}

result = {
    "schema": "siel.public-calculation.bqgcal043.raw.v1",
    "scout_id": "PUBLIC-RUN-BQGCAL-043-X1",
    "gate_id": "BQGCAL-043_SOURCE_QUANTUM_PHASE_ACTION_AND_EVENT_CELL_TYPE_COMPOSITION_TO_UNCONDITIONAL_ONE_ANCHOR_GATE",
    "source_commit": manifest["source_commit"],
    "source_snapshot_id": manifest["source_snapshot_id"],
    "bold_hypothesis": {
        "interpretive_leap": "the current finite collision phase and source four-cell are two typed faces of one physical action",
        "new_assumption": "the phase operator and BGCE325 scalar action share one source-native variational parent",
        "assumption_status_before_test": "NOT_DERIVED",
        "mechanism_class_change": "DETERMINANT_OR_FOCK_NORMALIZATION_TO_DIRECT_QUANTUM_PHASE_DENSITY_COMPOSITION",
    },
    "type_inventory": type_inventory,
    "exact_first_variation_witness": {
        "metric": "diag(-1,1,1,1)",
        "field": "lambda=t with unit target Fisher metric",
        "BGCE325_T00": str(continuum_T00),
        "fixed_collision_phase_metric_derivative": str(fixed_collision_metric_derivative),
        "match": variation_match,
    },
    "required_maps": required_maps,
    "gates": {
        "G1_HASHES": True,
        "G2_SOURCE_FOUR_CELL_DENSITY": True,
        "G3_CONDITIONAL_QUANTUM_ACTION_UNIT": True,
        "G4_SOURCE_NATIVE_NOETHER_GENERATOR": False,
        "G5_METRIC_DEPENDENT_SOURCE_UNITARY": False,
        "G6_PHASE_TO_SCALAR_ACTION_MORPHISM": False,
        "G7_METRIC_VARIATIONS_MATCH": variation_match,
        "G8_BQGCAL042_ONE_ANCHOR_THEOREM_RETAINED": True,
        "G9_NO_FIT_NO_SCAN": True,
    },
    "decision": "SCOPED_NO_GO_DIRECT_COMPOSITION_OF_THE_CURRENT_FIXED_COLLISION_QUANTUM_PHASE_WITH_THE_SOURCE_EVENT_CELL_AS_AN_UNCONDITIONAL_COMMON_PHYSICAL_ACTION__THE_PHASE_GENERATOR_IS_AN_OPERATOR_WHILE_BGCE325_IS_A_SCALAR_FIELD_FUNCTIONAL__THE_REQUIRED_SOURCE_MORPHISM_IS_ABSENT__FIXED_COLLISION_METRIC_VARIATION_IS_ZERO_BUT_THE_EXACT_BGCE325_WITNESS_HAS_T00_ONE_HALF__BQGCAL042_MINIMAL_ONE_EXTERNAL_ANCHOR_THEOREM_REMAINS_CLOSED_SCOPED_EXACT",
    "assessment": {
        "direct_phase_event_cell_physical_action": "SCOPED_NO_GO_CURRENT_FIXED_SOURCE",
        "conditional_action_unit": "RETAINED_SCOPED_PASS",
        "minimal_external_anchor_count_in_declared_typed_class": 1,
        "source_only_zero_anchor_absolute_scale": "NO_GO_RETAINED",
        "scale_rank_after_typed_composition": 1,
        "universal_anchor_value_and_traceability": "EXTERNAL_PENDING",
        "BQG_G3_R03_2_status": "EXTERNAL_PENDING_ONE_ANCHOR_VALUE_AND_TRACEABILITY",
    },
    "strongest_ordinary_alternative": "A four-density fixes integration type and units but does not turn an operator phase into a scalar variational action. The exact zero-versus-one-half witness realizes that type distinction.",
    "counter_intuition_scan": "The failure does not introduce a second scale and does not refute the quantum phase, event-cell measure, effective Hilbert stress or one-anchor theorem separately. It excludes only their direct identification without a common metric-dependent generating functional.",
    "falsifier": "A source-derived metric-dependent collision family U[g] and scalar CTP logarithmic functional whose time variation yields the collision phase and whose metric variation per source event cell equals the BGCE325 Hilbert stress would falsify this route exclusion.",
    "minimum_decisive_next_test": "Construct the source-native CTP logarithmic characteristic functional from the actual forward/backward collision pair, differentiate it with respect to metric and clock, and require one common nonzero generator and Hilbert-stress variation without fitted coefficients.",
    "evidence_status": "Theoretical derivation",
    "scientific_layer": "finite quantum phase to continuum variational action typing",
    "governance_class": "PUBLIC_SCOPED_SCIENTIFIC_DECISION",
    "claim_ceiling": "BQGCAL-043 excludes direct physical-action identification by composing the current fixed collision phase with the source event-cell density. It does not exclude a genuinely metric-dependent CTP characteristic functional, alter the scoped one-anchor rank theorem, determine the universal anchor value, predict Newton's constant or complete quantum gravity.",
    "next_gate": "BQGCAL-044_SOURCE_METRIC_DEPENDENT_CTP_LOG_CHARACTERISTIC_FUNCTIONAL_TO_COMMON_PHASE_AND_HILBERT_STRESS_GATE",
    "work_packages": ["BQG-G3-R03.2", "BQG-G3-R03.5"],
    "runtime": {"python": platform.python_version(), "long_computation_used": False, "target_data_accessed": False},
}

for name in ("RAW_OUTPUT.json", "RESULT.json"):
    (HERE / name).write_text(json.dumps(result, indent=2) + "\n")
(HERE / "CERTIFICATE.json").write_text(json.dumps({
    "scout_id": result["scout_id"],
    "fixed_collision_metric_derivative": "0",
    "continuum_T00_witness": "1/2",
    "variations_match": variation_match,
    "one_anchor_theorem_retained": True,
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
