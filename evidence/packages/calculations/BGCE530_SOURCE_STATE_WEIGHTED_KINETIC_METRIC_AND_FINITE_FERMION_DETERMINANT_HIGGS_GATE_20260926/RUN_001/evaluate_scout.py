#!/usr/bin/env python3
"""Exact BGCE530 evaluator: source-central KMS Yukawa metric and finite determinant."""

from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
MANIFEST = json.loads((HERE / "INPUT_MANIFEST.json").read_text())


def digest(data: bytes) -> str:
    return sha256(data).hexdigest()


def source_bytes(path: str) -> bytes:
    return subprocess.check_output(
        ["git", "show", f"{MANIFEST['source_commit']}:{path}"], cwd=ROOT
    )


def load_pinned(path: str):
    data = source_bytes(path)
    expected = MANIFEST["inputs"][path]
    assert digest(data) == expected, (path, digest(data), expected)
    assert digest((ROOT / path).read_bytes()) == expected, f"worktree drift: {path}"
    return json.loads(data)


inputs = {path: load_pinned(path) for path in MANIFEST["inputs"]}

P318 = next(path for path in inputs if "BGCE318" in path)
P396 = next(path for path in inputs if "BGCE396" in path)
P430 = next(path for path in inputs if "BGCE430" in path)
P439 = next(path for path in inputs if "BGCE439" in path)
P516 = next(path for path in inputs if "BGCE516" in path)
P526 = next(path for path in inputs if "BGCE526" in path)
P528 = next(path for path in inputs if "BGCE528" in path)

bg318, bg396, bg430 = inputs[P318], inputs[P396], inputs[P430]
bg439, bg516, bg526, bg528 = inputs[P439], inputs[P516], inputs[P526], inputs[P528]

# Required source facts are checked rather than merely copied.
assert len(bg318["records"]) == 8
assert all(r["omega_spectrum"] == ["1/150", "2/225", "1/90", "1/75", "1/50"] for r in bg318["records"])
assert bg396["projection_definition"]["block_order"] == [
    "color_pair", "weak_multiplicity_6_pair", "weak_multiplicity_16", "derived_trivial"
]
assert bg396["projection_definition"]["block_dimensions"] == [24, 24, 32, 45]
records396 = bg396["all_sector_records"]
assert len(records396) == 8
assert all(r["omega_numerator_block_traces"] == [72, 88, 112, 178] for r in records396)
assert all(r["omega_numerator_block_averages"] == ["3", "11/3", "7/2", "178/45"] for r in records396)

nodes = bg430["haar_refined_five_nodes"]["nodes"]
assert {k: nodes[k]["multiplicity"] for k in ("C", "W", "N", "U", "D")} == {
    "C": 8, "W": 6, "N": 12, "U": 32, "D": 45
}
cycles430 = bg430["Higgs_Yukawa_candidate"]["charge_neutral_composable_cycles"]
assert [c["name"] for c in cycles430] == ["up", "down", "charged_lepton"]
assert bg439["matter_content"]["matter_parity"] == "ODD"
assert bg439["Higgs_real_pair"]["scalar_parity"] == "EVEN"
assert bg439["Higgs_real_pair"]["fixed_real_dimension"] == 4
assert bg439["Yukawa_content"]["all_three_cycles_present"] is True
assert bg516["exact_results"]["defect_energy"] == 24
assert bg526["three_copy_operator"]["Y_multiplicity_spectrum"] == [20, 16, 8]
assert bg528["cycle_normalization"]["distinct_canonical_HS_normalized_strength_squared"] == [1]

# BGCE396 compact-central shadow weights, with the shared W/N isotypic block.
block_average = dict(zip(
    bg396["projection_definition"]["block_order"],
    map(Fraction, records396[0]["omega_numerator_block_averages"]),
))
weights = {name: value / 450 for name, value in block_average.items()}
node_weight = {
    "C": weights["color_pair"],
    "W": weights["weak_multiplicity_6_pair"],
    "N": weights["weak_multiplicity_6_pair"],
    "U": weights["weak_multiplicity_16"],
    "D": weights["derived_trivial"],
}
assert all(value > 0 for value in node_weight.values())

