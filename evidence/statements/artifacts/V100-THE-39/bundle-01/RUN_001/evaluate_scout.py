#!/usr/bin/env python3
"""BQGNEUT-024 fixed source-ordered Floquet CP/gap gate."""

from __future__ import annotations

import cmath
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import platform
import subprocess

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
MANIFEST = json.loads((HERE / "INPUT_MANIFEST.json").read_text())
Q = Fraction
N = 8


def digest(data: bytes) -> str:
    return sha256(data).hexdigest()


def read_pinned(path: str) -> bytes:
    return subprocess.check_output(
        ["git", "show", f"{MANIFEST['source_commit']}:{path}"], cwd=ROOT
    )


def qtext(x: Fraction) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


class Z15:
    """Exact Q(zeta_15) element in the power basis modulo Phi_15."""

    __slots__ = ("c",)

    def __init__(self, coeffs=()):
        a = [Q(x) for x in coeffs] + [Q(0)] * max(0, N - len(coeffs))
        self.c = tuple(a[:N])

    @staticmethod
    def rational(x):
        return Z15([Q(x)])

    @staticmethod
    def reduce(poly):
        p = [Q(x) for x in poly] + [Q(0)] * max(0, 15 - len(poly))
        # Phi_15=x^8-x^7+x^5-x^4+x^3-x+1.
        rhs = [Q(-1), Q(1), Q(0), Q(-1), Q(1), Q(-1), Q(0), Q(1)]
        for degree in range(len(p) - 1, 7, -1):
            value = p[degree]
            if value:
                p[degree] = Q(0)
                shift = degree - 8
                for j, coefficient in enumerate(rhs):
                    p[shift + j] += value * coefficient
        return Z15(p[:N])

    def __add__(self, other):
        other = other if isinstance(other, Z15) else Z15.rational(other)
        return Z15([a + b for a, b in zip(self.c, other.c)])

    __radd__ = __add__

    def __neg__(self):
        return Z15([-x for x in self.c])

    def __sub__(self, other):
        other = other if isinstance(other, Z15) else Z15.rational(other)
        return self + (-other)

    def __rsub__(self, other):
        return Z15.rational(other) - self

    def __mul__(self, other):
        other = other if isinstance(other, Z15) else Z15.rational(other)
        p = [Q(0)] * 15
        for i, a in enumerate(self.c):
            for j, b in enumerate(other.c):
                p[i + j] += a * b
        return Z15.reduce(p)

    __rmul__ = __mul__

    def __eq__(self, other):
        other = other if isinstance(other, Z15) else Z15.rational(other)
        return self.c == other.c

    def is_zero(self):
        return all(x == 0 for x in self.c)

    def conj(self):
        out = Z15()
        for i, a in enumerate(self.c):
            if a:
                out = out + a * zeta_pow(-i)
        return out

    def numeric(self):
        z = cmath.exp(2j * np.pi / 15)
        return sum(float(a) * z**i for i, a in enumerate(self.c))

    def serial(self):
        return [qtext(x) for x in self.c]


def zeta_pow(k):
    k %= 15
    p = [Q(0)] * (k + 1)
    p[k] = Q(1)
    return Z15.reduce(p)


ZERO = Z15()
ONE = Z15.rational(1)


def mat(rows):
    return tuple(tuple(x if isinstance(x, Z15) else Z15.rational(x) for x in row) for row in rows)


def eye():
    return mat([[1 if i == j else 0 for j in range(3)] for i in range(3)])


def mm(a, b):
    return tuple(tuple(sum((a[i][k] * b[k][j] for k in range(3)), ZERO) for j in range(3)) for i in range(3))


def madd(a, b):
    return tuple(tuple(a[i][j] + b[i][j] for j in range(3)) for i in range(3))


def msub(a, b):
    return tuple(tuple(a[i][j] - b[i][j] for j in range(3)) for i in range(3))


def mscale(s, a):
    return tuple(tuple(s * a[i][j] for j in range(3)) for i in range(3))


def dagger(a):
    return tuple(tuple(a[j][i].conj() for j in range(3)) for i in range(3))


