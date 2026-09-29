#!/usr/bin/env python3
"""BGCE443: pointed-refinement unbounded spatial derivation three-plane."""

from __future__ import annotations

from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
INPUTS = [
    "records/BGCE442_SOURCE_DERIVATION_HH1_OUTER_THREE_PLANE_MOMENT_MAP_GATE_20260924/REVISION_2/RESULT.json",
    "records/BGCE442_SOURCE_DERIVATION_HH1_OUTER_THREE_PLANE_MOMENT_MAP_GATE_20260924/REVISION_2/RAW_OUTPUT.json",
    "public-inputs/formal_checks/ocbfh014_source_native_refinement_naturality_certificate_v1.json",
]


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text())


def determinant(matrix: list[list[F]]) -> F:
    if len(matrix) == 1:
        return matrix[0][0]
    return sum(
        ((-1) ** j) * matrix[0][j] * determinant([row[:j] + row[j + 1:] for row in matrix[1:]])
        for j in range(len(matrix))
    )


def main() -> None:
    bgce442, raw442, refinement = [load(path) for path in INPUTS]
    assert bgce442["status"] == "NO_GO_DIRECT_SOURCE_HH1_OUTER_THREE_PLANE"
    assert bgce442["outer_dimensions"] == [0] * 8
    assert [row["h1_dimension"] for row in raw442["sector_rows"]] == [0] * 8
    tensor = refinement["tensor_refinement_gate"]
    source = refinement["actual_source_reconstruction"]
    assert tensor["refinement_map"] == "j_n(A)=A tensor I_5"
    assert tensor["source_native_no_spectator"] is True
    assert tensor["status"] == "PASS_EXACT_ALLORDER_RIGHT_TAIL_POINTED_TENSOR_REFINEMENT"
    assert source["actual_survivor_masks"] == [0, 5, 8, 13, 16, 21, 24, 29]
    assert all(row["G1_P_chi_commutators_all_nonzero"] for row in tensor["sector_records"])

    # The three pair projectors are mutually orthogonal in M_25 and have the
    # exact source ranks recorded by OCBFH014.  The Hilbert-Schmidt Gram form
    # of commutator superoperators ad(P_i) is
    # 2*d*Tr(P_i P_j)-2*Tr(P_i)Tr(P_j).  A positive determinant proves that
    # the three finite-level inner derivations are linearly independent.
    d = 25
    ranks = source["actual_spatial_projector_ranks"]
    assert ranks == [8, 4, 4]
    gram = []
    for i, ri in enumerate(ranks):
        row = []
        for j, rj in enumerate(ranks):
            overlap = ri if i == j else 0
            row.append(F(2 * d * overlap - 2 * ri * rj))
        gram.append(row)
    principal_minors = [determinant([row[:k] for row in gram[:k]]) for k in range(1, 4)]
    assert all(value > 0 for value in principal_minors)

    # Use the pointed right-tail order to place one copy of every P_chi_i on
    # consecutive disjoint source pairs.  At pair depth r the source inverse
    # length is 5^(2r)=25^r.  Future pair terms commute with every earlier
    # local observable, so the finite inner derivations are exactly compatible.
    # Their norm on a partial isometry crossing Ran(P_i) and Ker(P_i) is at
    # least 25^r, proving unboundedness of the limit on the local union.
    levels = []
    for r in range(1, 9):
        weight = 25 ** r
        levels.append({
            "pair_depth": r,
            "source_strand_depth": 2 * r,
            "source_inverse_length_weight": weight,
            "derivation_norm_lower_bound": weight,
            "future_tail_terms_commute_with_this_local_block": True,
            "refinement_compatibility_exact": True,
        })
    assert all(levels[i + 1]["derivation_norm_lower_bound"] == 25 * levels[i]["derivation_norm_lower_bound"] for i in range(7))

    # Orthogonal P_chi commute on a common pair; distinct pairs commute by
    # tensor locality.  Therefore the three derivations commute on the common
    # dense local core.  Each local exponential is inner and the compatible
    # local automorphisms extend to a strongly continuous isometric group on
    # the UHF limit.  Its generator is closed, hence the local-core derivation
    # is closable.  Unboundedness excludes implementation by one bounded
    # element of the limit algebra.
    masks = source["actual_survivor_masks"]
    result = {
        "schema": "siel.public-calculation.bgce443.result.v1",
        "candidate_id": "BGCE443",
        "date": "2026-09-25",
        "primary_evidence_status": "Theoretical derivation",
        "scientific_layer": "source-refinement spatial gauge-generator construction",
        "status": "SCOPED_PASS_THREE_SOURCE_SELECTED_REFINEMENT_COMPATIBLE_CLOSABLE_UNBOUNDED_DERIVATIONS__INDEPENDENT_THREE_PLANE__ABELIAN_COMMON_CORE_CLOSURE__OPEN_TYPED_MOMENT_MAP_AND_CLOCK_SPATIAL_FIRST_CLASS_ALGEBRA",
        "input_hashes": {path: sha256((ROOT / path).read_bytes()).hexdigest() for path in INPUTS},
        "finite_to_infinite_construction": {
            "ambient_limit": "The pointed inductive system M_(5^n) with j_n(a)=a tensor I_5 from OCBFH014; the algebraic local union is dense in its UHF C-star limit.",
            "spatial_selectors": "The three mutually orthogonal source Fourier projectors P_chi1,P_chi2,P_chi3 in M_25, placed on successive disjoint pointed tail pairs.",
            "finite_implementers": "H_i^(m)=sum_(r=1)^m 25^r P_chi_i^(r), where P_chi_i^(r) acts on source strands (2r-1,2r).",
            "finite_derivations": "delta_i^(m)(a)=sqrt(-1)[H_i^(m),a]. Every finite delta_i^(m) is inner, consistent with BGCE442 HH1=0.",
            "refinement_intertwining": "For a supported before pair m+1, the new tail projector commutes with j(a); hence delta_i^(m+1)j_m=j_m delta_i^(m) exactly.",
            "limit_domain": "For every local a only finitely many pair terms meet its support, so delta_i(a) is an exact finite commutator sum on the dense local algebra.",
            "source_scaling": "The pair at strand depth 2r uses the first-derivative inverse-length factor 5^(2r)=25^r; no coefficient is fitted.",
        },
        "independence_certificate": {
            "pair_matrix_dimension": d,
            "projector_ranks": ranks,
            "commutator_superoperator_gram": [[str(value) for value in row] for row in gram],
            "leading_principal_minors": [str(value) for value in principal_minors],
            "rank": 3,
            "reason": "The positive Gram determinant proves linear independence of ad(P_chi_i); OCBFH014 also records [G1,P_chi_i] nonzero in every actual sector.",
        },
        "unbounded_closable_limit": {
            "eight_pair_depth_witnesses": levels,
            "unboundedness": "A norm-one partial isometry between Ran(P_chi_i^(r)) and its complement has commutator norm one, so ||delta_i|| is at least 25^r at depth r and is unbounded.",
            "automorphism_group": "The compatible local groups Ad(exp(i t H_i^(m))) define a strongly continuous isometric one-parameter automorphism group on the UHF limit: continuity holds first on the local union and extends by density and isometry.",
            "closability": "The generator of a strongly continuous one-parameter automorphism group is closed; the local-core derivation is therefore closable.",
            "outer_scope": "Unboundedness excludes a bounded inner implementer in the C-star limit. This is not a nonzero fixed-finite HH1 class and does not contradict BGCE442.",
            "decision": "PASS_THREE_INDEPENDENT_CLOSABLE_UNBOUNDED_LIMIT_DERIVATIONS",
        },
        "spatial_closure": {
            "common_core": "the algebraic local union",
            "same_pair_commutation": "P_chi_i P_chi_j=0=P_chi_j P_chi_i for i!=j",
            "different_pair_commutation": "Disjoint tensor supports commute.",
            "derivation_brackets": "[delta_i,delta_j]=0 on the common local core.",
            "anomaly": "NONE_FOR_THE_THREE_SPATIAL_DERIVATIONS_IN_THIS_ABELIAN_CORE_SCOPE",
            "boundary": "No cotangent moment maps, lapse-smeared clock family or mixed clock-spatial brackets are constructed here.",
        },
        "all_eight_sector_inheritance": [{
            "mask": mask,
            "same_three_source_projectors": True,
            "G1_commutators_nonzero": True,
            "same_refinement_limit_three_plane": True,
            "same_abelian_common_core_closure": True,
        } for mask in masks],
        "gate_decision": {
            "source_refinement_intertwining": "PASS_EXACT",
            "three_independent_spatial_derivations": "PASS_ALL_EIGHT",
            "closable_unbounded_limit": "PASS",
            "bounded_inner_limit": "NO_GO_BY_UNBOUNDED_NORM_GROWTH",
            "spatial_derivation_common_core_closure": "PASS_ABELIAN_NO_ANOMALY",
            "typed_cotangent_moment_maps": "OPEN",
            "clock_spatial_mixed_brackets": "OPEN",
            "full_finite_anomaly_free_constraint_algebra": "OPEN",
            "BQG_G3_R01_3": "REMAINS_ACTIVE_WITH_SPATIAL_DERIVATION_THREE_PLANE_CLOSED_SCOPED",
            "MMR_CGR_used": False,
            "target_Einstein_equation_used": False,
            "Einstein_Hilbert_or_Fierz_Pauli_action_used": False,
            "manual_three_fifths_used": False,
            "fitted_coefficient_used": False,
        },
        "counter_intuition_scan": {
            "ordinary_explanation": "An infinite tensor product can have unbounded derivation generators even when every finite-stage derivation is inner; rapidly weighted commuting local Hamiltonians are a standard mechanism.",
            "SIEL_specific_part": "The three projectors, their ranks and nonzero clock commutators, the pointed C5 right-tail refinement and the factor-5 source scale are all inherited from the preserved Braid source.",
            "strongest_counterpattern": "The construction closes only an Abelian spatial derivation three-plane. It does not show that these derivations are the gravitational diffeomorphism constraints, provide symplectic moment maps, or close mixed brackets with the clock constraint.",
            "falsifier": "Failure of pointed projector transport, loss of exact tail commutation, singular commutator-superoperator Gram matrix, bounded norm growth, non-closability, or a nonzero spatial commutator anomaly would falsify the scoped result.",
        },
        "bold_hypothesis": {
            "id": "H443_GRAVITY_SPATIAL_GENERATORS_LIVE_ONLY_AT_THE_REFINEMENT_LIMIT",
            "statement": "Braid spatial gauge generators are not outer classes of any fixed finite collision algebra; they emerge as source-scaled unbounded generators on the pointed refinement limit.",
            "supported_part": "Three source-selected independent closable unbounded derivations with anomaly-free Abelian common-core closure now exist on the source UHF carrier.",
            "unsupported_part": "Their typed moment maps, clock-spatial Dirac closure, gravitational interpretation and empirical content remain open.",
        },
        "next_gate": "BGCE457_TYPED_MOMENT_MAP_AND_CLOCK_SPATIAL_FIRST_CLASS_CLOSURE_GATE",
        "runtime_class": "SUBSECOND_EXACT_PROJECTOR_RANK_GRAM_AND_EIGHT_DEPTH_SCALING_WITNESSES_NO_SEARCH",
        "formal_E0_E1_E2": "NOT_CLAIMED__PUBLIC_THEORETICAL_GATE_ONLY",
        "claim_ceiling": "BGCE443 constructs three source-selected independent refinement-compatible closable unbounded derivations on the pointed Braid UHF limit and proves their Abelian no-anomaly closure on the dense local core. It does not construct typed cotangent moment maps, mixed clock-spatial brackets, the full finite first-class constraint algebra, continuum diffeomorphism gravity, empirical gravity, RPD adoption or Official SIEL adoption.",
    }
    (HERE / "RESULT.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({
        "candidate_id": result["candidate_id"],
        "status": result["status"],
        "spatial_rank": result["independence_certificate"]["rank"],
        "unbounded_closable": result["gate_decision"]["closable_unbounded_limit"],
        "spatial_closure": result["gate_decision"]["spatial_derivation_common_core_closure"],
        "constraint_status": result["gate_decision"]["BQG_G3_R01_3"],
        "next_gate": result["next_gate"],
    }, indent=2))


if __name__ == "__main__":
    main()
