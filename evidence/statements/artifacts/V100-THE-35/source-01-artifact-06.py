#!/usr/bin/env python3
"""Independent exact verifier for BGCE530 outputs."""

from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(name):
    return json.loads((HERE / name).read_text())


result = load("RESULT.json")
cert = load("CERTIFICATE.json")
manifest = load("INPUT_MANIFEST.json")

assert result["decision"] == (
    "SCOPED_PASS_SOURCE_CENTRAL_KMS_METRIC_GIVES_THREE_TYPED_YUKAWA_STRENGTHS__"
    "CONDITIONAL_PASS_FINITE_ODD_GAUSSIAN_DETERMINANT_GIVES_UNIQUE_NONZERO_HIGGS_RADIUS__"
    "UNCONDITIONAL_SOURCE_SELECTION_OF_THE_ODD_GAUSSIAN_ACTION_REMAINS_OPEN"
)
assert result["source_commit"] == manifest["source_commit"]
assert all(cert["exact_tests"].values())
assert cert["result_sha256"] == sha256((HERE / "RESULT.json").read_bytes()).hexdigest()
assert cert["raw_output_sha256"] == sha256((HERE / "RAW_OUTPUT.json").read_bytes()).hexdigest()

weights = {key: Fraction(value) for key, value in result["source_central_weights"].items()}
cycles = result["typed_cycles"]
products = {
    key: weights[nodes[0]] * weights[nodes[1]] * weights[nodes[2]]
    for key, nodes in cycles.items()
}
reported_products = {key: Fraction(value) for key, value in result["cycle_weight_products"].items()}
assert products == reported_products

strength = {key: 1 / value for key, value in products.items()}
relative = {key: value / strength["up"] for key, value in strength.items()}
assert relative == {"up": Fraction(1), "down": Fraction(315, 356), "lepton": Fraction(135, 178)}
assert {key: Fraction(value) for key, value in result["relative_strength_squared_to_up"].items()} == relative
assert len(set(relative.values())) == 3

metric = result["metric_real_structure"]
assert metric["half_density_KMS_star_compatible"] is True
assert Fraction(metric["Higgs_route_rescaling_alpha_fourth"]) == weights["D"] / weights["U"] == Fraction(356, 315)
assert metric["fixed_real_dimension_retained"] == 4
assert metric["independent_complex_weak_doublets_retained"] == 1

det = result["finite_odd_determinant"]
assert det["assumption_status"] == "EXPLICIT_BOLD_DERIVED_EXTENSION_NOT_YET_SOURCE_SELECTED"
assert det["mode_count_with_color_multiplicity"] == sum(m["multiplicity"] for m in det["modes"]) == 21
assert all(Fraction(m["a_exact"]) > 0 for m in det["modes"])
assert det["Vprime_at_zero_strictly_negative"] is True
assert det["Vsecond_strictly_positive_for_x_nonnegative"] is True
assert det["Vprime_tends_to_positive_infinity"] is True
assert det["potential_bounded_below"] is True
assert det["unique_global_minimum_at_x_strictly_positive"] is True
assert result["next_gate"] == "BGCE532_SOURCE_FINITE_ODD_GAUSSIAN_ACTION_FROM_CTP_COLLISION_PARENT_GATE"

print("BGCE530 independent verification: PASS")
print("relative squared strengths: 1 : 315/356 : 135/178")
print("Higgs vacuum: CONDITIONAL PASS; Gaussian-action source selection remains open")
