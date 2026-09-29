#!/usr/bin/env python3
"""Reconstruct every BGCE443 R6 toy endpoint from retained raw exact matrices."""

from __future__ import annotations

import hashlib
import itertools
import json
import sys
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
Matrix = list[list[complex]]


def gauss(value: str) -> complex:
    assert isinstance(value, str)
    parsed = complex(value.replace("i", "j"))
    assert parsed.real.is_integer() and parsed.imag.is_integer()
    return parsed


def gaussian_string(value: complex) -> str:
    assert value.real.is_integer() and value.imag.is_integer()
    real, imag = int(value.real), int(value.imag)
    if imag == 0:
        return str(real)
    return f"{real}{imag:+d}i"


def zeros(rows: int, columns: int) -> Matrix:
    return [[0j for _ in range(columns)] for _ in range(rows)]


def dense(raw: dict) -> Matrix:
    assert set(raw) == {"rows", "columns", "entries"}
    rows, columns = raw["rows"], raw["columns"]
    assert isinstance(rows, int) and rows > 0 and isinstance(columns, int) and columns > 0
    out = zeros(rows, columns)
    seen = set()
    for entry in raw["entries"]:
        assert set(entry) == {"row", "column", "value"}
        row, column = entry["row"], entry["column"]
        assert isinstance(row, int) and 0 <= row < rows
        assert isinstance(column, int) and 0 <= column < columns
        assert (row, column) not in seen
        seen.add((row, column))
        value = gauss(entry["value"])
        assert value != 0
        out[row][column] = value
    return out


def identity(size: int) -> Matrix:
    return [[1 if row == column else 0 for column in range(size)] for row in range(size)]


def add(left: Matrix, right: Matrix) -> Matrix:
    return [[left[row][column] + right[row][column] for column in range(len(left[0]))] for row in range(len(left))]


def sub(left: Matrix, right: Matrix) -> Matrix:
    return [[left[row][column] - right[row][column] for column in range(len(left[0]))] for row in range(len(left))]


def scale(scalar: complex, matrix: Matrix) -> Matrix:
    return [[scalar * entry for entry in row] for row in matrix]


def matmul(left: Matrix, right: Matrix) -> Matrix:
    assert len(left[0]) == len(right)
    return [[sum(left[row][k] * right[k][column] for k in range(len(right))) for column in range(len(right[0]))] for row in range(len(left))]


def dagger(matrix: Matrix) -> Matrix:
    return [[matrix[row][column].conjugate() for row in range(len(matrix))] for column in range(len(matrix[0]))]


def equal(left: Matrix, right: Matrix) -> bool:
    return len(left) == len(right) and len(left[0]) == len(right[0]) and all(left[r][c] == right[r][c] for r in range(len(left)) for c in range(len(left[0])))


def commutator(left: Matrix, right: Matrix) -> Matrix:
    return sub(matmul(left, right), matmul(right, left))


def kron(left: Matrix, right: Matrix) -> Matrix:
    out = zeros(len(left) * len(right), len(left[0]) * len(right[0]))
    for i, j, k, l in itertools.product(range(len(left)), range(len(left[0])), range(len(right)), range(len(right[0]))):
        out[i * len(right) + k][j * len(right[0]) + l] = left[i][j] * right[k][l]
    return out


def tensor_all(matrices: list[Matrix]) -> Matrix:
    out: Matrix = [[1]]
    for matrix in matrices:
        out = kron(out, matrix)
    return out


def tensor_vectors(vectors: list[list[complex]]) -> list[complex]:
    out = [1]
    for vector in vectors:
        out = [left * right for left in out for right in vector]
    return out


def matvec(matrix: Matrix, vector: list[complex]) -> list[complex]:
    return [sum(row[column] * vector[column] for column in range(len(vector))) for row in matrix]


def vector_norm_square(vector: list[complex]) -> int:
    value = sum((entry.conjugate() * entry).real for entry in vector)
    assert value.is_integer()
    return int(value)


def frobenius_square(matrix: Matrix) -> int:
    value = sum((entry.conjugate() * entry).real for row in matrix for entry in row)
    assert value.is_integer()
    return int(value)


I2 = identity(2)


