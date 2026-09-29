#!/usr/bin/env python3
"""BGCE291: independent red-team of the BGCE290 stress/Ward promotion."""

from fractions import Fraction
from hashlib import sha256
from itertools import combinations_with_replacement
from pathlib import Path
import json
import subprocess

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
REVISION = "f91912dad311897cd4d658f7aa8718c5dccf6b53"


def rank(matrix):
    a = [[Fraction(x) for x in row] for row in matrix]
    if not a:
        return 0
    m, n, r = len(a), len(a[0]), 0
    for c in range(n):
        pivot = next((i for i in range(r, m) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        q = a[r][c]
        a[r] = [x / q for x in a[r]]
        for i in range(m):
            if i != r and a[i][c]:
                q = a[i][c]
                a[i] = [a[i][j] - q * a[r][j] for j in range(n)]
        r += 1
        if r == m:
            break
    return r


def frozen_bytes(path):
    return subprocess.check_output(["git", "show", f"{REVISION}:{path}"], cwd=ROOT)


def frozen_json(path):
    return json.loads(frozen_bytes(path))


def permutation_matrix(permutation):
    p = [[0] * 4 for _ in range(4)]
    for old, new in enumerate(permutation):
        p[new][old] = 1
    return p


PAIRS = list(combinations_with_replacement(range(4), 2))


def sym2_permutation_rep(permutation):
    pair_index = {pair: i for i, pair in enumerate(PAIRS)}
    r = [[0] * 10 for _ in range(10)]
    for col, (i, j) in enumerate(PAIRS):
        pair = tuple(sorted((permutation[i], permutation[j])))
        r[pair_index[pair]][col] = 1
    return r


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def sym2_congruence_rep(u):
    cols = []
    for i, j in PAIRS:
        a = [[Fraction(0) for _ in range(4)] for _ in range(4)]
        a[i][j] = Fraction(1, 2) if i != j else Fraction(1)
        a[j][i] = Fraction(1, 2) if i != j else Fraction(1)
        ua = matmul(list(map(list, zip(*u))), matmul(a, u))
        cols.append([ua[x][y] if x == y else 2 * ua[x][y] for x, y in PAIRS])
    return [list(row) for row in zip(*cols)]


def commutant_dimension(representations):
    equations = []
    for r in representations:
        for i in range(10):
            for j in range(10):
                row = [0] * 100
                for k in range(10):
                    row[i * 10 + k] += r[k][j]
                    row[k * 10 + j] -= r[i][k]
                equations.append(row)
    return 100 - rank(equations)


def main():
    matrix = json.loads((HERE / "SOURCE_MATRIX.json").read_text())
    checked = {}
    for path, expected in matrix["inputs_sha256"].items():
        payload = frozen_bytes(path)
        actual = sha256(payload).hexdigest()
        assert actual == expected
        checked[f"{REVISION}:{path}"] = actual

    p148 = frozen_json("audits/SRA_DPA_BGCE148_SOURCE_METRIC_FUNCTIONAL_TO_CTP_DIFFERENCE_GEOMETRY_NATURALITY_GATE_20260920/RESULT.json")
    p150 = frozen_json("audits/SRA_DPA_BGCE150_PREDECLARED_CHARACTER_OBSERVABLE_NULL_GRAM_AND_SOURCE_SOLDER_GATE_20260920/RESULT.json")
    p256 = frozen_json("audits/SRA_DPA_BGCE256_BRAID_INDUCED_EVENT_TRANSITION_COBORDER_TO_NEIGHBOR_COUPLING_LAW_GATE_20260921/RESULT.json")
    p267 = frozen_json("audits/SRA_DPA_BGCE267_SOURCE_DERIVED_IR_ACTION_TO_OFF_SHELL_STRESS_AND_WARD_NOETHER_GATE_20260922/RESULT.json")
    p268 = frozen_json("audits/SRA_DPA_BGCE268_SOURCE_GRAM_SCHUR_CHANNEL_TO_CAUSAL_METRIC_INTERTWINER_GATE_20260922/RESULT.json")
    p284 = frozen_json("audits/SRA_DPA_BGCE284_LOCAL_GL4_NATURALITY_AND_VARIATIONAL_STRESS_WARD_GATE_20260923/RESULT.json")
    p285 = frozen_json("audits/SRA_DPA_BGCE285_SOURCE_CYLINDER_MEASURE_AND_MARKOV_NATURALITY_TO_UNIQUE_MINIMAL_COVARIANT_PARENT_GATE_20260923/RESULT.json")
    p286 = frozen_json("audits/SRA_DPA_BGCE286_X21R1_METRIC_TANGENT_TO_BRAID_EVENT_CONDUCTANCE_VARIATION_GATE_20260923/RESULT.json")
    p287 = frozen_json("audits/SRA_DPA_BGCE287_SOURCE_EVENT_PATH_BKM_HORIZONTAL_CONDUCTANCE_LIFT_GATE_20260923/RESULT.json")
    p289 = frozen_json("audits/SRA_DPA_BGCE289_THETA_ODD_ANALYTIC_INTEGRABILITY_AND_HILBERT_INDEPENDENCE_GATE_20260923/RESULT.json")
    p290 = frozen_json("audits/SRA_DPA_BGCE290_INDEPENDENT_DOUBLED_A_SOURCE_TO_CAUSAL_METRIC_HILBERT_WARD_GATE_20260923/RAW_OUTPUT.json")

    source141 = frozen_bytes("audits/SRA_DPA_BGCE141_SOURCE_MARK_CHARGE_CYLINDER_CURRENT_TO_DOUBLED_METRIC_STRESS_FUNCTOR_GATE_20260919/evaluate.py").decode()
    source142 = frozen_bytes("audits/SRA_DPA_BGCE142_CHARGE_MIXED_RESPONSE_TO_LOCAL_DOUBLED_INFLUENCE_FUNCTIONAL_GATE_20260919/evaluate.py").decode()
    source_typed = all(token in source141 for token in [
        "observables = [generator, *spatial_observables]",
        "metric_functionals = [[None for _ in range(4)] for _ in range(4)]",
    ]) and "sum_A a_A F_A" in source142
    assert source_typed
    assert p148["positive_local_duality"]["local_inverse"] is True
    assert p148["positive_local_duality"]["physical_metric_identification"] is False

    u = [[Fraction(x, 2) for x in row] for row in [
        [1, 1, 1, 1],
        [1, 1, -1, -1],
        [1, -1, 1, -1],
        [1, -1, -1, 1],
    ]]
    induced = sym2_congruence_rep(u)
    induced_rank = rank(induced)
    assert induced_rank == p290["independent_metric_source_solder"]["Sym2_rank"] == 10

    generators = [
        (1, 0, 2, 3),
        (0, 2, 1, 3),
        (0, 1, 3, 2),
    ]
    source_reps = [sym2_permutation_rep(g) for g in generators]
    commutant_dim = commutant_dimension(source_reps)
    assert commutant_dim == 9

    fixed_carrier_only = (
        p268["spacetime_metric_deformation_naturality"] == "OPEN"
        and p268["Hilbert_stress_and_Ward_from_channel"] == "OPEN"
        and p150["comparison"]["physical_natural_intertwiner_derived"] is False
    )
    assert fixed_carrier_only

    first_order_only = (
        p286["first_order_curved_conductance_lift_existence"] == "PASS"
        and p287["active_source_Markov_transport_first_variation"] == "SOURCE_SELECTED_CANONICAL_CANDIDATE"
        and p287["full_nonlinear_integrability"] == "OPEN"
        and p287["full_finite_physical_parent_action"] == "OPEN"
    )
    assert first_order_only

    prior_nonuniqueness_survives = (
        p267["off_shell_metric_variation_uniquely_derived"] is False
        and p267["minimal_alpha_zero_is_currently_Braid_derived"] is False
        and p284["active_source_dynamics_under_arbitrary_GL4"] is False
        and p285["active_source_Markov_transport_over_curved_off_shell_metrics"] == "OPEN"
        and p285["minimal_parent_action_source_derived"] is False
    )
    assert prior_nonuniqueness_survives
    assert p256["Ward_derived"] is False
    assert p289["independent_a_to_physical_7plus3_metric_solder"] == "OPEN"

    # Red-team finding: these BGCE290 values were assigned after a coframe
    # identity; no frozen input supplies the missing finite nonlinear theorem.
    source290 = frozen_bytes("audits/SRA_DPA_BGCE290_INDEPENDENT_DOUBLED_A_SOURCE_TO_CAUSAL_METRIC_HILBERT_WARD_GATE_20260923/evaluate.py").decode()
    promoted_literal_assignments = all(token in source290 for token in [
        "active_event_coframe_transport = True",
        "curvature_potential_excluded_in_declared_class = True",
        "hilbert_stress_derived = True",
        "ward_identity_derived = True",
    ])
    assert promoted_literal_assignments

    output = {
        "schema": "siel.dpa.bgce291.raw.v1",
        "candidate_id": "BGCE291",
        "source_revision": REVISION,
        "input_hashes_verified": checked,
        "baseline_gate": "PASS_REVISION_MATCHED_PRIMARY_CODE_AND_BGCE148_150_256_267_268_284_285_286_287_289_290",
        "primary_evidence_status": "Independent theoretical scope audit with exact representation countercheck",
        "scientific_layer": "source typing, solder selection, active Markov transport and action provenance",
        "gate_results": {
            "G1_independent_a_source_typing": "PASS_FORMAL_DUAL_SOURCE_TO_TEN_SYMMETRIC_FUNCTIONALS",
            "G2_algebraic_Sym2_Hadamard_solder": "PASS_RANK10_CANONICAL_CANDIDATE",
            "G2_physical_solder_uniqueness": "FAIL_NOT_SELECTED_BY_S4_OR_FIXED_CARRIER_RESULTS",
            "G3_finite_nonlinear_active_Markov_transport": "FAIL_OPEN_FIRST_ORDER_CONNECTION_ONLY",
            "G4_same_source_derived_off_shell_action": "FAIL_CONDITIONAL_MINIMAL_PARENT_ONLY",
            "Hilbert_stress_Braid_only": "NOT_DERIVED",
            "Ward_Braid_only": "NOT_DERIVED",
        },
        "exact_checks": {
            "Sym2_Hadamard_rank": induced_rank,
            "S4_Sym2_commutant_dimension": commutant_dim,
            "S4_equivariance_selects_unique_solder": False,
            "BGCE290_promoted_conclusions_are_literal_assignments_after_strain_check": promoted_literal_assignments,
        },
        "surviving_result": {
            "independent_a_source_exists": True,
            "rank10_source_to_metric_candidate_exists": True,
            "fixed_matter_rank7_lock_has_an_algebraic_candidate_bypass": True,
            "physical_off_shell_selection": "OPEN",
            "first_order_BKM_horizontal_conductance_connection": "RETAINED",
            "finite_nonlinear_integrability": "OPEN",
        },
        "reversal": {
            "BGCE290_FULL_PASS": "NOT_SUSTAINED",
            "BGCE290_algebraic_rank10_solder": "RETAINED_AS_CANDIDATE",
            "BGCE290_active_transport": "REVERT_TO_OPEN",
            "BGCE290_Hilbert_stress": "REVERT_TO_CONDITIONAL",
            "BGCE290_Ward": "REVERT_TO_CONDITIONAL",
            "reason": "A pointwise coframe strain identity neither selects a physical solder from the nine-dimensional S4-equivariant commutant nor integrates the source-selected first-order conductance connection to a finite curved Markov family."
        },
        "shortest_missing_theorem": "Integrate the BGCE287 BKM-horizontal first-order conductance connection over the BGCE289 finite rank-ten metric neighborhood and prove path independence, positivity, detailed balance, refinement compatibility and equality of its continuum limit to the varied BKM parent; simultaneously show the physical a-to-metric solder is selected beyond S4 covariance.",
        "next_gate": "BGCE292_BKM_HORIZONTAL_CONNECTION_CURVATURE_AND_LOCAL_PATH_INDEPENDENCE_GATE",
        "decision": "RED_TEAM_PARTIAL_REVERSAL__THE_INDEPENDENT_TEN_A_SOURCES_AND_EXACT_RANK_TEN_HADAMARD_SYM2_MAP_SURVIVE_AS_AN_ALGEBRAIC_SOLDER_CANDIDATE__BUT_S4_EQUIVARIANCE_HAS_A_NINE_DIMENSIONAL_COMMUTANT_AND_THE_FIXED_CARRIER_RESULT_DOES_NOT_SELECT_AN_OFF_SHELL_PHYSICAL_METRIC_SOLDER__THE_SOURCE_RECORD_DERIVES_ONLY_A_FIRST_ORDER_BKM_HORIZONTAL_CONDUCTANCE_CONNECTION_WITH_NONLINEAR_INTEGRABILITY_AND_FULL_FINITE_PARENT_EXPLICITLY_OPEN__BGCE290_PROMOTED_ACTIVE_TRANSPORT_CURVATURE_EXCLUSION_HILBERT_STRESS_AND_WARD_BY_LITERAL_ASSIGNMENT_AFTER_A_POINTWISE_COFRAME_IDENTITY__THEREFORE_THE_FULL_PASS_IS_NOT_SUSTAINED_AND_BRAID_ONLY_HILBERT_STRESS_WARD_REMAIN_OPEN",
        "runtime_class": "SUBSECOND_EXACT_RATIONAL_REPRESENTATION_AND_SCOPE_AUDIT_NO_SCAN",
        "formal_E0_E1_E2": "NOT_CLAIMED__DPA_THEORETICAL_GATE_ONLY",
        "claim_ceiling": "BGCE291 independently confirms the formal ten-source typing and exact rank-ten Hadamard Sym2 solder candidate, but proves that S4 equivariance alone leaves a nine-dimensional commutant and confirms that the existing source record reaches only a first-order BKM-horizontal conductance connection with nonlinear integrability and the full finite parent still open. It therefore reverses BGCE290's active-transport and source-derived Hilbert/Ward promotions to conditional status. It does not refute the candidate solder, establish that no stronger Braid selector exists, derive Einstein dynamics, empirical gravity or completed quantum gravity."
    }
    (HERE / "RAW_OUTPUT.json").write_text(json.dumps(output, indent=2) + "\n")
    print(output["decision"])


if __name__ == "__main__":
    main()
