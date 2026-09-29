#!/usr/bin/env python3
"""BGCE490: source-structured Chebyshev LCU renormalization gate."""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
import math
from pathlib import Path
import sys

import mpmath as mp
import numpy as np


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
PATHS = {
    "b478": REPO / "audits/SRA_DPA_BGCE478_MINIMAL_TYPED_SELECT_O_OR_NORMALIZED_H_BLOCK_ENCODING_GENERATOR_GATE_20260925/DPA_SCOUT_001/RESULT.json",
    "b484": REPO / "audits/SRA_DPA_BGCE484_MINIMAL_MARKED_SOURCE_WORD_SELECT_AND_LCU_REALIZATION_GATE_20260925/DPA_SCOUT_001/RESULT.json",
    "b487": REPO / "audits/SRA_DPA_BGCE487_SOURCE_RAW_G1_ENCODED_SIGNAL_QUBIT_AND_SU2_CLOCK_GATE_20260925/DPA_SCOUT_001/RESULT.json",
    "b488": REPO / "audits/SRA_DPA_BGCE488_ENCODED_G1_CLOCK_TO_BLOCK_ENCODING_SIGNAL_INTERTWINER_AND_EXACT_QSP_COMPILER_GATE_20260925/DPA_SCOUT_001/RESULT.json",
    "b488raw": REPO / "audits/SRA_DPA_BGCE488_ENCODED_G1_CLOCK_TO_BLOCK_ENCODING_SIGNAL_INTERTWINER_AND_EXACT_QSP_COMPILER_GATE_20260925/DPA_SCOUT_001/RAW_OUTPUT.json",
    "b489": REPO / "audits/SRA_DPA_BGCE489_HERALDED_LCU_SUCCESS_AMPLIFICATION_OR_DETERMINISTIC_QUOTIENT_QSP_EFFICIENCY_GATE_20260925/DPA_SCOUT_001/RESULT.json",
    "b458e": REPO / "audits/SRA_DPA_BGCE458_BARE_BRAID_ORIENTED_CYCLE_TO_COMPLEX_KINEMATICS_GATE_20260925/DPA_SCOUT_001/evaluate_scout.py",
    "o14": REPO / "projects/active/discovery_partner/formal_checks/ocbfh014_source_native_refinement_naturality_check.py",
    "source": REPO / "audits/SRA_DPA_BGCE139_SOURCE_SPECTRAL_CYLINDER_OPERATIONAL_EVENT_IDENTIFICATION_GATE_20260919/RAW_OUTPUT.json",
}
EXPECTED = {
    "b478": "2266de6922d3753a53e1e1e91398744b134ab83b7e69bfba0f30ac0db7682518",
    "b484": "914898496153ae9574046b91a2cba2c792a056571754ef63fdf30b93e1bb7813",
    "b487": "0d0e2feb34fded05b3bfef6620efcf6ee7abf80ab4a83db33b580ab5c484b975",
    "b488": "00cba841ded9b78a1441406bdb7286109a62765971eae5283cc9d1bd5d982aad",
    "b488raw": "5e824bde3873b8b647f881fd1c9eb70d9a1d832dd5a6968a10b9672db689f490",
    "b489": "37a36da23f246bc8ca9013de7df96176c4940f1e1a8bde03a9be37a53bb4fd5a",
    "b458e": "f7fc8db4ab821c223e466e335b5c18a4c2dc824e6f0060471fcf9d53271d02a8",
    "o14": "176c75ac349f0f3f142d9c850ca0682436b7ad00cd179f6806de253d0a7acabb",
    "source": "ddf630fbaff1ae4e72c778f47dc2bed6906da0a8aa17d4e6a98d2c96791955e9",
}


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def source_cycles(b458) -> list[tuple[int, int, int]]:
    table = b458.pair_table_from_source()
    permutation = b458.compose(b458.perm_for_site(table, 0), b458.perm_for_site(table, 1))
    unseen = set(range(125))
    cycles = []
    while unseen:
        start = min(unseen)
        cycle = (start, permutation[start], permutation[permutation[start]])
        unseen -= set(cycle)
        if len(set(cycle)) == 3:
            cycles.append(cycle)
    assert len(cycles) == 36
    return cycles


def compressed_matrix(
    numerator: np.ndarray,
    denominator: int,
    factor: mp.mpc,
    cycles: list[tuple[int, int, int]],
    coefficients: list[mp.mpc],
) -> mp.matrix:
    matrix = mp.matrix(36)
    for left, left_cycle in enumerate(cycles):
        for right, right_cycle in enumerate(cycles):
            value = mp.mpc(0)
            for row in range(3):
                for column in range(3):
                    value += (
                        mp.conj(coefficients[row])
                        * factor
                        * int(numerator[left_cycle[row], right_cycle[column]])
                        * coefficients[column]
                    )
            matrix[left, right] = value / (3 * denominator)
    return matrix


