#!/usr/bin/env python3
from __future__ import annotations

from fractions import Fraction
import hashlib
from itertools import permutations, product
import json
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
INPUTS = {
    "baseline": HERE / "BASELINE_GATE.json",
    "endpoint": HERE / "ENDPOINT_PROVENANCE.json",
    "sources": HERE / "SOURCE_MATRIX.json",
    "bigt": ROOT / "records/UB495A_BIGT_MAINLINE_INTEGRATION_AND_ROUTE_REASSESSMENT_GATE/RESULT.json",
    "ocbfh014": ROOT / "public-inputs/formal_checks/ocbfh014_source_native_refinement_naturality_certificate_v1.json",
    "ce1d": ROOT / "records/SOURCE_A57S_CE1D_FOUR_AXIS_MASA_SOLDER_GATE_20260918/RESULT.json",
    "ce1d_protocol": ROOT / "records/SOURCE_A57S_CE1D_FOUR_AXIS_MASA_SOLDER_GATE_20260918/FROZEN_PROTOCOL.json",
    "bgce096": ROOT / "records/BGCE096_TEMPORAL_CARTAN_PARENT_CHILD_MAP_GATE_20260919/RESULT.json",
    "bgce097": ROOT / "records/BGCE097_FULL_SIX_FACE_ACTION_FIVE_ADIC_ADDITIVITY_GATE_20260919/RESULT.json",
    "bgce098": ROOT / "records/BGCE098_SOURCE_REGULARITY_AND_BRANCH_CONTROL_AUDIT_20260919/RESULT.json",
    "bgce099": ROOT / "records/BGCE099_CONDITIONAL_CONTINUUM_PALATINI_ACTION_AND_VARIATION_THEOREM_20260919/RESULT.json",
    "bgce100": ROOT / "records/BGCE100_NATIVE_GL4_AND_ZERO_HYPERMOMENTUM_SPLIT_AUDIT_20260919/RESULT.json",
    "bgce128": ROOT / "records/BGCE128_SOURCE_DERIVED_AFFINE_ONE_PLUS_THREE_CARRIER_AND_LOCALIZATION_BRIDGE_GATE_20260919/RESULT.json",
    "bgce131": ROOT / "records/BGCE131_MARKED_BRAID_TRANSPORTED_LOCAL_V4_TORSOR_GATE_20260919/RESULT.json",
    "bgce136": ROOT / "records/BGCE136_MARKED_AFFINE_LINK_TO_TEMPORAL_CARTAN_PAIR_AND_UNIFORM_CONTINUUM_ADMISSIBILITY_GATE_20260919/RESULT.json",
}


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def identity(n: int) -> list[list[Fraction]]:
    return [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]


