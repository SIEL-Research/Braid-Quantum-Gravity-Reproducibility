#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
manifest = json.loads((HERE / "INPUT_MANIFEST.json").read_text())
checks = {
    path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest
    for path, digest in manifest["inputs"].items()
}
assert all(checks.values())
docs = {path: json.loads((ROOT / path).read_text()) for path in manifest["inputs"]}
get = lambda token: next(v for p, v in docs.items() if token in p)
bg319, bg341, bg348, bg349, bg357, bg361, bh33 = (
    get(token) for token in
    ("BGCE319", "BGCE341", "BGCE348", "BGCE349", "BGCE357", "BGCE361", "BQGBH033")
)

# Frozen exact branch table.
branch = bg348["branch_resolved_identity"]
assert "D_alpha/2" in branch["raw_effect_tangent"]
assert "-D_alpha/2" in branch["Petz_effect_tangent"]
assert "=D_alpha" in branch["branch_contrast"]
assert "=0" in branch["unconditioned_cancellation"]
assert bh33["negative_unit_Petz_minus_raw_contrast_available"] is True
assert bh33["negative_radial_backreaction_coupling_uniquely_selected_by_existing_source_record"] is False

# Petz is fixed as a KMS adjoint relative to rho, while away from the base it
# is not itself a normalized physical Markov family.  This fixes a paired map,
# not an ordered radial force.
petz = bg341["nonsecular_KMS_adjoint"]
petz_is_KMS_adjoint = petz["equals_source_KMS_adjoint_at_base"] is True
petz_is_already_physical_markov_family = bg341["gate_decision"][
    "unital_CPTP_metric_family_without_extra_normalization"
]

# Theta preserves the source channel/reference state and reverses the modular
# parameter.  The source result explicitly lacks a typed map to the physical
# difference metric; it does not order the raw/Petz record.
theta = bg319["internal_source_level_result"]
theta_preserves_source_channel = theta["Theta_Reynolds_Theta_inverse_equals_Reynolds"] is True
theta_to_physical_difference_metric_map_exists = (
    "no typed source-natural map" not in bg319["decision"].lower()
)

# BGCE349 keeps the CTP and KMS Z2 gradings distinct.  Therefore reflected
# in/out or contour reversal cannot be silently reused to orient raw/Petz.
typing = bg349["two_Z2_typing"]
two_Z2_distinct = any("distinct" in str(v).lower() or "not" in str(v).lower() for v in typing.values())

# The physical prior-summed instrument cancels the first variation; the base
# record is a fair coin with identical conditional state maps and cannot
# bootstrap a branch orientation.
prior_summed_negative_response = False
base = bg361["base_record_obstruction"]
base_record_is_fair_and_maps_equal = (
    base["fixed_prior"] == ["1/2", "1/2"] and
    "raw_* = Petz_*" in base["conditional_state_maps"]
)
record_selects_unique_feedback = bg357["metric_update_nonuniqueness"][
    "unique_lambda_or_noise_scale_selected"
]

selector_results = {
    "Petz_KMS_adjoint_selects_Petz_minus_raw_as_physical_radial_reaction": False,
    "Theta_selects_Petz_minus_raw_as_physical_radial_reaction": False,
    "reflected_in_out_Z2_can_be_identified_with_raw_Petz_Z2": not two_Z2_distinct,
    "prior_summed_instrument_retains_negative_first_variation": prior_summed_negative_response,
    "base_raw_Petz_record_selects_unique_feedback": record_selects_unique_feedback,
}
negative_sign_uniquely_selected = any(selector_results.values())
assert negative_sign_uniquely_selected is False

result = {
    "schema": "siel.public-calculation.bqgbh034.raw_output.v1",
    "scout_id": "PUBLIC-RUN-BQGBH-034-X1",
    "source_revision": manifest["source_revision"],
    "all_input_hashes_match": all(checks.values()),
    "input_hash_checks": checks,
    "exact_branch_table": {
        "raw": "+D/2",
        "Petz": "-D/2",
        "raw_minus_Petz": "+D",
        "Petz_minus_raw": "-D",
        "prior_average": "0"
    },
    "Petz_is_source_fixed_KMS_adjoint": petz_is_KMS_adjoint,
    "Petz_is_already_normalized_physical_Markov_family": petz_is_already_physical_markov_family,
    "Theta_preserves_source_channel": theta_preserves_source_channel,
    "Theta_supplies_typed_physical_difference_metric_map": theta_to_physical_difference_metric_map_exists,
    "CTP_and_raw_Petz_are_distinct_Z2_gradings": two_Z2_distinct,
    "base_record_is_fair_and_conditional_maps_equal": base_record_is_fair_and_maps_equal,
    "selector_results": selector_results,
    "negative_radial_coupling_uniquely_selected": negative_sign_uniquely_selected,
    "target_Einstein_tensor_accessed": False,
    "target_stress_accessed": False,
    "coefficient_fit": False,
    "parameter_scan": False,
    "decision": "SCOPED_NO_GO_EXISTING_PETZ_KMS_ADJOINT_SOURCE_TIME_REVERSAL_AND_REFLECTED_IN_OUT_Z2_DO_NOT_UNIQUELY_SELECT_PETZ_MINUS_RAW_AS_THE_PHYSICAL_NEGATIVE_RADIAL_REACTION__THE_PRIOR_SUMMED_INSTRUMENT_REMAINS_ZERO__IRREVERSIBLE_SOURCE_DESCENT_LAW_REQUIRED",
    "next_gate": "BQGBH-035_SOURCE_RELATIVE_ENTROPY_PRODUCTION_TO_NEGATIVE_PALATINI_GRADIENT_GATE",
    "ordinary_explanation": "A reversible adjoint pair contains both signs.  A cancelling reaction needs a source-derived arrow such as entropy descent, not a relabeling of which member is subtracted first.",
    "strongest_counterpattern": "The Petz branch has the required minus one-half tangent, but using the branch alone changes the physical prior and Petz-minus-raw reverses the already frozen BGCE348 contrast convention.",
    "claim_ceiling": "Route exclusion for sign selection by the existing Petz/KMS, Theta and in/out structures only.  The exact source current and conditional relative Palatini stationary solution remain valid; irreversible source descent is open."
}
payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
(HERE / "RAW_OUTPUT.json").write_text(payload)
print(payload, end="")
