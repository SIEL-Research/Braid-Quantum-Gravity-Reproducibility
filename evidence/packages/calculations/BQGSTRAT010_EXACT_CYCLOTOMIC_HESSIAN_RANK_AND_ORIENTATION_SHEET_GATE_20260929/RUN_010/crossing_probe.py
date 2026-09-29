#!/usr/bin/env python3
"""Numerical transverse-crossing probe on the exact exceptional sectors."""

import json
from pathlib import Path
import numpy as np
import evaluate_exact as exact

HERE = Path(__file__).resolve().parent


def matrix_unit(index):
    p, q = divmod(index, 4)
    out = np.zeros((4, 4), dtype=complex)
    out[p, q] = 1
    return out


units = [matrix_unit(i) for i in range(16)]


def contract(r, s, matrix):
    total = 0j
    for u in range(16):
        p, q = divmod(u, 4)
        total += exact.contract_unit(r, s, u) * matrix[p, q]
    return total


def hessian(angles):
    z = np.exp(1j * np.array(angles, dtype=float))
    zi = np.conjugate(z)
    H = np.zeros((80, 80), dtype=complex)
    for r, s in exact.faces:
        minus = {r: 1 - zi[s], s: zi[r] - 1}
        plus = {r: 1 - z[s], s: z[r] - 1}
        for f in range(16):
            for direction, coefficient in minus.items():
                for u in range(16):
                    H[f, 16 + 16 * direction + u] += coefficient * exact.cross[(r, s, f, u)]
            for direction, coefficient in plus.items():
                for u in range(16):
                    H[16 + 16 * direction + u, f] += coefficient * exact.cross[(r, s, f, u)]
        legs = [(r, (), 1), (s, (r,), 1), (r, (s,), -1), (s, (), -1)]
        for i in range(4):
            di, shift_i, sign_i = legs[i]
            for j in range(i + 1, 4):
                dj, shift_j, sign_j = legs[j]
                phase_ij = phase_ji = 1 + 0j
                for t in shift_i:
                    phase_ij, phase_ji = phase_ij * z[t], phase_ji * zi[t]
                for t in shift_j:
                    phase_ij, phase_ji = phase_ij * zi[t], phase_ji * z[t]
                for u, X in enumerate(units):
                    row = 16 + 16 * di + u
                    for v, Y in enumerate(units):
                        coefficient = exact.comm[(r, s, u, v)]
                        if not coefficient:
                            continue
                        col = 16 + 16 * dj + v
                        weight = sign_i * sign_j * coefficient / 2
                        H[row, col] += weight * phase_ij
                        H[col, row] += weight * phase_ji
    return H


records = []
for digits in ((1, 0, 0, 1), (1, 0, 0, 4)):
    angles = 2 * np.pi * np.array(digits, dtype=float) / 5
    base = hessian(angles)
    hermitian_residual = float(np.max(np.abs(base - base.conjugate().T)))
    eigenvalues, eigenvectors = np.linalg.eigh(base)
    null = eigenvectors[:, np.abs(eigenvalues) < 1e-8]
    epsilon = 1e-6
    plus, minus = angles.copy(), angles.copy()
    plus[0] += epsilon
    minus[0] -= epsilon
    derivative = (hessian(plus) - hessian(minus)) / (2 * epsilon)
    crossing = null.conjugate().T @ derivative @ null
    crossing = (crossing + crossing.conjugate().T) / 2
    values = np.linalg.eigvalsh(crossing)
    nonzero = [float(value) for value in values if abs(value) > 1e-7]
    records.append({
        "digits": list(digits),
        "nullity": int(null.shape[1]),
        "hermitian_residual": hermitian_residual,
        "transverse_parameter": "theta_0",
        "crossing_rank_numeric": len(nonzero),
        "crossing_nonzero_eigenvalues_numeric": nonzero,
        "finite_difference_epsilon": epsilon,
    })

assert [record["nullity"] for record in records] == [16, 15]
assert [record["crossing_rank_numeric"] for record in records] == [2, 1]
assert all(record["hermitian_residual"] < 1e-12 for record in records)

output = {
    "schema": "siel.public-calculation.bqgstrat010.crossing-probe.v1",
    "classification": "NUMERICAL_SUPPORT_ONLY__NOT_AN_EXACT_CROSSING_CERTIFICATE",
    "records": records,
}
(HERE / "CROSSING_OUTPUT.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
print(json.dumps(output, indent=2, sort_keys=True))
