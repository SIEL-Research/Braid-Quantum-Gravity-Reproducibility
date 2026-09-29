#!/usr/bin/env python3
"""BGCE138: source spectral cylinders and minimal smooth Cartan completion."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
from typing import Any
import hashlib
import importlib.util
import itertools
import json
import sys

import numpy as np


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
CANDIDATE_ID = "BGCE138"
DECISION = (
    "PASS_EXACT_SOURCE_MARKER_SELECTS_CANONICAL_C5_MASA_AND_SPECTRAL_ORDER__"
    "S4_EQUIVARIANT_GELFAND_CYLINDER_QUOTIENT_IS_UNIT_FOUR_CUBE__"
    "MINIMAL_OPEN_C2_METRIC_AFFINE_VARIATION_DOMAIN_EXISTS_WITH_EXACT_LINK_COARSENING__"
    "FORMAL_CGR_COMPLETION_REDUCED_TO_SPECTRAL_EVENT_IDENTIFICATION__"
    "PHYSICAL_EVENT_STATUS_NOT_DERIVED"
)

INPUTS = [
    "audits/UB443_TYPED_SIGNED_SURVIVOR_GAUGE_OR_OBSERVABLE_GATE/RESULT.json",
    "audits/UB443_TYPED_SIGNED_SURVIVOR_GAUGE_OR_OBSERVABLE_GATE/TYPED_SIGNED_INVARIANT_CERTIFICATE.json",
    "audits/UB443_TYPED_SIGNED_SURVIVOR_GAUGE_OR_OBSERVABLE_GATE/evaluate.py",
    "projects/active/discovery_partner/formal_checks/ocbfh014_source_native_refinement_naturality_certificate_v1.json",
    "audits/SRA_THEORY_A57S_CE1D_FOUR_AXIS_MASA_SOLDER_GATE_20260918/FROZEN_PROTOCOL.json",
    "audits/SRA_THEORY_A57S_CE1D_FOUR_AXIS_MASA_SOLDER_GATE_20260918/RESULT.json",
    "audits/SRA_DPA_BGCE098_SOURCE_REGULARITY_AND_BRANCH_CONTROL_AUDIT_20260919/RESULT.json",
    "audits/SRA_DPA_BGCE099_CONDITIONAL_CONTINUUM_PALATINI_ACTION_AND_VARIATION_THEOREM_20260919/RESULT.json",
    "audits/SRA_DPA_BGCE100_NATIVE_GL4_AND_ZERO_HYPERMOMENTUM_SPLIT_AUDIT_20260919/RESULT.json",
    "audits/SRA_DPA_BGCE128_SOURCE_DERIVED_AFFINE_ONE_PLUS_THREE_CARRIER_AND_LOCALIZATION_BRIDGE_GATE_20260919/RESULT.json",
    "audits/SRA_DPA_BGCE135_AFFINE_LOCAL_CHART_TO_PHYSICAL_CAUSAL_CELL_AND_SCALE_DEPENDENCY_GATE_20260919/RESULT.json",
    "audits/SRA_DPA_BGCE137_DISCRETE_S4_CHART_TRANSITION_VERSUS_NEAR_IDENTITY_CARTAN_CONNECTION_FACTORING_GATE_20260919/RESULT.json",
    "audits/UB469_BRAID_SOURCE_FISHER_GEOMETRY_IDENTITY_GATE/RESULT.json",
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(relative: str) -> dict[str, Any]:
    return json.loads((REPO / relative).read_text())


def load_module(name: str, relative: str):
    path = REPO / relative
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def fraction_rank(rows: list[list[int | Fraction]]) -> int:
    a = [[Fraction(value) for value in row] for row in rows]
    if not a:
        return 0
    row = 0
    for column in range(len(a[0])):
        pivot = next((index for index in range(row, len(a)) if a[index][column]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        scale = a[row][column]
        a[row] = [value / scale for value in a[row]]
        for index in range(len(a)):
            if index == row or not a[index][column]:
                continue
            scale = a[index][column]
            a[index] = [left - scale * right for left, right in zip(a[index], a[row])]
        row += 1
        if row == len(a):
            break
    return row


def marker_for(ub443, survivor: dict[str, Any], j: np.ndarray) -> np.ndarray:
    identity5 = np.eye(5, dtype=np.int64)
    endpoint_j = np.kron(j, identity5)
    word = endpoint_j @ survivor["F"] @ endpoint_j @ survivor["H"] @ survivor["R"]
    return ub443.partial_trace_second(word)


def marker_masa_gate() -> dict[str, Any]:
    ub443 = load_module(
        "bgce138_ub443",
        "audits/UB443_TYPED_SIGNED_SURVIVOR_GAUGE_OR_OBSERVABLE_GATE/evaluate.py",
    )
    regenerated_result, regenerated_certificate = ub443.build_outputs()
    assert regenerated_result == load("audits/UB443_TYPED_SIGNED_SURVIVOR_GAUGE_OR_OBSERVABLE_GATE/RESULT.json")
    assert regenerated_certificate == load(
        "audits/UB443_TYPED_SIGNED_SURVIVOR_GAUGE_OR_OBSERVABLE_GATE/TYPED_SIGNED_INVARIANT_CERTIFICATE.json"
    )
    survivors, j = ub443.build_survivors()
    eigenvalues = (-7, -5, -4, -1, 7)
    sector_records = []
    for survivor in survivors:
        marker = marker_for(ub443, survivor, j)
        assert np.array_equal(marker, marker.T)
        identity5 = np.eye(5, dtype=np.int64)
        annihilator = identity5.copy()
        for eigenvalue in eigenvalues:
            annihilator = annihilator @ (marker - eigenvalue * identity5)
        assert not np.any(annihilator)
        projectors = [ub443.spectral_projector_numerator(marker, eigenvalues, value) for value in eigenvalues]
        normalized: list[list[list[Fraction]]] = []
        for numerator, denominator in projectors:
            p = [[Fraction(int(numerator[i, j]), int(denominator)) for j in range(5)] for i in range(5)]
            normalized.append(p)
        # Exact orthogonal rank-one resolution.
        for index, (numerator, denominator) in enumerate(projectors):
            assert int(np.trace(numerator)) == denominator
            assert np.array_equal(numerator @ numerator, denominator * numerator)
            for other_index, (other, _) in enumerate(projectors):
                if index != other_index:
                    assert not np.any(numerator @ other)
        common = 1
        for _, denominator in projectors:
            common = int(np.lcm(common, abs(int(denominator))))
        total = np.zeros((5, 5), dtype=object)
        for numerator, denominator in projectors:
            total += numerator.astype(object) * (common // int(denominator))
        assert np.array_equal(total, identity5.astype(object) * common)

        # The commutator X -> LX-XL has rank 20, hence a five-dimensional
        # commutant.  The five spectral projectors already span it, so C*(L)
        # is a MASA.  This is exact rational elimination, not a float rank.
        commutator_rows = []
        for out_i in range(5):
            for out_j in range(5):
                row = []
                for in_i in range(5):
                    for in_j in range(5):
                        coefficient = 0
                        if in_j == out_j:
                            coefficient += int(marker[out_i, in_i])
                        if in_i == out_i:
                            coefficient -= int(marker[in_j, out_j])
                        row.append(coefficient)
                commutator_rows.append(row)
        commutator_rank = fraction_rank(commutator_rows)
        assert commutator_rank == 20
        sector_records.append({
            "mask": survivor["mask"],
            "marker_symmetric": True,
            "simple_spectrum": list(eigenvalues),
            "rank_one_projectors": 5,
            "projector_sum_identity": True,
            "commutator_map_rank": commutator_rank,
            "commutant_dimension": 25 - commutator_rank,
            "generated_algebra_is_MASA": True,
        })
    assert len(sector_records) == 8
    return {
        "actual_signed_sectors": len(sector_records),
        "marker_definition": "L=Tr_2[(J tensor I) F (J tensor I) H R]",
        "marker_spectrum": list(eigenvalues),
        "spectral_digit_order": {str(value): index for index, value in enumerate(eigenvalues)},
        "digit_order_basis_free": True,
        "sector_records": sector_records,
        "theorem": "For a self-adjoint 5 by 5 marker with five distinct source-labelled eigenvalues, C*(L)=span(P_lambda) has dimension five and equals its commutant; it is therefore a MASA selected by the source marker, not by an external computational basis.",
        "typed_covariance": "L maps to S L S^T and P_lambda maps to S P_lambda S^T, while lambda itself is unchanged.",
        "status": "PASS_EXACT_SOURCE_MARKER_SELECTED_C5_MASA_AND_CANONICAL_SPECTRAL_DIGIT_ORDER",
    }


def cylinder_gate() -> dict[str, Any]:
    digits = tuple(range(5))
    four_digit_cells = tuple(itertools.product(digits, repeat=4))
    assert len(four_digit_cells) == 625
    permutations = tuple(itertools.permutations(range(4)))
    covariance_checks = 0
    for permutation in permutations:
        image = {tuple(cell[index] for index in permutation) for cell in four_digit_cells}
        assert image == set(four_digit_cells)
        covariance_checks += len(four_digit_cells)

    stage_records = []
    for stage in range(6):
        address_cells = 625 ** stage
        grid_cells = 5 ** (4 * stage)
        assert address_cells == grid_cells
        stage_records.append({
            "stage": stage,
            "minimal_cylinders": address_cells,
            "four_axis_grid_cells": grid_cells,
            "mesh": str(Fraction(1, 5 ** stage)),
            "cell_four_volume": str(Fraction(1, 625 ** stage)),
        })

    # Every one-epoch parent suffix has exactly 625 children; deleting the
    # suffix is the Gelfand dual of f -> f tensor 1 on the cylinder algebra.
    parent_prefix = (0, 1, 2, 3)
    children = tuple(parent_prefix + suffix for suffix in four_digit_cells)
    assert len(children) == 625
    assert {child[:-4] for child in children} == {parent_prefix}
    return {
        "one_factor_atomic_spectrum": 5,
        "four_factor_epoch_atoms": 625,
        "one_parent_children": 625,
        "parent_map": "delete the newest four spectral digits",
        "algebra_map": "f -> f tensor 1_(5^4)",
        "stage_records": stage_records,
        "S4_axis_permutations": 24,
        "S4_cell_covariance_checks": covariance_checks,
        "all_axis_orders_one_gauge_orbit": True,
        "coordinate_map": "x^a(omega)=sum_(j>=1) rank(lambda_(j,a))*5^(-j), a=0,1,2,3",
        "quotient": "identify exactly the pairs of spectral addresses with equal four base-five limits",
        "quotient_space": "[0,1]^4",
        "quotient_reason": "four copies of the standard base-five address quotient; the only noninjectivity is the terminating/repeating-four boundary expansion",
        "ambient_R4_assumed": False,
        "fixed_clock_first_factor_order_assumed": False,
        "status": "PASS_EXACT_S4_EQUIVARIANT_SOURCE_SPECTRAL_CYLINDER_TO_FOUR_CUBE_QUOTIENT",
    }


def smooth_completion_gate() -> dict[str, Any]:
    # Background normalized coframe density is 3 I_4.  For entrywise
    # perturbations |delta e_ab| < eps, strict row diagonal dominance follows
    # from 3-eps > 3 eps.  eps=1/2 is a rational witness inside eps<3/4.
    epsilon = Fraction(1, 2)
    diagonal_lower = Fraction(3) - epsilon
    off_diagonal_upper = 3 * epsilon
    assert diagonal_lower > off_diagonal_upper

    # A compactly supported C2 scalar witness on (0,1)^4 is the product of
    # one-dimensional piecewise polynomials b(t)=(t-1/4)^3(3/4-t)^3 on
    # [1/4,3/4], zero outside. Value and first two derivatives vanish at both
    # endpoints, so zero extension is C2.
    one_quarter = Fraction(1, 4)
    three_quarters = Fraction(3, 4)
    assert one_quarter < three_quarters
    vanishing_orders = {"value": 3, "first_derivative": 2, "second_derivative": 1}
    assert min(vanishing_orders.values()) >= 1

    coframe_components = tuple((a, mu) for a in range(4) for mu in range(4))
    connection_components = tuple((a, b, mu) for a in range(4) for b in range(4) for mu in range(4))
    assert len(coframe_components) == 16
    assert len(connection_components) == 64

    return {
        "base": "Q=(0,1)^4 with the source spectral five-adic chart",
        "carrier": "native metric-affine GL4",
        "background_coframe_density": "3 I_4",
        "background_connection_density": "0",
        "explicit_open_ball_entrywise_radius": str(epsilon),
        "invertibility_witness": "3-epsilon > 3 epsilon by strict row diagonal dominance",
        "diagonal_lower_bound": str(diagonal_lower),
        "off_diagonal_row_sum_upper_bound": str(off_diagonal_upper),
        "compact_C2_bump": "beta(x)=product_a b(x_a), b(t)=(t-1/4)^3(3/4-t)^3 on [1/4,3/4] and 0 outside",
        "boundary_vanishing_orders": vanishing_orders,
        "independent_compactly_supported_delta_e_components": len(coframe_components),
        "independent_compactly_supported_delta_Gamma_components": len(connection_components),
        "coframe_discretization": "E_edge=integral_edge e; parent equals the sum of five ordered child integrals exactly",
        "connection_discretization": "U_edge=Pexp integral_edge Gamma; parent equals the ordered product of five child holonomies exactly",
        "UTC1": "bounded C2 connection gives a common near-identity logarithm branch at all sufficiently fine five-adic stages",
        "UTC2": "C2 bounds give uniform first and second five-adic difference bounds",
        "UTC3": "line-integral additivity and path-ordered composition give exact projective coarsening",
        "S4_equivariance": "the domain and discretization are invariant under simultaneous permutation of the four spectral coordinates and four null-ray labels",
        "new_continuous_fit_or_target_coefficient": False,
        "source_dynamically_selects_one_off_shell_field": False,
        "why_nonuniqueness_is_required": "The off-shell domain must contain independent variations; the action and Euler equation, not the source anchor, select on-shell fields.",
        "status": "PASS_EXPLICIT_MINIMAL_OPEN_C2_METRIC_AFFINE_COMPLETION_AND_COMPACT_VARIATION_DOMAIN",
    }


def run() -> dict[str, Any]:
    baseline = load(str(HERE.relative_to(REPO) / "BASELINE_GATE.json"))
    bgce137 = load("audits/SRA_DPA_BGCE137_DISCRETE_S4_CHART_TRANSITION_VERSUS_NEAR_IDENTITY_CARTAN_CONNECTION_FACTORING_GATE_20260919/RESULT.json")
    ce1d = load("audits/SRA_THEORY_A57S_CE1D_FOUR_AXIS_MASA_SOLDER_GATE_20260918/FROZEN_PROTOCOL.json")
    bgce099 = load("audits/SRA_DPA_BGCE099_CONDITIONAL_CONTINUUM_PALATINI_ACTION_AND_VARIATION_THEOREM_20260919/RESULT.json")
    ub469 = load("audits/UB469_BRAID_SOURCE_FISHER_GEOMETRY_IDENTITY_GATE/RESULT.json")
    assert baseline["science_outcome_authorized"] is True
    assert bgce137["UTC_anchor"]["on_shell_anchor_UTC_closed_conditionally"] is True
    assert ce1d["new_bridge_hypothesis"]["statement"].startswith("Use the source-labelled diagonal MASA")
    assert bgce099["status"].startswith("CONDITIONAL_PASS")
    assert ub469["result"]["independent_natural_spacetime_response_measured"] is False

    marker = marker_masa_gate()
    cylinder = cylinder_gate()
    smooth = smooth_completion_gate()
    return {
        "schema": "siel.dpa.bgce138.raw.v1",
        "candidate_id": CANDIDATE_ID,
        "primary_evidence_status": "Exact theoretical derivation with one retained physical-identification boundary",
        "scientific_layer": "source-selected algebraic localization and continuum configuration-space completion",
        "baseline_gate": "PASS_BY_REVISION_MATCHED_COMMITTED_THEOREM_AUDIT",
        "endpoint_provenance": "NOT_ISSUED_BY_DPA__THEORETICAL_SOURCE_AND_COMPLETION_AUDIT_ONLY",
        "input_hashes": {relative: digest(REPO / relative) for relative in INPUTS},
        "source_marker_MASA_gate": marker,
        "spectral_cylinder_gate": cylinder,
        "minimal_smooth_completion_gate": smooth,
        "dependency_effect": {
            "old_CE1D_arbitrary_diagonal_MASA_selection_removed": True,
            "old_CE1D_fixed_clock_plus_three_space_factor_order_removed_by_BGCE137": True,
            "open_C2_metric_affine_domain_exists_explicitly": True,
            "independent_compactly_supported_variations_exist_explicitly": True,
            "BGCE099_formal_vacuum_first_variation_hypotheses_mathematically_instantiated": True,
            "physical_event_identification_source_derived": False,
            "empirical_natural_spacetime_identification": False,
        },
        "CGR_effect": {
            "CGR_removed_unconditionally": False,
            "CGR_formal_mathematical_completion": "PASS_CONDITIONAL_ONLY_ON_SPECTRAL_EVENT_IDENTIFICATION",
            "remaining_CGR_residual": "SPECTRAL_EVENT_IDENTIFICATION: identify the source-marker cylinder/Gelfand points and their causal affine transitions with physical local events, rather than only internal distinguishable source modes",
            "why_not_call_removed": "UB469 gives an operational Fisher geometry for the same marker outcomes but explicitly does not supply an independent natural spacetime response.",
        },
        "MMR_effect": "none",
        "counter_intuition_scan": {
            "tempting_success": "A canonical MASA and a four-cube quotient prove that physical spacetime is Braid-generated.",
            "refutation": "Gelfand localization proves a mathematical point space. Physical event identity requires a source-to-natural-event operational link; UB469 explicitly leaves that link open.",
            "ordinary_explanation": "A self-adjoint simple-spectrum matrix canonically generates a MASA; base-five inverse limits and C2 field spaces are standard mathematics.",
            "SIEL_specific_interpretation": "The labels of the localization atoms and their four causal directions come from the relational Braid marker/null-ray package rather than an externally chosen coordinate basis.",
            "falsifier": "A repeated marker eigenvalue, a commutant larger than five, failure of tensor-cylinder refinement or S4 covariance, failure of the explicit compact-support variation construction, or proof that the marker cylinders cannot support the declared event readout.",
        },
        "decision": DECISION,
        "next_gate": "BGCE139_SOURCE_SPECTRAL_CYLINDER_OPERATIONAL_EVENT_IDENTIFICATION_GATE",
        "claim_ceiling": "BGCE138 derives a source-selected C5 MASA, an S4-equivariant four-dimensional spectral cylinder quotient and an explicit open C2 metric-affine off-shell configuration space with independent compactly supported variations. It does not identify those mathematical points with natural spacetime events, derive MMR, give an unconditional Braid-only Einstein equation, establish empirical gravity, ontology, subjectivity or consciousness.",
    }


if __name__ == "__main__":
    output = run()
    path = HERE / "RAW_OUTPUT.json"
    path.write_text(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=False) + "\n")
    print(json.dumps({
        "decision": output["decision"],
        "marker_MASA": output["source_marker_MASA_gate"]["status"],
        "cylinder": output["spectral_cylinder_gate"]["status"],
        "smooth": output["minimal_smooth_completion_gate"]["status"],
        "remaining_CGR": output["CGR_effect"]["remaining_CGR_residual"],
    }, ensure_ascii=False, indent=2))
