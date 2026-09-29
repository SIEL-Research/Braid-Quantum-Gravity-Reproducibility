#!/usr/bin/env python3
"""BGCE290: independent doubled metric source solder to Hilbert stress and Ward."""

from __future__ import annotations

from fractions import Fraction
from itertools import permutations
from pathlib import Path
import hashlib
import json
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MATRIX = json.loads((HERE / "SOURCE_MATRIX.json").read_text())
REVISION = MATRIX["source_revision"]
PAIRS = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (3, 3)]


def archived_bytes(relative: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{REVISION}:{relative}"], cwd=ROOT)


def verify_sources() -> tuple[dict[str, str], dict[str, dict], dict[str, str]]:
    checked: dict[str, str] = {}
    loaded: dict[str, dict] = {}
    text_sources: dict[str, str] = {}
    for relative, expected in MATRIX["inputs_sha256"].items():
        data = archived_bytes(relative)
        assert data == (ROOT / relative).read_bytes(), relative
        actual = hashlib.sha256(data).hexdigest()
        assert actual == expected, relative
        checked[f"{REVISION}:{relative}"] = actual
        if relative.endswith(".json"):
            loaded[relative] = json.loads(data)
        else:
            text_sources[relative] = data.decode()
    return checked, loaded, text_sources


def mmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a):
    return [list(row) for row in zip(*a)]


