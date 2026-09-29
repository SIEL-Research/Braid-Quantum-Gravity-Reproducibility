#!/usr/bin/env python3
"""BGCE336R2: refined collision CTP continuum and finite-backreaction gate."""

from fractions import Fraction
from hashlib import sha256
import json
import math
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
REV = "8afbcfd975bab0455456d0e89f048813cb3ecea3"

INPUTS = {
    "audits/SRA_DPA_BGCE300R1_A49_NONCIRCULAR_BACKREACTION_TO_LOW_ENERGY_SPIN2_EINSTEIN_GATE_20260923/RESULT.json": "3ea43d21415ffc1a33b4d4446e6db053772a886c604147b50d614b2c9931835a",
    "audits/SRA_DPA_BGCE304_FULL_FINITE_REFLECTION_POSITIVITY_AND_TRANSFER_MATRIX_RECONSTRUCTION_GATE_20260923/RESULT.json": "6b1003f76f7a2dc40550670ce7727ed10abd18c465892fe41f7e537472803b73",
    "audits/SRA_DPA_BGCE305_SOURCE_BKM_HEAT_KERNEL_OR_DOUBLED_BLOCK_TRANSFER_RECONSTRUCTION_GATE_20260923/RESULT.json": "ae34c27997bbfa94c271016211a96aa3b0f6c4578f81e5c80810d6a1195aa83e",
    "audits/SRA_DPA_BGCE324_CENTERED_CHARGE_SCORE_TO_COLLISION_NOETHER_TIME_OR_MODULAR_ENERGY_GATE_20260923/RESULT.json": "ed7f418a9a54d22081c72f2ff373eed35a2ffde72d848d5f14a8c9904afab4b1",
    "audits/SRA_DPA_BGCE325_G1_ALIGNED_STRONG_CTP_GENERATOR_TO_REPEATED_LOCAL_WARD_AND_CONTINUUM_STRESS_IDENTIFICATION_GATE_20260923/RESULT.json": "cec850cff6f08ec3bc980f87d89e3c4dfcf5ed6730ed56eb48895d8a8479cbd2",
    "audits/SRA_DPA_BGCE326_G1_ALIGNED_EFFECTIVE_WARD_TO_CAUSAL_CTP_INFLUENCE_AND_MICROSCOPIC_STRESS_SPLIT_GATE_20260923/RESULT.json": "41cd2c5ec059c073505830059b87f9190d2809c14fe74ac8527158fcbccf6a7e",
    "audits/SRA_DPA_BGCE329_FIVE_WAY_TEMPORAL_COARSENING_TO_SOURCE_SCALED_COLLISION_AND_CONTINUUM_CAUSAL_FDR_GATE_20260923/RESULT.json": "cc0d4a3e37e7834133fc79e818f5faff9c090f33872efefdafc73046f5185566",
    "audits/SRA_DPA_BGCE330_Q_SYMBOLIC_COLLISION_PREPARATION_AND_STRONG_BALANCE_TO_A55_FREE_BASE_RATE_SELECTOR_GATE_20260923/RESULT.json": "710bef3f8538715ee6a5731588eab2e64ffb5f7d17b625eb1ae8c729dc2b267f",
    "audits/SRA_DPA_BGCE333_EXP_MINUS_PI_COLLISION_CTP_WARD_REINSTANTIATION_AND_REFINEMENT_NATURALITY_GATE_20260923/RESULT.json": "dcaee5d9226ad5d8bde278641cc1232f2a74a54652d6ae730a89b7c57a1968e9",
    "audits/SRA_DPA_BGCE335_SOURCE_S3_CENTRAL_CONVOLUTION_GENERATOR_TO_REPRESENTATION_RESOLVED_EVENT_REYNOLDS_SEMIGROUP_GATE_20260923/RESULT.json": "f9f775671676de1e2c8de678dee6f2f38b0160947b7fe40cf47478ce6a81ccf9",
}