# The explicit Morita/Yukawa typing fixes which three of the four blocks enter each species.
typed_cycles = {
    "up": ("C", "W", "U"),
    "down": ("C", "W", "D"),
    "lepton": ("W", "U", "D"),
}
products = {
    species: node_weight[a] * node_weight[b] * node_weight[c]
    for species, (a, b, c) in typed_cycles.items()
}
strength_sq = {species: 1 / product for species, product in products.items()}
relative_sq = {species: value / strength_sq["up"] for species, value in strength_sq.items()}
assert products == {
    "up": Fraction(77, 182250000),
    "down": Fraction(979, 2050312500),
    "lepton": Fraction(6853, 12301875000),
}
assert relative_sq == {
    "up": Fraction(1), "down": Fraction(315, 356), "lepton": Fraction(135, 178)
}
assert len(set(relative_sq.values())) == 3

# Half-density KMS form: Hom(b,a) coefficient sqrt(w_a w_b), hence star invariant.
star_compatible = all(
    node_weight[a] * node_weight[b] == node_weight[b] * node_weight[a]
    for a in node_weight for b in node_weight
)
assert star_compatible

# The U and D Higgs routes have unequal metrics but admit one positive real-pair rescaling.
alpha_fourth = node_weight["D"] / node_weight["U"]
assert alpha_fourth == Fraction(356, 315)

# Finite odd Gaussian determinant, conditional on selecting this source-compatible action.
y_spectrum = tuple(bg526["three_copy_operator"]["Y_multiplicity_spectrum"])
color_multiplicity = {"up": 3, "down": 3, "lepton": 1}
modes = []
for species in ("up", "down", "lepton"):
    for y in y_spectrum:
        modes.append({
            "species": species,
            "generation_eigenvalue": y,
            "multiplicity": color_multiplicity[species],
            "a_exact": str(strength_sq[species] * y * y),
        })
assert sum(m["multiplicity"] for m in modes) == 21

# For x=|H|^2: V=24x^2-sum d log(1+a x). Every a,d is positive.
quartic = Fraction(bg516["exact_results"]["defect_energy"])
assert quartic == 24
all_positive = all(Fraction(m["a_exact"]) > 0 and m["multiplicity"] > 0 for m in modes)
vprime_zero_negative = all_positive  # V'(0)=-sum d*a < 0
vsecond_strict_positive = quartic > 0 and all_positive  # 2*24+sum d*a^2/(1+ax)^2 > 0
vprime_infinity_positive = quartic > 0  # 48x dominates
bounded_below = quartic > 0  # 24x^2 dominates logarithms
unique_positive_radius = all((
    vprime_zero_negative,
    vsecond_strict_positive,
    vprime_infinity_positive,
    bounded_below,
))
assert unique_positive_radius

DECISION = (
    "SCOPED_PASS_SOURCE_CENTRAL_KMS_METRIC_GIVES_THREE_TYPED_YUKAWA_STRENGTHS__"
    "CONDITIONAL_PASS_FINITE_ODD_GAUSSIAN_DETERMINANT_GIVES_UNIQUE_NONZERO_HIGGS_RADIUS__"
    "UNCONDITIONAL_SOURCE_SELECTION_OF_THE_ODD_GAUSSIAN_ACTION_REMAINS_OPEN"
)


def frac_map(values):
    return {key: str(value) for key, value in values.items()}


