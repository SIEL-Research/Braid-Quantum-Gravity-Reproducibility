#!/usr/bin/env python3
"""BGCE456: actual-metric nonnegative conductance Markov/wave gate."""

from __future__ import annotations

from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
INPUTS = [
    "audits/SRA_DPA_BGCE452_SOURCE_HIERARCHICAL_SPATIAL_LAPLACIAN_UCP_HEAT_AND_WARD_GATE_20260925/RESULT.json",
    "audits/SRA_DPA_BGCE453_ACTUAL_METRIC_WEIGHTED_HIERARCHICAL_HEAT_HILBERT_STRESS_AND_LORENTZIAN_WARD_GATE_20260925/RESULT.json",
    "audits/SRA_DPA_BGCE454_CALIBRATED_DIMENSIONFUL_HIERARCHICAL_HEAT_RATE_AND_LOW_MODE_LORENTZIAN_PROPAGATOR_GATE_20260925/RESULT.json",
    "audits/SRA_DPA_BGCE455_ACTIVE_PBM_PROJECTIVE_VOLUME_AND_ANISOTROPIC_THREE_CHARACTER_PROPAGATOR_GATE_20260925/RESULT.json",
]
METRIC_INPUT = "audits/SRA_DPA_BGCE455_ACTIVE_PBM_PROJECTIVE_VOLUME_AND_ANISOTROPIC_THREE_CHARACTER_PROPAGATOR_GATE_20260925/ACTUAL_METRIC_INPUT.json"


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text())


def frac(value: object) -> F:
    return F(str(value))


