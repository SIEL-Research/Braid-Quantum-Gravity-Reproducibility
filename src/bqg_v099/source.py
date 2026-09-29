"""Exact reconstruction and verification of the v0.99 source class."""

from fractions import Fraction
import itertools
import json
from pathlib import Path

import numpy as np


N = 5
I5 = np.eye(N, dtype=np.int64)
I25 = np.eye(N * N, dtype=np.int64)


def load_source_data(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def endpoint_matrix(permutation: list[int]) -> np.ndarray:
    matrix = np.zeros((N, N), dtype=np.int64)
    for source, target in enumerate(permutation):
        matrix[target, source] = 1
    return matrix


def signed_crossing(columns: list[int], negative_rows: list[int]) -> np.ndarray:
    matrix = np.zeros((25, 25), dtype=np.int64)
    negative = set(negative_rows)
    for row, column in enumerate(columns):
        matrix[row, column] = -1 if row in negative else 1
    return matrix


def crossing_transform(operator: np.ndarray, endpoint_j: np.ndarray) -> np.ndarray:
    """Cr(T)[a,b;c,d] = T[b,Jd;Ja,c]."""
    permutation = [int(np.argmax(endpoint_j[:, index])) for index in range(N)]
    tensor = operator.reshape(N, N, N, N)
    crossed = np.empty_like(tensor)
    for a, b, c, d in itertools.product(range(N), repeat=4):
        crossed[a, b, c, d] = tensor[b, permutation[d], permutation[a], c]
    return crossed.reshape(25, 25)


def source_hamiltonian(r: np.ndarray, endpoint_j: np.ndarray) -> np.ndarray:
    p = crossing_transform(I25, endpoint_j)
    c = crossing_transform(r, endpoint_j)
    rc = r @ c
    return (
        6*c + 3*rc - 3*r@c@c + 3*crossing_transform(rc, endpoint_j)
        - 25*p - 6*c@p@c + 12*p@c + 12*c@p
    )


def partial_trace_second(matrix: np.ndarray) -> np.ndarray:
    return np.einsum("abcb->ac", matrix.reshape(5, 5, 5, 5))


def characteristic_coefficients(matrix: np.ndarray) -> list[int]:
    size = matrix.shape[0]
    x = matrix.astype(object)
    power = np.eye(size, dtype=object)
    traces = [0]
    for _ in range(size):
        power = power @ x
        traces.append(sum(power[index, index] for index in range(size)))
    coefficients = [1]
    for degree in range(1, size + 1):
        numerator = -sum(
            coefficients[degree-index] * traces[index]
            for index in range(1, degree + 1)
        )
        assert numerator % degree == 0
        coefficients.append(int(numerator // degree))
    return coefficients


def spectral_projector_numerator(
    marker: np.ndarray, eigenvalues: tuple[int, ...], eigenvalue: int
) -> tuple[np.ndarray, int]:
    numerator = I5.copy()
    denominator = 1
    for other in eigenvalues:
        if other != eigenvalue:
            numerator = numerator @ (marker - other*I5)
            denominator *= eigenvalue - other
    return numerator, denominator


def exchange_invariant(
    r: np.ndarray,
    projectors: dict[int, tuple[np.ndarray, int]],
    left: int,
    right: int,
) -> Fraction:
    flip = np.zeros((25, 25), dtype=np.int64)
    for a in range(5):
        for b in range(5):
            flip[5*b+a, 5*a+b] = 1
    ln, ld = projectors[left]
    rn, rd = projectors[right]
    return Fraction(
        int(np.trace(np.kron(ln, rn) @ r @ np.kron(rn, ln) @ flip)),
        (ld*rd)**2,
    )


def verify_source_class(data_path: Path) -> dict:
    data = load_source_data(data_path)
    columns = data["row_to_column"]
    endpoint_j = endpoint_matrix(data["endpoint_involution"])
    point = np.array(data["point"], dtype=np.int64)
    cup = sum(
        (np.kron(I5[:, index], endpoint_j @ I5[:, index]) for index in range(5)),
        start=np.zeros(25, dtype=np.int64),
    )
    cap_projector = np.outer(cup, cup)
    assert np.array_equal(cap_projector, crossing_transform(I25, endpoint_j))

    eigenvalues = tuple(data["marker_eigenvalues"])
    pairs = tuple(tuple(pair) for pair in data["exchange_pairs"])
    sector_triples = {}
    all_triples = []
    for sector in data["sectors"]:
        mask = sector["mask"]
        r = signed_crossing(columns, sector["negative_rows"])
        r12, r23 = np.kron(r, I5), np.kron(I5, r)
        assert np.array_equal(r.T @ r, I25)
        assert np.array_equal(r @ r, I25)
        assert np.array_equal(r12 @ r23 @ r12, r23 @ r12 @ r23)
        assert np.array_equal(r @ np.kron(point, point), np.kron(point, point))

        h = source_hamiltonian(r, endpoint_j)
        assert np.array_equal(h, h.T)
        assert np.array_equal(h @ (h-6*I25) @ (h-10*I25), np.zeros((25, 25), dtype=np.int64))
        f_num, p_num = h@h - 10*h + 12*I25, h@h - 6*h
        assert np.all(f_num % 12 == 0) and np.all(p_num % 8 == 0)
        f, p = f_num // 12, p_num // 8
        assert np.array_equal(p, cap_projector)
        assert np.array_equal(p @ p, 5*p)
        assert np.array_equal(h, 3*(I25-f) + 2*p)

        j1 = np.kron(endpoint_j, I5)
        marker = partial_trace_second(j1 @ f @ j1 @ h @ r)
        assert characteristic_coefficients(marker) == data["marker_characteristic_coefficients"]
        projectors = {
            value: spectral_projector_numerator(marker, eigenvalues, value)
            for value in eigenvalues
        }
        triple = [int(exchange_invariant(r, projectors, a, b)) for a, b in pairs]
        sector_triples[str(mask)] = triple
        all_triples.append(tuple(triple))

    assert len(set(all_triples)) == 8
    assert set(all_triples) == set(itertools.product((-1, 1), repeat=3))
    return {
        "status": "PASS",
        "representatives": len(data["sectors"]),
        "real_typed_orbits": len(set(all_triples)),
        "physical_sector_selection": data["claim_boundary"]["physical_sector_selection"],
        "sector_chi_triples": sector_triples,
        "common_hamiltonian_spectrum": {"0": 15, "6": 5, "10": 5},
    }
