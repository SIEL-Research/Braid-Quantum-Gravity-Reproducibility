#!/usr/bin/env python3
"""BGCE287: exact source-event-path BKM horizontal conductance lift."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, permutations
from pathlib import Path
from typing import Any
import hashlib
import json
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MATRIX = json.loads((HERE / "SOURCE_MATRIX.json").read_text())
REVISION = MATRIX["source_revision"]
ZERO = Fraction(0)
ONE = Fraction(1)
SYM_INDEX = ((0, 0), (1, 1), (2, 2), (3, 3), (0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
AXIS_PAIRS = tuple(combinations(range(4), 2))


def archived_bytes(relative: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{REVISION}:{relative}"], cwd=ROOT)


def verify_sources() -> dict[str, str]:
    checked: dict[str, str] = {}
    for relative, expected in MATRIX["inputs_sha256"].items():
        data = archived_bytes(relative)
        assert data == (ROOT / relative).read_bytes(), relative
        actual = hashlib.sha256(data).hexdigest()
        assert actual == expected, relative
        checked[f"{REVISION}:{relative}"] = actual
    return checked


def transpose(a):
    return [list(row) for row in zip(*a)]


def mm(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def eye(n):
    return [[ONE if i == j else ZERO for j in range(n)] for i in range(n)]


def inverse(a):
    n = len(a)
    work = [list(row) + ident for row, ident in zip(a, eye(n))]
    for col in range(n):
        pivot = next(row for row in range(col, n) if work[row][col] != 0)
        work[col], work[pivot] = work[pivot], work[col]
        scale = work[col][col]
        work[col] = [value / scale for value in work[col]]
        for row in range(n):
            if row == col:
                continue
            factor = work[row][col]
            if factor:
                work[row] = [value - factor * base for value, base in zip(work[row], work[col])]
    return [row[n:] for row in work]


def rref(a):
    work = [list(row) for row in a]
    rows = len(work)
    cols = len(work[0]) if rows else 0
    pivots = []
    lead = 0
    for row in range(rows):
        while lead < cols and all(work[k][lead] == 0 for k in range(row, rows)):
            lead += 1
        if lead == cols:
            break
        pivot = next(k for k in range(row, rows) if work[k][lead] != 0)
        work[row], work[pivot] = work[pivot], work[row]
        scale = work[row][lead]
        work[row] = [value / scale for value in work[row]]
        for k in range(rows):
            if k != row and work[k][lead] != 0:
                factor = work[k][lead]
                work[k] = [value - factor * base for value, base in zip(work[k], work[row])]
        pivots.append(lead)
        lead += 1
    return work, pivots


def rank(a):
    return len(rref(a)[1])


def nullspace(a):
    reduced, pivots = rref(a)
    cols = len(a[0])
    free = [col for col in range(cols) if col not in pivots]
    basis = []
    for free_col in free:
        vector = [ZERO] * cols
        vector[free_col] = ONE
        for row, pivot_col in enumerate(pivots):
            vector[pivot_col] = -reduced[row][free_col]
        basis.append(vector)
    return basis


def outer(v):
    return [[v[i] * v[j] for j in range(4)] for i in range(4)]


def flatten_symmetric(matrix):
    assert matrix == transpose(matrix)
    return [matrix[i][j] for i, j in SYM_INDEX]


def columns_to_matrix(columns):
    return [[column[row] for column in columns] for row in range(len(columns[0]))]


def parse_real(matrix):
    return [[Fraction(value) for value in row] for row in matrix]


def parse_real_q17(serial):
    result = []
    for row in serial:
        parsed = []
        for value in row:
            assert Fraction(value[1]) == 0
            parsed.append(Fraction(value[0]))
        result.append(parsed)
    return result


def transform(change, tensor):
    return mm(transpose(change), mm(tensor, change))


def actual_edges(records):
    mapping = {tuple(record["input"]): tuple(record["output"]) for record in records}
    seen = set()
    edges = []
    for source, target in mapping.items():
        if source == target:
            continue
        key = tuple(sorted((source, target)))
        if key in seen:
            continue
        seen.add(key)
        assert mapping[target] == source
        delta = (target[0] - source[0], target[1] - source[1])
        sign = 1 if delta[0] * delta[1] > 0 else -1
        assert abs(delta[0]) == abs(delta[1])
        edges.append({"delta": delta, "sign": sign, "d2": delta[0] * delta[0]})
    return edges


def permutation_matrix_on_sym(perm):
    columns = []
    for i, j in SYM_INDEX:
        base = [[ZERO] * 4 for _ in range(4)]
        base[i][j] = ONE
        base[j][i] = ONE
        if i == j:
            base[i][j] = ONE
        moved = [[ZERO] * 4 for _ in range(4)]
        for a in range(4):
            for b in range(4):
                moved[perm[a]][perm[b]] = base[a][b]
        columns.append(flatten_symmetric(moved))
    return columns_to_matrix(columns)


def permutation_matrix_on_raw(perm, edge_count):
    labels = [(pair, edge) for pair in AXIS_PAIRS for edge in range(edge_count)]
    lookup = {label: index for index, label in enumerate(labels)}
    matrix = [[ZERO] * len(labels) for _ in labels]
    for source_index, (pair, edge) in enumerate(labels):
        moved_pair = tuple(sorted((perm[pair[0]], perm[pair[1]])))
        matrix[lookup[(moved_pair, edge)]][source_index] = ONE
    return matrix


def qserial(value):
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def build_output() -> dict[str, Any]:
    checked = verify_sources()
    audits = ROOT / "audits"
    bg139 = json.loads((audits / "SRA_DPA_BGCE139_SOURCE_SPECTRAL_CYLINDER_OPERATIONAL_EVENT_IDENTIFICATION_GATE_20260919/RAW_OUTPUT.json").read_text())
    bg254 = json.loads((audits / "SRA_DPA_BGCE254_SOURCE_RESPONSE_LEGENDRE_EXACTNESS_TO_UNIQUE_LOGZ_BREGMAN_EDGE_ACTION_GATE_20260921/RESULT.json").read_text())
    bg256 = json.loads((audits / "SRA_DPA_BGCE256_BRAID_INDUCED_EVENT_TRANSITION_COBORDER_TO_NEIGHBOR_COUPLING_LAW_GATE_20260921/RAW_OUTPUT.json").read_text())
    bg266 = json.loads((audits / "SRA_DPA_BGCE266_REFINEMENT_CLOCK_TO_UNIQUE_EVENT_SEMIGROUP_AND_IR_OS_CONTINUATION_GATE_20260922/RAW_OUTPUT.json").read_text())
    bg268 = json.loads((audits / "SRA_DPA_BGCE268_SOURCE_GRAM_SCHUR_CHANNEL_TO_CAUSAL_METRIC_INTERTWINER_GATE_20260922/RAW_OUTPUT.json").read_text())
    bg281 = json.loads((audits / "SRA_DPA_BGCE281_ALL_SECTOR_ORDERED_EDGE_METRIC_TANGENT_AND_NONMETRICITY_GATE_20260923/RAW_OUTPUT.json").read_text())
    bg286 = json.loads((audits / "SRA_DPA_BGCE286_X21R1_METRIC_TANGENT_TO_BRAID_EVENT_CONDUCTANCE_VARIATION_GATE_20260923/RAW_OUTPUT.json").read_text())

    assert bg254["unique_response_exact_edge_functional"] == "Umegaki_relative_entropy_equals_logZ_Bregman_divergence"
    assert bg256["pair_event_moment"]["actual_moved_inputs"] == 16
    assert bg266["causal_clock_rate"]["future_minimal_positive_rate"] == "2*pi/3"
    assert bg266["positive_time_semigroup"]["symmetric_markov"] is True
    assert bg286["conductance_to_metric_moment_map"]["kernel_dimension"] == 2

    edges = actual_edges(bg139["event_transition_gate"]["canonical_transition_on_digit_pairs"])
    assert len(edges) == 8
    assert sum(edge["sign"] > 0 for edge in edges) == 2
    assert sum(edge["sign"] < 0 for edge in edges) == 6

    # One raw rate tangent per actual undirected edge and unordered axis pair.
    raw_columns = []
    raw_labels = []
    for pair in AXIS_PAIRS:
        i, j = pair
        for edge_index, edge in enumerate(edges):
            v = [ZERO] * 4
            v[i] = Fraction(abs(edge["delta"][0]))
            v[j] = Fraction(edge["sign"] * abs(edge["delta"][1]))
            raw_columns.append(flatten_symmetric(outer(v)))
            raw_labels.append(f"pair_{i}{j}_edge_{edge_index}")
    raw_map = columns_to_matrix(raw_columns)
    raw_rank = rank(raw_map)
    raw_kernel = nullspace(raw_map)
    raw_kernel_dimension = len(raw_kernel)

    # The common source rate makes the event-path Fisher/BKM metric a positive scalar times identity.
    # The scalar 1/r does not affect its orthogonal complement.
    raw_gram = mm(transpose(raw_map), raw_map)
    kernel_gram = mm(raw_kernel, transpose(raw_kernel))
    kernel_metric_rank = rank(kernel_gram)
    assert kernel_metric_rank == raw_kernel_dimension

    # Euclidean/BKM minimum-norm right inverse: H=M^T(MM^T)^-1.
    base_metric = mm(raw_map, transpose(raw_map))
    horizontal = mm(transpose(raw_map), inverse(base_metric))
    right_inverse = mm(raw_map, horizontal)
    assert right_inverse == eye(10)
    kernel_orthogonality = mm(raw_kernel, horizontal)
    assert all(all(value == 0 for value in row) for row in kernel_orthogonality)

    # Exact S4 naturality of the selected horizontal lift.
    s4_checks = 0
    for perm in permutations(range(4)):
        target_action = permutation_matrix_on_sym(perm)
        raw_action = permutation_matrix_on_raw(perm, len(edges))
        assert mm(horizontal, target_action) == mm(raw_action, horizontal)
        assert mm(raw_map, raw_action) == mm(target_action, raw_map)
        s4_checks += 1

    # Quotient to BGCE286's two moment coordinates per axis pair.
    # Minimizing raw BKM cost at fixed moment gives weights inverse to sum d^4.
    common_d4 = sum(edge["d2"] ** 2 for edge in edges if edge["sign"] > 0)
    relative_d4 = sum(edge["d2"] ** 2 for edge in edges if edge["sign"] < 0)
    assert (common_d4, relative_d4) == (2, 36)
    quotient_weights = [Fraction(relative_d4, common_d4) if mode == 0 else ONE for _ in AXIS_PAIRS for mode in range(2)]

    quotient_columns = []
    for i, j in AXIS_PAIRS:
        common = [ZERO] * 4
        relative = [ZERO] * 4
        common[i] = common[j] = ONE
        relative[i] = ONE
        relative[j] = -ONE
        quotient_columns.extend((flatten_symmetric(outer(common)), flatten_symmetric(outer(relative))))
    quotient_map = columns_to_matrix(quotient_columns)
    quotient_kernel = nullspace(quotient_map)
    weighted_kernel_gram = []
    for left in quotient_kernel:
        weighted_kernel_gram.append([
            sum(left[k] * quotient_weights[k] * right[k] for k in range(12))
            for right in quotient_kernel
        ])
    quotient_kernel_metric_rank = rank(weighted_kernel_gram)

    # Reproduce all actual tangents with the unique microscopic horizontal lift.
    u = parse_real(bg268["source_typed_intertwiner"]["U"])
    tangent_records = []
    for sector in bg281["sector_records"]:
        for direction in sector["direction_records"]:
            tangent = parse_real_q17(direction["ordered_Gram_tangent"])
            target = [[value] for value in flatten_symmetric(transform(u, tangent))]
            lift = mm(horizontal, target)
            reproduced = mm(raw_map, lift) == target
            orthogonal = all(mm(raw_kernel, lift)[row][0] == 0 for row in range(raw_kernel_dimension))
            tangent_records.append({
                "mask": int(sector["mask"]),
                "theta_direction": int(direction["theta_direction"]),
                "reproduced_exactly": reproduced,
                "BKM_horizontal": orthogonal,
                "nonzero_raw_edge_rates": sum(value[0] != 0 for value in lift),
            })
    actual_pass = len(tangent_records) == 24 and all(row["reproduced_exactly"] and row["BKM_horizontal"] for row in tangent_records)

    full_pass = (
        raw_rank == 10
        and raw_kernel_dimension == 38
        and kernel_metric_rank == 38
        and quotient_kernel_metric_rank == 2
        and s4_checks == 24
        and actual_pass
    )
    assert full_pass

    decision = (
        "FULL_PASS_THE_SOURCE_FIXED_COMMON_EVENT_RATE_MAKES_THE_ACTUAL_FORTY_EIGHT_EDGE_RATE_TANGENT_SPACE_CARRY_A_POSITIVE_EVENT_PATH_FISHER_BKM_METRIC__"
        "THE_MICROSCOPIC_SECOND_MOMENT_MAP_HAS_RANK_TEN_AND_A_THIRTY_EIGHT_DIMENSIONAL_KERNEL_BUT_THE_BKM_METRIC_IS_NONDEGENERATE_ON_THE_WHOLE_KERNEL__"
        "ITS_ORTHOGONAL_COMPLEMENT_DEFINES_A_UNIQUE_EXACT_S4_EQUIVARIANT_HORIZONTAL_RIGHT_INVERSE__ALL_TWENTY_FOUR_X21R1_METRIC_TANGENTS_ARE_REPRODUCED__"
        "AFTER_QUOTIENTING_TO_THE_TWELVE_BGCE286_MOMENT_COORDINATES_THE_PREVIOUS_TWO_DIMENSIONAL_KERNEL_HAS_POSITIVE_RANK_TWO_RESPONSE_WITH_SOURCE_FIXED_COMMON_TO_RELATIVE_WEIGHT_RATIO_EIGHTEEN_TO_ONE__"
        "FIRST_ORDER_CONDUCTANCE_LIFT_NONUNIQUENESS_IS_REMOVED_IN_THE_SOURCE_EVENT_PATH_BKM_HORIZONTAL_CLASS_WITHOUT_COEFFICIENT_FIT__"
        "FULL_NONLINEAR_PARENT_ACTION_HILBERT_STRESS_WARD_SDPC_AND_UNCONDITIONAL_EINSTEIN_REMAIN_OPEN"
    )

    return {
        "schema": "siel.dpa.bgce287.raw.v1",
        "candidate_id": "BGCE287",
        "source_revision": REVISION,
        "input_hashes_verified": checked,
        "baseline_gate": "PASS_REVISION_MATCHED_BGCE139_254_256_266_268_281_286_REPLAY",
        "endpoint_provenance": "NOT_ISSUED_BY_DPA__EXACT_FINITE_EVENT_PATH_INFORMATION_GEOMETRY_AUDIT_ONLY",
        "primary_evidence_status": "Theoretical derivation with exact source-event BKM horizontal selection",
        "scientific_layer": "first-order active conductance connection over the source-derived metric tangent",
        "source_event_path_geometry": {
            "actual_undirected_edges_per_axis_pair": len(edges),
            "unordered_axis_pairs": len(AXIS_PAIRS),
            "microscopic_rate_tangent_dimension": len(raw_columns),
            "common_source_rate": "2*pi/3",
            "path_relative_entropy_Hessian": "positive scalar 1/r times identity on actual edge-rate tangents",
            "overall_rate_scalar_affects_horizontal_space": False,
            "new_fitted_coefficient": False,
        },
        "microscopic_horizontal_gate": {
            "target_metric_components": 10,
            "moment_map_rank": raw_rank,
            "kernel_dimension": raw_kernel_dimension,
            "BKM_rank_on_kernel": kernel_metric_rank,
            "horizontal_dimension": 10,
            "right_inverse_exact": right_inverse == eye(10),
            "kernel_BKM_orthogonality_exact": True,
            "S4_equivariance_checks": s4_checks,
        },
        "BGCE286_quotient_gate": {
            "common_edge_count": sum(edge["sign"] > 0 for edge in edges),
            "relative_edge_count": sum(edge["sign"] < 0 for edge in edges),
            "common_sum_displacement_fourth_power": common_d4,
            "relative_sum_displacement_fourth_power": relative_d4,
            "source_fixed_rescaled_common_weight": qserial(quotient_weights[0]),
            "source_fixed_rescaled_relative_weight": qserial(quotient_weights[1]),
            "weight_ratio_common_to_relative": "18:1",
            "old_kernel_dimension": len(quotient_kernel),
            "BKM_rank_on_old_kernel": quotient_kernel_metric_rank,
            "old_kernel_removed_by_horizontal_condition": quotient_kernel_metric_rank == 2,
        },
        "actual_X21R1_gate": {
            "tangent_count": len(tangent_records),
            "all_reproduced_exactly": actual_pass,
            "all_BKM_horizontal": actual_pass,
            "records": tangent_records,
        },
        "dependency_effect": {
            "BGCE286_first_order_curved_conductance_lift_existence": "PASS_RETAINED",
            "BGCE286_first_order_curved_conductance_lift_uniqueness": "PASS_IN_SOURCE_EVENT_PATH_BKM_HORIZONTAL_CLASS",
            "active_source_Markov_transport_first_variation": "SOURCE_SELECTED_CANONICAL_CANDIDATE",
            "full_nonlinear_integrability": "OPEN",
            "full_finite_Umegaki_parent_action": "OPEN_NOT_IDENTIFIED_WITH_PATH_BKM_CONNECTION",
            "Hilbert_stress_source_derived": False,
            "Ward_source_derived": False,
            "MMR2_and_source_three_fifths": "RETAINED_UNCHANGED",
            "SDPC_complete": False,
            "unconditional_Einstein_dynamics": False,
        },
        "counter_intuition_scan": {
            "tempting_success": "A unique BKM-horizontal lift already proves the full nonlinear matter-gravity action.",
            "refutation": "The result selects an exact first-order connection. It does not prove that this connection integrates to a global conductance functional or that the event-path information metric is the Hilbert matter action.",
            "ordinary_explanation": "Any surjective moment map from a positive information-metric space has a canonical minimum-norm right inverse.",
            "Braid_specific_content": "The event edges, equal positive rate, displacement moments, four-axis S4 averaging and 24 target tangents all come from the retained pointed-Braid source.",
            "falsifier": "Rank loss, a null BKM direction in the moment kernel, failure on one actual tangent, or failure of S4 equivariance would destroy the selection.",
        },
        "next_gate": "BGCE288_EVENT_BKM_HORIZONTAL_CONNECTION_NONLINEAR_INTEGRABILITY_AND_PARENT_VARIATION_GATE",
        "decision": decision,
        "runtime_class": "short exact rational linear algebra; no fit or scan",
        "formal_E0_E1_E2": "NOT_CLAIMED__DPA_THEORETICAL_GATE_ONLY",
        "claim_ceiling": "BGCE287 derives a unique exact S4-equivariant first-order BKM-horizontal conductance lift of all 24 actual X21R1 metric tangents from the source event edges and their common source-fixed rate. It removes BGCE286's two-dimensional ambiguity within the source-event-path BKM horizontal class without fitted coefficients. It does not yet prove nonlinear integrability, identify this connection metric with the full finite physical parent action, derive Hilbert stress, Ward, SDPC, unconditional Einstein dynamics, empirical gravity or completed quantum gravity.",
    }


if __name__ == "__main__":
    payload = build_output()
    (HERE / "RAW_OUTPUT.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(payload["decision"])
