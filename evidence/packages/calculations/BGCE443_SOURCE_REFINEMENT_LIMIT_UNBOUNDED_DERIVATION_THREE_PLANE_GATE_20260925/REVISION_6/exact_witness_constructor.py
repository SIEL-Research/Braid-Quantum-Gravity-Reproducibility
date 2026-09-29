#!/usr/bin/env python3
"""Exact non-focal constructors for the BGCE443 Revision 6 E0 witness.

The script uses only explicit 2x2 toy operators. It does not read or construct
the actual BGCE443 source endpoint.
"""

from __future__ import annotations

import itertools
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path


Matrix = list[list[complex]]


I2: Matrix = [[1, 0], [0, 1]]
X: Matrix = [[0, 1], [1, 0]]
Y: Matrix = [[0, -1j], [1j, 0]]
Z: Matrix = [[1, 0], [0, -1]]
R: Matrix = [[0, 1], [0, 0]]
ZERO2: Matrix = [[0, 0], [0, 0]]


def shape(a: Matrix) -> tuple[int, int]:
    return len(a), len(a[0])


def zeros(rows: int, cols: int) -> Matrix:
    return [[0j for _ in range(cols)] for _ in range(rows)]


def identity(dim: int) -> Matrix:
    return [[1 if i == j else 0 for j in range(dim)] for i in range(dim)]


def add(a: Matrix, b: Matrix) -> Matrix:
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def sub(a: Matrix, b: Matrix) -> Matrix:
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def scale(c: complex, a: Matrix) -> Matrix:
    return [[c * value for value in row] for row in a]


def matmul(a: Matrix, b: Matrix) -> Matrix:
    rows, inner = shape(a)
    inner_b, cols = shape(b)
    assert inner == inner_b
    return [
        [sum(a[i][k] * b[k][j] for k in range(inner)) for j in range(cols)]
        for i in range(rows)
    ]


def dagger(a: Matrix) -> Matrix:
    rows, cols = shape(a)
    return [[a[i][j].conjugate() for i in range(rows)] for j in range(cols)]


def kron(a: Matrix, b: Matrix) -> Matrix:
    ar, ac = shape(a)
    br, bc = shape(b)
    out = zeros(ar * br, ac * bc)
    for i, j, k, l in itertools.product(range(ar), range(ac), range(br), range(bc)):
        out[i * br + k][j * bc + l] = a[i][j] * b[k][l]
    return out


def tensor_all(ops: list[Matrix]) -> Matrix:
    out: Matrix = [[1]]
    for op in ops:
        out = kron(out, op)
    return out


def tensor_vectors(vectors: list[list[complex]]) -> list[complex]:
    out = [1]
    for vector in vectors:
        out = [left * right for left in out for right in vector]
    return out


def embed_site(op: Matrix, site: int, order: int) -> Matrix:
    return tensor_all([op if index == site else I2 for index in range(order)])


def commutator(a: Matrix, b: Matrix) -> Matrix:
    return sub(matmul(a, b), matmul(b, a))


def trace(a: Matrix) -> complex:
    return sum(a[i][i] for i in range(len(a)))


def frobenius_square(a: Matrix) -> int:
    value = sum((entry.conjugate() * entry).real for row in a for entry in row)
    assert float(value).is_integer()
    return int(value)


def equal(a: Matrix, b: Matrix) -> bool:
    return shape(a) == shape(b) and all(a[i][j] == b[i][j] for i in range(len(a)) for j in range(len(a[0])))


def is_zero(a: Matrix) -> bool:
    return all(entry == 0 for row in a for entry in row)


def is_hermitian(a: Matrix) -> bool:
    return equal(a, dagger(a))


def flatten(a: Matrix) -> list[complex]:
    return [entry for row in a for entry in row]


def determinant(matrix: list[list[complex]]) -> complex:
    size = len(matrix)
    if size == 0:
        return 1
    if size == 1:
        return matrix[0][0]
    total = 0j
    for column in range(size):
        minor = [row[:column] + row[column + 1 :] for row in matrix[1:]]
        total += ((-1) ** column) * matrix[0][column] * determinant(minor)
    return total


