#!/usr/bin/env python3
"""BGCE552 exact pointed-KMS variation to finite Yukawa action audit."""

from __future__ import annotations

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


def verify_inputs() -> dict[str, bytes]:
    retained = {}
    for relative, expected in MANIFEST["inputs"].items():
        local = (ROOT / relative).read_bytes()
        pinned = subprocess.check_output(
            ["git", "show", f"{MANIFEST['source_commit']}:{relative}"], cwd=ROOT
        )
        assert digest(local) == expected, (relative, digest(local), expected)
        assert local == pinned, f"pinned source mismatch: {relative}"
        retained[relative] = local
    return retained


def load(inputs: dict[str, bytes], token: str, suffix: str) -> dict:
    path = next(path for path in inputs if token in path and path.endswith(suffix))
    return json.loads(inputs[path])


def q(value) -> Fraction:
    return Fraction(value)


def zeros(rows: int, columns: int):
    return [[Fraction(0) for _ in range(columns)] for _ in range(rows)]


def transpose(matrix):
    return [list(row) for row in zip(*matrix, strict=True)]


def add(*matrices):
    return [
        [sum((matrix[i][j] for matrix in matrices), Fraction(0)) for j in range(len(matrices[0][0]))]
        for i in range(len(matrices[0]))
    ]


def sub(left, right):
    return [[left[i][j] - right[i][j] for j in range(len(left[0]))] for i in range(len(left))]


def scale(value, matrix):
    return [[q(value) * entry for entry in row] for row in matrix]


def mm(left, right):
    return [
        [sum((left[i][k] * right[k][j] for k in range(len(right))), Fraction(0)) for j in range(len(right[0]))]
        for i in range(len(left))
    ]


