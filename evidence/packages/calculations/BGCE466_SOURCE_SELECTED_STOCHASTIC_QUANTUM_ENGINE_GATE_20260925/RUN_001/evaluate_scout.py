#!/usr/bin/env python3
"""BGCE466: source-scheduled stochastic quantum engine on the finite carrier."""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import itertools
import json
import math
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import expm


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
PATHS = {
    "o14": REPO / "public-inputs/formal_checks/ocbfh014_source_native_refinement_naturality_check.py",
    "source": REPO / "records/BGCE139_SOURCE_SPECTRAL_CYLINDER_OPERATIONAL_EVENT_IDENTIFICATION_GATE_20260919/RAW_OUTPUT.json",
    "b362": REPO / "records/BGCE362_SOURCE_BRAID_LABELLED_INSTRUMENT_RECORD_TO_CANONICAL_THREE_CONTROL_CYCLE_GATE_20260924/RESULT.json",
    "b458e": REPO / "records/BGCE458_BARE_BRAID_ORIENTED_CYCLE_TO_COMPLEX_KINEMATICS_GATE_20260925/RUN_001/evaluate_scout.py",
    "b459": REPO / "records/BGCE459_SOURCE_COUNTING_GLUE_TO_BORN_PROBABILITY_UNIQUENESS_GATE_20260925/RUN_001/RESULT.json",
    "b463": REPO / "records/BGCE463_RESIDUAL_TWO_COMPONENT_INVARIANT_IDENTIFICATION_GATE_20260925/RUN_001/RESULT.json",
    "b464": REPO / "records/BGCE464_WITHIN_SUPERSELECTION_SECTOR_ALGEBRA_IRREDUCIBILITY_GATE_20260925/RUN_001/RESULT.json",
    "b465": REPO / "records/BGCE465_SOURCE_GENERATORS_TO_PHYSICAL_CONTINUOUS_UNITARY_CONTROL_GATE_20260925/RUN_001/RESULT.json",
}
EXPECTED = {
    "o14": "176c75ac349f0f3f142d9c850ca0682436b7ad00cd179f6806de253d0a7acabb",
    "source": "ddf630fbaff1ae4e72c778f47dc2bed6906da0a8aa17d4e6a98d2c96791955e9",
    "b362": "487596c999eea55626332382b1b8afb6415de16e7656bbfb2a2c42136abe81d9",
    "b458e": "f7fc8db4ab821c223e466e335b5c18a4c2dc824e6f0060471fcf9d53271d02a8",
    "b459": "e251051f4e88e91fa2fb66ca6233226cf55bcc38c339860f0def0beba08957f3",
    "b463": "77c7b3fed88a0f1748fc590d4ddef83e39524d5ba6c1e9c59e5dade49bad2bf2",
    "b464": "c29d76d18980e8253260c87dd09c1c9cc7dfbf4e1dddbb1ba96ce63f41e69b2e",
    "b465": "6729bd4c969bd1177b5caa7eae43b495d38025306ba2cb6322b02bcd2525cbcf",
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


def permutation_matrix(perm: tuple[int, ...]) -> np.ndarray:
    matrix = np.zeros((len(perm), len(perm)), dtype=np.int64)
    for source, target in enumerate(perm):
        matrix[target, source] = 1
    return matrix


def cycles_of_three(perm: tuple[int, ...]) -> list[tuple[int, int, int]]:
    unseen = set(range(len(perm)))
    result = []
    while unseen:
        start = min(unseen)
        cycle = (start, perm[start], perm[perm[start]])
        unseen -= set(cycle)
        if len(set(cycle)) == 3:
            result.append(cycle)
    return result


def projective_distance(left: np.ndarray, right: np.ndarray) -> float:
    dimension = left.shape[0]
    squared = 2.0 * dimension - 2.0 * abs(np.trace(left.conj().T @ right))
    return math.sqrt(max(0.0, squared))


def run() -> dict:
    for name, path in PATHS.items():
        assert digest(path) == EXPECTED[name], name
    docs = {name: json.loads(PATHS[name].read_text()) for name in ("b362", "b459", "b463", "b464", "b465")}
    assert docs["b362"]["stochastic_three_control_cycle"]["law_on_orders"] == ["1/6"] * 6
    assert docs["b362"]["source_duration"]["duration"] == "pi/3"
    assert docs["b459"]["construction"]["complex_dimension"] == 36
    assert docs["b463"]["exact_grading"]["digit_bits_0_to_4"] == [0, 1, 0, 1, 0]
    assert docs["b464"]["decision"] == "CLOSED_SCOPED"
    assert docs["b465"]["decision"] == "SPLIT_SCOPED_PASS_AND_ROUTE_NO_GO"

    o14 = load_module("bgce466_o14", PATHS["o14"])
    b458 = load_module("bgce466_b458", PATHS["b458e"])
    b458.REPO = REPO
    b458.SOURCE = PATHS["source"]
    table = b458.pair_table_from_source()
    r1 = b458.perm_for_site(table, 0)
    r2 = b458.perm_for_site(table, 1)
    c = b458.compose(r1, r2)
    cinv = b458.inverse(c)
    cmat = permutation_matrix(c)
    cinvmat = permutation_matrix(cinv)
    identity125 = np.eye(125, dtype=np.int64)
    q = 2 * identity125 - cmat - cinvmat
    a = cmat - cinvmat
    cycles = cycles_of_three(c)
    assert len(cycles) == 36

    omega = np.exp(2j * np.pi / 3.0)
    basis = np.zeros((125, 36), dtype=complex)
    for column, cycle in enumerate(cycles):
        basis[list(cycle), column] = (1.0, omega * omega, omega)
    basis /= math.sqrt(3.0)
    assert np.linalg.norm(basis.conj().T @ basis - np.eye(36)) < 1e-12
    assert np.linalg.norm(a @ basis - 1j * math.sqrt(3.0) * basis) < 1e-12

    bits = tuple(docs["b463"]["exact_grading"]["digit_bits_0_to_4"])
    cycle_labels = []
    for first, _, _ in cycles:
        digits = (first // 25, (first // 5) % 5, first % 5)
        cycle_labels.append((-1) ** (bits[digits[0]] ^ bits[digits[1]] ^ bits[digits[2]]))
    labels = np.array(cycle_labels, dtype=np.int64)
    assert [int(np.sum(labels == sign)) for sign in (-1, 1)] == [18, 18]
    z = np.diag([
        (-1) ** (bits[index // 25] ^ bits[(index // 5) % 5] ^ bits[index % 5])
        for index in range(125)
    ]).astype(np.int64)

    survivors, projectors, _, _ = o14.reconstruct_actual_source()
    epsilon = math.pi / 3.0
    order_space = list(itertools.permutations(range(3)))
    records = []
    global_metrics = {
        "minimum_noncommutator_norm": float("inf"),
        "minimum_projective_order_separation": float("inf"),
        "maximum_hermitian_residual": 0.0,
        "maximum_unitary_residual": 0.0,
        "minimum_kraus_rank": 6,
    }

    for survivor in survivors:
        g_num, g_den, _, _ = o14.source_g1(survivor["R"].astype(np.int64))
        controls_125 = [g_num / g_den]
        exact_compression_records = []
        leakage_counts = [int(np.count_nonzero(g_num @ q - q @ g_num))]

        g_t = q @ g_num @ q
        g_linear = 3 * g_t - a @ g_t @ a
        assert np.array_equal(a @ g_linear, g_linear @ a)
        assert np.array_equal(z @ g_linear, g_linear @ z)
        assert np.array_equal(g_linear, g_linear.T)
        exact_compression_records.append({"generator": "G1", "nonzero_entries": int(np.count_nonzero(g_linear))})

        for index, (projector_num, projector_den) in enumerate(projectors, start=1):
            projector_num_125 = np.kron(projector_num, np.eye(5, dtype=np.int64))
            k_num = g_num @ projector_num_125 - projector_num_125 @ g_num
            leakage_counts.append(int(np.count_nonzero(k_num @ q - q @ k_num)))
            k_t = q @ k_num @ q
            k_linear = 3 * k_t - a @ k_t @ a
            assert np.array_equal(a @ k_linear, k_linear @ a)
            assert np.array_equal(z @ k_linear, k_linear @ z)
            assert np.array_equal(k_linear, -k_linear.T)
            assert np.count_nonzero(k_linear) > 0
            exact_compression_records.append({"generator": f"H{index}", "nonzero_entries": int(np.count_nonzero(k_linear))})
            controls_125.append(-1j * k_num / (g_den * projector_den))

        assert all(value > 0 for value in leakage_counts)
        compressed = [basis.conj().T @ control @ basis for control in controls_125]
        hermitian_residuals = [float(np.linalg.norm(control - control.conj().T)) for control in compressed]
        assert max(hermitian_residuals) < 1e-12
        grading_cross_norms = [float(np.linalg.norm(control[np.ix_(labels == -1, labels == 1)])) for control in compressed]
        assert max(grading_cross_norms) < 1e-12

        block_records = []
        for sign in (-1, 1):
            selector = labels == sign
            blocks = [control[np.ix_(selector, selector)] for control in compressed]
            ranks = [int(np.linalg.matrix_rank(control, tol=1e-10)) for control in blocks]
            commutator_norms = [float(np.linalg.norm(blocks[0] @ control - control @ blocks[0])) for control in blocks[1:]]
            assert min(commutator_norms) > 0.4
            phase_unitary = expm(-1j * epsilon * blocks[0])
            spatial_unitaries = [expm(-1j * epsilon * control) for control in blocks[1:]]
            order_unitaries = []
            for order in order_space:
                unitary = np.eye(18, dtype=complex)
                for index in order:
                    unitary = phase_unitary @ spatial_unitaries[index] @ unitary
                order_unitaries.append(unitary)
            unitary_residuals = [float(np.linalg.norm(unitary.conj().T @ unitary - np.eye(18))) for unitary in order_unitaries]
            minimum_separation = min(
                projective_distance(order_unitaries[left], order_unitaries[right])
                for left in range(6) for right in range(left)
            )
            gram = np.array([
                [np.trace(left.conj().T @ right) for right in order_unitaries]
                for left in order_unitaries
            ])
            kraus_rank = int(np.linalg.matrix_rank(gram, tol=1e-9))
            assert max(unitary_residuals) < 1e-11
            assert minimum_separation > 0.8
            assert kraus_rank == 6
            channel_identity = sum(unitary.conj().T @ unitary for unitary in order_unitaries) / 6.0
            assert np.linalg.norm(channel_identity - np.eye(18)) < 1e-11
            block_records.append({
                "grading": int(sign),
                "complex_dimension": 18,
                "generator_ranks": ranks,
                "G1_Hi_commutator_norms": commutator_norms,
                "minimum_projective_order_separation": minimum_separation,
                "six_order_kraus_gram_rank": kraus_rank,
                "maximum_unitary_residual": max(unitary_residuals),
                "mixed_unitary_channel": "CPTP_UNITAL",
            })
            global_metrics["minimum_noncommutator_norm"] = min(global_metrics["minimum_noncommutator_norm"], min(commutator_norms))
            global_metrics["minimum_projective_order_separation"] = min(global_metrics["minimum_projective_order_separation"], minimum_separation)
            global_metrics["maximum_unitary_residual"] = max(global_metrics["maximum_unitary_residual"], max(unitary_residuals))
            global_metrics["minimum_kraus_rank"] = min(global_metrics["minimum_kraus_rank"], kraus_rank)

        global_metrics["maximum_hermitian_residual"] = max(global_metrics["maximum_hermitian_residual"], max(hermitian_residuals))
        records.append({
            "mask": survivor["mask"],
            "direct_source_generator_carrier_leakage_nonzero_counts": leakage_counts,
            "canonical_compression_exact_records": exact_compression_records,
            "maximum_grading_cross_block_norm": max(grading_cross_norms),
            "blocks": block_records,
        })

    return {
        "schema": "siel.public-calculation.bgce466.raw.v1",
        "scout_id": "PUBLIC-RUN-BGCE466-001",
        "gate_id": "BGCE466",
        "attempt": "0001",
        "source_commit": "74ba3b72a45706ed2efa4652568f7753fc5c6868",
        "source_snapshot_id": "PUBLIC-SNAPSHOT-74ba3b72a457",
        "primary_evidence_status": "Exploratory theoretical derivation",
        "scientific_layer": "finite source-scheduled quantum-operation candidate",
        "forbidden_inputs_used": [],
        "signed_sectors_checked": 8,
        "grading_blocks_checked": 16,
        "carrier": "36 complex dimensions = 18(-) direct-sum 18(+)",
        "direct_125D_control_preserves_carrier": False,
        "direct_control_result": "NO_GO_ALL_FOUR_GENERATORS_LEAK_THE_BGCE458_CARRIER_IN_ALL_EIGHT_SECTORS",
        "interpretive_leap": "Treat the unique source-counting/cup orthogonal compression O -> B* O B as the effective Hamiltonian on the reconstructed quantum carrier before exponentiation.",
        "compression_status": "CANONICAL_AND_COEFFICIENT_FREE_BUT_PHYSICAL_IMPLEMENTATION_NOT_DERIVED",
        "engine_schedule": {
            "generators": ["compressed G1", "compressed H1", "compressed H2", "compressed H3"],
            "duration_each": "pi/3",
            "order_law": "uniform on all six permutations of H1,H2,H3",
            "pulse_step": "exp(-i pi compressed_G1/3) exp(-i pi compressed_Hi/3)",
            "duration_or_amplitude_fit_used": False,
            "deterministic_label_to_order_map_required": False,
        },
        "engine_channel": "E(rho)=1/6 sum_sigma U_sigma rho U_sigma^*",
        "engine_channel_status": "CPTP_UNITAL_Z2_PRESERVING_KRAUS_RANK_6_IN_ALL_16_BLOCKS",
        "all_blocks_noncommuting": True,
        "all_six_orders_projectively_distinct_in_all_blocks": True,
        "global_metrics": global_metrics,
        "records": records,
        "focal_decision": "SCOPED_PASS_FINITE_SOURCE_SCHEDULED_STOCHASTIC_QUANTUM_ENGINE_UNDER_CANONICAL_CARRIER_COMPRESSION_HYPOTHESIS",
        "strongest_counterpattern": "The original 125-dimensional G1/H_i pulses do not preserve the reconstructed carrier. The engine therefore depends on interpreting the canonical orthogonal compression as effective dynamics; no source actuator or physical Zeno mechanism implementing that compression has yet been derived.",
        "claim_ceiling": "This gate constructs a coefficient-free finite stochastic mixed-unitary engine on the BGCE458-464 carrier under the canonical compression hypothesis. It does not establish that the uncompressed source physically enacts the compressed Hamiltonians, physical time calibration, deterministic control, universal controllability, continuum/QFT quantum mechanics, empirical confirmation, Level 3, or Official SIEL adoption."
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