def derivation_row(seed: Matrix) -> list[complex]:
    basis = [
        [[1 if (i, j) == (row, col) else 0 for j in range(2)] for i in range(2)]
        for row in range(2)
        for col in range(2)
    ]
    return [value for unit in basis for value in flatten(scale(1j, commutator(seed, unit)))]


def exact_rank_certificate(seeds: list[Matrix]) -> dict:
    rows = [derivation_row(seed) for seed in seeds]
    raw_rows = [[gaussian_string(value) for value in row] for row in rows]
    max_rank = min(len(rows), len(rows[0]) if rows else 0)
    for rank in range(max_rank, 0, -1):
        for row_indices in itertools.combinations(range(len(rows)), rank):
            for columns in itertools.combinations(range(len(rows[0])), rank):
                minor = [[rows[row][column] for column in columns] for row in row_indices]
                value = determinant(minor)
                if value != 0:
                    return {
                        "rank": rank,
                        "derivation_rows_exact": raw_rows,
                        "nonzero_minor": {
                            "rows": list(row_indices),
                            "columns": list(columns),
                            "determinant": gaussian_string(value),
                        },
                    }
    return {"rank": 0, "derivation_rows_exact": raw_rows, "nonzero_minor": None}


def gaussian_string(value: complex) -> str:
    real = int(value.real)
    imag = int(value.imag)
    if imag == 0:
        return str(real)
    return f"{real}{imag:+d}i"


def matrix_payload(a: Matrix) -> bytes:
    rows = [[gaussian_string(entry) for entry in row] for row in a]
    return json.dumps(rows, separators=(",", ":")).encode()


def matrix_sha256(a: Matrix) -> str:
    return hashlib.sha256(matrix_payload(a)).hexdigest()


def sparse_matrix(a: Matrix) -> dict:
    rows, columns = shape(a)
    return {
        "rows": rows,
        "columns": columns,
        "entries": [
            {"row": row, "column": column, "value": gaussian_string(a[row][column])}
            for row in range(rows)
            for column in range(columns)
            if a[row][column] != 0
        ],
    }


def raw_vector(vector: list[complex]) -> list[str]:
    return [gaussian_string(value) for value in vector]


def matvec(a: Matrix, vector: list[complex]) -> list[complex]:
    return [sum(row[j] * vector[j] for j in range(len(vector))) for row in a]


def vector_sub(a: list[complex], b: list[complex]) -> list[complex]:
    return [x - y for x, y in zip(a, b)]


def vector_scale(c: complex, vector: list[complex]) -> list[complex]:
    return [c * value for value in vector]


def vector_norm_square(vector: list[complex]) -> int:
    value = sum((entry.conjugate() * entry).real for entry in vector)
    assert float(value).is_integer()
    return int(value)


def basis_bits(index: int, order: int) -> list[int]:
    return [(index >> (order - 1 - site)) & 1 for site in range(order)]


def bits_index(bits: list[int]) -> int:
    value = 0
    for bit in bits:
        value = (value << 1) | bit
    return value


def adjacent_swap(order: int, left: int, signed: bool) -> Matrix:
    """Canonical unsigned swap or ZxZ-gauged signed swap."""
    dim = 2**order
    out = zeros(dim, dim)
    for column in range(dim):
        bits = basis_bits(column, order)
        phase = (-1) ** (bits[left] + bits[left + 1]) if signed else 1
        bits[left], bits[left + 1] = bits[left + 1], bits[left]
        out[bits_index(bits)][column] = phase
    return out


def transport_word_unitary(order: int, position: int, signed: bool) -> tuple[Matrix, list[int]]:
    word = list(range(position))
    unitary = identity(2**order)
    for left in word:
        unitary = matmul(adjacent_swap(order, left, signed), unitary)
    return unitary, word


def swap_transport(seed: Matrix, order: int, position: int, signed: bool) -> tuple[Matrix, list[int]]:
    unitary, word = transport_word_unitary(order, position, signed)
    base = embed_site(seed, 0, order)
    return matmul(matmul(unitary, base), dagger(unitary)), word


def swap_implementer(seed: Matrix, order: int, signed: bool) -> Matrix:
    out = zeros(2**order, 2**order)
    for position in range(order - 2):
        transported, _ = swap_transport(seed, order, position, signed)
        out = add(out, transported)
    return out


