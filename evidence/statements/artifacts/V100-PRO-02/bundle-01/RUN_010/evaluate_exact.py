#!/usr/bin/env python3
"""Exact Q(zeta_5) rank classification for PUBLIC-RUN-BQGSTRAT-010."""

import hashlib
import itertools
import json
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE_MATRIX = json.loads((HERE / "SOURCE_MATRIX.json").read_text())

for source in SOURCE_MATRIX["sources"]:
    assert hashlib.sha256((ROOT / source["path"]).read_bytes()).hexdigest() == source["sha256"]


def eps4(items):
    if len(set(items)) < 4:
        return 0
    inversions = sum(items[i] > items[j] for i in range(4) for j in range(i + 1, 4))
    return -1 if inversions % 2 else 1


eta = [-1, 1, 1, 1]


def mul_units(u, v):
    p, q = divmod(u, 4)
    r, s = divmod(v, 4)
    return None if q != r else 4 * p + s


def contract_unit(face_r, face_s, u):
    c, d = divmod(u, 4)
    return sum(
        eps4((mu, nu, face_r, face_s)) * eps4((mu, nu, c, d)) * eta[d]
        for mu in range(4) for nu in range(4)
    )


def cross_contract(mu0, a0, face_r, face_s, u):
    c, d = divmod(u, 4)
    return sum(
        (eps4((mu0, nu, face_r, face_s)) * eps4((a0, nu, c, d))
         + eps4((nu, mu0, face_r, face_s)) * eps4((nu, a0, c, d))) * eta[d]
        for nu in range(4)
    )


faces = [(r, s) for r in range(4) for s in range(r + 1, 4)]
cross = {}
comm = {}
for r, s in faces:
    for f in range(16):
        mu, a = divmod(f, 4)
        for u in range(16):
            cross[(r, s, f, u)] = 2 * cross_contract(mu, a, r, s, u)
    for u in range(16):
        for v in range(16):
            uv, vu = mul_units(u, v), mul_units(v, u)
            comm[(r, s, u, v)] = (
                (0 if uv is None else contract_unit(r, s, uv))
                - (0 if vu is None else contract_unit(r, s, vu))
            )

ZERO = (F(0),) * 4
ONE = (F(1), F(0), F(0), F(0))


def add(a, b):
    return tuple(a[i] + b[i] for i in range(4))


def sub(a, b):
    return tuple(a[i] - b[i] for i in range(4))


def scale(q, a):
    return tuple(q * x for x in a)


def mul(a, b):
    if a == ZERO or b == ZERO:
        return ZERO
    c = [F(0)] * 7
    for i in range(4):
        for j in range(4):
            c[i + j] += a[i] * b[j]
    for degree in range(6, 3, -1):
        coefficient = c[degree]
        if coefficient:
            c[degree] = F(0)
            for j in range(degree - 4, degree):
                c[j] -= coefficient
    return tuple(c[:4])


def solve4(matrix, target):
    a = [list(matrix[i]) + [target[i]] for i in range(4)]
    row = 0
    for col in range(4):
        pivot = next(i for i in range(row, 4) if a[i][col])
        a[row], a[pivot] = a[pivot], a[row]
        value = a[row][col]
        a[row] = [x / value for x in a[row]]
        for i in range(4):
            if i != row and a[i][col]:
                value = a[i][col]
                a[i] = [a[i][j] - value * a[row][j] for j in range(5)]
        row += 1
    return tuple(a[i][4] for i in range(4))


@lru_cache(maxsize=None)
def inverse(a):
    assert a != ZERO
    basis = [tuple(F(i == j) for i in range(4)) for j in range(4)]
    columns = [mul(a, item) for item in basis]
    matrix = [[columns[j][i] for j in range(4)] for i in range(4)]
    return solve4(matrix, ONE)


def divide(a, b):
    return mul(a, inverse(b))


zeta = (F(0), F(1), F(0), F(0))
powers = [ONE]
for _ in range(1, 5):
    powers.append(mul(powers[-1], zeta))