def mtrace(a):
    return a[0][0] + a[1][1] + a[2][2]


def mnum(a):
    return np.array([[a[i][j].numeric() for j in range(3)] for i in range(3)], dtype=complex)


def projector(v):
    norm = sum(x * x for x in v)
    return mat([[Q(v[i] * v[j], norm) for j in range(3)] for i in range(3)])


def permutation_matrix(p):
    return mat([[1 if row == p[col] else 0 for col in range(3)] for row in range(3)])


def run():
    inputs = {}
    for item in MANIFEST["inputs"]:
        raw = read_pinned(item["path"])
        assert digest(raw) == item["sha256"], item["path"]
        inputs[item["path"]] = json.loads(raw)
    prior22 = next(v for p, v in inputs.items() if "BQGNEUT022" in p)
    prior23 = next(v for p, v in inputs.items() if "BQGNEUT023" in p)
    assert prior23["next_gate"].startswith("BQGNEUT-024")
    assert prior23["internal_neutral_carrier"]["generated_star_algebra"] == "M3(C)"
    assert prior23["source_weighted_gap_generator"]["dimensionless_spectrum"] == ["0", "4/5", "6/5"]

    C = permutation_matrix(tuple(prior22["source_conjugation"]["induced_coordinate_permutation"]))
    P0 = projector((1, 1, 1))
    P4 = projector((1, 1, -2))
    P6 = projector((1, -1, 0))
    a = zeta_pow(-4)  # exp[-i(2*pi/3)(4/5)]
    b = zeta_pow(-6)  # exp[-i(2*pi/3)(6/5)]
    omega = zeta_pow(5)
    E = madd(P0, madd(mscale(a, P4), mscale(b, P6)))
    U = mm(C, E)

    exact_unitary = mm(dagger(U), U) == eye() and mm(U, dagger(U)) == eye()
    uniform = (ONE, ONE, ONE)
    uniform_image = tuple(sum((U[i][j] * uniform[j] for j in range(3)), ZERO) for i in range(3))
    uniform_fixed = uniform_image == uniform

    half_sum = Q(1, 2) * (a + b)
    quadratic_discriminant = half_sum * half_sum - 4 * omega
    quadratic_at_one = ONE + half_sum + omega
    tr_u = mtrace(U)
    distinct_exact = not quadratic_discriminant.is_zero() and not quadratic_at_one.is_zero()
    not_equally_spaced_exact = not tr_u.is_zero()

    A = msub(U, dagger(U))
    aprod = A[0][1] * A[1][2] * A[2][0]
    twice_real_aprod = aprod + aprod.conj()
    cp_odd_numerator_exact_nonzero = not twice_real_aprod.is_zero()

    Un = mnum(U)
    unitary_residual = float(np.linalg.norm(Un.conj().T @ Un - np.eye(3)))
    normal_residual = float(np.linalg.norm(Un.conj().T @ Un - Un @ Un.conj().T))
    evals, evecs = np.linalg.eig(Un)
    idx0 = int(np.argmin(np.abs(evals - 1)))
    rest = [i for i in range(3) if i != idx0]
    rest.sort(key=lambda i: float(np.mod(np.angle(evals[i]), 2 * np.pi)))
    order = [idx0] + rest
    W = evecs[:, order]
    W = W / np.linalg.norm(W, axis=0)
    mixing_unitarity_residual = float(np.linalg.norm(W.conj().T @ W - np.eye(3)))
    J = float(np.imag(W[0, 0] * W[1, 1] * np.conj(W[0, 1]) * np.conj(W[1, 0])))

    phases = [0.0] + sorted(float(np.mod(np.angle(evals[i]), 2 * np.pi)) for i in rest)
    circular_gaps = [phases[1], phases[2] - phases[1], 2 * np.pi - phases[2]]
    min_gap = min(circular_gaps)
    min_gap_difference = min(abs(circular_gaps[i] - circular_gaps[j]) for i in range(3) for j in range(i + 1, 3))

    K = (Un - Un.conj().T) / (2j)
    kvals = np.linalg.eigvalsh(K)
    cp_numerator = float(np.imag(K[0, 1] * K[1, 2] * K[2, 0]))
    k_vandermonde = float(np.prod([kvals[j] - kvals[i] for i in range(3) for j in range(i + 1, 3)]))
    J_from_invariant = cp_numerator / k_vandermonde
    cp_exact_numeric_crosscheck = abs(cp_numerator - twice_real_aprod.numeric().real / 16) < 1e-12

    gates = {
        "G1_FIXED_SOURCE_ORDER_AND_C3_PERIOD_WITHOUT_SCAN": MANIFEST["fixed_operator"] == "U_F=C_g exp[-i(2*pi/3)L_w]" and not MANIFEST["parameter_scan_used"],
        "G2_FLOQUET_OPERATOR_EXACTLY_UNITARY": exact_unitary and unitary_residual < 1e-12,
        "G3_ONE_OPERATOR_HAS_DISTINCT_NON_EQUALLY_SPACED_EIGENPHASES": distinct_exact and not_equally_spaced_exact and min_gap > 1e-6 and min_gap_difference > 1e-6,
        "G4_SAME_OPERATOR_HAS_EXACT_NONZERO_CP_ODD_NUMERATOR": cp_odd_numerator_exact_nonzero and abs(J) > 1e-6 and abs(J - J_from_invariant) < 1e-10,
        "G5_SIMULTANEOUS_CP_AND_UNEQUAL_GAP_IN_ONE_PROPAGATOR": distinct_exact and not_equally_spaced_exact and cp_odd_numerator_exact_nonzero,
        "G6_PRIOR_PHI_COLLISION_SLOT_AND_LINEAR_RAW_PETZ_ERASURE_NOT_REDEFINED": prior22["history_process"]["collision_slot"] == "Phi" and prior22["history_process"]["raw_Petz_first_order_erasure_preserved"] is True,
        "G7_NO_EXTERNAL_THREE_GENERATION_CARRIER_FOR_NEUTRAL_OPERATIONAL_SECTOR": prior23["internal_neutral_carrier"]["external_three_generation_carrier_required_for_neutral_operational_sector"] is False,
        "G8_PHYSICAL_LEPTON_IDENTITY_AND_ABSOLUTE_SCALE_DERIVED": False,
        "G9_NO_TARGET_DATA_PARAMETER_SCAN_OR_LONG_COMPUTATION": not MANIFEST["target_data_accessed"] and not MANIFEST["parameter_scan_used"] and not MANIFEST["long_computation_used"],
    }
    simultaneous_pass = all(gates[k] for k in (
        "G1_FIXED_SOURCE_ORDER_AND_C3_PERIOD_WITHOUT_SCAN",
        "G2_FLOQUET_OPERATOR_EXACTLY_UNITARY",
        "G3_ONE_OPERATOR_HAS_DISTINCT_NON_EQUALLY_SPACED_EIGENPHASES",
        "G4_SAME_OPERATOR_HAS_EXACT_NONZERO_CP_ODD_NUMERATOR",
        "G5_SIMULTANEOUS_CP_AND_UNEQUAL_GAP_IN_ONE_PROPAGATOR",
        "G6_PRIOR_PHI_COLLISION_SLOT_AND_LINEAR_RAW_PETZ_ERASURE_NOT_REDEFINED",
        "G7_NO_EXTERNAL_THREE_GENERATION_CARRIER_FOR_NEUTRAL_OPERATIONAL_SECTOR",
        "G9_NO_TARGET_DATA_PARAMETER_SCAN_OR_LONG_COMPUTATION",
    ))
    physical_pmns_pass = simultaneous_pass and gates["G8_PHYSICAL_LEPTON_IDENTITY_AND_ABSOLUTE_SCALE_DERIVED"]

    tests = {
        "T1_PINNED_INPUT_HASHES_MATCH": True,
        "T2_CYCLOTOMIC_UNITARITY_EXACT": exact_unitary,
        "T3_UNIFORM_MODE_EXACTLY_FIXED": uniform_fixed,
        "T4_QUADRATIC_DISCRIMINANT_EXACT_NONZERO": not quadratic_discriminant.is_zero(),
        "T5_EIGENVALUE_ONE_NOT_ROOT_OF_QUADRATIC": not quadratic_at_one.is_zero(),
        "T6_TRACE_EXACT_NONZERO_SO_NOT_EQUAL_THIRDS": not_equally_spaced_exact,
        "T7_CP_ODD_NUMERATOR_EXACT_NONZERO": cp_odd_numerator_exact_nonzero,
        "T8_NUMERIC_RESIDUALS_SMALL": unitary_residual < 1e-12 and normal_residual < 1e-12 and mixing_unitarity_residual < 1e-12,
        "T9_DIRECT_AND_EIGENFRAME_JARLSKOG_MATCH": abs(J - J_from_invariant) < 1e-10 and cp_exact_numeric_crosscheck,
        "T10_FIXED_CIRCULAR_GAPS_POSITIVE_AND_PAIRWISE_UNEQUAL": min_gap > 1e-6 and min_gap_difference > 1e-6,
        "T11_NO_TARGET_SCAN_OR_LONG_COMPUTATION": gates["G9_NO_TARGET_DATA_PARAMETER_SCAN_OR_LONG_COMPUTATION"],
    }
    assert all(tests.values())

    decision = (
        "SCOPED_PASS_ONE_SOURCE_ORDERED_C3_WEIGHTED_FLOQUET_OPERATOR_IS_EXACTLY_"
        "UNITARY_AND_SIMULTANEOUSLY_HAS_DISTINCT_NON_EQUALLY_SPACED_EIGENPHASES_"
        "AND_EXACT_NONZERO_CP_ODD_NUMERATOR_WITHOUT_TARGETS_OR_SCAN__PHYSICAL_PMNS_"
        "AND_NEUTRINO_MASS_SCALE_REMAIN_OPEN_PENDING_LEPTON_TYPING_AND_ABSOLUTE_SCALE"
    )
    return {
        "schema": "siel.public-calculation.bqgneut024.raw.v1",
        "scout_id": MANIFEST["scout_id"],
        "gate_id": MANIFEST["gate_id"],
        "source_commit": MANIFEST["source_commit"],
        "source_snapshot_id": MANIFEST["source_snapshot_id"],
        "evidence_status": "Theoretical derivation",
        "scientific_layer": "finite source-ordered dimensionless neutral Floquet propagation",
        "decision": decision,
        "bold_hypothesis": {
            "interpretive_leap": "Compose the source-weighted interaction evolution and oriented C3 transport in their source history order over one positive C3 period.",
            "new_composition_law": MANIFEST["fixed_operator"],
            "source_status": "SOURCE_FIXED_DIMENSIONLESS_OPERATIONAL_CONSTRUCTION__PHYSICAL_TIME_MASS_AND_LEPTON_TYPING_OPEN"
        },
        "floquet_operator": {
            "definition": MANIFEST["fixed_operator"],
            "cyclotomic_field": "Q(zeta_15)",
            "exact_unitary": exact_unitary,
            "uniform_mode_fixed": uniform_fixed,
            "characteristic_factorization": "(lambda-1)*(lambda^2+(zeta_15^-4+zeta_15^-6)*lambda/2+zeta_15^5)",
            "quadratic_discriminant_exact_nonzero": not quadratic_discriminant.is_zero(),
            "trace_exact_nonzero": not tr_u.is_zero(),
            "eigenphases_radians_fixed_branch": phases,
            "circular_eigenphase_gaps_radians": circular_gaps,
            "minimum_gap": min_gap,
            "minimum_pairwise_gap_difference": min_gap_difference,
            "unitary_residual": unitary_residual,
            "normal_residual": normal_residual
        },
        "cp_certificate": {
            "twice_real_antihermitian_cycle_product_power_basis_coefficients": twice_real_aprod.serial(),
            "exact_nonzero": cp_odd_numerator_exact_nonzero,
            "hermitian_sine_generator_cycle_imaginary_part": cp_numerator,
            "sine_generator_eigenvalues": [float(x) for x in kvals],
            "Jarlskog": J,
            "Jarlskog_absolute": abs(J),
            "Jarlskog_from_invariant": J_from_invariant,
            "mixing_unitarity_residual": mixing_unitarity_residual,
            "overlap_modulus_squared": (np.abs(W) ** 2).tolist()
        },
        "noncompensating_gates": gates,
        "simultaneous_dimensionless_CP_gap_pass": simultaneous_pass,
        "external_neutral_carrier_removed_scoped": gates["G7_NO_EXTERNAL_THREE_GENERATION_CARRIER_FOR_NEUTRAL_OPERATIONAL_SECTOR"],
        "physical_PMNS_pass": physical_pmns_pass,
        "strongest_ordinary_alternative": "An oriented qutrit shift times a noncommuting weighted unitary generically has CP and unequal phases. The theorem establishes a source-fixed finite operational propagator, not its identity with natural neutrinos.",
        "counter_intuition_scan": "The same operator now carries CP and unequal gaps, but neither a physical weak-current typing nor a dimensionful mass scale follows from that internal spectral fact. Calling the result PMNS would still promote an operational qutrit into Standard-Model matter without the missing intertwiner.",
        "claim_ceiling": "One coefficient-free source-ordered dimensionless neutral qutrit Floquet operator is exactly unitary and simultaneously has a nonzero exact CP-odd numerator and unequal eigenphase gaps. The result does not identify this qutrit with physical lepton doublets, derive dimensionful neutrino masses, compare with data, establish empirical neutrino physics or complete quantum gravity.",
        "next_gate": "BQGNEUT-025_SOURCE_NATIVE_WEAK_CURRENT_INTERTWINER_TO_PHYSICAL_THREE_NEUTRINO_TYPING_GATE",
        "work_package": "BQG-G3-R03.8",
        "work_package_status": "ACTIVE",
        "tests": tests,
        "runtime": {"python": platform.python_version(), "numpy": np.__version__, "target_data_accessed": False, "parameter_scan_used": False, "long_computation_used": False}
    }