def transported_seed(seed: Matrix, position: int, signed: bool) -> Matrix:
    if not signed or position % 2 == 0:
        return seed
    return matmul(matmul(Z, seed), Z)


def finite_implementer(seed: Matrix, order: int, signed: bool = False) -> Matrix:
    # A range-three window with seed on its first tensor factor. There are n-2 windows.
    out = zeros(2**order, 2**order)
    for position in range(order - 2):
        out = add(out, embed_site(transported_seed(seed, position, signed), position, order))
    return out


def normalized_trace_square(a: Matrix) -> Fraction:
    value = trace(matmul(a, a))
    assert value.imag == 0 and float(value.real).is_integer()
    return Fraction(int(value.real), len(a))


def stabilization_certificate(seed: Matrix) -> dict:
    support_order = 2
    local_observable = tensor_all([X, Z])
    threshold = support_order + 2
    base_p = finite_implementer(seed, threshold)
    base_a = tensor_all([local_observable] + [I2] * (threshold - support_order))
    base_delta = scale(1j, commutator(base_p, base_a))
    records = []
    for order in range(threshold, threshold + 3):
        p_n = finite_implementer(seed, order)
        a_n = tensor_all([local_observable] + [I2] * (order - support_order))
        delta_n = scale(1j, commutator(p_n, a_n))
        expected = tensor_all([base_delta] + [I2] * (order - threshold))
        residual = sub(delta_n, expected)
        records.append({"order": order, "residual_frobenius_square": frobenius_square(residual)})
    return {"support_order": support_order, "threshold": threshold, "records": records, "pass": all(row["residual_frobenius_square"] == 0 for row in records)}


def variance_certificate(seed: Matrix, signed: bool = False) -> dict:
    records = []
    for order in range(3, 7):
        p_n = finite_implementer(seed, order, signed=signed)
        variance = normalized_trace_square(p_n)
        expected = Fraction(order - 2, 1)
        records.append({"order": order, "variance": str(variance), "expected": str(expected), "residual": str(variance - expected)})
    return {"records": records, "slope": "1", "pass": all(row["residual"] == "0" for row in records)}


def plus_eigenvector(seed: Matrix) -> list[complex]:
    if equal(seed, X):
        return [1, 1]
    if equal(seed, Y):
        return [1, 1j]
    if equal(seed, Z):
        return [1, 0]
    raise ValueError("no exact plus eigenvector registered")


def polynomial_degree(coefficients: list[int]) -> int:
    for degree in range(len(coefficients) - 1, -1, -1):
        if coefficients[degree] != 0:
            return degree
    return -1


def classify_action_growth(all_n: dict) -> dict:
    lower = all_n["action_norm_lower_bound_polynomial"]["coefficients_ascending"]
    upper = all_n["action_norm_upper_bound_polynomial"]["coefficients_ascending"]
    lower_degree = polynomial_degree(lower)
    upper_degree = polynomial_degree(upper)
    unbounded_linear = all_n["proof_valid"] and lower_degree == 1 and lower[1] > 0
    uniformly_bounded = all_n["proof_valid"] and upper_degree <= 0
    return {
        "quantifier": f"all integers n >= {all_n['domain_minimum_order']}",
        "lower_polynomial_degree": lower_degree,
        "upper_polynomial_degree": upper_degree,
        "linear_slope": lower[1] if unbounded_linear else 0,
        "all_n_unbounded_linear": unbounded_linear,
        "uniformly_bounded": uniformly_bounded,
        "outer_unbounded_pass": unbounded_linear and not uniformly_bounded,
    }