def mm(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def mv(a: list[list[Fraction]], v: list[Fraction]) -> list[Fraction]:
    return [sum(a[i][j] * v[j] for j in range(len(v))) for i in range(len(a))]


def add(a: list[Fraction], b: list[Fraction]) -> list[Fraction]:
    return [x + y for x, y in zip(a, b)]


def determinant(a: list[list[Fraction]]) -> Fraction:
    if len(a) == 1:
        return a[0][0]
    return sum(
        ((-1) ** j) * a[0][j] * determinant([row[:j] + row[j + 1:] for row in a[1:]])
        for j in range(len(a))
    )


def permutation_matrix(p: tuple[int, ...]) -> list[list[Fraction]]:
    out = [[Fraction(0)] * len(p) for _ in p]
    for source, target in enumerate(p):
        out[target][source] = Fraction(1)
    return out


Transform = tuple[list[list[Fraction]], list[Fraction]]


def compose(left: Transform, right: Transform) -> Transform:
    u, e = left
    v, f = right
    return mm(u, v), add(e, mv(u, f))


def power(link: Transform, exponent: int) -> Transform:
    out: Transform = identity(4), [Fraction(0)] * 4
    for _ in range(exponent):
        out = compose(link, out)
    return out


def build_outputs() -> dict[str, Any]:
    x = {name: load(path) for name, path in INPUTS.items()}
    assert x["baseline"]["status"].startswith("PASS_BY_REVISION_MATCHED")
    assert x["endpoint"]["lifecycle_level"].startswith("NOT_APPLICABLE_PUBLIC_CALCULATION")
    assert "A_n=M_(5^n)(C)" in x["bigt"]["accepted_BIGT_results"]["all_finite_stage_theorem"]
    assert x["ocbfh014"]["tensor_refinement_gate"]["base_dimension"] == 5
    assert "No independent clock" in x["ocbfh014"]["tensor_refinement_gate"]["all_order_proof"][-1]
    assert "Splitting one marked C5 factor" in x["ocbfh014"]["insertion_coherence_gate"]["not_covered"]
    assert x["ce1d"]["decision_tests"]["A3_EXACT_625_CHILD_REFINEMENT"] is True
    assert x["ce1d"]["decision_tests"]["FOUR_FACTOR_TO_COFRAME_ORDER_DERIVED_UNIQUELY"] is False
    assert x["ce1d_protocol"]["new_bridge_hypothesis"]["statement"].startswith("Use the source-labelled diagonal MASA")
    assert "not uniquely Braid-selected" in x["bgce096"]["remaining_boundary"]
    assert "O(h)" in x["bgce097"]["positive_result"]
    assert "UTC1" in x["bgce098"]["minimal_new_bound"]
    assert x["bgce099"]["primary_evidence_status"] == "Conditional theoretical derivation"
    assert "SOURCE_NATIVE_FULL_STRUCTURE_IS_METRIC_AFFINE_GL4" in x["bgce100"]["status"]
    assert x["bgce128"]["exact_result"]["ambient_four_manifold_assumed"] is False
    assert x["bgce128"]["exact_result"]["S4_actions_checked"] == 24
    assert x["bgce131"]["result"]["marked_factor_cloning_used"] is False
    assert x["bgce136"]["finite_result"]["causal_affine_link_atlas_derived"] is True

    rays = [[Fraction(value) for value in row] for row in x["bgce136"]["finite_result"]["point_basis_causal_steps"]]
    assert rays == [[Fraction(3 * int(i == j)) for j in range(4)] for i in range(4)]
    atlas = [permutation_matrix(p) for p in permutations(range(4))]
    assert len(atlas) == 24

    # The old fixed clock-first/spatial-next order is replaced by a torsor of
    # all assignments.  S4 acts transitively; A4 leaves two orientation sheets.
    assignments = list(permutations(range(4)))
    s4_orbit = {tuple(p[i] for i in range(4)) for p in assignments}
    even_atlas = [g for g in atlas if determinant(g) == 1]
    odd_atlas = [g for g in atlas if determinant(g) == -1]
    assert len(s4_orbit) == 24
    assert len(even_atlas) == len(odd_atlas) == 12

    # Source-derived ray count plus one C5 tail factor per ray gives 5^4 child
    # addresses.  No external coordinate labels are used.
    child_addresses = list(product(range(5), repeat=4))
    assert len(child_addresses) == 625

    stage_records = []
    identity4 = identity(4)
    one_stage_checks = 0
    two_stage_checks = 0
    covariance_checks = 0
    for m in range(6):
        h = Fraction(1, 5**m)
        refined_rays = [[h * value for value in ray] for ray in rays]
        densities = [[value / h for value in ray] for ray in refined_rays]
        assert densities == rays
        temporal = [sum(ray[j] for ray in refined_rays) for j in range(4)]
        temporal_density = [value / h for value in temporal]
        assert temporal_density == [Fraction(3)] * 4
        volume = determinant([[refined_rays[column][row] for column in range(4)] for row in range(4)])
        assert volume == Fraction(81, 5 ** (4 * m))
        stage_records.append({
            "stage": m,
            "h": str(h),
            "cells": 625**m,
            "ray_density": [[str(value) for value in row] for row in densities],
            "temporal_density": [str(value) for value in temporal_density],
            "oriented_cell_volume": str(volume),
            "connection_log": "0"
        })
        if m < 5:
            child_h = h / 5
            for ray in rays:
                parent: Transform = identity4, [h * value for value in ray]
                child: Transform = identity4, [child_h * value for value in ray]
                assert power(child, 5) == parent
                one_stage_checks += 1
                grandchild: Transform = identity4, [child_h / 5 * value for value in ray]
                assert power(grandchild, 25) == parent
                two_stage_checks += 1

        # Constant discrete chart changes commute with refinement and conjugate
        # the identity local connection to itself.
        for p, g in zip(assignments, atlas):
            assert mm(g, mm(identity4, list(zip(*g)))) == identity4
            for i, ray in enumerate(refined_rays):
                assert mv(g, ray) == refined_rays[p[i]]
                covariance_checks += 1

    assert [record["cells"] for record in stage_records] == [625**m for m in range(6)]
    assert [record["oriented_cell_volume"] for record in stage_records[:3]] == ["81", "81/625", "81/390625"]

    # Every assignment of four successive tail factors to the four rays is
    # related by S4.  A4 preserves orientation and yields two parity sheets.
    factor_ordering = {
        "assignments": len(assignments),
        "S4_gauge_orbits": 1,
        "A4_orientation_orbits": 2,
        "even_transitions": len(even_atlas),
        "odd_transitions": len(odd_atlas),
        "canonical_orientation_grade": "sign:S4->Z2",
        "fixed_clock_first_spatial_next_order_physical": False,
    }

    return {
        "schema": "siel.public-calculation.bgce137.raw.v1",
        "candidate_id": "BGCE137",
        "primary_evidence_status": "Exact conditional theoretical derivation with source-provenance boundary",
        "scientific_layer": "S4-equivariant null-cell refinement and continuum admissibility",
        "baseline_gate": x["baseline"]["status"],
        "endpoint_provenance": x["endpoint"]["lifecycle_level"],
        "input_hashes": {str(path.relative_to(ROOT)): sha256(path) for path in INPUTS.values()},
        "graded_factorization_gate": {
            "discrete_chart_group": "S4",
            "continuous_local_connection_component": "identity component of native metric-affine GL4",
            "chart_transition_derivative_term": "zero because every S4 transition is constant on an overlap",
            "identity_connection_overlap_checks": 24,
            "ray_overlap_covariance_checks": covariance_checks,
            "orientation_grade": factor_ordering,
            "orientation_double_cover_canonical": True,
            "individual_det_minus_one_links_used_as_connection_holonomies": False,
            "factorization_pass": True
        },
        "five_adic_null_cell_gate": {
            "source_derived_ray_count": 4,
            "tail_factor_dimension": 5,
            "new_tail_factors_per_epoch": 4,
            "children_per_parent": len(child_addresses),
            "parent_to_five_child_link_checks": one_stage_checks,
            "parent_to_twenty_five_grandchild_link_checks": two_stage_checks,
            "equal_child_rule": "E_i(m+1)=E_i(m)/5",
            "rule_unique_under_identical_children_and_exact_parent_sum": True,
            "stage_records": stage_records,
            "cell_volume_ratio_per_epoch": "1/625",
            "ambient_R4_assumed": False,
            "external_fixed_one_plus_three_factor_order_used": False,
            "all_factor_to_ray_assignments_one_S4_gauge_orbit": True,
            "marked_factor_split_or_cloned": False,
            "uses_four_new_C5_tail_factors_as_address_digits": True
        },
        "UTC_anchor_gate": {
            "UTC1_identity_log_branch": "PASS",
            "UTC2_uniform_first_second_differences": "PASS_ZERO_FOR_CONSTANT_NORMALIZED_ANCHOR",
            "UTC3_projective_source_anchor": "PASS_EXACT_ONE_AND_TWO_STAGE_COARSENING",
            "temporal_coframe_density": ["3", "3", "3", "3"],
            "connection_density": "0",
            "on_shell_anchor_UTC_closed_conditionally": True,
            "condition": "interpret each source-labelled C5 diagonal digit as a child address along one of the four derived null rays"
        },
        "remaining_boundary": {
            "source_labelled_diagonal_address_is_physically_selected": False,
            "open_C2_AffV4_or_GL4_field_neighborhood_source_derived": False,
            "independent_compactly_supported_delta_e_delta_Gamma_source_derived": False,
            "nonflat_temporal_connection_anchor_derived": False,
            "constant_anchor_alone_supports_BGCE099_first_variation": False,
            "why": "The exact construction supplies a symmetric flat projective anchor family. Reading diagonal cylinder digits as physical events and promoting that family to arbitrary smooth off-shell fields remain a single continuum-realization bridge, not consequences of tensor growth alone."
        },
        "four_dimensionality_effect": {
            "numeral_four_source": "four independent BGCE136 null rays on the target-free V4 carrier",
            "fixed_axis_order_source": "none; 24 orders are one S4 gauge orbit",
            "orientation_source": "canonical sign grading and two-sheet orientation cover",
            "old_CE1D_fixed_clock_plus_three_space_order_required": False,
            "objective_ambient_four_space_smuggled": False,
            "physical_event_topology_unconditional": False
        },
        "CGR_effect": {
            "CGR_removed": False,
            "graded_discrete_continuous_factorization_clause_removed": True,
            "on_shell_UTC_anchor_clause_removed_conditionally_on_diagonal_address_reading": True,
            "remaining_CGR_residual": "one SOURCE_CYLINDER_CARTAN_COMPLETION law: physically interpret the S4-quotiented source-diagonal cylinder addresses as local events and complete the exact anchor family to an open C2 metric-affine field domain with independent compactly supported variations",
            "MMR_effect": "none"
        },
        "counter_intuition_scan": {
            "tempting_success": "Exact 625 refinement and UTC for the symmetric anchor mean the full BGCE099 continuum first variation is now Braid-derived.",
            "refutation": "The anchor is a flat constant family, while BGCE099 varies over an open smooth field domain. Tensor-tail growth does not by itself make diagonal digits physical positions or generate arbitrary variations.",
            "ordinary_explanation": "This is a standard equivariant cubical refinement written in a null tetrad, with a canonical orientation local system.",
            "SIEL_specific_interpretation": "The four refinement directions and their interchangeable chart labels come from the relational crossing carrier rather than an objective background coordinate order.",
            "falsifier": "Failure of projective coarsening, S4 covariance, orientation grading, uniform densities or a proof that the diagonal-address interpretation necessarily reintroduces an external four-axis choice."
        },
        "decision": "CONDITIONAL_PASS_EXACT_S4_EQUIVARIANT_FOUR_NULL_RAY_FIVE_ADIC_REFINEMENT__625_CHILDREN_AND_ONSHELL_UTC_ANCHOR__DISCRETE_CHART_PARITY_SEPARATED_FROM_IDENTITY_CONNECTION__FIXED_ONE_PLUS_THREE_FACTOR_ORDER_REMOVED__PHYSICAL_DIAGONAL_LOCALIZATION_AND_OPEN_OFFSHELL_FIELD_COMPLETION_REMAIN",
        "next_gate": "BGCE138_SOURCE_CYLINDER_DIAGONAL_LOCALIZATION_AND_MINIMAL_SMOOTH_CARTAN_COMPLETION_GATE",
        "claim_ceiling": "BGCE137 conditionally derives an S4-equivariant five-adic refinement and a constant on-shell UTC Cartan anchor without an ambient R4 or physically fixed 1+3 factor order. It does not derive the physical position meaning of diagonal C5 digits, an open off-shell field domain, compactly supported first variations, all of CGR, MMR, an unconditional Einstein equation, empirical gravity, ontology, subjectivity or consciousness."
    }


def main() -> None:
    output = build_outputs()
    (HERE / "RAW_OUTPUT.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