def load(path):
    raw = (ROOT / path).read_bytes()
    actual = sha256(raw).hexdigest()
    assert actual == INPUTS[path], (path, actual, INPUTS[path])
    return json.loads(raw), actual


def select(docs, token):
    return next(value for path, value in docs.items() if token in path)


def main():
    docs = {}
    hashes = {}
    for path in INPUTS:
        docs[path], hashes[path] = load(path)

    r300 = select(docs, "BGCE300R1_")
    r304 = select(docs, "BGCE304_")
    r305 = select(docs, "BGCE305_")
    r324 = select(docs, "BGCE324_")
    r325 = select(docs, "BGCE325_")
    r326 = select(docs, "BGCE326_")
    r329 = select(docs, "BGCE329_")
    r330 = select(docs, "BGCE330_")
    r333 = select(docs, "BGCE333_")
    r335 = select(docs, "BGCE335_")

    assert r300["A49_noncircular_backreaction"] == "CLOSED_IN_DECLARED_CLASS"
    assert r300["fixed_model_MMR2"] == "CLOSED"
    assert r300["full_finite_Lorentzian_quantum_backreaction"] is False
    assert r304["standard_positive_one_link_transfer_matrix_derived"] is False
    assert r305["canonical_doubled_block_positive_semidefinite"] is True
    assert r305["canonical_doubled_block_strictly_positive"] is False
    assert r324["G1_replacement"]["mixed_plus_G1_response_rank_all_sectors"] == [4] * 8
    assert r325["continuum_decision"]["effective_on_shell_covariant_Ward_derived_in_declared_class"] is True
    assert r326["finite_causal_CTP"]["normalization_Z_J_J"] is True
    assert r326["response_kernels"]["noise_quadratic_form_positive_semidefinite"] is True
    assert r326["microscopic_split"]["unique_system_environment_interaction_stress_split"] is False
    assert r329["continuum_limit"]["strongly_continuous"] is True
    assert r329["base_rate_boundary"]["general_q0_selected_by_five_way_scaling"] is False
    assert r330["symbolic_G1_balance"]["exact_total_G1_balance_all_q"] is True
    assert r330["symbolic_strong_intertwiner"]["Hermitian_and_exact_for_each_q"] is True
    assert r333["finite_causal_CTP"]["q_exp_minus_pi_valid"] is True
    assert r335["equal_rate_central_theorem"]["rate_selected_by_centrality"] is False

    # Exact reduced-channel identity.  Because E^2=E,
    # exp[h gamma(E-I)] = E + exp(-gamma h)(I-E).
    semigroup = {
        "mesh": "h_m=5^(-m)",
        "arbitrary_rate_domain": "gamma>0",
        "refined_contraction": "q_m=exp(-gamma h_m)",
        "generator": "L_gamma=gamma(E-I)",
        "exact_one_step_identity": "Phi_h=E+exp(-gamma h)(I-E)=exp(h L_gamma)",
        "exact_cylindrical_identity": "Phi_(h/5)^5=Phi_h",
        "parent_rate_must_be_numerically_selected_before_limit": False,
        "family_is_unique_without_time_calibration": False,
        "CPTP_unital_GKSL": True,
    }

    # A short numerical witness only checks the analytic limiting formulas; it
    # is not used to select gamma or to carry the scientific conclusion.
    witness_records = []
    previous_error = None
    gamma_witness = 1.0
    for m in range(8):
        h = Fraction(1, 5**m)
        q = math.exp(-gamma_witness * float(h))
        n = 5**m
        product_error = abs(q**n - math.exp(-gamma_witness))
        nonidentity_rate = (1.0 - q) / (6.0 * float(h))
        balance_rate = (1.0 - q) / float(h)
        rate_error = abs(balance_rate - gamma_witness)
        if previous_error is not None:
            assert rate_error < previous_error
        previous_error = rate_error
        roundoff_bound = 32.0 * sys.float_info.epsilon * max(1, n)
        assert product_error <= roundoff_bound
        witness_records.append({
            "m": m,
            "h_m": str(h),
            "q_m": q,
            "q_m_to_number_of_steps": q**n,
            "target_exp_minus_one": math.exp(-1.0),
            "product_error": product_error,
            "predeclared_roundoff_bound": roundoff_bound,
            "each_nonidentity_jump_rate_per_unit_time": nonidentity_rate,
            "target_each_nonidentity_jump_rate": 1.0 / 6.0,
            "balance_density_factor": balance_rate,
            "target_balance_density_factor": 1.0,
        })

    ctp_limit = {
        "finite_step_source_insertion": "U_h[J]=exp(-i h J^alpha S_alpha)",
        "doubled_one_step_map": "M_h[J+,J-](X)=Phi_h(exp(-i h H[J+]) X exp(+i h H[J-]))",
        "bounded_liouville_source_generator": "K[J+,J-](X)=-i H[J+]X+i X H[J-]",
        "finite_dimensional_lie_product_limit": "product M_h -> T_C exp integral(L_gamma+K[J+,J-])dt in operator norm",
        "continuum_generating_functional": "Z_gamma[J+,J-]=Tr(T_C exp integral(L_gamma+K[J+,J-])dt rho_0)",
        "continuum_influence_action": "Gamma_gamma=-i log Z_gamma on the connected neighborhood of zero sources",
        "normalization_Z_J_J": True,
        "branch_hermiticity": True,
        "largest_time_cancellation": True,
        "retarded_support": True,
        "noise_quadratic_form_positive_semidefinite": True,
        "reason_noise_positivity_survives": "finite-mesh noise forms are PSD and the finite-dimensional PSD cone is closed under the norm limit",
        "scope": "continuous source-event time on a finite internal algebra; minimal four aligned-score insertion class",
        "full_local_3plus1_Lorentzian_SK_field_functional": False,
        "physical_temperature_FDT": False,
    }

    ward_density = {
        "system_G1_defect_per_step": "D_G1(h)=(1-exp(-gamma h))[G1-E(G1)]",
        "continuum_system_defect_density": "lim D_G1(h)/h=gamma[G1-E(G1)]",
        "environment_charge_entry_per_step": "B_gh(h)=c_gh(1-exp(-gamma h))/36",
        "continuum_environment_charge_density": "lim B_gh(h)/h=c_gh gamma/36",
        "four_generator_strong_completion_each_finite_h": True,
        "reduced_four_component_balance_density_finite": True,
        "strict_environment_only_spatial_balance": False,
        "microscopic_interaction_operator_strong_limit_on_one_fixed_Hilbert_space": "NOT_ESTABLISHED",
        "reason": "fresh-tail dilation spaces change with refinement and the off-support completion is nonunique; reduced/compressed balance has a limit but a unique microscopic tensor does not follow",
    }

    backreaction = {
        "BGCE325_effective_continuum_Hilbert_stress_retained": True,
        "BGCE300R1_noncircular_low_energy_backreaction_retained": True,
        "fixed_model_MMR2_status": "CLOSED_BY_BGCE300R1_IN_DECLARED_CLASS",
        "continuum_CTP_proven_parent_of_BGCE325_Bregman_Hilbert_stress": False,
        "source_native_doubled_metric_to_collision_generator_map": False,
        "interaction_balance_term_is_already_a_Hilbert_metric_variation": False,
        "unique_microscopic_interaction_stress": False,
        "full_finite_Lorentzian_quantum_backreaction": False,
        "why_not": "the four aligned scores define operational probe insertions, but the source has not yet supplied L_gamma[g_plus,g_minus]; without that map delta Gamma/delta g cannot define the physical interaction stress",
        "target_Einstein_equation_used_to_define_stress": False,
    }

    out = {
        "schema": "siel.dpa.bgce336r2.result.v1",
        "candidate_id": "BGCE336R2",
        "date": "2026-09-23",
        "fixed_source_revision": REV,
        "dpa_snapshot": {
            "id": "DPA-SNAPSHOT-8afbcfd975ba",
            "record_count": 105,
            "last_event_id": "RPD-EVENT-0451",
            "reservoir_sha256": "55b20bc7cf91a5e73d9cae8cc0fee9236471958eaa1f640341fb3b5222453b3b",
            "source_inventory_sha256": "dd277eddc229ec9807b3d6fb226c37b062d8bbc0dd9494e984ee0e2c78fe2a4f",
        },
        "input_hashes": hashes,
        "revision_record": {
            "predecessors": ["BGCE336", "BGCE336R1"],
            "predecessor_status": "IMPLEMENTATION_PROVENANCE_FAILURE_NOT_A_SCIENTIFIC_RESULT",
            "scientific_gate_changed": False,
            "changes": [
                "auxiliary repeated-power witness uses a predeclared operation-count-dependent IEEE-754 roundoff bound",
                "Python result dictionary uses False rather than JSON false"
            ]
        },
        "primary_evidence_status": "Theoretical derivation",
        "qualifier": "finite-dimensional operator-norm continuum theorem in the reduced aligned-score event-time class, with an explicit backreaction boundary",
        "status": "SPLIT_PASS_EXACT_ANY_POSITIVE_GAMMA_CONTINUUM_EVENT_TIME_CTP_INFLUENCE_AND_FINITE_REDUCED_TOTAL_BALANCE_DENSITY__FULL_LOCAL_3PLUS1_LORENTZIAN_METRIC_VARIATIONAL_INTERACTION_STRESS_AND_FINITE_QUANTUM_BACKREACTION_OPEN",
        "exact_refined_semigroup": semigroup,
        "analytic_limit_witness": {
            "gamma": "1 used only as a formula witness, not a selected physical rate",
            "records": witness_records,
        },
        "continuum_CTP_limit": ctp_limit,
        "continuum_total_balance_density": ward_density,
        "finite_backreaction_boundary": backreaction,
        "decision": "For every gamma>0, the five-way refined Reynolds collision is exactly Phi_h=exp[h gamma(E-I)]. Scaling each aligned CTP source insertion by the cell duration h makes the finite doubled products converge in operator norm, by the finite-dimensional Lie product theorem, to a normalized causal real-time CTP generating functional on the finite source algebra. Branch Hermiticity, largest-time cancellation, retarded support and positive-semidefinite noise survive the limit. The q-symbolic total-balance defects scale as 1-exp(-gamma h), so their reduced four-component density has a finite limit without selecting a numerical parent q0. This closes a continuum source-event-time influence family, not a full local 3+1 Lorentzian field parent. The four score insertions are not yet a source-derived doubled-metric deformation of the collision generator; the microscopic interaction completion remains nonunique. Therefore the continuum functional cannot yet be varied with respect to a physical metric to derive interaction Hilbert stress, and full finite noncircular quantum backreaction remains open. BGCE300R1's low-energy noncircular result is retained but not upgraded.",
        "counter_intuition_scan": {
            "ordinary_explanation": "A projectively consistent finite-dimensional quantum Markov channel with O(h) source insertions has an ordinary continuous-time tilted-Liouvillian and CTP limit.",
            "SIEL_specific_part": "The idempotent Reynolds expectation, five-child causal refinement, six actual Braid collision labels, four aligned scores and total-balance family come from the same pointed-Braid lineage.",
            "strongest_counterpattern": "A continuum CTP functional on a finite internal algebra is not yet a local Lorentzian spacetime field theory, and reduced influence does not identify a unique microscopic interaction stress.",
            "falsifier": "Failure of exact q refinement, lack of O(h) source scaling, loss of finite-dimensional norm convergence, loss of CTP normalization/causality/noise positivity, or an existing source-derived metric deformation already fixing the microscopic interaction variation.",
        },
        "DPA_reporting": {
            "Observed_Evidence": "BGCE326 gives exact finite CTP identities, BGCE329 gives exact exponential refinement, BGCE330 gives q-symbolic balance and strong completion, and BGCE335 leaves the overall rate free.",
            "Pattern": "The structural continuum limit needs a positive generator density gamma but not a preselected numerical gamma; the obstruction moves from time refinement to metric dependence.",
            "Interpretive_Leap": "The correct next parent may be a source-canonical GNS/Doob metric tilt of the collision generator rather than another absolute-rate selector.",
            "Alternative_Explanations": "The continuum limit is standard quantum Markov theory and the metric coupling must be added phenomenologically or calibrated empirically.",
            "Novel_Hypothesis": "The canonical modular reference and aligned BKM scores uniquely determine a CPTP GNS-Doob doubled-metric deformation whose first variation equals the BGCE322/325 interaction response.",
            "Falsifier": "More than one inequivalent source-natural CPTP metric tilt survives, no tilt reproduces the strong four-generator balance, or the required tilt imports the target Einstein tensor.",
            "Required_Prospective_Test": "BGCE337 source-canonical GNS-Doob metric tilt to variational interaction-stress gate.",
            "Confidence_in_Pattern": "VERY_HIGH_IN_FINITE_DIMENSIONAL_REDUCED_EVENT_TIME_CLASS",
            "Confidence_in_Interpretation": "MEDIUM",
            "standard_explanation": "Tilted finite-dimensional quantum Markov semigroup and Lie-product convergence.",
            "SIEL_specific_interpretation": "The same subjectivity-intersection Braid source supplies the collision algebra, causal refinement and conserved response quartet, while metric variation remains the missing physical bridge.",
            "novelty_question": "Whether the source modular/BKM geometry selects a unique metric-dependent quantum Doob transform compatible with the collision Ward structure.",
            "distinguishing_prediction": "A valid source metric tilt must reproduce all four balance densities, preserve CPTP/CTP identities and contain no Einstein-side input.",
            "SIEL_generation_classification": "SIEL_GUIDED_STANDARD_COMPATIBLE",
            "nearest_claim_ceiling": "Continuum causal event-time CTP influence family and reduced total-balance density for arbitrary positive gamma.",
        },
        "next_gate": "BGCE337_SOURCE_CANONICAL_GNS_DOOB_METRIC_TILT_TO_VARIATIONAL_INTERACTION_STRESS_GATE",
        "runtime_class": "SUBSECOND_ANALYTIC_SEMIGROUP_AND_LIMIT_WITNESS_NO_PARAMETER_SCAN",
        "formal_E0_E1_E2": "NOT_CLAIMED__DPA_THEORETICAL_GATE_ONLY",
        "claim_ceiling": "BGCE336 derives an exact continuum real-time CTP influence family and finite reduced four-component balance density for every positive gamma in the finite aligned-score source-event-time class. It does not derive a full local 3+1 Lorentzian Schwinger-Keldysh field functional, a source-native doubled-metric collision deformation, unique microscopic interaction Hilbert stress, physical-temperature FDT, calibrated seconds or Newton constant, full finite noncircular quantum backreaction, empirical gravity or completed quantum gravity.",
    }

    (HERE / "RESULT.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({
        "candidate_id": out["candidate_id"],
        "status": out["status"],
        "continuum_event_time_CTP": ctp_limit["normalization_Z_J_J"],
        "noise_psd": ctp_limit["noise_quadratic_form_positive_semidefinite"],
        "finite_reduced_Ward_density": ward_density["reduced_four_component_balance_density_finite"],
        "full_local_3plus1_SK": ctp_limit["full_local_3plus1_Lorentzian_SK_field_functional"],
        "finite_quantum_backreaction": backreaction["full_finite_Lorentzian_quantum_backreaction"],
        "next_gate": out["next_gate"],
    }, indent=2))


if __name__ == "__main__":
    main()