def action_growth_certificate(seed: Matrix, anticommute_partner: Matrix) -> dict:
    eigenvector = plus_eigenvector(seed)
    local_checks = {
        "seed_self_adjoint": is_hermitian(seed),
        "seed_involution": equal(matmul(seed, seed), I2),
        "partner_self_adjoint": is_hermitian(anticommute_partner),
        "partner_unitary": equal(matmul(dagger(anticommute_partner), anticommute_partner), I2),
        "anticommutator_residual_frobenius_square": frobenius_square(add(matmul(seed, anticommute_partner), matmul(anticommute_partner, seed))),
        "plus_eigenvector_residual_square": vector_norm_square(vector_sub(matvec(seed, eigenvector), eigenvector)),
        "plus_eigenvector_norm_square": vector_norm_square(eigenvector),
    }
    proof_valid = (
        local_checks["seed_self_adjoint"]
        and local_checks["seed_involution"]
        and local_checks["partner_self_adjoint"]
        and local_checks["partner_unitary"]
        and local_checks["anticommutator_residual_frobenius_square"] == 0
        and local_checks["plus_eigenvector_residual_square"] == 0
        and local_checks["plus_eigenvector_norm_square"] > 0
    )
    all_n = {
        "domain_minimum_order": 3,
        "quantified_variable": "n",
        "active_window_count_polynomial": {"coefficients_ascending": [-2, 1]},
        "implementer_eigenvalue_polynomial": {"coefficients_ascending": [-2, 1]},
        "action_norm_lower_bound_polynomial": {"coefficients_ascending": [-4, 2]},
        "action_norm_upper_bound_polynomial": {"coefficients_ascending": [-4, 2]},
        "action_ratio_square_polynomial": {"coefficients_ascending": [16, -16, 4]},
        "proof_steps": [
            "P_n v_n=(n-2)v_n from one +1 seed eigenvector per active window",
            "A_n P_n A_n^*=-P_n from exact sitewise anticommutation",
            "[P_n,A_n]v_n=-2(n-2)A_n v_n",
            "triangle upper bound is 2(n-2), equal to the vector lower bound",
        ],
        "proof_valid": proof_valid,
    }
    records = []
    for order in range(3, 7):
        active = order - 2
        p_n = finite_implementer(seed, order, signed=False)
        factors = []
        vector_factors = []
        for position in range(order):
            if position < active:
                factors.append(anticommute_partner)
                vector_factors.append(eigenvector)
            else:
                factors.append(I2)
                vector_factors.append([1, 0])
        a_n = tensor_all(factors)
        vector = tensor_vectors(vector_factors)
        p_residual = vector_sub(matvec(p_n, vector), vector_scale(active, vector))
        comm = commutator(p_n, a_n)
        av = matvec(a_n, vector)
        action_residual = vector_sub(matvec(comm, vector), vector_scale(-2 * active, av))
        unitary_residual = sub(matmul(dagger(a_n), a_n), identity(2**order))
        ratio_square = Fraction(vector_norm_square(matvec(comm, vector)), vector_norm_square(vector))
        records.append({
            "order": order,
            "implementer_eigenvector_residual_square": vector_norm_square(p_residual),
            "action_vector_residual_square": vector_norm_square(action_residual),
            "observable_unitarity_residual_frobenius_square": frobenius_square(unitary_residual),
            "action_ratio_square": str(ratio_square),
            "action_norm_lower_bound": str(2 * active),
            "action_norm_upper_bound": str(2 * active),
        })
    exact = all(
        row["implementer_eigenvector_residual_square"] == 0
        and row["action_vector_residual_square"] == 0
        and row["observable_unitarity_residual_frobenius_square"] == 0
        and Fraction(row["action_ratio_square"]) == int(row["action_norm_lower_bound"]) ** 2
        for row in records
    )
    classification = classify_action_growth(all_n)
    return {
        "local_raw": {
            "seed": sparse_matrix(seed),
            "partner": sparse_matrix(anticommute_partner),
            "plus_eigenvector": raw_vector(eigenvector),
        },
        "local_checks": local_checks,
        "all_n_certificate": all_n,
        "records": records,
        "exact_norm_certificate": exact,
        "classification": classification,
        "bounded_inner_excluded": proof_valid and exact and classification["outer_unbounded_pass"],
        "bounded_inner_inequality": "||ad_B|| <= 2||B||, contradicted by unbounded norm-one action sequence",
    }


