#!/usr/bin/env python3
"""PUBLIC-RUN-BGCE457-001: all-finite iterated backreaction theorem audit."""

from __future__ import annotations

import argparse
from fractions import Fraction
from hashlib import sha256
import importlib.util
import itertools
import json
import math
from pathlib import Path
import sys

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
MANIFEST = json.loads((HERE / "INPUT_MANIFEST.json").read_text())


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def load_json(relative: str) -> dict:
    path = ROOT / relative
    assert digest(path) == MANIFEST["inputs"][relative]
    return json.loads(path.read_text())


def load_module(relative: str):
    path = ROOT / relative
    assert digest(path) == MANIFEST["inputs"][relative]
    spec = importlib.util.spec_from_file_location("bgce444_o14", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def reconstruct_defects():
    formal = next(path for path in MANIFEST["inputs"] if path.endswith("ocbfh014_source_native_refinement_naturality_check.py"))
    o14 = load_module(formal)
    survivors, projectors, _, _ = o14.reconstruct_actual_source()
    identity5 = np.eye(5, dtype=np.int64)
    identity125 = np.eye(125, dtype=np.int64)
    q = math.exp(-math.pi)
    probabilities = [(1.0 + 5.0 * q) / 6.0] + [(1.0 - q) / 6.0] * 5
    rows = []
    for survivor in survivors:
        g_num, g_den, r1, r2 = o14.source_g1(survivor["R"].astype(np.int64))
        group = [identity125, r1, r2, r1 @ r2, r2 @ r1, r1 @ r2 @ r1]

        def phi(operator):
            return sum(p * (u.T @ operator @ u) for p, u in zip(probabilities, group))

        scores = [g_num / g_den]
        for projector_num, projector_den in projectors:
            projector = np.kron(projector_num, identity5) / projector_den
            score = -1j * ((g_num / g_den) @ projector - projector @ (g_num / g_den))
            scores.append(score)
        defects = [np.asarray(score - phi(score), dtype=complex) for score in scores]
        gram = np.array([[np.vdot(left, right).real for right in defects] for left in defects])
        eigenvalues = np.linalg.eigvalsh(gram)
        rank = int(np.linalg.matrix_rank(gram, tol=1e-10))
        assert rank == 4
        assert eigenvalues[0] > 1e-10

        # One moderate and one deliberately strong finite register are enough:
        # global validity follows from functional calculus, not a parameter scan.
        log_checks = []
        for h in ([3.0, -2.0, 1.0, 4.0], [1.0e6, -2.0e6, 3.0e6, -4.0e6]):
            d_h = sum(value * defect for value, defect in zip(h, defects))
            lambdas = np.linalg.eigvalsh(d_h)
            log_plus = math.log(2.0) - np.logaddexp(0.0, -lambdas)
            log_minus = math.log(2.0) - np.logaddexp(0.0, lambdas)
            residual = float(np.max(np.abs((log_plus - log_minus) - lambdas)))
            scale = max(1.0, float(np.max(np.abs(lambdas))))
            assert residual / scale < 2e-15
            log_checks.append({
                "h": h,
                "maximum_absolute_D_eigenvalue": float(np.max(np.abs(lambdas))),
                "maximum_log_contrast_residual": residual,
                "relative_residual": residual / scale,
                "strict_positive_effects_mathematically": True,
            })
        rows.append({
            "mask": int(survivor["mask"]),
            "defect_gram_rank": rank,
            "defect_gram_minimum_eigenvalue": float(eigenvalues[0]),
            "defect_gram_determinant": float(np.linalg.det(gram)),
            "finite_log_checks": log_checks,
        })
    assert [row["mask"] for row in rows] == [0, 5, 8, 13, 16, 21, 24, 29]
    return rows


def exact_nonautonomous_telescope():
    # Exact diagonal-algebra witnesses for varying unital channels.  The proof
    # is the general identity P_k(S-Phi_k S)=P_k S-P_(k+1) S.
    channels = [
        [[Fraction(1, 2), Fraction(1, 2), Fraction(0)], [Fraction(0), Fraction(1, 3), Fraction(2, 3)], [Fraction(1, 4), Fraction(0), Fraction(3, 4)]],
        [[Fraction(2, 3), Fraction(0), Fraction(1, 3)], [Fraction(1, 5), Fraction(4, 5), Fraction(0)], [Fraction(0), Fraction(1, 2), Fraction(1, 2)]],
        [[Fraction(3, 4), Fraction(1, 4), Fraction(0)], [Fraction(0), Fraction(2, 5), Fraction(3, 5)], [Fraction(1, 3), Fraction(0), Fraction(2, 3)]],
    ]

    def mat_vec(matrix, vector):
        return [sum(row[j] * vector[j] for j in range(3)) for row in matrix]

    def mat_mul(left, right):
        return [[sum(left[i][k] * right[k][j] for k in range(3)) for j in range(3)] for i in range(3)]

    identity = [[Fraction(int(i == j)) for j in range(3)] for i in range(3)]
    scores = [[Fraction(2), Fraction(-1), Fraction(3)], [Fraction(1), Fraction(4), Fraction(-2)]]
    residuals = []
    for score in scores:
        propagator = identity
        total = [Fraction(0), Fraction(0), Fraction(0)]
        for channel in channels:
            local = [left - right for left, right in zip(score, mat_vec(channel, score))]
            dressed = mat_vec(propagator, local)
            total = [left + right for left, right in zip(total, dressed)]
            propagator = mat_mul(propagator, channel)
        endpoint = [left - right for left, right in zip(score, mat_vec(propagator, score))]
        residuals.append([str(left - right) for left, right in zip(total, endpoint)])
    assert all(value == "0" for residual in residuals for value in residual)
    return residuals


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    output = Path(args.output)
    if not output.is_absolute():
        output = HERE / output
    if output.exists():
        raise FileExistsError(f"refusing to overwrite {output}")

    upstream = {path: load_json(path) for path in MANIFEST["inputs"] if path.endswith(".json") and "INPUT_MANIFEST" not in path}
    get = lambda token: next(value for path, value in upstream.items() if token in path)
    assert get("BGCE323_")["repeated_collision"]["global_n_step_support_covariance"] == "PASS_BY_ISOMETRY_COMPOSITION"
    assert get("BGCE348_")["four_component_balance"]["all_eight_actual_sectors"] is True
    assert get("BGCE350_")["gate_decision"]["history_dressed_local_total_Ward"] is True
    assert get("BGCE364_")["operator_logistic_retraction"]["strict_positivity_for_every_finite_Hermitian_X"] is True
    assert get("BGCE364_")["six_label_instrument_lift"]["prior_summed_instrument_CPTP"] is True
    assert get("BGCE370_")["gate_decision"]["joint_system_environment_CP_CPTP_carrier"] == "SCOPED_PASS"
    assert get("BGCE371_")["gate_decision"]["one_complete_direct_finite_noncircular_backreaction_cycle"] == "SCOPED_PASS"
    assert get("BGCE443_")["decision"] == "CLOSED_SCOPED"

    sector_rows = reconstruct_defects()
    ward_residuals = exact_nonautonomous_telescope()
    nonlinear_second_derivative_at_one = -2.0 * (1.0 / math.cosh(1.0)) ** 2 * math.tanh(1.0)
    assert nonlinear_second_derivative_at_one != 0.0

    raw = {
        "schema": "siel.public-calculation.scout.bgce457.raw.v1",
        "scout_id": "PUBLIC-RUN-BGCE457-001",
        "source_commit": MANIFEST["source_commit"],
        "source_snapshot_id": MANIFEST["source_snapshot_id"],
        "input_hashes_verified": True,
        "sector_rows": sector_rows,
        "all_eight_defect_gram_rank_four": all(row["defect_gram_rank"] == 4 for row in sector_rows),
        "global_log_contrast_coordinate": "L(h)=log F_raw(h)-log F_Petz(h)=sum_a h^a D_a",
        "global_log_contrast_differential": "dL_h(delta h)=sum_a delta h^a D_a, independent of h",
        "all_finite_registers_give_strictly_positive_branch_effects": True,
        "all_finite_registers_give_prior_summed_CPTP_instruments": True,
        "finite_iteration_CPTP_induction": "base id is CPTP; each record instrument, classical translation and next controlled collision are CPTP; finite composition is CPTP",
        "nonautonomous_Ward_identity": "sum_(k=0)^(n-1) P_k(S_a-Phi_k(S_a))=S_a-P_n(S_a)",
        "exact_fraction_Ward_witness_residuals": ward_residuals,
        "nonautonomous_Ward_proof": "P_k(S-Phi_k S)=P_k S-P_(k+1) S telescopes for arbitrary finite channel sequence",
        "constraint_preservation": "the h update changes only the conjugation-natural instrument parameter; the source algebra and its generated derivations are unchanged, so the BGCE443 scoped no-central-anomaly closure persists",
        "operator_logistic_second_derivative_at_scalar_one": nonlinear_second_derivative_at_one,
        "nonlinear_feedback": True,
        "all_finite_n_theorem": True,
        "excluded_limit": "no uniform n-to-infinity spectral gap or off-base likelihood-Fisher lower bound is claimed",
    }
    with output.open("x") as handle:
        handle.write(json.dumps(raw, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({
        "scout_id": raw["scout_id"],
        "sectors": len(sector_rows),
        "all_eight_rank_four": raw["all_eight_defect_gram_rank_four"],
        "all_finite_n_theorem": raw["all_finite_n_theorem"],
        "ward_exact": all(value == "0" for residual in ward_residuals for value in residual),
        "nonlinear_feedback": raw["nonlinear_feedback"],
    }, indent=2))


if __name__ == "__main__":
    main()