def hessian(digits):
    z = [powers[d] for d in digits]
    zi = [powers[(-d) % 5] for d in digits]
    matrix = [[ZERO for _ in range(80)] for _ in range(80)]

    def accumulate(i, j, value):
        if value != ZERO:
            matrix[i][j] = add(matrix[i][j], value)

    for r, s in faces:
        minus = {r: sub(ONE, zi[s]), s: sub(zi[r], ONE)}
        plus = {r: sub(ONE, z[s]), s: sub(z[r], ONE)}
        for f in range(16):
            for direction, coefficient in minus.items():
                for u in range(16):
                    accumulate(f, 16 + 16 * direction + u, scale(F(cross[(r, s, f, u)]), coefficient))
            for direction, coefficient in plus.items():
                for u in range(16):
                    accumulate(16 + 16 * direction + u, f, scale(F(cross[(r, s, f, u)]), coefficient))
        legs = [(r, (), 1), (s, (r,), 1), (r, (s,), -1), (s, (), -1)]
        for i in range(4):
            di, shift_i, sign_i = legs[i]
            for j in range(i + 1, 4):
                dj, shift_j, sign_j = legs[j]
                phase_ij = phase_ji = ONE
                for t in shift_i:
                    phase_ij, phase_ji = mul(phase_ij, z[t]), mul(phase_ji, zi[t])
                for t in shift_j:
                    phase_ij, phase_ji = mul(phase_ij, zi[t]), mul(phase_ji, z[t])
                for u in range(16):
                    row = 16 + 16 * di + u
                    for v in range(16):
                        coefficient = comm[(r, s, u, v)]
                        if not coefficient:
                            continue
                        col = 16 + 16 * dj + v
                        weight = F(sign_i * sign_j * coefficient, 2)
                        accumulate(row, col, scale(weight, phase_ij))
                        accumulate(col, row, scale(weight, phase_ji))
    return matrix


def exact_rank(matrix):
    a = [row[:] for row in matrix]
    rank = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(rank, len(a)) if a[i][col] != ZERO), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        pivot_value = a[rank][col]
        for i in range(rank + 1, len(a)):
            if a[i][col] == ZERO:
                continue
            factor = divide(a[i][col], pivot_value)
            a[i][col] = ZERO
            for j in range(col + 1, len(a[0])):
                if a[rank][j] != ZERO:
                    a[i][j] = sub(a[i][j], mul(factor, a[rank][j]))
        rank += 1
    return rank


def main():
    profile = Counter()
    exceptional = []
    orbit_records = []
    seen = set()
    for digits in itertools.product(range(5), repeat=4):
        if digits in seen:
            continue
        orbit = set()
        for multiplier in (1, 2, 3, 4):
            for permutation in itertools.permutations((1, 2, 3)):
                orbit.add(((multiplier * digits[0]) % 5,) + tuple((multiplier * digits[i]) % 5 for i in permutation))
        seen.update(orbit)
        representative = min(orbit)
        rank = exact_rank(hessian(representative))
        record = {
            "representative": list(representative),
            "orbit_size": len(orbit),
            "rank": rank,
            "nullity": 80 - rank,
        }
        orbit_records.append(record)
        profile[rank] += len(orbit)
        if rank < 66:
            record["members"] = [list(item) for item in sorted(orbit)]
            exceptional.append(record)
    assert len(seen) == 625
    assert len(orbit_records) == 45
    assert profile == Counter({66: 600, 64: 12, 65: 12, 60: 1})
    output = {
        "schema": "siel.public-calculation.bqgstrat010.exact-rank.v1",
        "field": "Q(zeta_5), zeta_5^4+zeta_5^3+zeta_5^2+zeta_5+1=0",
        "symbol_dimension": 80,
        "sector_count": 625,
        "exact_orbit_count": 45,
        "rank_profile": {str(rank): count for rank, count in sorted(profile.items())},
        "exceptional_orbits": exceptional,
        "all_orbits": orbit_records,
        "decision_inputs_are_floating_point": False,
        "dense_parent_matrix_materialized": False,
    }
    (HERE / "RAW_OUTPUT.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output["rank_profile"], sort_keys=True))


if __name__ == "__main__":
    main()