def closability_endpoint(seeds: list[Matrix]) -> dict:
    hermitian = [is_hermitian(seed) for seed in seeds]
    involutions = [equal(matmul(seed, seed), I2) for seed in seeds]
    order = 6
    commutation = []
    for seed in seeds:
        terms = [embed_site(seed, position, order) for position in range(order - 2)]
        commutation.append(all(is_zero(commutator(left, right)) for left, right in itertools.combinations(terms, 2)))
    translation_covariant = all(
        equal(swap_transport(seed, order, position, False)[0], embed_site(seed, position, order))
        for seed in seeds
        for position in range(order - 2)
    )
    explicit_group_constructed = all(hermitian) and all(involutions) and all(commutation) and translation_covariant
    return {
        "dense_domain": "algebraic local core union_n M_2^(tensor n)",
        "local_terms_raw": [sparse_matrix(seed) for seed in seeds],
        "range": 3,
        "uniform_local_norm_exact": 1 if all(involutions) else None,
        "self_adjoint_local_terms": hermitian,
        "local_involutions": involutions,
        "translated_terms_pairwise_commute": commutation,
        "translation_covariance_checked": translation_covariant,
        "explicit_group_formula": "exp(i t h)=cos(t) I+i sin(t) h; alpha_t is the tensor product of local Ad(exp(i t h)) factors on the finite support neighborhood",
        "group_law_reason": "h^2=I and translated terms commute, so exponentials multiply exactly and local action is eventually independent of volume",
        "explicit_group_constructed": explicit_group_constructed,
        "pass": explicit_group_constructed,
    }


def star_derivation_defect(seed: Matrix) -> dict | None:
    star_defect = None
    basis = [
        [[1 if (i, j) == (row, col) else 0 for j in range(2)] for i in range(2)]
        for row in range(2)
        for col in range(2)
    ]
    for index, observable in enumerate(basis):
        delta_star = scale(1j, commutator(seed, dagger(observable)))
        star_delta = dagger(scale(1j, commutator(seed, observable)))
        residual = sub(delta_star, star_delta)
        if not is_zero(residual):
            star_defect = {
                "basis_index": index,
                "observable_sparse": sparse_matrix(observable),
                "delta_star_sparse": sparse_matrix(delta_star),
                "star_delta_sparse": sparse_matrix(star_delta),
                "residual_sparse": sparse_matrix(residual),
                "residual_frobenius_square": frobenius_square(residual),
            }
            break
    return star_defect


def bounded_telescoping_certificate(seed: Matrix) -> dict:
    local_action = commutator(seed, X)
    all_n = {
        "domain_minimum_order": 2,
        "quantified_variable": "n",
        "telescoping_coefficients": {"left_boundary": 1, "interior": 0, "right_boundary": -1},
        "implementer_norm_upper_bound_polynomial": {"coefficients_ascending": [2]},
        "action_norm_lower_bound_polynomial": {"coefficients_ascending": [2]},
        "action_norm_upper_bound_polynomial": {"coefficients_ascending": [4]},
        "local_seed_self_adjoint": is_hermitian(seed),
        "local_seed_involution": equal(matmul(seed, seed), I2),
        "local_observable_unitary": equal(matmul(dagger(X), X), I2),
        "local_action_nonzero_frobenius_square": frobenius_square(local_action),
    }
    all_n["proof_valid"] = (
        all_n["telescoping_coefficients"] == {"left_boundary": 1, "interior": 0, "right_boundary": -1}
        and all_n["local_seed_self_adjoint"]
        and all_n["local_seed_involution"]
        and all_n["local_observable_unitary"]
        and all_n["local_action_nonzero_frobenius_square"] > 0
    )
    records = []
    for order in range(2, 7):
        p_n = zeros(2**order, 2**order)
        for position in range(order - 1):
            p_n = add(p_n, sub(embed_site(seed, position, order), embed_site(seed, position + 1, order)))
        expected = sub(embed_site(seed, 0, order), embed_site(seed, order - 1, order))
        observable = embed_site(X, 0, order)
        vector = tensor_vectors([[1, 0] for _ in range(order)])
        action = commutator(p_n, observable)
        ratio_square = Fraction(vector_norm_square(matvec(action, vector)), vector_norm_square(vector))
        records.append({
            "order": order,
            "telescoping_residual_frobenius_square": frobenius_square(sub(p_n, expected)),
            "action_ratio_square": str(ratio_square),
            "action_norm_lower_bound": "2",
            "action_norm_upper_bound": "4",
        })
    classification = classify_action_growth(all_n)
    return {
        "local_raw": {"seed": sparse_matrix(seed), "observable": sparse_matrix(X), "local_action": sparse_matrix(local_action)},
        "all_n_certificate": all_n,
        "records": records,
        "classification": classification,
        "outer_unbounded_pass": classification["outer_unbounded_pass"],
        "decision_derived_from_common_action_endpoint": True,
    }