def embed_site(operator: Matrix, site: int, order: int) -> Matrix:
    return tensor_all([operator if index == site else I2 for index in range(order)])


def finite_implementer(seed: Matrix, order: int) -> Matrix:
    out = zeros(2**order, 2**order)
    for position in range(order - 2):
        out = add(out, embed_site(seed, position, order))
    return out


def matrix_payload(matrix: Matrix) -> bytes:
    rows = [[gaussian_string(entry) for entry in row] for row in matrix]
    return json.dumps(rows, separators=(",", ":")).encode()


def matrix_hash(matrix: Matrix) -> str:
    return hashlib.sha256(matrix_payload(matrix)).hexdigest()


def determinant(matrix: Matrix) -> complex:
    if not matrix:
        return 1
    if len(matrix) == 1:
        return matrix[0][0]
    return sum(((-1) ** column) * matrix[0][column] * determinant([row[:column] + row[column + 1 :] for row in matrix[1:]]) for column in range(len(matrix)))


def rank_certificate(endpoint: dict) -> int:
    rows = [[gauss(value) for value in row] for row in endpoint["derivation_rows_exact"]]
    maximum = min(len(rows), len(rows[0]) if rows else 0)
    computed_rank = 0
    computed_minor = None
    for rank in range(maximum, 0, -1):
        for row_indices in itertools.combinations(range(len(rows)), rank):
            for columns in itertools.combinations(range(len(rows[0])), rank):
                value = determinant([[rows[row][column] for column in columns] for row in row_indices])
                if value != 0:
                    computed_rank = rank
                    computed_minor = {"rows": list(row_indices), "columns": list(columns), "determinant": gaussian_string(value)}
                    break
            if computed_minor:
                break
        if computed_minor:
            break
    assert endpoint["rank"] == computed_rank
    assert endpoint["nonzero_minor"] == computed_minor
    return computed_rank


def polynomial_degree(coefficients: list[int]) -> int:
    for degree in range(len(coefficients) - 1, -1, -1):
        if coefficients[degree] != 0:
            return degree
    return -1


def polynomial_value(coefficients: list[int], n: int) -> int:
    return sum(coefficient * n**degree for degree, coefficient in enumerate(coefficients))


def classify(all_n: dict) -> dict:
    lower = all_n["action_norm_lower_bound_polynomial"]["coefficients_ascending"]
    upper = all_n["action_norm_upper_bound_polynomial"]["coefficients_ascending"]
    lower_degree, upper_degree = polynomial_degree(lower), polynomial_degree(upper)
    unbounded = all_n["proof_valid"] and lower_degree == 1 and lower[1] > 0
    bounded = all_n["proof_valid"] and upper_degree <= 0
    return {
        "quantifier": f"all integers n >= {all_n['domain_minimum_order']}",
        "lower_polynomial_degree": lower_degree,
        "upper_polynomial_degree": upper_degree,
        "linear_slope": lower[1] if unbounded else 0,
        "all_n_unbounded_linear": unbounded,
        "uniformly_bounded": bounded,
        "outer_unbounded_pass": unbounded and not bounded,
    }


def basis_bits(index: int, order: int) -> list[int]:
    return [(index >> (order - 1 - site)) & 1 for site in range(order)]


def bits_index(bits: list[int]) -> int:
    value = 0
    for bit in bits:
        value = (value << 1) | bit
    return value


def adjacent_swap(order: int, left: int, signed: bool) -> Matrix:
    out = zeros(2**order, 2**order)
    for column in range(2**order):
        bits = basis_bits(column, order)
        phase = (-1) ** (bits[left] + bits[left + 1]) if signed else 1
        bits[left], bits[left + 1] = bits[left + 1], bits[left]
        out[bits_index(bits)][column] = phase
    return out


def swap_implementer(seed: Matrix, order: int, signed: bool) -> Matrix:
    out = zeros(2**order, 2**order)
    for position in range(order - 2):
        unitary = identity(2**order)
        for left in range(position):
            unitary = matmul(adjacent_swap(order, left, signed), unitary)
        out = add(out, matmul(matmul(unitary, embed_site(seed, 0, order)), dagger(unitary)))
    return out


