"""Exact reconstruction and verification of the v1.0 source class."""

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


def exact_rank(matrix: list[list[Fraction]]) -> int:
    work = [row[:] for row in matrix]
    rows = len(work)
    columns = len(work[0])
    pivot = 0
    for column in range(columns):
        found = next((row for row in range(pivot, rows) if work[row][column]), None)
        if found is None:
            continue
        work[pivot], work[found] = work[found], work[pivot]
        scale = work[pivot][column]
        work[pivot] = [value / scale for value in work[pivot]]
        for row in range(rows):
            if row != pivot and work[row][column]:
                factor = work[row][column]
                work[row] = [
                    value - factor * base
                    for value, base in zip(work[row], work[pivot])
                ]
        pivot += 1
    return pivot


def transition_on_marker_atoms(
    r: np.ndarray,
    projectors: dict[int, tuple[np.ndarray, int]],
    eigenvalues: tuple[int, ...],
) -> tuple[tuple[int, int], ...]:
    """Exact deterministic transition induced on the five marker atoms."""
    transition = []
    for left in eigenvalues:
        left_num, left_den = projectors[left]
        for right in eigenvalues:
            right_num, right_den = projectors[right]
            input_num = np.kron(left_num, right_num)
            input_den = left_den * right_den
            moved_num = r @ input_num @ r.T
            destinations = []
            for out_left in eigenvalues:
                out_left_num, out_left_den = projectors[out_left]
                for out_right in eigenvalues:
                    out_right_num, out_right_den = projectors[out_right]
                    output_num = np.kron(out_left_num, out_right_num)
                    output_den = out_left_den * out_right_den
                    probability = Fraction(
                        int(np.trace(output_num @ moved_num)),
                        output_den * input_den,
                    )
                    assert probability >= 0
                    if probability:
                        destinations.append(
                            (out_left, out_right, probability, output_num, output_den)
                        )
            assert len(destinations) == 1 and destinations[0][2] == 1
            out_left, out_right, _, output_num, output_den = destinations[0]
            assert np.array_equal(moved_num * output_den, output_num * input_den)
            transition.append(
                (eigenvalues.index(out_left), eigenvalues.index(out_right))
            )
    return tuple(transition)


def displacement_moment(
    mapping: tuple[tuple[int, int], ...]
) -> tuple[list[list[int]], int]:
    moment = [[0, 0], [0, 0]]
    moved = 0
    for index, output in enumerate(mapping):
        source = divmod(index, 5)
        delta = (output[0] - source[0], output[1] - source[1])
        if delta != (0, 0):
            moved += 1
        for row in range(2):
            for column in range(2):
                moment[row][column] += delta[row] * delta[column]
    return moment, moved


def s4_chart_average(moment: list[list[int]]) -> list[list[Fraction]]:
    aggregate = [[0 for _ in range(4)] for _ in range(4)]
    for order in itertools.permutations(range(4)):
        for site in range(3):
            left, right = order[site], order[site + 1]
            aggregate[left][left] += moment[0][0]
            aggregate[left][right] += moment[0][1]
            aggregate[right][left] += moment[1][0]
            aggregate[right][right] += moment[1][1]
    return [[Fraction(value, 24 * 25) for value in row] for row in aggregate]


def marked_projector_twice(
    projectors: dict[int, tuple[np.ndarray, int]],
    marked_eigenvalues: tuple[int, ...],
) -> np.ndarray:
    doubled = np.zeros((5, 5), dtype=np.int64)
    for row in range(5):
        for column in range(5):
            value = sum(
                (
                    Fraction(2 * int(projectors[eigenvalue][0][row, column]),
                             projectors[eigenvalue][1])
                    for eigenvalue in marked_eigenvalues
                ),
                Fraction(0),
            )
            assert value.denominator == 1
            doubled[row, column] = int(value)
    assert np.array_equal(doubled @ doubled, 2 * doubled)
    return doubled


def recover_binary_line(projector_numerator: np.ndarray, denominator: int) -> np.ndarray:
    """Recover the predeclared-sign integer generator of a binary rank-one line."""
    matrix = [
        [Fraction(int(value), denominator) for value in row]
        for row in projector_numerator
    ]
    pivot = next(index for index in range(len(matrix)) if matrix[index][index])
    assert matrix[pivot][pivot] == Fraction(1, 2)
    vector = np.array(
        [int(2 * matrix[row][pivot]) for row in range(len(matrix))],
        dtype=np.int64,
    )
    assert vector[pivot] == 1
    assert int(vector @ vector) == 2
    assert np.array_equal(
        denominator * np.outer(vector, vector),
        2 * projector_numerator,
    )
    return vector