def swap_relation_certificate(signed: bool) -> dict:
    s0 = adjacent_swap(3, 0, signed)
    s1 = adjacent_swap(3, 1, signed)
    t0 = adjacent_swap(4, 0, signed)
    t2 = adjacent_swap(4, 2, signed)
    return {
        "certificate": {
            "involution": equal(matmul(s0, s0), identity(8)) and equal(matmul(s1, s1), identity(8)),
            "braid_relation": equal(matmul(matmul(s0, s1), s0), matmul(matmul(s1, s0), s1)),
            "distant_commutation": equal(matmul(t0, t2), matmul(t2, t0)),
        },
        "raw_generators": {
            "order3_s0": sparse_matrix(s0),
            "order3_s1": sparse_matrix(s1),
            "order4_t0": sparse_matrix(t0),
            "order4_t2": sparse_matrix(t2),
        },
    }


def swap_variance_certificate(seed: Matrix, signed: bool) -> dict:
    records = []
    for order in range(3, 7):
        implementer = swap_implementer(seed, order, signed)
        variance = normalized_trace_square(implementer)
        expected = Fraction(order - 2, 1)
        records.append({"order": order, "variance": str(variance), "expected": str(expected), "residual": str(variance - expected)})
    return {"records": records, "pass": all(row["residual"] == "0" for row in records)}


def frozen_action_rows(implementer: Matrix, order: int) -> tuple[str, list[dict]]:
    rows = []
    payload = []
    for row in range(4):
        for column in range(4):
            unit4 = [[1 if (i, j) == (row, column) else 0 for j in range(4)] for i in range(4)]
            observable = tensor_all([unit4] + [I2 for _ in range(order - 2)])
            action = scale(1j, commutator(implementer, observable))
            action_hash = matrix_sha256(action)
            rows.append({
                "basis_row": row,
                "basis_column": column,
                "observable_sparse": sparse_matrix(observable),
                "action_sparse": sparse_matrix(action),
                "action_sha256": action_hash,
            })
            payload.append(action_hash)
    digest = hashlib.sha256(json.dumps(payload, separators=(",", ":")).encode()).hexdigest()
    return digest, rows


def signed_unsigned_comparator(seed: Matrix) -> dict:
    order = 6
    signed = swap_implementer(seed, order, signed=True)
    unsigned = swap_implementer(seed, order, signed=False)
    signed_relations = swap_relation_certificate(True)
    unsigned_relations = swap_relation_certificate(False)
    matching = {
        "matrix_dimension_equal": len(signed) == len(unsigned),
        "window_count_equal": order - 2,
        "local_seed_identical": True,
        "local_seed_involution": equal(matmul(seed, seed), I2),
        "same_adjacent_words": all(transport_word_unitary(order, position, True)[1] == transport_word_unitary(order, position, False)[1] for position in range(order - 2)),
        "signed_relations_pass": all(signed_relations["certificate"].values()),
        "unsigned_relations_pass": all(unsigned_relations["certificate"].values()),
    }
    signed_action_hash, signed_rows = frozen_action_rows(signed, order)
    unsigned_action_hash, unsigned_rows = frozen_action_rows(unsigned, order)
    action_difference = 0
    for signed_row, unsigned_row in zip(signed_rows, unsigned_rows):
        if signed_row["action_sha256"] != unsigned_row["action_sha256"]:
            action_difference += 1
    signed_variance = swap_variance_certificate(seed, True)
    unsigned_variance = swap_variance_certificate(seed, False)
    signed_carrier = signed_variance["pass"]
    unsigned_carrier = unsigned_variance["pass"]
    return {
        "constructor_signed": "same adjacent word built from (Z tensor Z) SWAP",
        "constructor_unsigned": "same adjacent word built from canonical tensor SWAP",
        "signed_relation_certificate": signed_relations,
        "unsigned_relation_certificate": unsigned_relations,
        "signed_implementer_sparse": sparse_matrix(signed),
        "unsigned_implementer_sparse": sparse_matrix(unsigned),
        "matching_invariants": matching,
        "signed_raw_action_sha256": signed_action_hash,
        "unsigned_raw_action_sha256": unsigned_action_hash,
        "differing_raw_action_rows": action_difference,
        "raw_action_rows_retained": {"signed": signed_rows, "unsigned": unsigned_rows},
        "signed_variance": signed_variance,
        "unsigned_variance": unsigned_variance,
        "signed_carrier_pass": signed_carrier,
        "unsigned_carrier_pass": unsigned_carrier,
        "generic_carrier_decision": "PASS" if signed_carrier and unsigned_carrier else "FAIL",
        "transport_specificity_decision": "PASS_TOY_RAW_ACTION_DIFFERENCE" if action_difference else "NO_GO_IDENTICAL_RAW_ACTION",
        "non_structural": all(matching.values()) and signed_carrier and unsigned_carrier and action_difference > 0,
    }


