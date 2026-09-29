#!/usr/bin/env python3
"""BGCE283: exact S4 chart-equivariant metric/nonmetricity tensor gluing."""

from __future__ import annotations

from fractions import Fraction
from itertools import permutations
from pathlib import Path
from typing import Any
import hashlib
import json
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MATRIX = json.loads((HERE / "SOURCE_MATRIX.json").read_text())
REVISION = MATRIX["source_revision"]
CROSS_REVISION = MATRIX["cross_source_revision"]
X21 = "public-inputs/DISC-009/CP-HYP-033-X21R1/RAW_PACKET_OUTPUTS.json"
MASKS = (0, 5, 8, 13, 16, 21, 24, 29)
Q17 = tuple[Fraction, Fraction]
ZERO: Q17 = (Fraction(0), Fraction(0))
ONE: Q17 = (Fraction(1), Fraction(0))


def archived_bytes(revision: str, relative: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{revision}:{relative}"], cwd=ROOT)


def verify_sources() -> dict[str, str]:
    checked = {}
    for relative, expected in MATRIX["inputs_sha256"].items():
        data = archived_bytes(REVISION, relative)
        assert data == (ROOT / relative).read_bytes(), relative
        actual = hashlib.sha256(data).hexdigest()
        assert actual == expected, relative
        checked[f"{REVISION}:{relative}"] = actual
    for relative, expected in MATRIX["cross_source_inputs_sha256"].items():
        data = archived_bytes(CROSS_REVISION, relative)
        actual = hashlib.sha256(data).hexdigest()
        assert actual == expected, relative
        checked[f"{CROSS_REVISION}:{relative}"] = actual
    return checked


def mm(left, right):
    result = [[ZERO for _ in range(len(right[0]))] for _ in range(len(left))]
    for i in range(len(left)):
        for k in range(len(right)):
            if left[i][k] == ZERO:
                continue
            for j in range(len(right[0])):
                if right[k][j] != ZERO:
                    result[i][j] = qadd(result[i][j], qmul(left[i][k], right[k][j]))
    return result


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def qadd(left: Q17, right: Q17) -> Q17:
    return (left[0] + right[0], left[1] + right[1])


def qsub(left: Q17, right: Q17) -> Q17:
    return (left[0] - right[0], left[1] - right[1])


def qmul(left: Q17, right: Q17) -> Q17:
    return (
        left[0] * right[0] + 17 * left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def qinv(value: Q17) -> Q17:
    denominator = value[0] * value[0] - 17 * value[1] * value[1]
    if denominator == 0:
        raise ZeroDivisionError
    return (value[0] / denominator, -value[1] / denominator)


def qrank(matrix) -> int:
    work = [list(row) for row in matrix]
    rows = len(work)
    columns = len(work[0]) if rows else 0
    rank = 0
    for column in range(columns):
        pivot = next((row for row in range(rank, rows) if work[row][column] != ZERO), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = qinv(work[rank][column])
        work[rank] = [qmul(value, inverse) for value in work[rank]]
        for row in range(rows):
            if row == rank or work[row][column] == ZERO:
                continue
            factor = work[row][column]
            work[row] = [qsub(value, qmul(factor, base)) for value, base in zip(work[row], work[rank])]
        rank += 1
    return rank


def qmatrix_from_fraction(matrix):
    return [[(Fraction(value), Fraction(0)) for value in row] for row in matrix]


def parse_qmatrix(serial):
    return [[(Fraction(value[0]), Fraction(value[1])) for value in row] for row in serial]


def permutation_matrix(p):
    matrix = [[ZERO for _ in range(4)] for _ in range(4)]
    for source, target in enumerate(p):
        matrix[target][source] = ONE
    return matrix


def qmatrix_serial(matrix):
    return [[[str(value[0]), str(value[1])] for value in row] for row in matrix]


def signed_monomial(matrix) -> bool:
    allowed = {ZERO, ONE, (Fraction(-1), Fraction(0))}
    return (
        all(value in allowed for row in matrix for value in row)
        and all(sum(value != ZERO for value in row) == 1 for row in matrix)
        and all(sum(matrix[row][column] != ZERO for row in range(4)) == 1 for column in range(4))
    )


def square_action(matrix):
    return [[qmul(value, value) for value in row] for row in matrix]


def linear_combination(matrices, coefficients):
    result = [[ZERO for _ in range(4)] for _ in range(4)]
    for matrix, coefficient in zip(matrices, coefficients):
        for row in range(4):
            for column in range(4):
                result[row][column] = qadd(result[row][column], qmul(matrix[row][column], coefficient))
    return result


def transform_metric(change, metric):
    return mm(transpose(change), mm(metric, change))


def build_output() -> dict[str, Any]:
    checked = verify_sources()
    p = ROOT / "audits"
    bg282 = json.loads((p / "BGCE282_SOURCE_EVENT_CYLINDER_METRIC_CHAIN_RULE_GATE_20260923/RESULT.json").read_text())
    bg281 = json.loads((p / "BGCE281_ALL_SECTOR_ORDERED_EDGE_METRIC_TANGENT_AND_NONMETRICITY_GATE_20260923/RAW_OUTPUT.json").read_text())
    bg280 = json.loads((p / "BGCE280_ALL_SECTOR_CHARACTERISTIC_ZERO_ZERO_CONNECTION_LIFT_20260923/RESULT.json").read_text())
    bg268 = json.loads((p / "BGCE268_SOURCE_GRAM_SCHUR_CHANNEL_TO_CAUSAL_METRIC_INTERTWINER_GATE_20260922/RAW_OUTPUT.json").read_text())
    bg137 = json.loads((p / "BGCE137_DISCRETE_S4_CHART_TRANSITION_VERSUS_NEAR_IDENTITY_CARTAN_CONNECTION_FACTORING_GATE_20260919/RESULT.json").read_text())
    x21 = json.loads(archived_bytes(CROSS_REVISION, X21))
    assert bg282["source_event_cylinder_metric_chain_rule"] == "PASS"
    assert bg280["all_sector_all_theta_characteristic_zero_connection"] == "PASS"
    assert bg137["graded_Cartan_factorization"]["factor_to_ray_assignments"] == 24
    assert bg137["graded_Cartan_factorization"]["constant_chart_transition_derivative_term"] == "zero"

    u = qmatrix_from_fraction(bg268["source_typed_intertwiner"]["U"])
    identity = [[ONE if row == column else ZERO for column in range(4)] for row in range(4)]
    assert mm(u, transpose(u)) == identity
    ray_permutations = list(permutations(range(4)))
    atlas = []
    for permutation in ray_permutations:
        ray = permutation_matrix(permutation)
        carrier = mm(u, mm(ray, transpose(u)))
        label = square_action(carrier)
        assert signed_monomial(carrier)
        assert mm(transpose(carrier), carrier) == identity
        assert carrier[0][0] in (ONE, (Fraction(-1), Fraction(0)))
        assert all(carrier[0][column] == ZERO for column in range(1, 4))
        assert all(carrier[row][0] == ZERO for row in range(1, 4))
        assert label[0][0] == ONE
        atlas.append({"permutation": permutation, "ray": ray, "carrier": carrier, "label": label})

    def key(matrix):
        return tuple(value for row in matrix for value in row)

    ray_lookup = {key(item["ray"]): index for index, item in enumerate(atlas)}
    carrier_cocycle_checks = 0
    label_cocycle_checks = 0
    for left in atlas:
        for right in atlas:
            combined_ray = mm(left["ray"], right["ray"])
            combined = atlas[ray_lookup[key(combined_ray)]]
            assert mm(left["carrier"], right["carrier"]) == combined["carrier"]
            assert mm(left["label"], right["label"]) == combined["label"]
            carrier_cocycle_checks += 1
            label_cocycle_checks += 1

    carrier_image_size = len({key(item["carrier"]) for item in atlas})
    label_image_size = len({key(item["label"]) for item in atlas})
    label_kernel_size = sum(item["label"] == identity for item in atlas)

    gram_by_mask = {
        int(item["mask"]): qmatrix_from_fraction(item["ordered_edge_gram"])
        for item in x21["carrier_records"]
    }
    tangent_by_mask = {
        int(item["mask"]): [parse_qmatrix(direction["ordered_Gram_tangent"]) for direction in item["direction_records"]]
        for item in bg281["sector_records"]
    }

    metric_packets = 0
    tangent_packets = 0
    overlap_pair_packets = 0
    sector_records = []
    for mask in MASKS:
        gram = gram_by_mask[mask]
        tangents = tangent_by_mask[mask]
        sector_metric = 0
        sector_tangent = 0
        for chart in atlas:
            c = chart["carrier"]
            s = chart["label"]
            ray = chart["ray"]
            chart_gram = transform_metric(c, gram)
            ray_gram = transform_metric(u, gram)
            chart_ray_gram = transform_metric(u, chart_gram)
            expected_ray_gram = transform_metric(ray, ray_gram)
            assert chart_ray_gram == expected_ray_gram
            sector_metric += 1
            metric_packets += 1
            for local_direction in range(3):
                coefficients = [s[index + 1][local_direction + 1] for index in range(3)]
                chart_tangent = transform_metric(c, linear_combination(tangents, coefficients))
                ray_tangent = transform_metric(u, linear_combination(tangents, coefficients))
                chart_ray_tangent = transform_metric(u, chart_tangent)
                expected_ray_tangent = transform_metric(ray, ray_tangent)
                assert chart_ray_tangent == expected_ray_tangent
                assert chart_tangent == transpose(chart_tangent)
                assert qrank(chart_tangent) == 2
                sector_tangent += 1
                tangent_packets += 1

        # Verify double-overlap composition on the full tangent packet.
        for left in atlas:
            for right in atlas:
                combined = atlas[ray_lookup[key(mm(left["ray"], right["ray"]))]]
                for local_direction in range(3):
                    combined_coefficients = [combined["label"][i + 1][local_direction + 1] for i in range(3)]
                    direct = transform_metric(combined["carrier"], linear_combination(tangents, combined_coefficients))
                    # Apply the left transition first and then the right one;
                    # this must equal the matrix product left*right used above.
                    left_packet = []
                    for direction in range(3):
                        coefficients = [left["label"][i + 1][direction + 1] for i in range(3)]
                        left_packet.append(transform_metric(left["carrier"], linear_combination(tangents, coefficients)))
                    right_coefficients = [right["label"][i + 1][local_direction + 1] for i in range(3)]
                    sequential = transform_metric(right["carrier"], linear_combination(left_packet, right_coefficients))
                    assert sequential == direct
                    overlap_pair_packets += 1
                    assert sequential == transpose(sequential)

        sector_records.append({
            "mask": mask,
            "metric_chart_covariance_packets": sector_metric,
            "tangent_and_nonmetricity_chart_covariance_packets": sector_tangent,
            "double_overlap_tangent_cocycle_packets": 24 * 24 * 3,
            "all_chart_tangents_symmetric_rank_two": True,
            "constant_transition_keeps_zero_connection": True,
            "nonmetricity_equals_transformed_metric_tangent": True,
        })

    full_pass = all([
        carrier_image_size == 24,
        label_image_size == 6,
        label_kernel_size == 4,
        carrier_cocycle_checks == label_cocycle_checks == 576,
        metric_packets == 192,
        tangent_packets == 576,
        overlap_pair_packets == 8 * 24 * 24 * 3,
    ])
    decision = (
        "PASS_THE_SOURCE_FIXED_HADAMARD_INTERTWINER_TRANSPORTS_ALL_TWENTY_FOUR_S4_RAY_CHARTS_TO_EXACT_CLOCK_FIXED_SIGNED_MONOMIAL_CARRIER_TRANSITIONS__"
        "THE_PROJECTOR_LABEL_ACTION_HAS_SIX_ELEMENT_SPATIAL_S3_IMAGE_AND_FOUR_ELEMENT_KERNEL_WITH_ALL_FIVE_HUNDRED_SEVENTY_SIX_COCYCLES_EXACT__"
        "ALL_ONE_HUNDRED_NINETY_TWO_METRIC_AND_FIVE_HUNDRED_SEVENTY_SIX_TANGENT_NONMETRICITY_CHART_PACKETS_OBEY_EXACT_CHARACTER_AND_RAY_TENSOR_COVARIANCE__"
        "ALL_DOUBLE_OVERLAPS_COMPOSE_EXACTLY_AND_CONSTANT_TRANSITIONS_KEEP_THE_BGCE280_CONNECTION_ZERO__"
        "THE_CONTINUOUS_FIRST_ORDER_METRIC_NONMETRICITY_FIELD_THEREFORE_GLUES_AS_AN_S4_EQUIVARIANT_TENSOR_ON_THE_SOURCE_OPERATIONAL_EVENT_ATLAS__"
        "ARBITRARY_DIFFEO_NATURAL_SPACETIME_VALIDATION_MU_TANGENT_STRESS_WARD_AND_EINSTEIN_REMAIN_OPEN"
        if full_pass else
        "FAIL_THE_BGCE282_FIXED_CHART_METRIC_RESPONSE_DOES_NOT_GLUE_AS_AN_S4_EQUIVARIANT_SOURCE_EVENT_TENSOR"
    )

    return {
        "schema": "siel.public-calculation.bgce283.raw.v1",
        "candidate_id": "BGCE283",
        "source_revision": REVISION,
        "cross_source_revision": CROSS_REVISION,
        "input_hashes_verified": checked,
        "baseline_gate": "PASS_REVISION_MATCHED_BGCE137_268_280_281_282_AND_X21R1_EXACT_MATRIX_REPLAY",
        "endpoint_provenance": "NOT_ISSUED_BY_PUBLIC__THEORETICAL_EXACT_FINITE_ATLAS_COCYCLE_AUDIT_ONLY",
        "primary_evidence_status": "Theoretical derivation with exact finite-group cocycle and tensor-overlap identities",
        "scientific_layer": "S4-equivariant first-order metric/nonmetricity tensor gluing on the source operational event atlas",
        "atlas_representation": {
            "ray_chart_count": len(atlas),
            "carrier_transition_definition": "C_pi=U P_pi U^T",
            "all_carrier_transitions_clock_fixed_signed_monomial_orthogonal": True,
            "carrier_image_size": carrier_image_size,
            "projector_label_action_definition": "S_pi=C_pi entrywise-square",
            "label_image_size": label_image_size,
            "label_kernel_size": label_kernel_size,
            "label_image": "S3 permutations of the three spatial theta/projector directions",
            "carrier_cocycle_checks": carrier_cocycle_checks,
            "label_cocycle_checks": label_cocycle_checks,
            "constant_overlap_transition_derivative": "zero",
        },
        "sector_records": sector_records,
        "summary": {
            "sector_count": len(sector_records),
            "metric_chart_covariance_packets": metric_packets,
            "tangent_nonmetricity_chart_covariance_packets": tangent_packets,
            "double_overlap_tangent_cocycle_packets": overlap_pair_packets,
            "all_chart_tangents_symmetric_exact_rank_two": full_pass,
            "all_connections_remain_exact_zero": full_pass,
            "source_event_atlas_tensor_gluing": full_pass,
        },
        "dependency_effect": {
            "BGCE282_fixed_chart_chain_rule_retained": True,
            "S4_chart_independent_metric_tensor_bundle_on_source_event_atlas": full_pass,
            "S4_chart_independent_nonmetricity_tensor_bundle_on_source_event_atlas": full_pass,
            "continuous_first_order_source_event_tensor_field": full_pass,
            "arbitrary_smooth_diffeomorphism_covariance": False,
            "empirical_natural_spacetime_identification_and_calibration": False,
            "mu_direction_X21R1_metric_tangent": False,
            "Hilbert_stress": False,
            "Ward_identity": False,
            "Einstein_dynamics": False,
            "fixed_event_conditioned_MMR2": "RETAINED",
            "source_three_fifths": "RETAINED_NOT_USED",
        },
        "counter_intuition_scan": {
            "tempting_failure": "The Hadamard carrier match fixes only one clock projector and does not transport the full atlas or metric response.",
            "refutation": "All 24 transported chart matrices, both finite-group representations, every sector metric, every theta tangent/nonmetricity and all double overlaps are checked exactly.",
            "ordinary_explanation": "A constant finite-group atlas and a representation define an associated tensor bundle; the project-specific content is that the atlas, Hadamard solder, metrics and nonmetricities are all pinned outputs of the same Braid lineage.",
            "tempting_overclaim": "S4 atlas covariance already proves arbitrary diffeomorphism covariance and natural spacetime validity.",
            "overclaim_refutation": "Only the source-derived finite chart atlas and declared smooth completion are covered; arbitrary smooth coordinate changes and empirical calibration remain untested.",
            "strongest_falsifier": "Failure to extend the S4 overlap law to the open local GL4/diffeomorphism domain needed by the variational stress and Ward identity.",
        },
        "next_gate": "BGCE284_LOCAL_GL4_NATURALITY_AND_VARIATIONAL_STRESS_WARD_GATE",
        "decision": decision,
        "runtime_class": "SHORT_EXACT_FINITE_GROUP_TENSOR_GLUE_GATE",
        "formal_E0_E1_E2": "NOT_CLAIMED__THEORETICAL_EXACT_FINITE_ATLAS_AUDIT_ONLY",
        "claim_ceiling": "BGCE283 tests exact S4-atlas overlap and cocycle gluing for the committed X21R1 metric, BGCE281 theta tangents and BGCE280 zero-connection nonmetricity. A PASS proves a continuous first-order S4-equivariant tensor field on the source-derived operational event atlas. It does not prove arbitrary smooth diffeomorphism covariance, empirical identification/calibration with natural spacetime, the mu metric tangent, Hilbert stress, Ward conservation, Einstein dynamics or empirical quantum gravity.",
    }


def main() -> None:
    output = build_output()
    (HERE / "RAW_OUTPUT.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    print(output["decision"])


if __name__ == "__main__":
    main()