def main():
    raw = run()
    keys = (
        "schema", "scout_id", "gate_id", "source_commit", "source_snapshot_id",
        "evidence_status", "scientific_layer", "decision", "bold_hypothesis",
        "floquet_operator", "cp_certificate", "noncompensating_gates",
        "simultaneous_dimensionless_CP_gap_pass", "external_neutral_carrier_removed_scoped",
        "physical_PMNS_pass", "strongest_ordinary_alternative", "counter_intuition_scan",
        "claim_ceiling", "next_gate", "work_package", "work_package_status", "runtime"
    )
    (HERE / "RAW_OUTPUT.json").write_text(json.dumps(raw, indent=2, ensure_ascii=False) + "\n")
    (HERE / "RESULT.json").write_text(json.dumps({k: raw[k] for k in keys}, indent=2, ensure_ascii=False) + "\n")
    (HERE / "CERTIFICATE.json").write_text(json.dumps({
        "schema": "siel.public-calculation.bqgneut024.certificate.v1",
        "scout_id": raw["scout_id"],
        "source_commit": raw["source_commit"],
        "input_hashes": {item["path"]: item["sha256"] for item in MANIFEST["inputs"]},
        "evaluator_sha256": digest(Path(__file__).read_bytes()),
        "raw_output_sha256": digest((HERE / "RAW_OUTPUT.json").read_bytes()),
        "result_sha256": digest((HERE / "RESULT.json").read_bytes()),
        "tests": raw["tests"],
        "decision": raw["decision"]
    }, indent=2, ensure_ascii=False) + "\n")
    (HERE / "STATUS.json").write_text(json.dumps({"scout_id": raw["scout_id"], "status": "COMPLETE", "decision": raw["decision"], "next_gate": raw["next_gate"]}, indent=2, ensure_ascii=False) + "\n")
    (HERE / "EXECUTION_LOG.json").write_text(json.dumps({"iteration": 1, "command": "python3 evaluate_scout.py", "runtime_class": "subsecond exact Q(zeta_15) plus one 3x3 eigendecomposition", "result_informed_change": False}, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
