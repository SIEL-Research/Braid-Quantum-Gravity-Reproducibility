#!/usr/bin/env python3
"""BGCE546 exact pointed KMS response selector audit."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
MANIFEST = json.loads((HERE / "INPUT_MANIFEST.json").read_text())
SOURCE_COMMIT = MANIFEST["source_commit"]
ROLES = ("Q", "u_c", "d_c", "L", "e_c")
ZERO = "000"
NEIGHBOURS = ("001", "010", "100")
CHARACTERS = ((0, 0, 1), (0, 1, 0), (1, 0, 0))


def verify_inputs() -> None:
    for relative, expected in MANIFEST["inputs"].items():
        raw = (ROOT / relative).read_bytes()
        assert sha256(raw).hexdigest() == expected
        assert raw == subprocess.check_output(["git", "show", f"{SOURCE_COMMIT}:{relative}"], cwd=ROOT)


def load(token: str, suffix: str) -> dict:
    path = next(path for path in MANIFEST["inputs"] if token in path and path.endswith(suffix))
    return json.loads((ROOT / path).read_text())


def zeros(rows: int, columns: int):
    return [[Fraction(0) for _ in range(columns)] for _ in range(rows)]


def transpose(matrix):
    return [list(row) for row in zip(*matrix, strict=True)]


def mm(left, right):
    return [[sum((left[i][k] * right[k][j] for k in range(len(right))), Fraction(0)) for j in range(len(right[0]))] for i in range(len(left))]


def add(*matrices):
    return [[sum((matrix[i][j] for matrix in matrices), Fraction(0)) for j in range(len(matrices[0][0]))] for i in range(len(matrices[0]))]


def sub(left, right):
    return [[left[i][j] - right[i][j] for j in range(len(left[0]))] for i in range(len(left))]


def scale(value, matrix):
    return [[value * entry for entry in row] for row in matrix]


def outer(left, right):
    return [[Fraction(a * b) for b in right] for a in left]


def matrix_rank(matrix) -> int:
    values = [[Fraction(value) for value in row] for row in matrix]
    if not values:
        return 0
    rank = 0
    for column in range(len(values[0])):
        pivot = next((row for row in range(rank, len(values)) if values[row][column]), None)
        if pivot is None:
            continue
        values[rank], values[pivot] = values[pivot], values[rank]
        pivot_value = values[rank][column]
        values[rank] = [value / pivot_value for value in values[rank]]
        for row in range(len(values)):
            if row != rank and values[row][column]:
                factor = values[row][column]
                values[row] = [left - factor * right for left, right in zip(values[row], values[rank], strict=True)]
        rank += 1
    return rank


def determinant(matrix) -> Fraction:
    values = [[Fraction(value) for value in row] for row in matrix]
    det = Fraction(1)
    for column in range(len(values)):
        pivot = next((row for row in range(column, len(values)) if values[row][column]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            values[column], values[pivot] = values[pivot], values[column]
            det *= -1
        pivot_value = values[column][column]
        det *= pivot_value
        for row in range(column + 1, len(values)):
            factor = values[row][column] / pivot_value
            for entry in range(column, len(values)):
                values[row][entry] -= factor * values[column][entry]
    return det


def characteristic_coefficients(matrix):
    trace = sum(matrix[i][i] for i in range(3))
    second = (
        matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        + matrix[0][0] * matrix[2][2] - matrix[0][2] * matrix[2][0]
        + matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1]
    )
    return trace, second, determinant(matrix)


def cubic_discriminant(trace, second, determinant_value):
    return (
        trace * trace * second * second
        - 4 * second * second * second
        - 4 * trace * trace * trace * determinant_value
        - 27 * determinant_value * determinant_value
        + 18 * trace * second * determinant_value
    )


def character(k, x):
    return (-1) ** sum(a * b for a, b in zip(k, x, strict=True))


def serialize(value):
    if isinstance(value, Fraction):
        return str(value)
    if isinstance(value, list):
        return [serialize(item) for item in value]
    if isinstance(value, dict):
        return {key: serialize(item) for key, item in value.items()}
    return value


def run() -> dict:
    verify_inputs()
    bg416 = load("BGCE416_", "RESULT.json")
    bg433 = load("BGCE433_", "CERTIFICATE.json")
    bg509_diagnostic = load("BGCE509_", "DIAGNOSTIC.json")
    bg509_result = load("BGCE509_", "RESULT.json")
    bg530 = load("BGCE530_", "RESULT.json")
    bg532 = load("BGCE532_", "RESULT.json")
    bg544 = load("BGCE544_", "RESULT.json")

    assert "both star orientations equally" in bg416["decisive_result"]
    character_record = bg433["universal_derived_character"]
    assert character_record["named_order"] == list(ROLES)
    assert bg509_result["decision"].startswith("SCOPED_PASS_SOURCE_ORIENTATION_INCIDENCE_TWO_PLUS_ONE")
    assert bg530["metric_real_structure"]["half_density_KMS_star_compatible"] is True
    assert bg532["branch_pairing"]["forward"] == "M_H" and bg532["branch_pairing"]["reverse"] == "M_H*"
    assert bg544["exact_results"]["generated_associative_algebra"] == "M3(R)"

    dimensions_by_charge = {
        item["sixY"]: (1 if item["color"] == "1" else 3) * (1 if item["weak"] == "1" else 2)
        for item in character_record["left_Weyl_character"]
    }
    role_multiplicity = dict(zip(ROLES, (dimensions_by_charge[value] for value in character_record["named_order_sixY"]), strict=True))
    assert role_multiplicity == {"Q": 6, "u_c": 3, "d_c": 3, "L": 2, "e_c": 1}
    node_weight = {node: Fraction(value) for node, value in bg530["source_central_weights"].items()}

    objects = bg509_diagnostic["selected_objects"]
    assert all(key in objects for key in (ZERO, *NEIGHBOURS))

    def kernel(left_key: str, right_key: str) -> Fraction:
        total = Fraction(0)
        left_roles = objects[left_key]["roles"]
        right_roles = objects[right_key]["roles"]
        for role in ROLES:
            if left_roles[role] == right_roles[role]:
                source, target = left_roles[role]
                total += role_multiplicity[role] * node_weight[source] * node_weight[target]
        return total

    correlation = [[kernel(left, right) for right in (ZERO, *NEIGHBOURS)] for left in (ZERO, *NEIGHBOURS)]
    assert correlation == transpose(correlation)
    pointed_response = [
        [kernel(left, right) - kernel(left, ZERO) for right in NEIGHBOURS]
        for left in NEIGHBOURS
    ]
    symmetric_gram = [
        [kernel(left, right) - kernel(left, ZERO) - kernel(ZERO, right) + kernel(ZERO, ZERO) for right in NEIGHBOURS]
        for left in NEIGHBOURS
    ]
    assert symmetric_gram == transpose(symmetric_gram)

    sign_vectors = [[character(k, tuple(int(bit) for bit in neighbour)) for k in CHARACTERS] for neighbour in NEIGHBOURS]
    assert matrix_rank(sign_vectors) == 3
    ones = [1, 1, 1]
    left_generators = [outer(ones, signs) for signs in sign_vectors]
    right_generators = [transpose(matrix) for matrix in left_generators]
    basis_products = [[mm(right_generators[i], left_generators[j]) for j in range(3)] for i in range(3)]
    selector = zeros(3, 3)
    for i in range(3):
        for j in range(3):
            selector = add(selector, scale(pointed_response[i][j], basis_products[i][j]))

    reverse_selector = transpose(selector)
    normality_commutator = sub(mm(selector, reverse_selector), mm(reverse_selector, selector))
    mass_operator = mm(reverse_selector, selector)
    trace, second, determinant_value = characteristic_coefficients(mass_operator)
    discriminant = cubic_discriminant(trace, second, determinant_value)
    selector_rank = matrix_rank(selector)
    commutator_rank = matrix_rank(normality_commutator)
    mass_rank = matrix_rank(mass_operator)
    pass_rule = selector_rank == 3 and commutator_rank > 0 and determinant_value > 0 and discriminant > 0

    symmetric_selector = zeros(3, 3)
    for i in range(3):
        for j in range(3):
            symmetric_selector = add(symmetric_selector, scale(symmetric_gram[i][j], basis_products[i][j]))
    symmetric_control_commutator_rank = matrix_rank(sub(mm(symmetric_selector, transpose(symmetric_selector)), mm(transpose(symmetric_selector), symmetric_selector)))

    decision = (
        "SCOPED_PASS_POINTED_RIGHT_KMS_RESPONSE_SELECTS_FULL_RANK_NONNORMAL_FLAVOUR_OPERATOR_WITH_THREE_DISTINCT_POSITIVE_SINGULAR_VALUES_IN_DECLARED_CLASS__PHYSICAL_IDENTIFICATION_REMAINS_INTERPRETIVE"
        if pass_rule else
        "SCOPED_NO_GO_POINTED_RIGHT_KMS_RESPONSE_SELECTS_FULL_RANK_NONNORMAL_THREE_SINGULAR_VALUE_FLAVOUR_OPERATOR_IN_DECLARED_CLASS"
    )

    return {
        "schema": "siel.dpa.bgce546.raw.v1",
        "scout_id": "DPA-SCOUT-BGCE546-001",
        "source_commit": SOURCE_COMMIT,
        "evidence_status": "Theoretical derivation",
        "scientific_layer": "finite source-derived flavour-selector construction",
        "role_multiplicity": role_multiplicity,
        "node_weights": node_weight,
        "vertex_order": [ZERO, *NEIGHBOURS],
        "KMS_correlation_kernel": correlation,
        "pointed_right_response_kernel": pointed_response,
        "symmetric_difference_Gram_control": symmetric_gram,
        "BGCE544_selector": selector,
        "reverse_branch_selector": reverse_selector,
        "forward_reverse_transpose_exact": reverse_selector == transpose(selector),
        "selector_rank": selector_rank,
        "normality_commutator": normality_commutator,
        "normality_commutator_rank": commutator_rank,
        "mass_operator_YtY": mass_operator,
        "mass_operator_rank": mass_rank,
        "mass_characteristic_coefficients": {"trace": trace, "second": second, "determinant": determinant_value},
        "mass_cubic_discriminant": discriminant,
        "three_distinct_positive_singular_value_squares": determinant_value > 0 and discriminant > 0,
        "symmetric_control_selector": symmetric_selector,
        "symmetric_control_normality_commutator_rank": symmetric_control_commutator_rank,
        "pass_rule": pass_rule,
        "decision": decision,
        "ordinary_explanation": "The one-sided pointed derivative of a symmetric KMS kernel can be nonnormal because it keeps source/target order; the symmetric second-difference Gram is the ordinary Hessian control and cannot by itself justify a physical flavour interpretation.",
        "counter_intuition": "Even an exact PASS proves only that the already pointed and CTP-oriented source data select this operator inside the declared response-kernel class. It does not prove uniqueness among all possible source functionals or agreement with observed flavour physics.",
        "claim_ceiling": "This result concerns the BGCE439 derived groupoid, BGCE530 KMS metric, BGCE532 forward/reverse CTP pairing and BGCE544 M3 basis. It does not establish uniqueness among all source functionals, observed or absolute masses, CKM/PMNS, CP violation, neutrino closure, actual-crossing specificity, empirical Standard-Model confirmation or completed quantum gravity."
    }


def summarize(raw: dict) -> dict:
    return {
        "schema": "siel.dpa.bgce546.result.v1",
        "scout_id": raw["scout_id"],
        "source_commit": raw["source_commit"],
        "evidence_status": raw["evidence_status"],
        "scientific_layer": raw["scientific_layer"],
        "decision": raw["decision"],
        "exact_results": {
            "selector_rank": raw["selector_rank"],
            "normality_commutator_rank": raw["normality_commutator_rank"],
            "mass_operator_rank": raw["mass_operator_rank"],
            "mass_operator_determinant": raw["mass_characteristic_coefficients"]["determinant"],
            "mass_cubic_discriminant": raw["mass_cubic_discriminant"],
            "three_distinct_positive_singular_value_squares": raw["three_distinct_positive_singular_value_squares"],
            "forward_reverse_transpose_exact": raw["forward_reverse_transpose_exact"],
            "symmetric_control_normality_commutator_rank": raw["symmetric_control_normality_commutator_rank"],
            "pass_rule": raw["pass_rule"]
        },
        "construction": "K_ij=C(e_i,e_j)-C(e_i,0) from the source-central half-density KMS correlation of role-labelled directed orientation edges; Y=sum K_ij L_i^*L_j in the BGCE544 basis",
        "source_status": "DERIVED_KERNEL_AND_ORDERED_CTP_BRANCH_PAIR_WITH_SPECULATIVE_PHYSICAL_FLAVOUR_IDENTIFICATION",
        "bold_hypothesis_status": "SUPPORTED_IN_DECLARED_CLASS" if raw["pass_rule"] else "FALSIFIED_IN_DECLARED_CLASS",
        "ordinary_explanation": raw["ordinary_explanation"],
        "counter_intuition": raw["counter_intuition"],
        "work_package": "BQG-G3-R03.7",
        "work_package_status": "ACTIVE",
        "next_gate": "BGCE548_SOURCE_SELECTED_FLAVOUR_SINGULAR_VALUES_TO_RELATIVE_FERMION_MASS_AND_HIERARCHY_GATE" if raw["pass_rule"] else "BGCE548_INTERACTING_FERMION_KERNEL_OR_SELECTOR_FAMILY_NO_GO_GATE",
        "formal_E0_E1_E2": "NOT_CLAIMED__DPA_THEORETICAL_DERIVATION_ONLY",
        "claim_ceiling": raw["claim_ceiling"]
    }


if __name__ == "__main__":
    raw = run()
    result = summarize(raw)
    raw_serial = serialize(raw)
    result_serial = serialize(result)
    (HERE / "RAW_OUTPUT.json").write_text(json.dumps(raw_serial, indent=2, ensure_ascii=False) + "\n")
    (HERE / "RESULT.json").write_text(json.dumps(result_serial, indent=2, ensure_ascii=False) + "\n")
    certificate = {
        "schema": "siel.dpa.bgce546.certificate.v1",
        "scout_id": raw["scout_id"],
        "source_commit": SOURCE_COMMIT,
        "input_hashes": MANIFEST["inputs"],
        "evaluator_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "raw_output_sha256": sha256((HERE / "RAW_OUTPUT.json").read_bytes()).hexdigest(),
        "result_sha256": sha256((HERE / "RESULT.json").read_bytes()).hexdigest(),
        "decision": result["decision"]
    }
    (HERE / "CERTIFICATE.json").write_text(json.dumps(certificate, indent=2, ensure_ascii=False) + "\n")
    status = {
        "schema": "siel.dpa.scout.status.v1",
        "scout_id": raw["scout_id"],
        "gate_id": "BGCE546",
        "status": "COMPLETE",
        "decision": result["decision"],
        "work_package": result["work_package"],
        "next_gate": result["next_gate"]
    }
    (HERE / "STATUS.json").write_text(json.dumps(status, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(result_serial, indent=2, ensure_ascii=False))
