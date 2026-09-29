#!/usr/bin/env python3
"""PUBLIC-RUN-BGCE464-001: exact within-Z2-sector matrix-algebra gate."""

from __future__ import annotations

from collections import Counter, deque
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys

import numpy as np


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
PATHS = {
    "bgce459_result": REPO / "records/BGCE459_SOURCE_COUNTING_GLUE_TO_BORN_PROBABILITY_UNIQUENESS_GATE_20260925/RUN_001/RESULT.json",
    "bgce459_raw": REPO / "records/BGCE459_SOURCE_COUNTING_GLUE_TO_BORN_PROBABILITY_UNIQUENESS_GATE_20260925/RUN_001/RAW_OUTPUT.json",
    "bgce463_result": REPO / "records/BGCE463_RESIDUAL_TWO_COMPONENT_INVARIANT_IDENTIFICATION_GATE_20260925/RUN_001/RESULT.json",
    "bgce463_raw": REPO / "records/BGCE463_RESIDUAL_TWO_COMPONENT_INVARIANT_IDENTIFICATION_GATE_20260925/RUN_001/RAW_OUTPUT.json",
    "bgce463_eval": REPO / "records/BGCE463_RESIDUAL_TWO_COMPONENT_INVARIANT_IDENTIFICATION_GATE_20260925/RUN_001/evaluate_scout.py",
    "ub443": REPO / "records/UB443_TYPED_SIGNED_SURVIVOR_GAUGE_OR_OBSERVABLE_GATE/evaluate.py",
}
EXPECTED = {
    "bgce459_result": "e251051f4e88e91fa2fb66ca6233226cf55bcc38c339860f0def0beba08957f3",
    "bgce459_raw": "3ee60445d4a516e4ed5abca170d27505421b9990cdc8003167fae792568f8e3d",
    "bgce463_result": "77c7b3fed88a0f1748fc590d4ddef83e39524d5ba6c1e9c59e5dade49bad2bf2",
    "bgce463_raw": "0072421a66c0ca0d64d8c26b0c939865c81c8561685d58008145988a36bf891e",
    "bgce463_eval": "3701a07f08c29ce4b7d22d28c642230b763ffe2ee5677382508c018a2d95b2b0",
    "ub443": "ad53908146ba65d9de71994c0b297fac759a05c4938378f6cc962bbf9eae8c9e",
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


def three_cycles(perm: tuple[int, ...]) -> list[tuple[int, int, int]]:
    unseen = set(range(len(perm)))
    result = []
    while unseen:
        start = min(unseen)
        cycle = []
        value = start
        while value not in cycle:
            cycle.append(value)
            value = perm[value]
        unseen -= set(cycle)
        if len(cycle) == 3:
            minimum = min(cycle)
            ordered = [minimum]
            ordered.append(perm[ordered[-1]])
            ordered.append(perm[ordered[-1]])
            result.append(tuple(ordered))
    return sorted(result)


def components(adjacency: list[set[int]]) -> list[list[int]]:
    unseen = set(range(len(adjacency)))
    result = []
    while unseen:
        start = min(unseen)
        component = {start}
        queue = deque([start])
        while queue:
            value = queue.popleft()
            for moved in adjacency[value]:
                if moved not in component:
                    component.add(moved)
                    queue.append(moved)
        unseen -= component
        result.append(sorted(component))
    return result


def run() -> dict:
    for name, expected in EXPECTED.items():
        assert digest(PATHS[name]) == expected, name
    bgce459 = json.loads(PATHS["bgce459_result"].read_text())
    bgce463 = json.loads(PATHS["bgce463_result"].read_text())
    assert bgce459["construction"]["complex_dimension"] == 36
    assert "C-invariant source-cylinder sums" in bgce459["construction"]["source_typed_observables"]
    bits = tuple(bgce463["exact_grading"]["digit_bits_0_to_4"])
    assert bits == (0, 1, 0, 1, 0)

    h = load_module("bgce463_for_bgce464", PATHS["bgce463_eval"])
    g = load_module("bgce462_for_bgce464", h.PATHS["bgce462_eval"])
    b = load_module("bgce458_for_bgce464", g.PATHS["bgce458_eval"])
    b.REPO = REPO
    b.SOURCE = g.PATHS["source"]
    table = b.pair_table_from_source()
    r1 = b.perm_for_site(table, 0)
    r2 = b.perm_for_site(table, 1)
    c = b.compose(r1, r2)
    cinv = b.inverse(c)
    cmat = g.permutation_matrix(c)
    cinvmat = g.permutation_matrix(cinv)
    identity125 = np.eye(125, dtype=np.int64)
    q = 2 * identity125 - cmat - cinvmat
    a = cmat - cinvmat
    cycles = three_cycles(c)
    assert len(cycles) == 36

    cycle_labels = []
    for cycle in cycles:
        labels = set()
        for atom_index in cycle:
            atom = (atom_index // 25, (atom_index // 5) % 5, atom_index % 5)
            parity = bits[atom[0]] ^ bits[atom[1]] ^ bits[atom[2]]
            labels.add(1 if parity == 0 else -1)
        assert len(labels) == 1
        cycle_labels.append(next(iter(labels)))
    grading_dimensions = Counter(cycle_labels)

    ub443 = load_module("ub443_for_bgce464", PATHS["ub443"])
    survivors, endpoint = ub443.build_survivors()
    endpoint = endpoint.astype(np.int64)
    identity5 = np.eye(5, dtype=np.int64)
    endpoint_ops = [
        np.kron(np.kron(endpoint, identity5), identity5),
        np.kron(np.kron(identity5, endpoint), identity5),
        np.kron(np.kron(identity5, identity5), endpoint),
    ]

    sector_records = []
    canonical_partitions = set()
    for survivor in survivors:
        f = survivor["F"].astype(np.int64)
        p = survivor["P"].astype(np.int64)
        named_operators = [
            ("J0", endpoint_ops[0]), ("J1", endpoint_ops[1]), ("J2", endpoint_ops[2]),
            ("F12", np.kron(f, identity5)), ("F23", np.kron(identity5, f)),
            ("P12", np.kron(p, identity5)), ("P23", np.kron(identity5, p)),
        ]
        adjacency = [set([index]) for index in range(len(cycles))]
        operator_records = []
        cross_grading_edges = 0
        for name, operator in named_operators:
            t = q @ operator @ q
            linear = 3 * t - a @ t @ a
            assert np.array_equal(linear, linear.T)
            assert np.array_equal(a @ linear, linear @ a)
            edges = []
            new_edges = []
            for left in range(len(cycles)):
                for right in range(left + 1, len(cycles)):
                    if np.any(linear[np.ix_(cycles[left], cycles[right])]):
                        edges.append((left, right))
                        cross_grading_edges += cycle_labels[left] != cycle_labels[right]
                        if right not in adjacency[left]:
                            new_edges.append((left, right))
                        adjacency[left].add(right)
                        adjacency[right].add(left)
            operator_records.append({
                "operator": name,
                "complex_line_pairs": len(edges),
                "new_graph_edges_when_added": len(new_edges),
            })
        comps = components(adjacency)
        component_sizes = sorted(len(value) for value in comps)
        component_labels = []
        for component in comps:
            labels = {cycle_labels[index] for index in component}
            assert len(labels) == 1
            component_labels.append(next(iter(labels)))
        partition = tuple(sorted(tuple(value) for value in comps))
        canonical_partitions.add(partition)
        sector_records.append({
            "mask": survivor["mask"],
            "component_count": len(comps),
            "component_complex_dimensions": component_sizes,
            "component_grading_labels": component_labels,
            "cross_grading_edges": cross_grading_edges,
            "operator_records": operator_records,
        })

    all_two = all(row["component_count"] == 2 for row in sector_records)
    all_sizes_match = all(row["component_complex_dimensions"] == sorted(grading_dimensions.values()) for row in sector_records)
    no_cross = all(row["cross_grading_edges"] == 0 for row in sector_records)
    universal_partition = len(canonical_partitions) == 1
    passed = all_two and all_sizes_match and no_cross and universal_partition
    dims = sorted(grading_dimensions.values())
    return {
        "schema": "siel.public-calculation.bgce464.raw.v1",
        "scout_id": "PUBLIC-RUN-BGCE464-001",
        "gate_id": "BGCE464",
        "attempt": "0001",
        "source_commit": "f0f5a77425897b4e74719598967b635abc457101",
        "source_snapshot_id": "PUBLIC-SNAPSHOT-f0f5a7742589",
        "primary_evidence_status": "Theoretical derivation",
        "scientific_layer": "finite source observable-algebra irreducibility",
        "forbidden_inputs_used": [],
        "complex_lines": len(cycles),
        "source_cylinder_minimal_projectors": len(cycles),
        "grading_complex_dimensions": {str(label): grading_dimensions[label] for label in sorted(grading_dimensions)},
        "signed_sectors_checked": len(survivors),
        "sector_records": sector_records,
        "universal_complex_line_partition": universal_partition,
        "all_sectors_connected_within_each_grading": passed,
        "global_generated_dagger_algebra_complex_dimension": sum(value * value for value in dims) if passed else None,
        "global_commutant_complex_dimension": 2 if passed else None,
        "within_sector_commutant_complex_dimensions": [1, 1] if passed else None,
        "matrix_unit_argument": "Cycle-cylinder projectors give E_ii. For each nonzero graph edge, E_ii L E_j is a nonzero complex scalar times E_ij; dagger gives E_ji and connected paths give every matrix unit within that grading sector.",
        "focal_decision": "PASS_SCOPED_FULL_COMPLEX_MATRIX_ALGEBRA_WITHIN_EACH_SOURCE_Z2_SUPERSELECTION_SECTOR" if passed else "NO_GO_GENERATOR_GRAPH_SPLITS_INSIDE_A_SOURCE_Z2_SECTOR",
        "operational_status": "OPEN_CATEGORICAL_GENERATORS_NOT_YET_DERIVED_AS_PHYSICAL_HAMILTONIAN_CONTROLS",
        "strongest_counterpattern": "Finite algebraic irreducibility does not show that the source morphisms can be enacted as continuous physical controls or that the same closure survives continuum and field-theory limits.",
        "claim_ceiling": "This gate can establish only the full finite complex dagger algebra and scalar commutant within each fixed source Z2 superselection sector. It does not establish physical Hamiltonian controllability, continuum/QFT completion, empirical quantum mechanics, pointed-Braid specificity, confirmation, Level 3 or Official SIEL adoption."
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
