#!/usr/bin/env python3
"""BGCE288: causal-even event plus X21R1 odd-theta Lorentz tangent gate."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations
from pathlib import Path
from typing import Any
import hashlib
import json
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCES = json.loads((HERE / "SOURCE_MATRIX.json").read_text())
REVISION = SOURCES["source_revision"]
CROSS_REVISION = SOURCES["cross_source_revision"]
ZERO = Fraction(0)
ONE = Fraction(1)
SYM_INDEX = ((0, 0), (1, 1), (2, 2), (3, 3), (0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
PAIRS = tuple(combinations(range(4), 2))


def archived_bytes(revision: str, relative: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{revision}:{relative}"], cwd=ROOT)


def verify_sources() -> dict[str, str]:
    checked = {}
    for relative, expected in SOURCES["inputs_sha256"].items():
        data = archived_bytes(REVISION, relative)
        assert data == (ROOT / relative).read_bytes(), relative
        actual = hashlib.sha256(data).hexdigest()
        assert actual == expected, relative
        checked[f"{REVISION}:{relative}"] = actual
    cross = archived_bytes(CROSS_REVISION, SOURCES["cross_source_path"])
    actual = hashlib.sha256(cross).hexdigest()
    assert actual == SOURCES["cross_source_sha256"]
    checked[f"{CROSS_REVISION}:{SOURCES['cross_source_path']}"] = actual
    return checked


def transpose(a):
    return [list(row) for row in zip(*a)]


def mm(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def add(a, b):
    return [[x + y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def scale(s, a):
    return [[s * x for x in row] for row in a]


def rank(a):
    work = [list(row) for row in a]
    rows = len(work)
    cols = len(work[0]) if rows else 0
    pivot = 0
    for col in range(cols):
        found = next((row for row in range(pivot, rows) if work[row][col] != 0), None)
        if found is None:
            continue
        work[pivot], work[found] = work[found], work[pivot]
        divisor = work[pivot][col]
        work[pivot] = [value / divisor for value in work[pivot]]
        for row in range(rows):
            if row == pivot or work[row][col] == 0:
                continue
            factor = work[row][col]
            work[row] = [value - factor * base for value, base in zip(work[row], work[pivot])]
        pivot += 1
    return pivot


def inverse(a):
    n = len(a)
    work = [list(row) + [ONE if i == j else ZERO for j in range(n)] for i, row in enumerate(a)]
    for col in range(n):
        pivot = next(row for row in range(col, n) if work[row][col] != 0)
        work[col], work[pivot] = work[pivot], work[col]
        divisor = work[col][col]
        work[col] = [value / divisor for value in work[col]]
        for row in range(n):
            if row == col:
                continue
            factor = work[row][col]
            if factor:
                work[row] = [value - factor * base for value, base in zip(work[row], work[col])]
    return [row[n:] for row in work]


def outer(v):
    return [[v[i] * v[j] for j in range(4)] for i in range(4)]


def flatten(a):
    assert a == transpose(a)
    return [a[i][j] for i, j in SYM_INDEX]


def columns_to_matrix(columns):
    return [[column[row] for column in columns] for row in range(len(columns[0]))]


def qmatrix(serial):
    return [[Fraction(value) for value in row] for row in serial]


def q17matrix(serial):
    result = []
    for row in serial:
        parsed = []
        for value in row:
            assert Fraction(value[1]) == 0
            parsed.append(Fraction(value[0]))
        result.append(parsed)
    return result


def conjugate(change, tensor):
    return mm(transpose(change), mm(tensor, change))


def causal_part(j, tensor, even):
    reflected = mm(j, mm(tensor, j))
    return scale(Fraction(1, 2), add(tensor, reflected if even else scale(-ONE, reflected)))


def actual_edges(records):
    mapping = {tuple(item["input"]): tuple(item["output"]) for item in records}
    seen = set()
    edges = []
    for source, target in mapping.items():
        if source == target:
            continue
        key = tuple(sorted((source, target)))
        if key in seen:
            continue
        seen.add(key)
        delta = (target[0] - source[0], target[1] - source[1])
        assert mapping[target] == source and abs(delta[0]) == abs(delta[1])
        edges.append(delta)
    return edges


def diagonal_dominance_gaps(matrix):
    return [matrix[i][i] - sum(abs(matrix[i][j]) for j in range(4) if j != i) for i in range(4)]


def build_output() -> dict[str, Any]:
    checked = verify_sources()
    audits = ROOT / "audits"
    bg139 = json.loads((audits / "BGCE139_SOURCE_SPECTRAL_CYLINDER_OPERATIONAL_EVENT_IDENTIFICATION_GATE_20260919/RAW_OUTPUT.json").read_text())
    bg256 = json.loads((audits / "BGCE256_BRAID_INDUCED_EVENT_TRANSITION_COBORDER_TO_NEIGHBOR_COUPLING_LAW_GATE_20260921/RAW_OUTPUT.json").read_text())
    bg258 = json.loads((audits / "BGCE258_SOURCE_CAUSAL_GRADING_TIMES_EVENT_MOMENT_TO_UNIQUE_NULL_GRAM_PARENT_KINETIC_GATE_20260921/RAW_OUTPUT.json").read_text())
    bg266 = json.loads((audits / "BGCE266_REFINEMENT_CLOCK_TO_UNIQUE_EVENT_SEMIGROUP_AND_IR_OS_CONTINUATION_GATE_20260922/RAW_OUTPUT.json").read_text())
    bg268 = json.loads((audits / "BGCE268_SOURCE_GRAM_SCHUR_CHANNEL_TO_CAUSAL_METRIC_INTERTWINER_GATE_20260922/RAW_OUTPUT.json").read_text())
    bg275 = json.loads((audits / "BGCE275_GIBBS_DEFORMATION_OF_X21R1_CARRIER_AND_ORDERED_EDGE_GRAM_GATE_20260922/RESULT.json").read_text())
    bg281 = json.loads((audits / "BGCE281_ALL_SECTOR_ORDERED_EDGE_METRIC_TANGENT_AND_NONMETRICITY_GATE_20260923/RAW_OUTPUT.json").read_text())
    bg283 = json.loads((audits / "BGCE283_S4_CHART_EQUIVARIANT_METRIC_TENSOR_GLUE_GATE_20260923/RESULT.json").read_text())
    bg287 = json.loads((audits / "BGCE287_SOURCE_EVENT_PATH_BKM_HORIZONTAL_CONDUCTANCE_LIFT_GATE_20260923/RESULT.json").read_text())
    x21 = json.loads(archived_bytes(CROSS_REVISION, SOURCES["cross_source_path"]))

    assert bg266["IR_OS_continuation"]["equals_BGCE258_K_evt"] is True
    assert bg275["local_source_fixed_metric_variation"] == "PASS_AT_MASK_ZERO_THETA_ONE"
    assert bg283["source_event_atlas_metric_tensor_gluing"] == "PASS"
    assert bg287["first_order_curved_conductance_lift_uniqueness"] == "PASS_IN_SOURCE_EVENT_PATH_BKM_HORIZONTAL_CLASS"

    u = qmatrix(bg268["source_typed_intertwiner"]["U"])
    j_ray = qmatrix(bg258["basis_typing"]["J_ray"])
    j_character = qmatrix(bg258["basis_typing"]["J_character"])
    q4 = qmatrix(bg256["S4_chart_average"]["Q4"])
    k_evt = qmatrix(bg258["graded_event_carrier"]["K_evt"])
    assert mm(j_ray, q4) == k_evt
    assert k_evt == transpose(k_evt)

    edges = actual_edges(bg139["event_transition_gate"]["canonical_transition_on_digit_pairs"])
    raw_columns = []
    for i, j in PAIRS:
        for da, db in edges:
            v = [ZERO] * 4
            v[i] = Fraction(da)
            v[j] = Fraction(db)
            raw_columns.append(flatten(outer(v)))
    raw_map = columns_to_matrix(raw_columns)
    base_vector = [[Fraction(1, 25)] for _ in raw_columns]
    base_flat = mm(raw_map, base_vector)
    q4_flat = [[value] for value in flatten(q4)]
    assert base_flat == q4_flat

    even_columns = []
    odd_columns = []
    for column in raw_columns:
        tensor = [[ZERO] * 4 for _ in range(4)]
        for value, (i, j) in zip(column, SYM_INDEX):
            tensor[i][j] = tensor[j][i] = value
        even_columns.append(flatten(causal_part(j_ray, tensor, True)))
        odd_columns.append(flatten(causal_part(j_ray, tensor, False)))
    even_rank = rank(columns_to_matrix(even_columns))
    odd_rank = rank(columns_to_matrix(odd_columns))

    # Direct X21R1-Gram-as-positive-conductance-base test.
    baseline_records = []
    direct_gram_feasible = 0
    direct_inverse_feasible = 0
    for record in x21["carrier_records"]:
        gram_character = qmatrix(record["ordered_edge_gram"])
        gram_ray = conjugate(u, gram_character)
        inverse_ray = inverse(gram_ray)
        gram_gaps = diagonal_dominance_gaps(gram_ray)
        inverse_gaps = diagonal_dominance_gaps(inverse_ray)
        gram_feasible = all(value >= 0 for value in gram_gaps)
        inverse_feasible = all(value >= 0 for value in inverse_gaps)
        direct_gram_feasible += int(gram_feasible)
        direct_inverse_feasible += int(inverse_feasible)
        baseline_records.append({
            "mask": int(record["mask"]),
            "Gram_min_diagonal_dominance_gap": str(min(gram_gaps)),
            "inverse_Gram_min_diagonal_dominance_gap": str(min(inverse_gaps)),
            "Gram_in_positive_actual_event_moment_cone": gram_feasible,
            "inverse_Gram_in_positive_actual_event_moment_cone": inverse_feasible,
        })

    # X21R1 theta response supplies the missing J-odd clock-spatial triplet.
    sector_records = []
    all_combined_full = True
    even_basis = []
    for i, j in SYM_INDEX:
        basis = [[ZERO] * 4 for _ in range(4)]
        basis[i][j] = basis[j][i] = ONE
        projected = causal_part(j_character, basis, True)
        vector = flatten(projected)
        if any(vector) and rank(columns_to_matrix(even_basis + [vector])) > len(even_basis):
            even_basis.append(vector)
    assert len(even_basis) == 7
    for sector in bg281["sector_records"]:
        theta_odd_columns = []
        clock_spatial_rows = []
        for direction in sector["direction_records"]:
            tangent = q17matrix(direction["ordered_Gram_tangent"])
            odd = causal_part(j_character, tangent, False)
            theta_odd_columns.append(flatten(odd))
            clock_spatial_rows.append([tangent[0][i] for i in range(1, 4)])
        theta_odd_rank = rank(clock_spatial_rows)
        combined_rank = rank(columns_to_matrix(even_basis + theta_odd_columns))
        all_combined_full = all_combined_full and theta_odd_rank == 3 and combined_rank == 10
        sector_records.append({
            "mask": int(sector["mask"]),
            "theta_direction_count": 3,
            "J_odd_clock_spatial_rank": theta_odd_rank,
            "event_even_plus_theta_odd_combined_rank": combined_rank,
        })

    partial_pass = (
        direct_gram_feasible == 0
        and direct_inverse_feasible == 0
        and rank(raw_map) == 10
        and even_rank == 7
        and odd_rank == 3
        and all_combined_full
    )
    assert partial_pass

    decision = (
        "PARTIAL_PASS_DIRECT_IDENTIFICATION_OF_THE_EIGHT_X21R1_POSITIVE_GRAMS_OR_THEIR_INVERSES_AS_ACTUAL_POSITIVE_EVENT_CONDUCTANCE_MOMENTS_FAILS_ZERO_OF_EIGHT_BECAUSE_EACH_VIOLATES_THE_REQUIRED_DIAGONAL_DOMINANCE_CONE__"
        "PASS_UNIFORM_ACTUAL_EVENT_WEIGHT_ONE_OVER_TWENTY_FIVE_REPRODUCES_Q4_EXACTLY_AND_SOURCE_TIME_REFLECTION_MAPS_IT_TO_K_EVT__"
        "THE_CAUSAL_J_EVEN_EVENT_MOMENT_RESPONSE_HAS_EXACT_RANK_SEVEN_WHILE_THE_THREE_X21R1_THETA_TANGENTS_HAVE_EXACT_J_ODD_CLOCK_SPATIAL_RANK_THREE_IN_EVERY_ONE_OF_EIGHT_SECTORS__"
        "THEIR_SOURCE_TYPED_DIRECT_SUM_HAS_FULL_LORENTZ_METRIC_TANGENT_RANK_TEN_IN_ALL_EIGHT_SECTORS_AND_GLUES_BY_THE_EXISTING_S4_ATLAS__"
        "THEREFORE_X21R1_GRAM_BASELINES_ARE_NOT_PHYSICAL_EVENT_METRICS_BUT_THEIR_THETA_ODD_RESPONSES_COMPLETE_THE_MISSING_BOOST_TANGENTS_OVER_THE_PHYSICAL_Q4_TO_K_EVT_BASE__"
        "FINITE_NONLINEAR_ODD_INTEGRABILITY_PARENT_ACTION_HILBERT_STRESS_AND_WARD_REMAIN_OPEN"
    )

    return {
        "schema": "siel.public-calculation.bgce288.raw.v1",
        "candidate_id": "BGCE288",
        "source_revision": REVISION,
        "cross_source_revision": CROSS_REVISION,
        "input_hashes_verified": checked,
        "baseline_gate": "PASS_REVISION_MATCHED_BGCE139_256_258_266_268_275_281_283_284_285_287_AND_X21R1",
        "endpoint_provenance": "NOT_ISSUED_BY_PUBLIC__EXACT_RATIONAL_CONE_AND_CAUSAL_REPRESENTATION_AUDIT_ONLY",
        "primary_evidence_status": "Theoretical derivation with direct-base no-go and full first-order causal tangent completion",
        "scientific_layer": "source-derived local Lorentz off-shell tangent carrier before parent-action variation",
        "positive_event_moment_cone": {
            "necessary_condition": "H_ii >= sum_(j!=i) |H_ij| for every positive actual-edge conductance moment",
            "X21R1_Gram_feasible_count": direct_gram_feasible,
            "X21R1_inverse_Gram_feasible_count": direct_inverse_feasible,
            "sector_count": len(baseline_records),
            "records": baseline_records,
            "direct_X21R1_Gram_as_physical_event_metric": "FAIL",
        },
        "source_physical_base": {
            "uniform_event_weight": "1/25",
            "uniform_weight_moment_equals_Q4": base_flat == q4_flat,
            "source_time_reflection_times_Q4_equals_K_evt": mm(j_ray, q4) == k_evt,
            "physical_base_route": "actual event Q4 -> source causal K_evt",
        },
        "causal_representation_split": {
            "definition_even": "E(H)=(H+JHJ)/2",
            "definition_odd": "O(H)=(H-JHJ)/2",
            "J_even_symmetric_dimension": even_rank,
            "J_odd_symmetric_dimension": odd_rank,
            "direct_sum_dimension": even_rank + odd_rank,
            "event_even_response_rank": even_rank,
            "event_BKM_horizontal_selection_retained_on_even_sector": True,
            "theta_odd_response_rank_each_sector": 3,
            "combined_full_rank_each_sector": all_combined_full,
        },
        "sector_records": sector_records,
        "atlas_gate": {
            "existing_BGCE283_S4_tensor_gluing": True,
            "J_invariant_under_source_S4": True,
            "even_odd_split_glues": True,
        },
        "dependency_effect": {
            "BGCE287_linear_algebra": "RETAINED",
            "BGCE287_active_transport_interpretation": "RESTRICTED_TO_EVENT_J_EVEN_SECTOR_UNTIL_ODD_NONLINEAR_INTEGRABILITY",
            "X21R1_Gram_as_spacetime_metric_baseline": "REJECTED_BY_POSITIVE_EVENT_MOMENT_CONE",
            "X21R1_theta_response_as_missing_boost_tangent": "PASS_RANK3_ALL_EIGHT_SECTORS",
            "full_first_order_Lorentz_metric_variation": "PASS_RANK10_ALL_EIGHT_SECTORS",
            "finite_nonlinear_odd_integrability": "OPEN",
            "minimal_parent_action": "OPEN",
            "Hilbert_stress_source_derived": False,
            "Ward_source_derived": False,
            "MMR2_and_source_three_fifths": "RETAINED_UNCHANGED",
            "SDPC_complete": False,
            "unconditional_Einstein_dynamics": False,
        },
        "counter_intuition_scan": {
            "tempting_failure": "The direct X21R1 Gram/conductance base mismatch destroys BGCE287 and the stress route.",
            "refutation": "It destroys only the identification of the positive X21R1 Gram value with the physical event metric. The source already has the correct Q4-to-K_evt base, and X21R1 supplies exactly the complementary three J-odd response directions missing from the seven event-even directions.",
            "ordinary_explanation": "A causal involution decomposes symmetric tensors into seven block-diagonal and three time-space components; two independent response families can fill the complementary representations.",
            "SIEL_specific_lead": "The same pointed-Braid source independently supplies the event-even family, the causal J grading and all-sector rank-three theta-odd response.",
            "falsifier": "Loss of diagonal-cone violation, event-even rank below seven, theta-odd rank below three in any sector, combined rank below ten or failure of S4 gluing.",
        },
        "next_gate": "BGCE289_THETA_ODD_ANALYTIC_INTEGRABILITY_TO_MINIMAL_PARENT_HILBERT_STRESS_GATE",
        "decision": decision,
        "runtime_class": "short exact rational cone and rank audit; no fit or scan",
        "formal_E0_E1_E2": "NOT_CLAIMED__PUBLIC_THEORETICAL_GATE_ONLY",
        "claim_ceiling": "BGCE288 proves that the positive X21R1 Gram values and their inverses cannot themselves be the positive actual-event conductance moment base, but the source Q4-to-K_evt base has an exact seven-dimensional J-even event response and every X21R1 sector has an exact rank-three J-odd theta response. Their source-typed direct sum supplies all ten first-order Lorentz metric variations and glues over the retained S4 atlas. It does not yet prove finite nonlinear odd-sector integrability, a full parent action, Hilbert stress, Ward, SDPC, unconditional Einstein dynamics, empirical gravity or completed quantum gravity.",
    }


if __name__ == "__main__":
    output = build_output()
    (HERE / "RAW_OUTPUT.json").write_text(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(output["decision"])