def normalized_trace_square(matrix: Matrix) -> Fraction:
    value = sum(matmul(matrix, matrix)[i][i] for i in range(len(matrix)))
    assert value.imag == 0 and value.real.is_integer()
    return Fraction(int(value.real), len(matrix))


def reconstruct_stabilization(seed: Matrix) -> dict:
    local = tensor_all([[[0, 1], [1, 0]], [[1, 0], [0, -1]]])
    threshold = 4
    base_p = finite_implementer(seed, threshold)
    base_a = tensor_all([local] + [I2] * 2)
    base_delta = scale(1j, commutator(base_p, base_a))
    records = []
    for order in range(4, 7):
        p_n = finite_implementer(seed, order)
        a_n = tensor_all([local] + [I2] * (order - 2))
        delta = scale(1j, commutator(p_n, a_n))
        expected = tensor_all([base_delta] + [I2] * (order - threshold))
        records.append({"order": order, "residual_frobenius_square": frobenius_square(sub(delta, expected))})
    return {"support_order": 2, "threshold": 4, "records": records, "pass": all(row["residual_frobenius_square"] == 0 for row in records)}


def reconstruct_variance(seed: Matrix) -> dict:
    records = []
    for order in range(3, 7):
        variance = normalized_trace_square(finite_implementer(seed, order))
        expected = Fraction(order - 2, 1)
        records.append({"order": order, "variance": str(variance), "expected": str(expected), "residual": str(variance - expected)})
    return {"records": records, "slope": "1", "pass": all(row["residual"] == "0" for row in records)}


def reconstruct_action(endpoint: dict) -> None:
    seed = dense(endpoint["local_raw"]["seed"])
    partner = dense(endpoint["local_raw"]["partner"])
    eigenvector = [gauss(value) for value in endpoint["local_raw"]["plus_eigenvector"]]
    checks = {
        "seed_self_adjoint": equal(seed, dagger(seed)),
        "seed_involution": equal(matmul(seed, seed), I2),
        "partner_self_adjoint": equal(partner, dagger(partner)),
        "partner_unitary": equal(matmul(dagger(partner), partner), I2),
        "anticommutator_residual_frobenius_square": frobenius_square(add(matmul(seed, partner), matmul(partner, seed))),
        "plus_eigenvector_residual_square": vector_norm_square([left - right for left, right in zip(matvec(seed, eigenvector), eigenvector)]),
        "plus_eigenvector_norm_square": vector_norm_square(eigenvector),
    }
    assert endpoint["local_checks"] == checks
    proof = all([checks["seed_self_adjoint"], checks["seed_involution"], checks["partner_self_adjoint"], checks["partner_unitary"]]) and checks["anticommutator_residual_frobenius_square"] == 0 and checks["plus_eigenvector_residual_square"] == 0 and checks["plus_eigenvector_norm_square"] > 0
    all_n = endpoint["all_n_certificate"]
    assert all_n["domain_minimum_order"] == 3 and all_n["active_window_count_polynomial"]["coefficients_ascending"] == [-2, 1]
    assert all_n["implementer_eigenvalue_polynomial"]["coefficients_ascending"] == [-2, 1]
    assert all_n["action_norm_lower_bound_polynomial"]["coefficients_ascending"] == [-4, 2]
    assert all_n["action_norm_upper_bound_polynomial"]["coefficients_ascending"] == [-4, 2]
    assert all_n["action_ratio_square_polynomial"]["coefficients_ascending"] == [16, -16, 4]
    assert all_n["proof_valid"] is proof
    assert endpoint["classification"] == classify(all_n)
    reconstructed_rows = []
    for order in range(3, 7):
        active = order - 2
        p_n = finite_implementer(seed, order)
        observable = tensor_all([partner if site < active else I2 for site in range(order)])
        vector = tensor_vectors([eigenvector if site < active else [1, 0] for site in range(order)])
        p_residual = [left - active * right for left, right in zip(matvec(p_n, vector), vector)]
        action = commutator(p_n, observable)
        av = matvec(observable, vector)
        action_residual = [left + 2 * active * right for left, right in zip(matvec(action, vector), av)]
        ratio = Fraction(vector_norm_square(matvec(action, vector)), vector_norm_square(vector))
        reconstructed_rows.append({
            "order": order,
            "implementer_eigenvector_residual_square": vector_norm_square(p_residual),
            "action_vector_residual_square": vector_norm_square(action_residual),
            "observable_unitarity_residual_frobenius_square": frobenius_square(sub(matmul(dagger(observable), observable), identity(2**order))),
            "action_ratio_square": str(ratio),
            "action_norm_lower_bound": str(polynomial_value([-4, 2], order)),
            "action_norm_upper_bound": str(polynomial_value([-4, 2], order)),
        })
    assert endpoint["records"] == reconstructed_rows
    exact = all(row["implementer_eigenvector_residual_square"] == 0 and row["action_vector_residual_square"] == 0 and row["observable_unitarity_residual_frobenius_square"] == 0 and Fraction(row["action_ratio_square"]) == int(row["action_norm_lower_bound"]) ** 2 for row in reconstructed_rows)
    assert endpoint["exact_norm_certificate"] is exact
    assert endpoint["bounded_inner_excluded"] is (proof and exact and endpoint["classification"]["outer_unbounded_pass"])