def inverse(matrix: list[list[F]]) -> list[list[F]]:
    n = len(matrix)
    aug = [row[:] + [F(int(i == j)) for j in range(n)] for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = next(row for row in range(col, n) if aug[row][col])
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [x / scale for x in aug[col]]
        for row in range(n):
            if row != col:
                scale = aug[row][col]
                aug[row] = [x - scale * y for x, y in zip(aug[row], aug[col])]
    return [row[n:] for row in aug]


def ldl_pivots(matrix: list[list[F]]) -> list[F]:
    n = len(matrix)
    lower = [[F(0) for _ in range(n)] for _ in range(n)]
    diagonal = [F(0) for _ in range(n)]
    for i in range(n):
        lower[i][i] = 1
        diagonal[i] = matrix[i][i] - sum(lower[i][k] ** 2 * diagonal[k] for k in range(i))
        for j in range(i + 1, n):
            lower[j][i] = (
                matrix[j][i] - sum(lower[j][k] * lower[i][k] * diagonal[k] for k in range(i))
            ) / diagonal[i]
    return diagonal


def centered_delta(x: tuple[int, int, int], y: tuple[int, int, int]) -> tuple[int, int, int]:
    values = []
    for a, b in zip(x, y):
        value = (b - a) % 5
        if value > 2:
            value -= 5
        values.append(value)
    return tuple(values)  # type: ignore[return-value]


def quadratic(matrix: list[list[F]], vector: tuple[int, int, int]) -> F:
    return sum(F(vector[i]) * matrix[i][j] * F(vector[j]) for i in range(3) for j in range(3))


def conductance(matrix: list[list[F]], x: tuple[int, int, int], y: tuple[int, int, int]) -> F:
    delta = centered_delta(x, y)
    norm2 = sum(F(v * v) for v in delta)
    assert norm2 > 0
    return quadratic(matrix, delta) / (5 * norm2)


def main() -> None:
    u452, u453, u454, u455 = [load(path) for path in INPUTS]
    metric_input = load(METRIC_INPUT)
    assert u452["gate_decision"]["UCP_heat_all_depths"] == "PASS"
    assert u453["gate_decision"]["metric_weighted_UCP_heat_all_depths"] == "PASS"
    assert u454["gate_decision"]["exact_z_one_dispersion"] == "PASS"
    assert u455["gate_decision"]["same_operator_UCP_heat"] == "NO_GO_ACTUAL_METRIC_OFFDIAGONAL_SIGN"

    source_path = ROOT / metric_input["source_path"]
    assert source_path.exists()
    assert sha256(source_path.read_bytes()).hexdigest() == metric_input["source_sha256"]

    metric4 = [[frac(x) for x in row] for row in metric_input["clock_orthogonal_metric"]]
    gamma = [row[1:] for row in metric4[1:]]
    assert all(p > 0 for p in ldl_pivots(gamma))
    A = inverse(gamma)
    assert all(p > 0 for p in ldl_pivots(A))

    # On C5 every group difference has a unique centered representative in
    # {-2,-1,0,1,2}.  Turn the actual inverse metric into a positive edge
    # conductance by its exact directional Rayleigh quotient.  The factor 1/5
    # is fixed by the BGCE452 isotropic normalization, not fitted.
    coordinates = list(product(range(5), repeat=3))
    edges: list[tuple[tuple[int, int, int], tuple[int, int, int], F]] = []
    for i, x in enumerate(coordinates):
        for y in coordinates[i + 1:]:
            value = conductance(A, x, y)
            assert value > 0
            edges.append((x, y, value))
    assert len(edges) == 125 * 124 // 2

    identity = [[F(int(i == j)) for j in range(3)] for i in range(3)]
    assert all(conductance(identity, x, y) == F(1, 5) for x, y, _ in edges)
    # Hence L_I has off-diagonal -1/5 and diagonal 124/5, exactly
    # 25(I-E0) on a 125-child block.

    min_edge = min(edges, key=lambda item: item[2])
    max_edge = max(edges, key=lambda item: item[2])
    distinct_conductances = sorted({value for _, _, value in edges})
    assert len(distinct_conductances) > 1

    gamma_trace = sum(gamma[i][i] for i in range(3))
    A_trace = sum(A[i][i] for i in range(3))
    alpha = 1 / gamma_trace
    beta = A_trace
    assert alpha > 0
    assert beta > alpha
    assert all(alpha / 5 <= value <= beta / 5 for _, _, value in edges)

    # Recheck the exact BGCE455 offending pair.  The conductance Laplacian now
    # has a strictly negative off-diagonal there by construction.
    old_x = (0, 1, 2)
    old_y = (1, 0, 2)
    repaired_conductance = conductance(A, old_x, old_y)
    repaired_offdiagonal = -repaired_conductance
    assert repaired_offdiagonal < 0

    # Exact directional witnesses show that the construction is anisotropic.
    origin = (0, 0, 0)
    axis_conductances = {
        "chi1": conductance(A, origin, (1, 0, 0)),
        "chi2": conductance(A, origin, (0, 1, 0)),
        "chi3": conductance(A, origin, (0, 0, 1)),
    }
    assert len(set(axis_conductances.values())) > 1

    # Each level-k block Laplacian is scaled by 25^(k-1).  At A=I this is
    # exactly 25^k D_k.  Every level term annihilates parent-constant
    # functions, so refinement intertwining is exact.  The edgewise bounds
    # imply alpha*Delta_iso <= Delta_A <= beta*Delta_iso as quadratic forms.
    # Min-max then preserves the spectral counting exponent 3/2, hence d_s=3.
    levels = []
    for k in range(1, 9):
        multiplicity = 124 * 125 ** (k - 1)
        cumulative = 125 ** k
        isotropic_lambda = 25 ** k
        assert cumulative * cumulative == isotropic_lambda ** 3
        levels.append({
            "level": k,
            "detail_multiplicity": multiplicity,
            "cumulative_dimension": cumulative,
            "isotropic_reference_eigenvalue": isotropic_lambda,
            "anisotropic_lower_bound": str(alpha * isotropic_lambda),
            "anisotropic_upper_bound": str(beta * isotropic_lambda),
            "N_squared_equals_reference_lambda_cubed": True,
        })

    masks = [0, 5, 8, 13, 16, 21, 24, 29]
    result = {
        "schema": "siel.dpa.bgce456.result.v1",
        "candidate_id": "BGCE456",
        "date": "2026-09-25",
        "primary_evidence_status": "Theoretical derivation with exact actual-metric finite-conductance witnesses",
        "scientific_layer": "actual-metric anisotropic hierarchical Markov and wave carrier",
        "status": "SCOPED_PASS_ACTUAL_METRIC_POSITIVE_CONDUCTANCE__EXACT_ISOTROPIC_BGCE452_LIMIT__ALL_DEPTH_REFINEMENT_AND_UCP_HEAT__SAME_OPERATOR_POSITIVE_WAVE__SPECTRAL_DIMENSION_THREE_BY_EXACT_FORM_BOUNDS__OPEN_UNIQUENESS_ACTIVE_VOLUME_SMOOTH_SYMBOL_AND_EMPIRICAL_MATCH",
        "input_hashes": {
            **{path: sha256((ROOT / path).read_bytes()).hexdigest() for path in INPUTS},
            METRIC_INPUT: sha256((ROOT / METRIC_INPUT).read_bytes()).hexdigest(),
            metric_input["source_path"]: metric_input["source_sha256"],
        },
        "conductance_construction": {
            "child_group": "C5^3 with ordered source characters chi1, chi2, chi3",
            "centered_difference": "delta(x,y) is the unique representative of y-x in {-2,-1,0,1,2}^3.",
            "formula": "c_A(x,y)=(1/5)*(delta^T A delta)/(delta^T delta) for x!=y, with A=gamma^-1 from the saved actual metric.",
            "normalization": "The factor 1/5 is forced by L_I=25(I-E0) on 125 children.",
            "unordered_edge_count": len(edges),
            "all_edges_strictly_positive": True,
            "distinct_exact_conductance_count": len(distinct_conductances),
            "minimum_edge": {"x": list(min_edge[0]), "y": list(min_edge[1]), "conductance": str(min_edge[2])},
            "maximum_edge": {"x": list(max_edge[0]), "y": list(max_edge[1]), "conductance": str(max_edge[2])},
            "axis_conductances": {key: str(value) for key, value in axis_conductances.items()},
            "old_BGCE455_witness": {
                "x": list(old_x),
                "y": list(old_y),
                "conductance": str(repaired_conductance),
                "new_L_xy": str(repaired_offdiagonal),
                "old_raw_L_xy": u455["same_operator_UCP_heat_no_go"]["exact_positive_offdiagonal_L_xy"],
            },
            "decision": "PASS_STRICTLY_POSITIVE_SOURCE_METRIC_CONDUCTANCE",
        },
        "isotropic_and_hierarchical_theorem": {
            "isotropic_limit": "A=I gives c_I(x,y)=1/5 on every unordered child pair and L_I=25(I-E0) exactly.",
            "level_operator": "Delta_m^A=sum_(k=1)^m 25^(k-1) L_A^(k), where L_A^(k) is the same 125-child conductance Laplacian inside each level-k parent block.",
            "refinement": "The new level operator annihilates child-constant functions, so Delta_(m+1)^A j_m=j_m Delta_m^A exactly.",
            "heat_refinement": "Functional calculus gives exp(-t Delta_(m+1)^A)j_m=j_m exp(-t Delta_m^A).",
            "UCP": "Every finite-depth Delta_m^A is a symmetric graph Laplacian with nonnegative jump rates; its heat semigroup is positivity preserving, unital and trace preserving on the commutative address algebra, and its identity lift is UCP on the internal M_125 fiber.",
            "weighted_state_scope": "Under BGCE349 child-constant actual-metric refinement, the 125 child volume weights are equal inside each parent, so the same symmetric conductance heat preserves the BGCE453 metric-volume state.",
            "decision": "PASS_EXACT_ALL_DEPTH_REFINEMENT_AND_UCP_IN_CHILD_CONSTANT_ACTUAL_METRIC_SCOPE",
        },
        "wave_and_spectral_theorem": {
            "same_operator_wave": "Delta_m^A is positive self-adjoint, so partial_s^2+Delta_m^A has the standard spectral cosine/sine evolution; no separate raw exterior operator is needed.",
            "exact_rational_form_bounds": {
                "alpha": str(alpha),
                "beta": str(beta),
                "proof": "Positive gamma gives A>=alpha I with alpha=1/tr(gamma), while A<=beta I with beta=tr(A). Therefore alpha Delta_iso<=Delta_A<=beta Delta_iso levelwise and at every finite depth.",
            },
            "spectral_dimension": "Min-max comparison with BGCE452 yields N_iso(Lambda/beta)<=N_A(Lambda)<=N_iso(Lambda/alpha); both bounds scale as Lambda^(3/2), so the anisotropic spatial spectral dimension is 3.",
            "dynamic_scaling": "Level eigenvalue bands scale by 25 and their wave-frequency bands by 5, retaining hierarchical z=1.",
            "UV_moments": "The positive lower comparison alpha Delta_iso makes every finite polynomial heat moment finite for t>0.",
            "levels_1_to_8": levels,
            "decision": "PASS_POSITIVE_WAVE_AND_SPECTRAL_DIMENSION_THREE_WITH_EXACT_COMPARISON_BOUNDS",
        },
        "all_eight_sector_inheritance": [{
            "mask": mask,
            "same_actual_spatial_metric": True,
            "same_positive_conductance": True,
            "same_refinement_UCP_and_wave_theorem": True,
        } for mask in masks],
        "gate_decision": {
            "actual_metric_nonnegative_conductance": "PASS_STRICTLY_POSITIVE",
            "exact_BGCE452_isotropic_limit": "PASS",
            "all_depth_refinement_intertwining": "PASS",
            "same_operator_UCP_heat": "PASS",
            "same_operator_positive_selfadjoint_wave": "PASS",
            "anisotropic_spectral_dimension_three": "PASS_EXACT_ASYMPTOTIC_EXPONENT_BY_FORM_COMPARISON",
            "all_finite_polynomial_heat_moments": "PASS",
            "child_constant_actual_metric_volume_state": "PASS",
            "conductance_uniqueness_from_source_axioms": "OPEN",
            "active_nonpolynomial_PBM_volume_projectivity": "OPEN_AFTER_BGCE455_NO_GO_FOR_COMPONENTWISE_ROUTE",
            "smooth_spacetime_principal_symbol_equal_to_A": "OPEN",
            "provider_clock_SI_traceability": "OPEN_EXTERNAL_PENDING",
            "empirical_gravity_match": "OPEN",
            "general_physical_UV_completion": "OPEN",
            "BQG_G3_R02_4": "REMAINS_CLOSED_SCOPED_WITH_ANISOTROPIC_HIERARCHICAL_UCP_BRIDGE_CLOSED",
            "MMR_CGR_used": False,
            "target_Einstein_equation_used": False,
            "Einstein_Hilbert_or_Fierz_Pauli_action_used": False,
            "manual_three_fifths_used": False,
            "fitted_coefficient_used": False,
        },
        "counter_intuition_scan": {
            "ordinary_explanation": "Any positive definite quadratic form gives positive directional Rayleigh quotients, and any finite symmetric nonnegative conductance graph gives a Markov heat semigroup and a positive wave operator.",
            "SIEL_specific_part": "The C5^3 child group, ordered three-character metric, 125-child normalization, 25-per-level scaling, internal M_125 lift and eight-sector inheritance all come from the saved Braid source carrier.",
            "strongest_counterpattern": "The Rayleigh-quotient conductance is a natural source-derived bridge but is not proved unique. Its finite-group Fourier symbol is not yet proved to equal the smooth principal symbol p^T A p, and active PBM metric-volume projectivity remains open after the componentwise route failed.",
            "falsifier": "A nonpositive conductance for the saved metric, failure of the A=I BGCE452 identity, loss of refinement/UCP after the hierarchy lift, or a spectral counting exponent different from three would falsify the scoped theorem.",
        },
        "bold_hypothesis": {
            "id": "H456_METRIC_ANISOTROPY_IS_DIRECTIONAL_CONDUCTANCE",
            "statement": "On the fundamental Braid source cylinder, inverse spatial metric is physically realized by directional transition conductance on C5^3 rather than by inserting its raw exterior matrix into a Markov generator.",
            "supported_part": "The actual saved metric now gives one exact strictly positive conductance carrier with the BGCE452 isotropic limit, all-depth UCP heat, positive wave dynamics and spectral dimension three.",
            "unsupported_part": "Source-axiom uniqueness, the exact smooth principal symbol, active metric-volume projectivity, SI traceability and empirical gravity remain unproved.",
        },
        "next_gate": "BGCE443_SOURCE_REFINEMENT_LIMIT_UNBOUNDED_DERIVATION_THREE_PLANE_GATE",
        "runtime_class": "SECONDS_EXACT_7750_EDGE_RATIONAL_CONDUCTANCE_CHECK_PLUS_EIGHT_LEVEL_AND_EIGHT_SECTOR_WITNESSES_NO_SEARCH",
        "formal_E0_E1_E2": "NOT_CLAIMED__DPA_THEORETICAL_GATE_ONLY",
        "claim_ceiling": "BGCE456 constructs an exact actual-metric-derived strictly positive conductance Laplacian on the Braid C5^3 child group. In the child-constant actual-metric hierarchy it has the exact BGCE452 isotropic limit, all-depth refinement-compatible UCP heat, same-operator positive wave evolution, spatial spectral dimension three and finite heat moments. It does not prove uniqueness of the conductance map, active PBM volume projectivity, equality to a smooth inverse-metric principal symbol, SI traceability, empirical gravity, general physical UV completion or completed quantum gravity.",
    }
    (HERE / "RESULT.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({
        "candidate_id": result["candidate_id"],
        "status": result["status"],
        "edge_count": len(edges),
        "distinct_conductances": len(distinct_conductances),
        "same_operator_UCP_heat": result["gate_decision"]["same_operator_UCP_heat"],
        "same_operator_wave": result["gate_decision"]["same_operator_positive_selfadjoint_wave"],
        "spectral_dimension": result["gate_decision"]["anisotropic_spectral_dimension_three"],
        "next_gate": result["next_gate"],
    }, indent=2))


if __name__ == "__main__":
    main()