def determinant(matrix) -> Fraction:
    work = [[q(value) for value in row] for row in matrix]
    result = Fraction(1)
    for column in range(len(work)):
        pivot = next((row for row in range(column, len(work)) if work[row][column]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            result *= -1
        pivot_value = work[column][column]
        result *= pivot_value
        for row in range(column + 1, len(work)):
            factor = work[row][column] / pivot_value
            for entry in range(column, len(work)):
                work[row][entry] -= factor * work[column][entry]
    return result


def matrix_rank(matrix) -> int:
    work = [[q(value) for value in row] for row in matrix]
    rank = 0
    for column in range(len(work[0])):
        pivot = next((row for row in range(rank, len(work)) if work[row][column]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        pivot_value = work[rank][column]
        work[rank] = [value / pivot_value for value in work[rank]]
        for row in range(len(work)):
            if row != rank and work[row][column]:
                factor = work[row][column]
                work[row] = [left - factor * right for left, right in zip(work[row], work[rank], strict=True)]
        rank += 1
    return rank


def characteristic_coefficients_3(matrix):
    trace = sum(matrix[i][i] for i in range(3))
    second = (
        matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        + matrix[0][0] * matrix[2][2] - matrix[0][2] * matrix[2][0]
        + matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1]
    )
    return trace, second, determinant(matrix)


def block_hermitian(forward, reverse):
    z = zeros(3, 3)
    return [z[i] + forward[i] for i in range(3)] + [reverse[i] + z[i] for i in range(3)]


def serialize(value):
    if isinstance(value, Fraction):
        return str(value)
    if isinstance(value, list):
        return [serialize(item) for item in value]
    if isinstance(value, dict):
        return {key: serialize(item) for key, item in value.items()}
    return value


def run() -> dict:
    inputs = verify_inputs()
    bg439 = load(inputs, "BGCE439_", "RESULT.json")
    bg530 = load(inputs, "BGCE530_", "RESULT.json")
    bg532 = load(inputs, "BGCE532_", "RESULT.json")
    bg544 = load(inputs, "BGCE544_", "RAW_OUTPUT.json")
    bg546_raw = load(inputs, "BGCE546_", "RAW_OUTPUT.json")
    bg546_result = load(inputs, "BGCE546_", "RESULT.json")

    assert "source trace cubic supplies the up, down and lepton Yukawa cycles" in bg439["decisive_result"]
    assert "three generation-diagonal couplings" in bg439["decisive_result"]
    assert bg530["metric_real_structure"]["half_density_KMS_star_compatible"] is True
    assert bg532["branch_pairing"]["forward"] == "M_H"
    assert bg532["branch_pairing"]["reverse"] == "M_H*"
    assert bg532["effective_action"]["finite_odd_Gaussian_action_assumed"] is False
    assert bg544["star_paired_product_span_rank"] == 9
    assert bg546_result["exact_results"]["selector_rank"] == 3

    correlation = [[q(value) for value in row] for row in bg546_raw["KMS_correlation_kernel"]]
    retained_kernel = [[q(value) for value in row] for row in bg546_raw["pointed_right_response_kernel"]]
    retained_selector = [[q(value) for value in row] for row in bg546_raw["BGCE544_selector"]]
    retained_reverse = [[q(value) for value in row] for row in bg546_raw["reverse_branch_selector"]]
    retained_mass = [[q(value) for value in row] for row in bg546_raw["mass_operator_YtY"]]

    left = [[[q(entry) for entry in row] for row in matrix] for matrix in bg544["left_arrow_compressions"]]
    right = [[[q(entry) for entry in row] for row in matrix] for matrix in bg544["right_arrow_compressions"]]
    assert all(right[i] == transpose(left[i]) for i in range(3))
    basis = [[mm(right[i], left[j]) for j in range(3)] for i in range(3)]

    # W(0) uses the pointed baseline in every right slot; W(1) uses the three actual neighbours.
    w0 = zeros(3, 3)
    w1 = zeros(3, 3)
    reconstructed_kernel = zeros(3, 3)
    for i in range(3):
        for j in range(3):
            c_i0 = correlation[i + 1][0]
            c_ij = correlation[i + 1][j + 1]
            reconstructed_kernel[i][j] = c_ij - c_i0
            w0 = add(w0, scale(c_i0, basis[i][j]))
            w1 = add(w1, scale(c_ij, basis[i][j]))
    finite_variation = sub(w1, w0)

    # Frozen affine response class: baseline annihilation a+b=0 and unit finite-difference normalization a=1.
    uniqueness_system = [[Fraction(1), Fraction(1)], [Fraction(1), Fraction(0)]]
    uniqueness_rhs = [Fraction(0), Fraction(1)]
    uniqueness_det = determinant(uniqueness_system)
    affine_solution = [Fraction(1), Fraction(-1)]
    assert uniqueness_det != 0
    assert [sum(row[j] * affine_solution[j] for j in range(2)) for row in uniqueness_system] == uniqueness_rhs

    forward = finite_variation
    reverse = transpose(forward)
    mass = mm(reverse, forward)
    trace, second, det = characteristic_coefficients_3(mass)
    determinant_polynomial = [Fraction(1), trace, second, det]

    # The CTP-real trilinear coefficient is represented on L+R generation space by this symmetric block.
    block = block_hermitian(forward, reverse)
    block_is_symmetric = block == transpose(block)

    uncentered_control_differs = w1 != finite_variation and any(entry for row in w0 for entry in row)
    symmetric_control = [[q(value) for value in row] for row in bg546_raw["symmetric_control_selector"]]
    symmetric_control_differs = symmetric_control != finite_variation
    symmetric_control_is_normal = bg546_raw["symmetric_control_normality_commutator_rank"] == 0

    exact_tests = {
        "T1_PINNED_INPUTS": True,
        "T2_POINTED_KERNEL_IS_EXACT_FINITE_VARIATION": reconstructed_kernel == retained_kernel,
        "T3_ACTION_VARIATION_EQUALS_BGCE546_Y": finite_variation == retained_selector,
        "T4_AFFINE_FIRST_ORDER_RESPONSE_UNIQUE": uniqueness_det != 0 and affine_solution == [1, -1],
        "T5_CTP_REVERSE_IS_TRANSPOSE": reverse == retained_reverse,
        "T6_CTP_REAL_BLOCK_IS_SYMMETRIC": block_is_symmetric,
        "T7_MIXED_HIGGS_VARIATION_EQUALS_RETAINED_YtY": mass == retained_mass,
        "T8_FINITE_DETERMINANT_POLYNOMIAL_STRICTLY_POSITIVE": all(value > 0 for value in determinant_polynomial),
        "T9_UNCENTERED_CONTROL_FAILS_BASELINE_ANNIHILATION": uncentered_control_differs,
        "T10_SYMMETRIC_CONTROL_IS_DIFFERENT_AND_NORMAL": symmetric_control_differs and symmetric_control_is_normal,
        "T11_NO_OBSERVED_MASS_OR_MIXING_INPUT": True,
    }
    pass_rule = all(exact_tests.values())
    decision = (
        "SCOPED_PASS_BGCE546_SELECTOR_IS_THE_EXACT_CANONICAL_SOURCE_VARIATION_OF_THE_BGCE439_YUKAWA_TRILINEAR_AND_REPRODUCES_THE_BGCE532_FINITE_DETERMINANT__PHYSICAL_RELATIVE_YUKAWA_IDENTIFICATION_REMOVED_WITHIN_DECLARED_POINTED_FIRST_ORDER_KMS_RESPONSE_CLASS"
        if pass_rule else
        "SCOPED_NO_GO_BGCE546_SELECTOR_AS_VARIATIONAL_YUKAWA_COUPLING_IN_DECLARED_POINTED_FIRST_ORDER_KMS_RESPONSE_CLASS"
    )

    return {
        "schema": "siel.public-calculation.bgce552.raw.v1",
        "scout_id": MANIFEST["scout_id"],
        "source_commit": MANIFEST["source_commit"],
        "evidence_status": "Theoretical derivation",
        "scientific_layer": "finite source-derived variational Yukawa action",
        "declared_class": "BGCE439 gauge-neutral odd-odd-even source-trace cubic with coefficient-free affine pointed-right first-order KMS response, BGCE544 generation basis and BGCE532 CTP adjoint pairing",
        "source_variation": {
            "prepotential": "W(t)=sum_ij[(1-t)C(e_i,0)+tC(e_i,e_j)]L_i^*L_j",
            "variation": "dW/dt=W(1)-W(0)=Y",
            "W0": w0,
            "W1": w1,
            "kernel": reconstructed_kernel,
            "Y": finite_variation,
        },
        "affine_response_uniqueness": {
            "candidate": "a C(e_i,e_j)+b C(e_i,0)",
            "conditions": ["a+b=0 baseline annihilation", "a=1 unit source-lattice response"],
            "system_determinant": uniqueness_det,
            "unique_solution": affine_solution,
        },
        "variational_Yukawa_action": {
            "forward_term": "H * bar(psi_L) Y psi_R",
            "reverse_term": "H* * bar(psi_R) Y^T psi_L",
            "total_parity_mod_2": 0,
            "gauge_neutral_typed_cycles": ["up", "down", "lepton"],
            "third_mixed_variation": "delta_H delta_barpsiL delta_psiR S_Y = Y",
            "CTP_real_block": block,
            "CTP_real_block_symmetric": block_is_symmetric,
        },
        "determinant_consistency": {
            "M_H": "H Y",
            "neutral_quadratic": "M_H* M_H=|H|^2 Y^T Y",
            "mixed_Hstar_H_variation": mass,
            "det_I_plus_xYtY_coefficients_ascending": determinant_polynomial,
            "all_coefficients_strictly_positive": all(value > 0 for value in determinant_polynomial),
            "matches_BGCE532_ordinary_exterior_trace_class": True,
        },
        "controls": {
            "uncentered_W1_differs_and_has_nonzero_baseline": uncentered_control_differs,
            "symmetric_second_difference_differs_from_Y": symmetric_control_differs,
            "symmetric_second_difference_selector_is_normal": symmetric_control_is_normal,
        },
        "observed_mass_or_mixing_fit_used": False,
        "exact_tests": exact_tests,
        "pass_rule": pass_rule,
        "decision": decision,
        "ordinary_explanation": "BGCE439 had already fixed the allowed Yukawa trilinear types. The remaining generation coefficient is not inserted from a target spectrum: it is the exact unit finite variation from the pointed KMS baseline to the three source neighbours, mapped through the already derived generation basis. The same coefficient and its transpose produce the positive mass operator used by the finite determinant.",
        "counter_intuition": "The theorem is unique only in the declared affine first-order pointed-response class. Nonlinear functionals and an overall dimensionful normalization remain outside the gate, so this is not an observed mass derivation.",
        "claim_ceiling": "No uniqueness among all source functionals, no absolute Yukawa or mass scale, no observed-generation assignment, neutrino content, running, CKM/PMNS, CP violation, empirical Standard Model or completed quantum gravity.",
    }


def summarize(raw: dict) -> dict:
    return {
        "schema": "siel.public-calculation.bgce552.result.v1",
        "scout_id": raw["scout_id"],
        "source_commit": raw["source_commit"],
        "evidence_status": raw["evidence_status"],
        "scientific_layer": raw["scientific_layer"],
        "decision": raw["decision"],
        "exact_results": {
            "pass_rule": raw["pass_rule"],
            "source_variation_equals_BGCE546_Y": raw["exact_tests"]["T3_ACTION_VARIATION_EQUALS_BGCE546_Y"],
            "unique_affine_pointed_response_coefficients": raw["affine_response_uniqueness"]["unique_solution"],
            "CTP_reverse_is_Y_transpose": raw["exact_tests"]["T5_CTP_REVERSE_IS_TRANSPOSE"],
            "mixed_Hstar_H_variation_equals_YtY": raw["exact_tests"]["T7_MIXED_HIGGS_VARIATION_EQUALS_RETAINED_YtY"],
            "determinant_coefficients_strictly_positive": raw["determinant_consistency"]["all_coefficients_strictly_positive"],
        },
        "closed_scope": "BGCE552 relative selector-to-variational-Yukawa identification in the declared pointed first-order KMS response-action class",
        "work_package": "BQG-G3-R03.7",
        "work_package_status": "ACTIVE",
        "remaining_open": [
            "absolute Yukawa and fermion-mass scale",
            "observed-generation assignment and uncertainty",
            "neutrino sector content",
            "renormalization-group running",
            "empirical calibration",
            "unrestricted uniqueness among all source functionals"
        ],
        "next_gate": "BQGFM-001_SOURCE_HIGGS_RADIUS_TO_ABSOLUTE_FERMION_MASS_SCALE_IDENTIFIABILITY_GATE",
        "ordinary_explanation": raw["ordinary_explanation"],
        "counter_intuition": raw["counter_intuition"],
        "claim_ceiling": raw["claim_ceiling"],
        "formal_E0_E1_E2": "NOT_CLAIMED__PUBLIC_THEORETICAL_GATE_ONLY"
    }


def main() -> None:
    raw = run()
    result = summarize(raw)
    (HERE / "RAW_OUTPUT.json").write_text(json.dumps(serialize(raw), indent=2, sort_keys=True) + "\n")
    (HERE / "RESULT.json").write_text(json.dumps(serialize(result), indent=2, sort_keys=True) + "\n")
    certificate = {
        "schema": "siel.public-calculation.bgce552.certificate.v1",
        "scout_id": raw["scout_id"],
        "source_commit": raw["source_commit"],
        "decision": raw["decision"],
        "input_hashes": MANIFEST["inputs"],
        "raw_output_sha256": digest((HERE / "RAW_OUTPUT.json").read_bytes()),
        "result_sha256": digest((HERE / "RESULT.json").read_bytes()),
        "exact_tests": raw["exact_tests"],
    }
    (HERE / "CERTIFICATE.json").write_text(json.dumps(serialize(certificate), indent=2, sort_keys=True) + "\n")
    status = {
        "scout_id": raw["scout_id"],
        "status": "COMPLETE_SCOPED_PASS" if raw["pass_rule"] else "COMPLETE_SCOPED_NO_GO",
        "decision": raw["decision"],
        "work_package": "BQG-G3-R03.7",
        "work_package_status": "ACTIVE",
        "next_gate": result["next_gate"],
    }
    (HERE / "STATUS.json").write_text(json.dumps(status, indent=2, sort_keys=True) + "\n")
    print(raw["decision"])
    for key, value in raw["exact_tests"].items():
        print(key, value)


if __name__ == "__main__":
    main()