def reconstruct_bounded(endpoint: dict) -> None:
    seed = dense(endpoint["local_raw"]["seed"])
    observable2 = dense(endpoint["local_raw"]["observable"])
    local_action = commutator(seed, observable2)
    assert equal(local_action, dense(endpoint["local_raw"]["local_action"]))
    all_n = endpoint["all_n_certificate"]
    expected_proof = equal(seed, dagger(seed)) and equal(matmul(seed, seed), I2) and equal(matmul(dagger(observable2), observable2), I2) and frobenius_square(local_action) > 0
    assert all_n["telescoping_coefficients"] == {"left_boundary": 1, "interior": 0, "right_boundary": -1}
    assert all_n["implementer_norm_upper_bound_polynomial"]["coefficients_ascending"] == [2]
    assert all_n["action_norm_lower_bound_polynomial"]["coefficients_ascending"] == [2]
    assert all_n["action_norm_upper_bound_polynomial"]["coefficients_ascending"] == [4]
    assert all_n["proof_valid"] is expected_proof
    assert endpoint["classification"] == classify(all_n)
    records = []
    for order in range(2, 7):
        p_n = zeros(2**order, 2**order)
        for position in range(order - 1):
            p_n = add(p_n, sub(embed_site(seed, position, order), embed_site(seed, position + 1, order)))
        expected = sub(embed_site(seed, 0, order), embed_site(seed, order - 1, order))
        observable = embed_site(observable2, 0, order)
        vector = tensor_vectors([[1, 0] for _ in range(order)])
        action = commutator(p_n, observable)
        ratio = Fraction(vector_norm_square(matvec(action, vector)), vector_norm_square(vector))
        records.append({"order": order, "telescoping_residual_frobenius_square": frobenius_square(sub(p_n, expected)), "action_ratio_square": str(ratio), "action_norm_lower_bound": "2", "action_norm_upper_bound": "4"})
    assert endpoint["records"] == records
    assert endpoint["outer_unbounded_pass"] is endpoint["classification"]["outer_unbounded_pass"]


def reconstruct_closability(endpoint: dict) -> bool:
    seeds = [dense(raw) for raw in endpoint["local_terms_raw"]]
    hermitian = [equal(seed, dagger(seed)) for seed in seeds]
    involutions = [equal(matmul(seed, seed), I2) for seed in seeds]
    commutation = []
    for seed in seeds:
        terms = [embed_site(seed, position, 6) for position in range(4)]
        commutation.append(all(frobenius_square(commutator(left, right)) == 0 for left, right in itertools.combinations(terms, 2)))
    covariance = all(equal(matmul(matmul(swap_word(6, position, False), embed_site(seed, 0, 6)), dagger(swap_word(6, position, False))), embed_site(seed, position, 6)) for seed in seeds for position in range(4))
    constructed = all(hermitian) and all(involutions) and all(commutation) and covariance
    assert endpoint["self_adjoint_local_terms"] == hermitian
    assert endpoint["local_involutions"] == involutions
    assert endpoint["translated_terms_pairwise_commute"] == commutation
    assert endpoint["translation_covariance_checked"] is covariance
    assert endpoint["explicit_group_constructed"] is constructed
    assert endpoint["pass"] is constructed
    return constructed