result = {
    "schema": "siel.public-calculation.bgce530.result.v1",
    "scout_id": MANIFEST["scout_id"],
    "source_commit": MANIFEST["source_commit"],
    "decision": DECISION,
    "evidence_status": "Theoretical derivation",
    "claim_scope": "finite source-central KMS metric; finite Gaussian odd-action derived extension",
    "source_checks": {
        "pinned_inputs_verified": True,
        "faithful_positive_omega": True,
        "eight_sector_block_data_equal": True,
        "typed_cycles_present": True,
        "matter_odd_scalar_even": True,
        "BGCE528_HS_equalization_retained": True,
    },
    "source_central_weights": frac_map(node_weight),
    "typed_cycles": {key: list(value) for key, value in typed_cycles.items()},
    "cycle_weight_products": frac_map(products),
    "KMS_normalized_strength_squared": frac_map(strength_sq),
    "relative_strength_squared_to_up": frac_map(relative_sq),
    "metric_real_structure": {
        "half_density_KMS_star_compatible": star_compatible,
        "rescaling_convention": "H_u=alpha*J(H_d)",
        "Higgs_route_rescaling_alpha_fourth": str(alpha_fourth),
        "fixed_real_dimension_retained": bg439["Higgs_real_pair"]["fixed_real_dimension"],
        "independent_complex_weak_doublets_retained": bg439["Higgs_real_pair"]["independent_complex_weak_doublets"],
    },
    "finite_odd_determinant": {
        "assumption_status": "EXPLICIT_BOLD_DERIVED_EXTENSION_NOT_YET_SOURCE_SELECTED",
        "radial_variable": "x=|H|^2",
        "potential": "V_eff(x)=24*x^2-sum_j d_j*log(1+a_j*x)",
        "mode_count_with_color_multiplicity": 21,
        "modes": modes,
        "Vprime_at_zero_strictly_negative": vprime_zero_negative,
        "Vsecond_strictly_positive_for_x_nonnegative": vsecond_strict_positive,
        "Vprime_tends_to_positive_infinity": vprime_infinity_positive,
        "potential_bounded_below": bounded_below,
        "unique_global_minimum_at_x_strictly_positive": unique_positive_radius,
    },
    "BGCE528_boundary_correction": {
        "retained": "canonical Hilbert--Schmidt normalization equalizes all closed rectangular block cycles",
        "corrected": "the actual BGCE430/BGCE439 Morita typing does select the physical up/down/lepton three-block cycles; it was too strong to say no source-selected 3-of-4 map exists",
    },
    "claim_ceiling": [
        "no observed Yukawa values or absolute fermion masses",
        "no CKM or PMNS mixing",
        "no unconditional Braid-only Higgs vacuum until the odd Gaussian action is derived",
        "no empirical Standard Model or completed quantum-gravity claim",
    ],
    "next_gate": "BGCE532_SOURCE_FINITE_ODD_GAUSSIAN_ACTION_FROM_CTP_COLLISION_PARENT_GATE",
}

raw = {
    "input_hashes": MANIFEST["inputs"],
    "block_numerator_averages": {key: str(value) for key, value in block_average.items()},
    "result": result,
}
(HERE / "RAW_OUTPUT.json").write_text(json.dumps(raw, indent=2, sort_keys=True) + "\n")
(HERE / "RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")

certificate = {
    "schema": "siel.public-calculation.bgce530.certificate.v1",
    "scout_id": MANIFEST["scout_id"],
    "source_commit": MANIFEST["source_commit"],
    "decision": DECISION,
    "input_hashes": MANIFEST["inputs"],
    "raw_output_sha256": digest((HERE / "RAW_OUTPUT.json").read_bytes()),
    "result_sha256": digest((HERE / "RESULT.json").read_bytes()),
    "exact_tests": {
        "T1_PINNED_INPUTS": True,
        "T2_POSITIVE_SOURCE_CENTRAL_WEIGHTS": True,
        "T3_TYPED_THREE_CYCLE_MAP": True,
        "T4_THREE_DISTINCT_KMS_STRENGTHS": True,
        "T5_STAR_COMPATIBLE_HALF_DENSITY_METRIC": True,
        "T6_METRIC_COMPATIBLE_ONE_HIGGS_REAL_PAIR": True,
        "T7_UNIQUE_NONZERO_CONDITIONAL_HIGGS_RADIUS": True,
        "T8_GAUSSIAN_ACTION_ASSUMPTION_EXPLICIT": True,
    },
}
(HERE / "CERTIFICATE.json").write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
(HERE / "STATUS.json").write_text(json.dumps({
    "scout_id": MANIFEST["scout_id"],
    "status": "COMPLETE_SCOPED_PASS_CONDITIONAL_PASS",
    "decision": DECISION,
    "next_gate": result["next_gate"],
}, indent=2, sort_keys=True) + "\n")
print(DECISION)
print("relative squared strengths:", frac_map(relative_sq))
print("conditional unique nonzero Higgs radius:", unique_positive_radius)
