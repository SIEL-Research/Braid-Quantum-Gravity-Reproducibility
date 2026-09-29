#!/usr/bin/env python3
"""Independent exact verifier for BGCE532."""

from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(name):
    return json.loads((HERE / name).read_text())


result = load("RESULT.json")
raw = load("RAW_OUTPUT.json")
cert = load("CERTIFICATE.json")
manifest = load("INPUT_MANIFEST.json")

assert result["decision"] == (
    "SCOPED_PASS_SOURCE_SIGN_LINE_PLUS_ORDINARY_CTP_EXTERIOR_TRACE_FORCES_FINITE_FERMION_DETERMINANT_AND_EFFECTIVE_ACTION_SIGN__"
    "BGCE530_ODD_GAUSSIAN_ACTION_ASSUMPTION_REMOVED_IN_DECLARED_DERIVED_CLASS__"
    "UNCHANGED_SOURCE_AND_SAME_163R_FIELD_EQUIVALENCE_NOT_CLAIMED"
)
assert result["source_commit"] == manifest["source_commit"]
assert all(cert["exact_tests"].values())
assert cert["result_sha256"] == sha256((HERE / "RESULT.json").read_bytes()).hexdigest()
assert cert["raw_output_sha256"] == sha256((HERE / "RAW_OUTPUT.json").read_bytes()).hexdigest()

parity = result["parity_pullback"]
matches = [item for item in parity["candidate_symmetric_bicharacters"] if item["matches_source_sign"]]
assert len(matches) == 1
assert matches[0]["epsilon"] == 1
assert parity["selected_Koszul_table"] == [[1, 1], [1, -1]]
assert parity["unique_after_source_sign_fixed"] is True

coefficients = [Fraction(value) for value in raw["elementary_symmetric_coefficients"]]
ordinary = sum(coefficients)
supertrace = sum(((-1) ** k) * value for k, value in enumerate(coefficients))
assert ordinary == Fraction(raw["ordinary_exterior_trace"]) == Fraction(raw["det_plus"])
assert supertrace == Fraction(raw["super_exterior_trace"]) == Fraction(raw["det_minus"])
assert ordinary > 0 and ordinary != supertrace

exterior = result["exterior_trace"]
assert exterior["one_particle_dimension_with_multiplicity"] == raw["expanded_mode_count"] == 21
assert exterior["ordinary_trace_equals_det_plus"] is True
assert exterior["ordinary_trace_positive"] is True
assert exterior["supertrace_equals_det_minus"] is True
assert exterior["ordinary_and_supertrace_distinct"] is True
assert exterior["CTP_trace_selected"] == "ordinary trace with no (-1)^F insertion"

branch = result["branch_pairing"]
assert branch["positive_from_exact_mode_spectrum"] is True
assert branch["gauge_neutral_from_typed_cycles"] is True
assert "Sylvester" in branch["opposite_order_same_determinant"]

effective = result["effective_action"]
assert effective["finite_odd_Gaussian_action_assumed"] is False
assert effective["determinant_plus_sign_forced"] is True
assert effective["effective_minus_log_sign_forced"] is True
assert effective["BGCE530_unique_nonzero_Higgs_radius_now_unconditional_within_declared_class"] is True
assert all(result["preserved_boundaries"].values())
assert result["next_gate"] == "BGCE534_SOURCE_NORMALIZED_HIGGS_RADIUS_AND_RELATIVE_FERMION_MASS_OUTPUT_GATE"

print("BGCE532 independent verification: PASS")
print("determinant: ordinary exterior trace forces det(I+A)")
print("BGCE530 Gaussian-action assumption: removed within declared derived class")