def swap_word(order: int, position: int, signed: bool) -> Matrix:
    unitary = identity(2**order)
    for left in range(position):
        unitary = matmul(adjacent_swap(order, left, signed), unitary)
    return unitary


def reconstruct_comparator(comparator: dict) -> bool:
    seed = [[0, 1], [1, 0]]
    relation_truth = {}
    for transport, signed in (("signed", True), ("unsigned", False)):
        endpoint = comparator[f"{transport}_relation_certificate"]
        raw = endpoint["raw_generators"]
        expected = {
            "order3_s0": adjacent_swap(3, 0, signed),
            "order3_s1": adjacent_swap(3, 1, signed),
            "order4_t0": adjacent_swap(4, 0, signed),
            "order4_t2": adjacent_swap(4, 2, signed),
        }
        for key, matrix in expected.items():
            assert equal(dense(raw[key]), matrix)
        s0, s1, t0, t2 = expected["order3_s0"], expected["order3_s1"], expected["order4_t0"], expected["order4_t2"]
        certificate = {"involution": equal(matmul(s0, s0), identity(8)) and equal(matmul(s1, s1), identity(8)), "braid_relation": equal(matmul(matmul(s0, s1), s0), matmul(matmul(s1, s0), s1)), "distant_commutation": equal(matmul(t0, t2), matmul(t2, t0))}
        assert endpoint["certificate"] == certificate
        relation_truth[transport] = all(certificate.values())

    implementers = {}
    for transport, signed in (("signed", True), ("unsigned", False)):
        implementers[transport] = swap_implementer(seed, 6, signed)
        assert equal(dense(comparator[f"{transport}_implementer_sparse"]), implementers[transport])
        variance_records = []
        for order in range(3, 7):
            variance = normalized_trace_square(swap_implementer(seed, order, signed))
            expected = Fraction(order - 2, 1)
            variance_records.append({"order": order, "variance": str(variance), "expected": str(expected), "residual": str(variance - expected)})
        variance_endpoint = comparator[f"{transport}_variance"]
        assert variance_endpoint["records"] == variance_records
        assert variance_endpoint["pass"] is all(row["residual"] == "0" for row in variance_records)
        assert comparator[f"{transport}_carrier_pass"] is variance_endpoint["pass"]

    digests = {}
    retained = comparator["raw_action_rows_retained"]
    for transport in ("signed", "unsigned"):
        rows = retained[transport]
        assert len(rows) == 16 and {(row["basis_row"], row["basis_column"]) for row in rows} == {(row, column) for row in range(4) for column in range(4)}
        hashes = []
        for row in rows:
            basis = [[1 if (i, j) == (row["basis_row"], row["basis_column"]) else 0 for j in range(4)] for i in range(4)]
            observable = tensor_all([basis] + [I2] * 4)
            assert equal(dense(row["observable_sparse"]), observable)
            action = scale(1j, commutator(implementers[transport], observable))
            assert equal(dense(row["action_sparse"]), action)
            assert row["action_sha256"] == matrix_hash(action)
            hashes.append(row["action_sha256"])
        digests[transport] = hashlib.sha256(json.dumps(hashes, separators=(",", ":")).encode()).hexdigest()
        assert comparator[f"{transport}_raw_action_sha256"] == digests[transport]
    differences = sum(left["action_sha256"] != right["action_sha256"] for left, right in zip(retained["signed"], retained["unsigned"]))
    assert comparator["differing_raw_action_rows"] == differences
    matching = comparator["matching_invariants"]
    expected_matching = {"matrix_dimension_equal": True, "window_count_equal": 4, "local_seed_identical": True, "local_seed_involution": True, "same_adjacent_words": True, "signed_relations_pass": relation_truth["signed"], "unsigned_relations_pass": relation_truth["unsigned"]}
    assert matching == expected_matching
    both_carriers = comparator["signed_carrier_pass"] and comparator["unsigned_carrier_pass"]
    assert comparator["generic_carrier_decision"] == ("PASS" if both_carriers else "FAIL")
    assert comparator["transport_specificity_decision"] == ("PASS_TOY_RAW_ACTION_DIFFERENCE" if differences else "NO_GO_IDENTICAL_RAW_ACTION")
    reconstructed = all(matching.values()) and both_carriers and differences > 0
    assert comparator["non_structural"] is reconstructed
    return reconstructed