def run() -> dict:
    for name, path in PATHS.items():
        assert digest(path) == EXPECTED[name], name
    docs = {
        name: json.loads(PATHS[name].read_text())
        for name in ("b478", "b484", "b487", "b488", "b488raw", "b489")
    }
    assert docs["b478"]["bold_hypothesis_result"] == "SCOPED_PASS"
    assert docs["b484"]["status"] == "SCOPED_PASS_WITH_RETAINED_NO_GO"
    assert docs["b487"]["status"] == "SCOPED_PASS"
    assert docs["b488"]["status"] == "CLOSED_SCOPED"
    assert docs["b489"]["status"] == "SPLIT_CLOSED_SCOPED_AND_NO_GO"

    b458 = load_module("bgce490_b458", PATHS["b458e"])
    o14 = load_module("bgce490_o14", PATHS["o14"])
    b458.REPO = REPO
    b458.SOURCE = PATHS["source"]
    cycles = source_cycles(b458)
    survivors, source_projectors, _, source_meta = o14.reconstruct_actual_source()
    old_records = {
        (int(record["mask"]), record["control"]): record
        for record in docs["b488raw"]["records"]
    }

    mp.mp.dps = 70
    omega = mp.exp(2 * mp.j * mp.pi / 3)
    carrier_coefficients = [mp.mpc(1), omega * omega, omega]
    records = []
    maximum_interpolation_residual = mp.mpf(0)
    maximum_walk_residual = mp.mpf(0)

    for survivor in survivors:
        g_num, g_den, _, _ = o14.source_g1(survivor["R"].astype(np.int64))
        controls = [("G1", 5, g_num, g_den, mp.mpc(1))]
        for index, (projector_num, projector_den) in enumerate(source_projectors, start=1):
            lifted = np.kron(projector_num, np.eye(5, dtype=np.int64))
            commutator = g_num @ lifted - lifted @ g_num
            controls.append((f"H{index}", 10, commutator, g_den * projector_den, -mp.j))

        for name, alpha, numerator, denominator, factor in controls:
            hamiltonian = compressed_matrix(
                numerator, denominator, factor, cycles, carrier_coefficients
            )
            eigenvalues, _ = mp.eighe(hamiltonian)
            nodes = []
            for row in range(eigenvalues.rows):
                value = mp.re(eigenvalues[row])
                if not nodes or abs(value - nodes[-1]) > mp.mpf("1e-50"):
                    nodes.append(value)
            count = len(nodes)
            assert 15 <= count <= 32
            normalized_nodes = [value / alpha for value in nodes]
            assert max(abs(value) for value in normalized_nodes) < 1
            targets = [mp.exp(-mp.j * mp.pi * value / 3) for value in nodes]
            chebyshev = mp.matrix([
                [mp.chebyt(degree, value) for degree in range(count)]
                for value in normalized_nodes
            ])
            coefficients = mp.lu_solve(chebyshev, mp.matrix(targets))
            interpolation_residual = max(
                abs(
                    sum(chebyshev[row, degree] * coefficients[degree] for degree in range(count))
                    - targets[row]
                )
                for row in range(count)
            )
            maximum_interpolation_residual = max(
                maximum_interpolation_residual, interpolation_residual
            )

            # Scalar certificate for the canonical Halmos walk:
            # R(x)=[[x,sqrt(1-x^2)],[-sqrt(1-x^2),x]],
            # so the upper-left entry of R(x)^k is T_k(x).
            walk_residual = mp.mpf(0)
            for value in normalized_nodes:
                defect = mp.sqrt(1 - value * value)
                walk = mp.matrix([[value, defect], [-defect, value]])
                power = mp.eye(2)
                for degree in range(count):
                    walk_residual = max(
                        walk_residual,
                        abs(power[0, 0] - mp.chebyt(degree, value)),
                    )
                    power = power * walk
            maximum_walk_residual = max(maximum_walk_residual, walk_residual)

            normalization = sum(abs(value) for value in coefficients)
            success_probability = 1 / (normalization * normalization)
            amplitude = 1 / normalization
            theta = mp.asin(amplitude)
            ordinary_prefix = int(mp.floor(mp.pi / (4 * theta) - mp.mpf("0.5")))
            phase_matched_calls = 2 * ordinary_prefix + 3
            maximum_degree = count - 1
            total_block_encoding_queries = phase_matched_calls * maximum_degree
            old_log10_probability = mp.mpf(
                str(old_records[(int(survivor["mask"]), name)]["log10_heralding_success_probability"])
            )
            new_log10_probability = mp.log10(success_probability)
            records.append({
                "mask": int(survivor["mask"]),
                "control": name,
                "distinct_spectral_nodes": count,
                "chebyshev_degree": maximum_degree,
                "chebyshev_LCU_branches": count,
                "log10_coefficient_l1_normalization": float(mp.log10(normalization)),
                "log10_unamplified_success_probability": float(new_log10_probability),
                "success_probability_improvement_orders": float(
                    new_log10_probability - old_log10_probability
                ),
                "exact_phase_matched_base_calls": phase_matched_calls,
                "total_H_block_encoding_queries": total_block_encoding_queries,
                "interpolation_residual_70_digit": mp.nstr(interpolation_residual, 8),
                "walk_identity_residual_70_digit": mp.nstr(walk_residual, 8),
            })

    assert len(records) == 32
    assert maximum_interpolation_residual < mp.mpf("1e-60")
    assert maximum_walk_residual < mp.mpf("1e-60")

    return {
        "schema": "siel.dpa.bgce490.raw.v1",
        "scout_id": "DPA-SCOUT-BGCE490-001",
        "gate_id": "BGCE490",
        "attempt": "0001",
        "source_commit": "90a18fccd770d241e2887df89a95005f93779899",
        "primary_evidence_status": "Theoretical derivation",
        "scientific_layer": "source-spectrum Chebyshev walk compiler and low-normalization exact LCU",
        "focal_decision": "CLOSED_SCOPED_SOURCE_STRUCTURED_CHEBYSHEV_LCU_RENORMALIZATION_AND_EXACT_PHASE_MATCHED_ACTUATOR",
        "bold_hypothesis": "Do not amplify the ill-conditioned Lagrange-product LCU. Use the canonical Halmos walk to block-encode Chebyshev powers, then transform the exact finite-spectrum remainder into its unique Chebyshev coefficients.",
        "exact_walk_identity": "For A=H/alpha, D=sqrt(I-A^2), BE(H)=[[A,D],[D,-A]], Z=diag(I,-I), and R=Z BE(H), the commuting functional calculus gives <0|R^k|0>=T_k(A).",
        "compiler": {
            "polynomial": "P_H(x)=sum_(k=0)^(m-1) c_k T_k(x), uniquely fixed by P_H(lambda_j/alpha)=exp(-i*pi*lambda_j/3)",
            "SELECT": "coherently select the finite powers R^k, k=0,...,m-1",
            "normalization": "s_C=sum_k |c_k|",
            "success_block": "exp(-i*pi*H/3)/s_C",
            "exact_determinization": "BGCE489 arbitrary-phase final iterate applied to the new known success 1/s_C^2",
            "coefficient_fit": False,
            "manual_phase_tuning": False,
        },
        "four_probability_role": "The source-V4 four-probability 1+3 carrier remains the exact outer selector of G1,H1,H2,H3. Chebyshev compilation acts only inside the selected branch and therefore does not require raw V4 reflection compression.",
        "cases_checked": len(records),
        "signed_sectors_checked": 8,
        "control_families_checked": ["G1", "H1", "H2", "H3"],
        "distinct_node_count_range": [
            min(item["distinct_spectral_nodes"] for item in records),
            max(item["distinct_spectral_nodes"] for item in records),
        ],
        "coefficient_l1_log10_range": [
            min(item["log10_coefficient_l1_normalization"] for item in records),
            max(item["log10_coefficient_l1_normalization"] for item in records),
        ],
        "unamplified_success_log10_range": [
            min(item["log10_unamplified_success_probability"] for item in records),
            max(item["log10_unamplified_success_probability"] for item in records),
        ],
        "success_improvement_orders_range": [
            min(item["success_probability_improvement_orders"] for item in records),
            max(item["success_probability_improvement_orders"] for item in records),
        ],
        "exact_phase_matched_base_call_range": [
            min(item["exact_phase_matched_base_calls"] for item in records),
            max(item["exact_phase_matched_base_calls"] for item in records),
        ],
        "total_H_block_encoding_query_range": [
            min(item["total_H_block_encoding_queries"] for item in records),
            max(item["total_H_block_encoding_queries"] for item in records),
        ],
        "maximum_interpolation_residual_70_digit": mp.nstr(maximum_interpolation_residual, 8),
        "maximum_walk_identity_residual_70_digit": mp.nstr(maximum_walk_residual, 8),
        "numerical_precision_digits": mp.mp.dps,
        "mpmath_version": mp.__version__,
        "counter_intuition_scan": "BGCE489's enormous lower bound was not a no-go for the target operation; it was a no-go for amplifying the BGCE488 Lagrange normalization. Changing to the source-compatible Chebyshev walk changes the queried black box and reduces s before amplification, without altering the exact spectral values.",
        "scope_boundary": "Closure uses the BGCE478 typed canonical Halmos block-encoding constructor, BGCE484 typed coherent finite-list routing, BGCE487 continuous source clock, and finite tensor/control composition. It is not a derivation of the square-root defect or controlled powers from bare adjacent-Braid words, nor a hardware timing/error estimate, seconds calibration, continuum/QFT limit or empirical confirmation.",
        "next_gate": "BGCE491_TYPED_HALMOS_CHEBYSHEV_WALK_TO_SOURCE_WORD_LOCAL_COMPILATION_GATE",
        "records": records,
        "source_metadata": source_meta,
    }


if __name__ == "__main__":
    result = run()
    (HERE / "RAW_OUTPUT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "gate_id": result["gate_id"],
        "decision": result["focal_decision"],
        "cases_checked": result["cases_checked"],
        "unamplified_success_log10_range": result["unamplified_success_log10_range"],
        "success_improvement_orders_range": result["success_improvement_orders_range"],
        "phase_matched_base_call_range": result["exact_phase_matched_base_call_range"],
        "total_H_query_range": result["total_H_block_encoding_query_range"],
        "next_gate": result["next_gate"],
    }, indent=2, sort_keys=True))