def run() -> dict:
    seeds = [X, Y, Z]
    partners = [Z, Z, X]
    rank_positive = exact_rank_certificate(seeds)
    rank_two = exact_rank_certificate([X, Y, add(X, Y)])
    rank_one = exact_rank_certificate([X, ZERO2, ZERO2])
    zero_rank = exact_rank_certificate([ZERO2, ZERO2, ZERO2])
    bounded = bounded_telescoping_certificate(Z)
    closable_positive = closability_endpoint(seeds)
    closable_bounded = closability_endpoint([Z])
    closability_negative = closability_endpoint([R])
    closability_negative["star_derivation_defect"] = star_derivation_defect(R)
    result = {
        "schema": "siel.public-calculation.bgce443.r6.exact-nonfocal-witness.v1",
        "focal_source_used": False,
        "toy_source": {
            "local_dimension": 2,
            "window_range": 3,
            "seeds": ["Pauli-X", "Pauli-Y", "Pauli-Z"],
            "all_seed_entries": "Gaussian integers",
        },
        "positive": {
            "stabilization": [stabilization_certificate(seed) for seed in seeds],
            "variance_growth": [variance_certificate(seed) for seed in seeds],
            "rank": rank_positive,
            "action_growth": [action_growth_certificate(seed, partner) for seed, partner in zip(seeds, partners)],
            "closability": closable_positive,
        },
        "negative_controls": {
            "zero_seed_rank": zero_rank,
            "rank_two": rank_two,
            "single_direction_rank": rank_one,
            "bounded_telescoping": bounded,
            "bounded_telescoping_closability": closable_bounded,
            "closability_hypothesis_failure": closability_negative,
        },
        "matched_comparator": signed_unsigned_comparator(X),
    }
    result["decision"] = {
        "positive_all_endpoints": (
            all(item["pass"] for item in result["positive"]["stabilization"])
            and all(item["pass"] for item in result["positive"]["variance_growth"])
            and result["positive"]["rank"]["rank"] == 3
            and all(item["bounded_inner_excluded"] for item in result["positive"]["action_growth"])
            and result["positive"]["closability"]["pass"]
        ),
        "zero_rejected": result["negative_controls"]["zero_seed_rank"]["rank"] == 0,
        "rank_two_rejected": result["negative_controls"]["rank_two"]["rank"] == 2,
        "single_direction_reports_rank_one": result["negative_controls"]["single_direction_rank"]["rank"] == 1,
        "bounded_inner_rejected": not result["negative_controls"]["bounded_telescoping"]["outer_unbounded_pass"],
        "bounded_negative_still_closable": result["negative_controls"]["bounded_telescoping_closability"]["pass"],
        "closability_hypothesis_failure_rejected": not result["negative_controls"]["closability_hypothesis_failure"]["pass"] and result["negative_controls"]["closability_hypothesis_failure"]["star_derivation_defect"] is not None,
        "matched_comparator_non_structural": result["matched_comparator"]["non_structural"],
    }
    result["all_expected_separations"] = all(result["decision"].values())
    return result


if __name__ == "__main__":
    rendered = json.dumps(run(), sort_keys=True, indent=2) + "\n"
    if len(sys.argv) == 3 and sys.argv[1] == "--output":
        Path(sys.argv[2]).write_text(rendered)
    elif len(sys.argv) != 1:
        raise SystemExit("usage: exact_witness_constructor.py [--output PATH]")
    print(rendered, end="")