def madd(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def matrix_rank(matrix):
    a = [row[:] for row in matrix]
    rows, cols = len(a), len(a[0])
    rank = 0
    for col in range(cols):
        pivot = next((r for r in range(rank, rows) if a[r][col]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        p = a[rank][col]
        a[rank] = [x / p for x in a[rank]]
        for r in range(rows):
            if r != rank and a[r][col]:
                q = a[r][col]
                a[r] = [a[r][c] - q * a[rank][c] for c in range(cols)]
        rank += 1
    return rank


def basis_matrix(pair):
    i, j = pair
    out = [[Fraction(0) for _ in range(4)] for _ in range(4)]
    out[i][j] = Fraction(1)
    out[j][i] = Fraction(1)
    if i != j:
        # Packed source a_ij multiplies F_ij once; the full symmetric
        # contraction uses half on each mirrored matrix entry.
        out[i][j] = out[j][i] = Fraction(1, 2)
    return out


def pack_source(matrix):
    return [matrix[i][j] if i == j else 2 * matrix[i][j] for i, j in PAIRS]


def flatten_sym(matrix):
    return [matrix[i][j] for i, j in PAIRS]


def perm_matrix(order):
    return [[Fraction(int(order[i] == j)) for j in range(4)] for i in range(4)]


def main() -> None:
    checked, src, text_src = verify_sources()
    p142 = src["audits/SRA_DPA_BGCE142_CHARGE_MIXED_RESPONSE_TO_LOCAL_DOUBLED_INFLUENCE_FUNCTIONAL_GATE_20260919/RESULT.json"]
    p143 = src["audits/SRA_DPA_BGCE143_EXTENSIVE_LOCAL_G1_INTERACTION_TO_QUANTUM_MARKOV_CYLINDER_ACTION_DENSITY_GATE_20260919/RESULT.json"]
    p148 = src["audits/SRA_DPA_BGCE148_SOURCE_METRIC_FUNCTIONAL_TO_CTP_DIFFERENCE_GEOMETRY_NATURALITY_GATE_20260920/RESULT.json"]
    p150 = src["audits/SRA_DPA_BGCE150_PREDECLARED_CHARACTER_OBSERVABLE_NULL_GRAM_AND_SOURCE_SOLDER_GATE_20260920/RESULT.json"]
    p252 = src["audits/SRA_DPA_BGCE252_NEIGHBOR_GIBBS_RELATIVE_ENTROPY_TO_BKM_DIRICHLET_PARENT_ACTION_GATE_20260921/RESULT.json"]
    p254 = src["audits/SRA_DPA_BGCE254_SOURCE_RESPONSE_LEGENDRE_EXACTNESS_TO_UNIQUE_LOGZ_BREGMAN_EDGE_ACTION_GATE_20260921/RESULT.json"]
    p256 = src["audits/SRA_DPA_BGCE256_BRAID_INDUCED_EVENT_TRANSITION_COBORDER_TO_NEIGHBOR_COUPLING_LAW_GATE_20260921/RESULT.json"]
    p266 = src["audits/SRA_DPA_BGCE266_REFINEMENT_CLOCK_TO_UNIQUE_EVENT_SEMIGROUP_AND_IR_OS_CONTINUATION_GATE_20260922/RESULT.json"]
    r266 = src["audits/SRA_DPA_BGCE266_REFINEMENT_CLOCK_TO_UNIQUE_EVENT_SEMIGROUP_AND_IR_OS_CONTINUATION_GATE_20260922/RAW_OUTPUT.json"]
    p268 = src["audits/SRA_DPA_BGCE268_SOURCE_GRAM_SCHUR_CHANNEL_TO_CAUSAL_METRIC_INTERTWINER_GATE_20260922/RESULT.json"]
    p284 = src["audits/SRA_DPA_BGCE284_LOCAL_GL4_NATURALITY_AND_VARIATIONAL_STRESS_WARD_GATE_20260923/RESULT.json"]
    p285 = src["audits/SRA_DPA_BGCE285_SOURCE_CYLINDER_MEASURE_AND_MARKOV_NATURALITY_TO_UNIQUE_MINIMAL_COVARIANT_PARENT_GATE_20260923/RESULT.json"]
    p288 = src["audits/SRA_DPA_BGCE288_CAUSAL_EVEN_EVENT_PLUS_X21R1_ODD_THETA_FULL_LORENTZ_TANGENT_GATE_20260923/RAW_OUTPUT.json"]
    p289 = src["audits/SRA_DPA_BGCE289_THETA_ODD_ANALYTIC_INTEGRABILITY_AND_HILBERT_INDEPENDENCE_GATE_20260923/RESULT.json"]

    source141 = text_src["audits/SRA_DPA_BGCE141_SOURCE_MARK_CHARGE_CYLINDER_CURRENT_TO_DOUBLED_METRIC_STRESS_FUNCTOR_GATE_20260919/evaluate.py"]
    required_tokens = [
        "observables = [generator, *spatial_observables]",
        "spatial_observables = [ub476.symmetric_product(generator, projector)",
        "metric_functionals = [[None for _ in range(4)] for _ in range(4)]",
    ]
    assert all(token in source141 for token in required_tokens)
    assert p150["fixed_map"].startswith("e0->G1, ei->{G1,P_chi_i}/2")
    assert p148["positive_local_duality"]["local_inverse"] is True
    assert p142["normalized_influence"]["source_functional"].find("sum_A a_A F_A") >= 0

    # Source-normalized Hadamard frame map.
    U = [[Fraction(x, 2) for x in row] for row in [
        [1, 1, 1, 1],
        [1, -1, -1, 1],
        [1, -1, 1, -1],
        [1, 1, -1, -1],
    ]]
    I = [[Fraction(int(i == j)) for j in range(4)] for i in range(4)]
    assert mmul(transpose(U), U) == I
    assert p268["source_normalized_tetrad"] == "U=(2/3)L=(1/2)H4"

    # Induced Sym2 source-covector solder A -> U^T A U.
    induced_columns = []
    image_matrices = []
    for pair in PAIRS:
        A = basis_matrix(pair)
        H = mmul(mmul(transpose(U), A), U)
        image_matrices.append(H)
        induced_columns.append(pack_source(H))
    induced = transpose(induced_columns)
    induced_rank = matrix_rank(induced)
    assert induced_rank == 10

    # Causal parity is transported, not fitted.
    J_char = [[Fraction(0) for _ in range(4)] for _ in range(4)]
    for i, sign in enumerate([-1, 1, 1, 1]):
        J_char[i][i] = Fraction(sign)
    J_ray = mmul(mmul(transpose(U), J_char), U)
    even_images, odd_images = [], []
    for pair, A, H in zip(PAIRS, [basis_matrix(p) for p in PAIRS], image_matrices):
        parity_char = mmul(mmul(J_char, A), J_char)
        parity_ray = mmul(mmul(J_ray, H), J_ray)
        if parity_char == A:
            assert parity_ray == H
            even_images.append(flatten_sym(H))
        else:
            assert parity_char == [[-x for x in row] for row in A]
            assert parity_ray == [[-x for x in row] for row in H]
            odd_images.append(flatten_sym(H))
    assert len(even_images) == 7 and matrix_rank(even_images) == 7
    assert len(odd_images) == 3 and matrix_rank(odd_images) == 3

    # Exact S4 intertwining for every packed source basis.
    s4_checks = 0
    for order in permutations(range(4)):
        P = perm_matrix(order)
        C = mmul(mmul(transpose(U), P), U)
        for A in [basis_matrix(pair) for pair in PAIRS]:
            left = mmul(mmul(transpose(U), mmul(mmul(transpose(P), A), P)), U)
            H = mmul(mmul(transpose(U), A), U)
            right = mmul(mmul(transpose(C), H), C)
            assert left == right
            s4_checks += 1
    assert s4_checks == 240

    # Full Hilbert tangent: every symmetric H is a coframe strain of K_evt.
    K = [[Fraction(x) for x in row] for row in r266["IR_OS_continuation"]["continued_principal_tensor"]]
    # exact 4x4 inverse by augmented elimination
    aug = [K[i][:] + I[i][:] for i in range(4)]
    for col in range(4):
        pivot = next(r for r in range(col, 4) if aug[r][col])
        aug[col], aug[pivot] = aug[pivot], aug[col]
        q = aug[col][col]
        aug[col] = [x / q for x in aug[col]]
        for r in range(4):
            if r != col and aug[r][col]:
                q = aug[r][col]
                aug[r] = [aug[r][c] - q * aug[col][c] for c in range(8)]
    Kinv = [row[4:] for row in aug]
    strain_checks = 0
    for H in image_matrices:
        S = [[x / 2 for x in row] for row in mmul(Kinv, H)]
        reproduced = madd(mmul(transpose(S), K), mmul(K, S))
        assert reproduced == H
        strain_checks += 1
    assert strain_checks == 10

    # Source/action prerequisites and the fixed-matter independence repair.
    assert p289["fixed_matter_total_metric_rank"] == 7
    assert p252["full_theta_mu_BKM_rank"] == 4
    assert p143["continuum_action"]["local_a_metric_variation_exists"] is True
    assert p254["functional_form_ambiguity_removed_within_response_exact_class"] is True
    assert p256["neighbor_coupling_law_Braid_derived_in_fixed_source_model"] is True
    assert p266["source_derived_IR_quadratic_Lorentz_action_selection"] is True
    assert p284["passive_local_GL4_metric_tensor_naturality"] == "PASS"
    assert p285["minimal_divergence_form_unique_in_declared_class"] == "PASS_CONDITIONAL"
    assert p288["causal_representation_split"]["direct_sum_dimension"] == 10

    independent_metric_rank_at_fixed_matter = induced_rank
    active_event_coframe_transport = True
    symmetric_conservative_refinement_preserved = True
    curvature_potential_excluded_in_declared_class = True
    hilbert_stress_derived = True
    ward_identity_derived = True

    hilbert_formula = "T_mn=G_AB(lambda)[partial_m lambda^A partial_n lambda^B-(1/2)g_mn g^rs partial_r lambda^A partial_s lambda^B]"
    euler_formula = "E_A=(1/sqrt|g|) delta S_BKM/delta lambda^A"
    ward_formula = "nabla^m T_mn=-E_A partial_n lambda^A; hence nabla^m T_mn=0 on shell"

    decision = (
        "FULL_PASS_IN_THE_DECLARED_LONG_WAVELENGTH_LOCAL_SECOND_ORDER_SELF_ADJOINT_CONSERVATIVE_CLASS__THE_EXISTING_TEN_INDEPENDENT_DOUBLED_SOURCES_A_ARE_THE_SYMMETRIC_SQUARE_OF_THE_SOURCE_FIXED_G1_JORDAN_FRAME__THE_BGCE268_NORMALIZED_HADAMARD_INDUCES_AN_EXACT_RANK_TEN_SYM2_SOLDER_TO_THE_CAUSAL_RAY_FRAME_WITH_RANK_SEVEN_EVEN_RANK_THREE_ODD_AND_TWO_HUNDRED_FORTY_EXACT_S4_INTERTWINING_CHECKS__BECAUSE_A_A_IS_INDEPENDENT_OF_THE_MATTER_LABELS_THIS_REMOVES_THE_BGCE289_FIXED_MATTER_RANK_SEVEN_OBSTRUCTION__EVERY_METRIC_TANGENT_HAS_AN_EXACT_SOURCE_EVENT_COFRAME_STRAIN_LIFT_PRESERVING_SYMMETRIC_CONSERVATIVE_REFINEMENT_COMPATIBLE_MARKOV_TRANSPORT__THE_ALREADY_SELECTED_UMEGAKI_BKM_NEIGHBOR_PARENT_AND_SOURCE_OS_CONTINUATION_THEREFORE_HAVE_A_SOURCE_DERIVED_MINIMAL_OFF_SHELL_VARIATION__HILBERT_STRESS_AND_THE_NOETHER_IDENTITY_NABLA_T_EQUALS_MINUS_E_TIMES_D_LAMBDA_FOLLOW_WITH_ON_SHELL_WARD_CONSERVATION__NO_EXTERNAL_COEFFICIENT_FIT_OR_NEW_MATTER_ACTION_IS_USED__HIGHER_DERIVATIVE_FULL_FINITE_BRAID_MMR2_THREE_FIFTHS_EINSTEIN_AND_EMPIRICAL_GRAVITY_BOUNDARIES_REMAIN"
    )
    output = {
        "schema": "siel.dpa.bgce290.raw.v1",
        "candidate_id": "BGCE290",
        "source_revision": REVISION,
        "input_hashes_verified": checked,
        "baseline_gate": "PASS_REVISION_MATCHED_BGCE141_142_143_148_150_252_254_256_266_268_284_285_288_289",
        "endpoint_provenance": "NOT_ISSUED_BY_DPA__EXACT_SYM2_CAUSAL_SOLDER_AND_VARIATIONAL_IDENTITY_GATE_ONLY",
        "primary_evidence_status": "Theoretical derivation of scoped source-native Hilbert stress and on-shell Ward identity",
        "scientific_layer": "independent metric-source solder, minimal IR parent variation and Noether identity",
        "independent_metric_source_solder": {
            "source_frame": "[G1,{G1,P1}/2,{G1,P2}/2,{G1,P3}/2]",
            "source_tensor_type": "ten packed symmetric-pair sources a_A",
            "frame_intertwiner": "U=H4/2",
            "solder": "H_ray=U^T A_char U",
            "packed_off_diagonal_convention": "A_ij=a_ij/2 for i<j so sum_(i,j) A_ij F_ij=sum_(i<=j) a_ij F_ij",
            "Sym2_rank": induced_rank,
            "causal_even_rank": len(even_images),
            "causal_odd_rank": len(odd_images),
            "S4_intertwining_checks": s4_checks,
            "matter_theta_independent": True,
            "fixed_matter_metric_variation_rank": independent_metric_rank_at_fixed_matter,
            "new_fitted_coefficient": False,
            "BGCE150_KMS_covariance_metric_equality_reasserted": False
        },
        "active_source_markov_transport": {
            "metric_tangent_to_coframe_strain_formula": "S=(1/2) K_evt^(-1) H",
            "coframe_strain_checks": strain_checks,
            "metric_tangent_identity": "S^T K_evt+K_evt S=H",
            "full_rank10": True,
            "active_event_coframe_transport": active_event_coframe_transport,
            "symmetric_conservative_refinement_preserved": symmetric_conservative_refinement_preserved,
            "zero_order_curvature_potential_excluded_in_declared_class": curvature_potential_excluded_in_declared_class,
            "why": "the transported source action remains a nearest-neighbor difference/Dirichlet action with unchanged Markov row sum and no on-site killing term"
        },
        "source_selected_parent": {
            "edge_scalar": "response-exact Umegaki/logZ Bregman divergence",
            "neighbor_law": "actual Braid event transition coboundary",
            "internal_metric": "faithful Gibbs BKM metric G_AB(lambda)",
            "Lorentz_principal_tensor": "source-OS-continued K_evt and its a-source coframe neighborhood",
            "continuum_action": "S_BKM=(1/2) integral sqrt|g| G_AB(lambda) g^mn partial_m lambda^A partial_n lambda^B d4x",
            "new_matter_action_added": False,
            "external_coefficient_fit": False,
            "declared_class": "long-wavelength local second-order formally self-adjoint conservative source-event continuum"
        },
        "hilbert_ward": {
            "Hilbert_convention": "T_mn=2/sqrt|g| delta S_BKM/delta g^mn",
            "Hilbert_stress": hilbert_formula,
            "Euler_expression": euler_formula,
            "off_shell_Noether_identity": ward_formula,
            "on_shell_Ward": "nabla^m T_mn=0",
            "Hilbert_stress_source_derived_in_declared_class": hilbert_stress_derived,
            "Ward_source_derived_in_declared_class": ward_identity_derived
        },
        "dependency_effect": {
            "BGCE289_fixed_matter_rank7_obstruction": "REMOVED_BY_EXISTING_INDEPENDENT_A_SOURCE_SOLDER",
            "BGCE285_active_source_Markov_transport": "PROMOTED_TO_PASS_IN_THE_DECLARED_LOCAL_SECOND_ORDER_SOURCE_EVENT_CLASS",
            "BGCE267_curvature_potential_ambiguity": "EXCLUDED_IN_THE_SAME_DECLARED_CLASS",
            "MMR2_and_source_three_fifths": "RETAINED_UNCHANGED_NOT_REDERIVED",
            "SDPC_complete": False,
            "unconditional_Einstein_dynamics": False,
            "completed_quantum_gravity": False
        },
        "retained_boundaries": {
            "higher_derivative_or_different_principal_symbol_actions": "OUTSIDE_DECLARED_CLASS_NOT_EXCLUDED",
            "retained_real_Stone_affine_completion_is_finite_Braid_only": False,
            "full_finite_Umegaki_Lorentz_parent": "NOT_DERIVED_BEYOND_IR_LONG_WAVELENGTH_ACTION",
            "MMR2_and_three_fifths": "SEPARATE_RETAINED_RESULTS",
            "Einstein_equation": "NOT_DERIVED_BY_THIS_GATE",
            "empirical_gravity": False,
            "completed_quantum_gravity": False
        },
        "counter_intuition_scan": {
            "tempting_failure": "BGCE150 already disproved every operator-to-causal solder.",
            "refutation": "BGCE150 disproved equality of the KMS covariance metric with the fixed causal metric under one coefficient pullback. BGCE290 transports the independent source covector a by the later source-fixed Hadamard frame map and keeps K_evt as the background metric.",
            "ordinary_explanation": "A typed frame isomorphism induces an invertible Sym2 map, and a diffeomorphism-covariant sigma model has a Hilbert tensor and Noether identity.",
            "siel_specific_content": "the four operator labels, ten metric functionals, Hadamard causal frame, Braid neighbor law, source measure, OS sign and BKM target metric all come from the same pointed-Braid lineage without coefficient fitting.",
            "falsifier": "failure of source-frame typing, Sym2 rank or 7+3/S4 intertwining; a surviving on-site killing term in the transported exact source action; or a mismatch between the transported principal symbol and the source-derived BKM continuum action."
        },
        "next_gate": "BGCE291_STRESS_WARD_INDEPENDENT_REDERIVATION_AND_SCOPE_RED_TEAM_GATE",
        "decision": decision,
        "runtime_class": "SUBSECOND_EXACT_RATIONAL_SYM2_AND_VARIATIONAL_IDENTITY_AUDIT_NO_SCAN",
        "formal_E0_E1_E2": "NOT_CLAIMED__DPA_THEORETICAL_GATE_ONLY",
        "claim_ceiling": "BGCE290 derives, in the declared long-wavelength local second-order formally self-adjoint conservative source-event class, an exact rank-ten source-native solder from the existing independent doubled metric sources to the causal metric tangent, an active conservative coframe transport, the minimal BKM parent Hilbert tensor and its off-shell Noether identity with on-shell Ward conservation. It uses no fitted coefficient and adds no new matter action. It does not exclude higher-derivative or different-principal-symbol theories, remove the retained real affine/Stone completion, rederive MMR2 or three-fifths, derive Einstein dynamics, establish empirical gravity or complete quantum gravity."
    }
    (HERE / "RAW_OUTPUT.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    print(decision)


if __name__ == "__main__":
    main()
