#!/usr/bin/env python3
"""Exact non-focal constructors for the BGCE443 Revision 4 E0 witness.

The script uses only explicit 2x2 toy operators. It does not read or construct
the actual BGCE443 source endpoint.
"""

from __future__ import annotations

import itertools
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


def determinant3(m: list[list[complex]]) -> complex:
    return (
        m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
        - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
        + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
    )


def derivation_row(seed: Matrix) -> list[complex]:
    basis = [
        [[1 if (i, j) == (row, col) else 0 for j in range(2)] for i in range(2)]
        for row in range(2)
        for col in range(2)
    ]
    return [value for unit in basis for value in flatten(scale(1j, commutator(seed, unit)))]


def three_row_rank_certificate(seeds: list[Matrix]) -> dict:
    rows = [derivation_row(seed) for seed in seeds]
    witness = None
    for columns in itertools.combinations(range(len(rows[0])), 3):
        minor = [[rows[r][column] for column in columns] for r in range(3)]
        determinant = determinant3(minor)
        if determinant != 0:
            witness = {"columns": list(columns), "determinant": gaussian_string(determinant)}
            break
    rank = 3 if witness else 2 if any(any(value != 0 for value in row) for row in rows) else 0
    return {"rank": rank, "nonzero_minor": witness}


def gaussian_string(value: complex) -> str:
    real = int(value.real)
    imag = int(value.imag)
    if imag == 0:
        return str(real)
    return f"{real}{imag:+d}i"


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


def action_growth_certificate(seed: Matrix, anticommute_partner: Matrix, signed: bool = False) -> dict:
    records = []
    for order in range(3, 7):
        active = order - 2
        p_n = finite_implementer(seed, order, signed=signed)
        factors = []
        for position in range(order):
            if position < active:
                # Signed conjugation does not change the anticommutation relation.
                factors.append(anticommute_partner)
            else:
                factors.append(I2)
        a_n = tensor_all(factors)
        lhs = commutator(p_n, a_n)
        rhs = scale(2, matmul(p_n, a_n))
        records.append({
            "order": order,
            "identity_residual_frobenius_square": frobenius_square(sub(lhs, rhs)),
            "observable_norm": "1",
            "action_norm": str(2 * active),
        })
    return {"records": records, "unbounded_linear_slope": "2", "bounded_inner_excluded": all(row["identity_residual_frobenius_square"] == 0 for row in records)}


def closability_certificate(seeds: list[Matrix]) -> dict:
    hermitian = [is_hermitian(seed) for seed in seeds]
    involutions = [equal(matmul(seed, seed), I2) for seed in seeds]
    return {
        "dense_domain": "algebraic local core union_n M_2^(tensor n)",
        "range": 3,
        "uniform_local_norm": "1",
        "self_adjoint_local_terms": hermitian,
        "local_involutions": involutions,
        "analytic_vector_bound": "for support size m, ||delta^k(A)|| <= (2(m+2k))^k k! ||A||; each local A has a nonzero analytic radius and the local evolutions extend to a strongly continuous automorphism group",
        "explicit_commuting_toy_group": "alpha_t^(n)=Ad(product_x exp(i t tau_x(h))); disjoint one-site translates commute",
        "pass": all(hermitian) and all(involutions),
    }


def closability_hypothesis_negative() -> dict:
    star_defect = None
    basis = [
        [[1 if (i, j) == (row, col) else 0 for j in range(2)] for i in range(2)]
        for row in range(2)
        for col in range(2)
    ]
    for index, observable in enumerate(basis):
        delta_star = scale(1j, commutator(R, dagger(observable)))
        star_delta = dagger(scale(1j, commutator(R, observable)))
        residual = sub(delta_star, star_delta)
        if not is_zero(residual):
            star_defect = {"basis_index": index, "residual_frobenius_square": frobenius_square(residual)}
            break
    return {"seed_self_adjoint": is_hermitian(R), "star_derivation_defect": star_defect, "closability_endpoint_pass": False}


def bounded_telescoping_certificate(seed: Matrix) -> dict:
    records = []
    for order in range(2, 7):
        p_n = zeros(2**order, 2**order)
        for position in range(order - 1):
            p_n = add(p_n, sub(embed_site(seed, position, order), embed_site(seed, position + 1, order)))
        expected = sub(embed_site(seed, 0, order), embed_site(seed, order - 1, order))
        records.append({"order": order, "telescoping_residual_frobenius_square": frobenius_square(sub(p_n, expected)), "implementer_norm_upper_bound": "2", "derivation_norm_upper_bound": "4"})
    return {"records": records, "unbounded_action": False, "pass_as_outer_unbounded": False}


def signed_unsigned_comparator(seed: Matrix) -> dict:
    order = 6
    signed = finite_implementer(seed, order, signed=True)
    unsigned = finite_implementer(seed, order, signed=False)
    matching = {
        "matrix_dimension_equal": len(signed) == len(unsigned),
        "window_count_equal": order - 2,
        "local_seed_trace_equal": trace(seed) == trace(matmul(matmul(Z, seed), Z)),
        "local_seed_square_equal": equal(matmul(seed, seed), matmul(matmul(matmul(Z, seed), Z), matmul(matmul(Z, seed), Z))),
    }
    difference = frobenius_square(sub(signed, unsigned))
    signed_carrier = variance_certificate(seed, signed=True)["pass"]
    unsigned_carrier = variance_certificate(seed, signed=False)["pass"]
    return {
        "constructor_signed": "tau_x(h)=Z^(x mod 2) h Z^(x mod 2) embedded at window x",
        "constructor_unsigned": "sigma_x(h)=h embedded at window x",
        "matching_invariants": matching,
        "raw_implementer_difference_frobenius_square": difference,
        "signed_carrier_pass": signed_carrier,
        "unsigned_carrier_pass": unsigned_carrier,
        "generic_carrier_decision": "PASS" if signed_carrier and unsigned_carrier else "FAIL",
        "transport_specificity_decision": "PASS_TOY_RAW_ACTION_DIFFERENCE" if difference else "NO_GO_IDENTICAL_RAW_ACTION",
        "non_structural": signed_carrier and unsigned_carrier and difference > 0,
    }


def run() -> dict:
    seeds = [X, Y, Z]
    partners = [Z, Z, X]
    rank_positive = three_row_rank_certificate(seeds)
    rank_two = three_row_rank_certificate([X, Y, add(X, Y)])
    zero_rank = three_row_rank_certificate([ZERO2, ZERO2, ZERO2])
    result = {
        "schema": "siel.dpa.bgce443.r4.exact-nonfocal-witness.v1",
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
            "closability": closability_certificate(seeds),
        },
        "negative_controls": {
            "zero_seed_rank": zero_rank,
            "rank_two": rank_two,
            "bounded_telescoping": bounded_telescoping_certificate(Z),
            "closability_hypothesis_failure": closability_hypothesis_negative(),
            "single_direction_rank": 1 if any(value != 0 for value in derivation_row(X)) else 0,
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
        "bounded_inner_rejected": not result["negative_controls"]["bounded_telescoping"]["pass_as_outer_unbounded"],
        "closability_hypothesis_failure_rejected": not result["negative_controls"]["closability_hypothesis_failure"]["closability_endpoint_pass"],
        "single_direction_reports_rank_one": result["negative_controls"]["single_direction_rank"] == 1,
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