def validate(result: dict, schema: dict) -> dict:
    assert result["schema"] == schema["result_schema"]
    assert result["focal_source_used"] is False
    positive, negative = result["positive"], result["negative_controls"]
    assert len(positive["action_growth"]) == 3
    seeds = [dense(endpoint["local_raw"]["seed"]) for endpoint in positive["action_growth"]]
    for endpoint in positive["action_growth"]:
        reconstruct_action(endpoint)
    assert positive["stabilization"] == [reconstruct_stabilization(seed) for seed in seeds]
    assert positive["variance_growth"] == [reconstruct_variance(seed) for seed in seeds]
    assert rank_certificate(positive["rank"]) == 3
    assert rank_certificate(negative["zero_seed_rank"]) == 0
    assert rank_certificate(negative["single_direction_rank"]) == 1
    assert rank_certificate(negative["rank_two"]) == 2
    reconstruct_bounded(negative["bounded_telescoping"])
    positive_close = reconstruct_closability(positive["closability"])
    bounded_close = reconstruct_closability(negative["bounded_telescoping_closability"])
    failed_close = reconstruct_closability(negative["closability_hypothesis_failure"])
    defect = negative["closability_hypothesis_failure"]["star_derivation_defect"]
    observable = dense(defect["observable_sparse"])
    failed_seed = dense(negative["closability_hypothesis_failure"]["local_terms_raw"][0])
    delta_star = scale(1j, commutator(failed_seed, dagger(observable)))
    star_delta = dagger(scale(1j, commutator(failed_seed, observable)))
    residual = sub(delta_star, star_delta)
    assert equal(dense(defect["delta_star_sparse"]), delta_star)
    assert equal(dense(defect["star_delta_sparse"]), star_delta)
    assert equal(dense(defect["residual_sparse"]), residual)
    assert defect["residual_frobenius_square"] == frobenius_square(residual) > 0
    comparator = reconstruct_comparator(result["matched_comparator"])
    decisions = {
        "positive_all_endpoints": all(item["pass"] for item in positive["stabilization"]) and all(item["pass"] for item in positive["variance_growth"]) and positive["rank"]["rank"] == 3 and all(item["bounded_inner_excluded"] for item in positive["action_growth"]) and positive_close,
        "zero_rejected": negative["zero_seed_rank"]["rank"] == 0,
        "rank_two_rejected": negative["rank_two"]["rank"] == 2,
        "single_direction_reports_rank_one": negative["single_direction_rank"]["rank"] == 1,
        "bounded_inner_rejected": not negative["bounded_telescoping"]["outer_unbounded_pass"],
        "bounded_negative_still_closable": bounded_close,
        "closability_hypothesis_failure_rejected": not failed_close and defect is not None,
        "matched_comparator_non_structural": comparator,
    }
    assert result["decision"] == decisions
    assert result["all_expected_separations"] is all(decisions.values())
    return {"schema": "siel.public-calculation.bgce443.r6.retention-validation-result.v1", "status": "PASS", "all_n_certificates_reconstructed": 4, "rank_endpoints_reconstructed": 4, "raw_action_matrices_reconstructed": 32, "relation_certificates_reconstructed": 2, "decisions_reconstructed": len(decisions), "all_expected_separations": result["all_expected_separations"]}


if __name__ == "__main__":
    result = json.loads((HERE / "WITNESS_RESULT.json").read_text())
    schema = json.loads((HERE / "RAW_ROW_SCHEMA.json").read_text())
    rendered = json.dumps(validate(result, schema), sort_keys=True, indent=2) + "\n"
    if len(sys.argv) == 3 and sys.argv[1] == "--output":
        Path(sys.argv[2]).write_text(rendered)
    elif len(sys.argv) != 1:
        raise SystemExit("usage: validate_retention.py [--output PATH]")
    print(rendered, end="")