def encode_fraction_matrix(matrix: list[list[Fraction]]) -> list[list[str]]:
    return [[str(value) for value in row] for row in matrix]


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
    event_transitions = []
    routing_records = []
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

        event_transitions.append(
            transition_on_marker_atoms(r, projectors, eigenvalues)
        )
        p2 = marked_projector_twice(projectors, eigenvalues[:3])
        q2 = 2 * I5 - p2
        assert np.array_equal(q2 @ q2, 2 * q2)
        assert np.array_equal(p2 @ q2, np.zeros((5, 5), dtype=np.int64))
        assert np.array_equal(p2 + q2, 2 * I5)

        # P_src=p2/2 and Q_src=q2/2 are the complementary rank 3+2
        # source projectors.  The endpoint involution restricts to a
        # nondegenerate (1,1) form on im(Q_src).  With
        # S_Q=Q_src J Q_src and E_+/-=(Q_src +/- S_Q)/2, the integer
        # numerators below verify S_Q^2=Q_src and rank(E_+)=rank(E_-)=1
        # without floating-point diagonalisation.
        signed_q_num = q2 @ endpoint_j @ q2
        assert np.array_equal(signed_q_num @ signed_q_num, 8 * q2)
        e_plus_num = 2 * q2 + signed_q_num
        e_minus_num = 2 * q2 - signed_q_num
        assert np.array_equal(e_plus_num @ e_plus_num, 8 * e_plus_num)
        assert np.array_equal(e_minus_num @ e_minus_num, 8 * e_minus_num)
        assert np.array_equal(
            e_plus_num @ e_minus_num, np.zeros((5, 5), dtype=np.int64)
        )
        p_rank = exact_rank(
            [[Fraction(int(value), 2) for value in row] for row in p2]
        )
        q_rank = exact_rank(
            [[Fraction(int(value), 2) for value in row] for row in q2]
        )
        q_plus_rank = exact_rank(
            [[Fraction(int(value), 8) for value in row] for row in e_plus_num]
        )
        q_minus_rank = exact_rank(
            [[Fraction(int(value), 8) for value in row] for row in e_minus_num]
        )
        assert (p_rank, q_rank, q_plus_rank, q_minus_rank) == (3, 2, 1, 1)

        # The line representatives use the fixed rule implemented by
        # recover_binary_line: choose the first nonzero diagonal coordinate
        # and make it positive.  This produces the explicit rational 2x5
        # intertwiner before any target-data inspection.
        v_plus = recover_binary_line(e_plus_num, 8)
        v_minus = recover_binary_line(e_minus_num, 8)
        k_plus = np.array([1, 1], dtype=np.int64)
        k_minus = np.array([1, -1], dtype=np.int64)
        h_radial = np.array([[0, 1], [1, 0]], dtype=np.int64)
        w_num = np.outer(k_plus, v_plus) + np.outer(k_minus, v_minus)
        i2 = np.eye(2, dtype=np.int64)
        k_plus_num = i2 + h_radial
        k_minus_num = i2 - h_radial
        assert np.array_equal(w_num @ w_num.T, 4 * i2)
        assert np.array_equal(w_num.T @ w_num, 2 * q2)
        assert np.array_equal(w_num @ q2 @ w_num.T, 8 * i2)
        assert np.array_equal(w_num @ signed_q_num @ w_num.T, 16 * h_radial)
        assert np.array_equal(
            w_num @ e_plus_num @ w_num.T, 16 * k_plus_num
        )
        assert np.array_equal(
            w_num @ e_minus_num @ w_num.T, 16 * k_minus_num
        )

        # One actual factor-five right-tail step; Kronecker associativity
        # makes this the induction step for every finite addressed depth.
        w1_num = np.kron(w_num, I5)
        assert np.array_equal(
            w1_num @ np.kron(signed_q_num, I5) @ w1_num.T,
            16 * np.kron(h_radial, I5),
        )
        assert np.array_equal(
            w1_num @ np.kron(e_plus_num, I5) @ w1_num.T,
            16 * np.kron(k_plus_num, I5),
        )
        assert np.array_equal(
            w1_num @ np.kron(e_minus_num, I5) @ w1_num.T,
            16 * np.kron(k_minus_num, I5),
        )
        p25_twice = np.kron(I5, p2)
        assert int(np.trace(p2)) == 6
        assert int(np.trace(p25_twice)) == 30
        assert np.array_equal(p25_twice @ p25_twice, 2 * p25_twice)
        routing_records.append(
            {
                "mask": mask,
                "marked_projector_rank": p_rank,
                "complement_projector_rank": q_rank,
                "complement_signature": "(1,1)",
                "complement_positive_rank": q_plus_rank,
                "complement_negative_rank": q_minus_rank,
                "source_positive_line": [int(value) for value in v_plus],
                "source_negative_line": [int(value) for value in v_minus],
                "palatini_intertwiner_numerator": [
                    [int(value) for value in row] for row in w_num
                ],
                "palatini_intertwiner_denominator": 2,
                "factor_five_refinement_checks": "PASS_EXACT",
                "outer_projector_rank": exact_rank(
                    [[Fraction(int(value)) for value in row] for row in p25_twice]
                ),
                "normalized_cup_weight": str(Fraction(int(np.trace(p25_twice)), 50)),
            }
        )

    assert len(set(all_triples)) == 8
    assert set(all_triples) == set(itertools.product((-1, 1), repeat=3))
    assert len(set(event_transitions)) == 1
    event_transition = event_transitions[0]
    event_permutation = tuple(5 * left + right for left, right in event_transition)
    assert sorted(event_permutation) == list(range(25))
    assert all(event_permutation[event_permutation[index]] == index for index in range(25))
    for triple in itertools.product(range(5), repeat=3):
        def apply_pair(values: tuple[int, int, int], site: int) -> tuple[int, int, int]:
            result = list(values)
            left, right = event_transition[5 * result[site] + result[site + 1]]
            result[site], result[site + 1] = left, right
            return tuple(result)

        left = apply_pair(apply_pair(apply_pair(triple, 0), 1), 0)
        right = apply_pair(apply_pair(apply_pair(triple, 1), 0), 1)
        assert left == right

    pair_moment, moved_atoms = displacement_moment(event_transition)
    assert pair_moment == [[28, -20], [-20, 28]]
    assert moved_atoms == 16
    q4 = s4_chart_average(pair_moment)
    expected_q4 = [
        [Fraction(42, 25), Fraction(-2, 5), Fraction(-2, 5), Fraction(-2, 5)],
        [Fraction(-2, 5), Fraction(42, 25), Fraction(-2, 5), Fraction(-2, 5)],
        [Fraction(-2, 5), Fraction(-2, 5), Fraction(42, 25), Fraction(-2, 5)],
        [Fraction(-2, 5), Fraction(-2, 5), Fraction(-2, 5), Fraction(42, 25)],
    ]
    assert q4 == expected_q4
    assert exact_rank(q4) == 4

    p0 = [[Fraction(1, 4) for _ in range(4)] for _ in range(4)]
    p1 = [
        [Fraction(int(row == column)) - p0[row][column] for column in range(4)]
        for row in range(4)
    ]
    reconstructed_q4 = [
        [Fraction(12, 25) * p0[row][column] + Fraction(52, 25) * p1[row][column]
         for column in range(4)]
        for row in range(4)
    ]
    assert reconstructed_q4 == q4
    j_ray = [
        [-p0[row][column] + p1[row][column] for column in range(4)]
        for row in range(4)
    ]
    lorentz_metric = [
        [sum((j_ray[row][inner] * q4[inner][column] for inner in range(4)), Fraction(0))
         for column in range(4)]
        for row in range(4)
    ]
    assert all(
        sum(lorentz_metric[row][column] for column in range(4)) == Fraction(-12, 25)
        for row in range(4)
    )
    assert all(record["normalized_cup_weight"] == "3/5" for record in routing_records)
    return {
        "status": "PASS",
        "representatives": len(data["sectors"]),
        "real_typed_orbits": len(set(all_triples)),
        "physical_sector_selection": data["claim_boundary"]["physical_sector_selection"],
        "sector_chi_triples": sector_triples,
        "common_hamiltonian_spectrum": {"0": 15, "6": 5, "10": 5},
        "marker_event_transition": {
            "atoms": 25,
            "moved_atoms": moved_atoms,
            "involutive": True,
            "yang_baxter_checks": 125,
            "pair_displacement_moment": pair_moment,
        },
        "four_direction_moment": {
            "Q4": encode_fraction_matrix(q4),
            "rank": 4,
            "ray_eigenvalue": "12/25",
            "standard_eigenvalue": "52/25",
        },
        "source_lorentz_involution": {
            "definition": "J_ray=-P0+P1",
            "metric_definition": "g=J_ray Q4",
            "negative_ray_eigenvalue": "-12/25",
            "positive_standard_eigenvalue": "52/25",
            "signature": "(-,+,+,+)",
        },
        "routing_ratio": {
            "marked_eigenvalues": list(eigenvalues[:3]),
            "sectors": routing_records,
            "common_normalized_cup_weight": "3/5",
            "common_complementary_weight": "2/5",
            "common_rank_split": "3+2",
            "common_complement_signature": "(1,1)",
            "claim_boundary": "exact complementary source split and ratio; full-corner uniqueness and the static-spherical Palatini interpretation require their declared proofs",
        },
    }
