#!/usr/bin/env python3
"""BGCE452: hierarchical five-adic spatial Laplacian and UCP heat theorem."""

from __future__ import annotations

from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
INPUTS = [
    "audits/SRA_DPA_BGCE349_BRANCH_RESOLVED_CHOI_TRANSFER_TO_LOCAL_3PLUS1_DOUBLED_METRIC_LORENTZIAN_PARENT_GATE_20260924/RESULT.json",
    "audits/SRA_DPA_BGCE350_FINITE_SOURCE_CYLINDER_PARENT_TO_LOCAL_HISTORY_DRESSED_TOTAL_WARD_IDENTITY_GATE_20260924/RESULT.json",
    "audits/SRA_DPA_BGCE445_AF_QUASILOCAL_CPTP_ALL_SCALE_COMPLETION_GATE_20260925/RESULT.json",
    "audits/SRA_DPA_BGCE451_SOURCE_SPATIAL_HODGE_HEAT_UV_CARRIER_AND_REFINEMENT_NATURALITY_GATE_20260925/RESULT.json",
]


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text())


def main() -> None:
    u349, u350, u445, u451 = [load(path) for path in INPUTS]
    assert u349["gate_decision"]["local_source_cylinder_parent"] is True
    assert u350["gate_decision"]["history_dressed_local_total_Ward"] is True
    assert u445["gate_decision"]["unique_quasilocal_extension"] == "PASS"
    assert u451["gate_decision"]["existing_child_constant_refinement_intertwining"] == "NO_GO"

    # Exact finite-depth bookkeeping for levels 1..8.  There are 5^3=125
    # spatial children and inverse-square cell scaling 5^2=25.
    levels = []
    cumulative = 1
    for k in range(1, 9):
        multiplicity = 124 * 125 ** (k - 1)
        cumulative += multiplicity
        eigenvalue = 25 ** k
        assert cumulative == 125 ** k
        # Exact three-dimensional spectral counting identity.
        assert cumulative * cumulative == eigenvalue ** 3
        levels.append({
            "level": k,
            "detail_multiplicity": multiplicity,
            "cumulative_dimension": cumulative,
            "eigenvalue": eigenvalue,
            "N_squared_equals_lambda_cubed": True,
        })

    # Coefficients of the heat map at a symbolic decreasing sequence a_k.
    # A concrete rational witness a_k=2^-k verifies convexity without using
    # it to choose the physical heat time.
    a = [F(1)] + [F(1, 2**k) for k in range(1, 9)]
    convex = [1 - a[1]] + [a[k] - a[k + 1] for k in range(1, 8)] + [a[8]]
    assert all(c >= 0 for c in convex)
    assert sum(convex) == 1

    result = {
        "schema": "siel.dpa.bgce452.result.v1",
        "candidate_id": "BGCE452",
        "date": "2026-09-25",
        "primary_evidence_status": "Theoretical exact hierarchical operator-algebra theorem with finite-level arithmetic witnesses",
        "scientific_layer": "fundamental source-cylinder ultraviolet completion candidate",
        "status": "SCOPED_PASS_REFINEMENT_INTERTWINING_FIVE_ADIC_HIERARCHICAL_SPATIAL_LAPLACIAN__UCP_HEAT_SEMIGROUP__EXACT_SPECTRAL_DIMENSION_THREE__ALL_FINITE_POLYNOMIAL_COMPOSITE_MOMENTS_FINITE__CONSERVATIVE_BLOCK_WARD__OPEN_PHYSICAL_RATE_ACTUAL_METRIC_WEIGHT_AND_LORENTZIAN_ACTION_INSERTION",
        "input_hashes": {path: sha256((ROOT / path).read_bytes()).hexdigest() for path in INPUTS},
        "source_construction": {
            "spatial_branching": "B=5^3=125 children per source-clock slice",
            "nested_expectations": "On level m let E_k^(m), 0<=k<=m, be the uniform trace-preserving conditional expectation onto level-k child-constant cylinder functions; E_m=I and E_j E_k=E_min(j,k).",
            "detail_projectors": "D_k=E_k-E_(k-1), k>=1; the D_k are pairwise orthogonal self-adjoint projections in the uniform source trace.",
            "generator": "Delta_m=sum_(k=1)^m 25^k D_k, where 25^k=(5^-k)^-2 is the source spatial inverse-square scaling.",
            "internal_lift": "Delta_m acts on the address factor and identity acts on M_125; hence it commutes with the block-identical internal collision channel.",
            "no_target_or_fit": True,
        },
        "exact_refinement": {
            "embedding": "j_m copies a level-m function to all 125 spatial children; p_m uniformly averages those children and p_m j_m=I.",
            "intertwining": "Delta_(m+1) j_m=j_m Delta_m because the new detail D_(m+1) annihilates child-constant functions and all older conditional expectations commute with j_m.",
            "heat_intertwining": "H_(m+1,t) j_m=j_m H_(m,t) for H_(m,t)=exp(-t Delta_m).",
            "AF_compatibility": "The heat maps therefore define one map on the algebraic union and extend contractively to the same BGCE445 AF/quasi-local limit.",
        },
        "UCP_heat_theorem": {
            "spectral_form": "H_(m,t)=E_0+sum_(k=1)^m exp(-t 25^k)(E_k-E_(k-1)).",
            "convex_form": "With a_k=exp(-t25^k), H_(m,t)=a_m I+(1-a_1)E_0+sum_(k=1)^(m-1)(a_k-a_(k+1))E_k.",
            "proof": "For t>=0 the coefficients are nonnegative and sum to one. Every E_k is a unital completely positive conditional expectation, so H_(m,t) is UCP, trace preserving and completely contractive.",
            "semigroup": "Orthogonality of D_k gives H_(m,t+s)=H_(m,t)H_(m,s).",
            "rational_convexity_witness_a_k_2^-k": [str(value) for value in convex],
        },
        "spectral_dimension_and_UV": {
            "level_k_eigenvalue": "lambda_k=25^k",
            "level_k_multiplicity": "mu_k=124*125^(k-1)",
            "cumulative_count": "N(lambda_k)=1+sum_(j=1)^k mu_j=125^k=(25^k)^(3/2)=lambda_k^(3/2)",
            "spectral_dimension": 3,
            "levels_1_to_8_exact": levels,
            "all_finite_moments": "For every t>0 and finite r>=0, sum_k mu_k(1+lambda_k)^r exp(-t lambda_k) converges because exponential decay in 25^k dominates 125^k*25^(rk).",
            "no_continuum_momentum_cutoff": True,
        },
        "discrete_Ward": {
            "conservative_generator_form": "Delta_m=25(I-E_0)+sum_(k=1)^(m-1)(25^(k+1)-25^k)(I-E_k).",
            "constant_preservation": "Delta_m 1=0 and H_(m,t)1=1.",
            "total_balance": "Every I-E_k has zero uniform block sum; the generator is a positive sum of within-parent block averaging currents, so address probability/current lost at one child is gained inside the same parent block.",
            "collision_Ward_compatibility": "Address expectations commute with the identical internal collision map, so the BGCE350 block-local system-plus-environment Ward telescope is retained on the dense local cylinder algebra.",
            "scope": "This is the uniform source measure Ward law. Metric-volume-weighted stress divergence and a same-action Lorentzian Hilbert variation are not yet proved.",
        },
        "counter_intuition_scan": {
            "ordinary_explanation": "A nested conditional-expectation filtration carries a standard hierarchical Markov Laplacian. Its multiplicity 125 and inverse-square eigenvalue scaling 25 force spectral dimension three.",
            "SIEL_specific_part": "The filtration, 125 spatial children, source clock split, M_125 collision fiber and block Ward are all inherited from the Braid source cylinder rather than selected from a target continuum field theory.",
            "strongest_counterpattern": "The hierarchical generator is ultrametric/block-local rather than the nearest-neighbor smooth Laplacian. UV finiteness on this fundamental carrier does not by itself prove the correct smooth-spacetime propagator, Lorentz invariance, measured gravity or the metric-weighted stress law.",
            "falsifier": "Failure of conditional-expectation compatibility, loss of UCP under the internal lift, a wrong spectral counting exponent, or inability to couple the generator to the actual metric parent while preserving the total Ward identity.",
        },
        "gate_decision": {
            "exact_multiresolution_intertwiner": "PASS",
            "UCP_heat_all_depths": "PASS",
            "spectral_dimension_three": "PASS_EXACT",
            "all_finite_polynomial_composite_moments": "PASS",
            "uniform_source_measure_Ward": "PASS_SCOPED",
            "source_fixed_dimensionless_generator_normalization": "PASS_BY_CELL_INVERSE_SQUARE",
            "physical_dimensionful_heat_rate": "OPEN",
            "actual_metric_weighted_Hilbert_stress_and_Ward": "OPEN",
            "same_action_Lorentzian_insertion": "OPEN",
            "smooth_spacetime_empirical_UV_completion": "OPEN",
            "fundamental_source_cylinder_UV_completion": "CLOSED_SCOPED",
            "BQG_G3_R02": "CLOSED_SCOPED_WITH_PHYSICAL_CONTINUUM_MATCH_OPEN",
        },
        "bold_hypothesis": {
            "id": "H452_FUNDAMENTAL_HIERARCHICAL_SPACE",
            "statement": "The physical ultraviolet carrier is the source-cylinder hierarchical spatial filtration itself, with Delta=sum 25^k D_k, rather than a smooth nearest-neighbor continuum extrapolated beyond its domain.",
            "conditional_physical_consequence": "If the BGCE349 Lorentzian parent couples its spatial composite observables through this generator at any positive calibrated heat time, every finite polynomial UV moment is finite without counterterm fitting and the spatial spectral dimension is exactly three.",
            "boundary": "The if-clause is not yet the same-action metric coupling theorem.",
        },
        "next_gate": "BGCE453_ACTUAL_METRIC_WEIGHTED_HIERARCHICAL_HEAT_HILBERT_STRESS_AND_LORENTZIAN_WARD_GATE",
        "runtime_class": "SUBSECOND_EXACT_FILTRATION_ALGEBRA_AND_EIGHT_LEVEL_INTEGER_WITNESS_NO_SCAN",
        "formal_E0_E1_E2": "NOT_CLAIMED__DPA_THEORETICAL_GATE_ONLY",
        "claim_ceiling": "BGCE452 closes a nonperturbative ultraviolet theorem for the fundamental uniform-measure source-cylinder hierarchy: exact all-depth UCP heat dynamics, spectral dimension three, all finite polynomial moments and a conservative block Ward law.  It does not yet prove the physical dimensionful rate, actual metric-volume weighting, same-action Lorentzian Hilbert stress, smooth-spacetime propagator, empirical gravity or completed quantum gravity.",
    }
    (HERE / "RESULT.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({
        "candidate_id": result["candidate_id"],
        "status": result["status"],
        "spectral_dimension": result["spectral_dimension_and_UV"]["spectral_dimension"],
        "fundamental_UV": result["gate_decision"]["fundamental_source_cylinder_UV_completion"],
        "next_gate": result["next_gate"],
    }, indent=2))


if __name__ == "__main__":
    main()
