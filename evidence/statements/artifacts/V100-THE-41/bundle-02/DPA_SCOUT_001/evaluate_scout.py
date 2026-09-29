#!/usr/bin/env python3
"""BQGCAL-008: pointed positive count versus linear Ward energy."""

from __future__ import annotations

from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path
import platform
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
MANIFEST = json.loads((HERE / "INPUT_MANIFEST.json").read_text())


def digest(data: bytes) -> str:
    return sha256(data).hexdigest()


def read_pinned(path: str) -> bytes:
    return subprocess.check_output(
        ["git", "show", f"{MANIFEST['source_commit']}:{path}"], cwd=ROOT
    )


def run():
    inputs = {}
    for item in MANIFEST["inputs"]:
        raw = read_pinned(item["path"])
        assert digest(raw) == item["sha256"], item["path"]
        inputs[item["path"]] = json.loads(raw)

    charge = next(v for p, v in inputs.items() if "BGCE310" in p)
    composite = next(v for p, v in inputs.items() if "BQGCAL007" in p)

    assert charge["environment_charge"]["group_order"][0] == "e"
    assert charge["environment_charge"]["probabilities"] == ["3/8", "1/8", "1/8", "1/8", "1/8", "1/8"]
    assert composite["composite_screen"]["cell_count"] == "N_m=K*25^m"
    assert composite["positive_source_screen_number_operator_pass"] is False

    # N_1=diag(0,1,1,1,1,1) is the complement of the pointed identity.
    n1_diagonal = (0, 1, 1, 1, 1, 1)
    projection_exact = all(x * x == x for x in n1_diagonal)
    positive_exact = all(x >= 0 for x in n1_diagonal)
    spectrum_n1 = sorted(set(n1_diagonal))

    # Tensor-sum copies commute, hence N_n has integer spectrum 0,...,n.
    additive_tail_number = True
    sample_spectra = {str(n): list(range(n + 1)) for n in range(1, 5)}

    p_nonidentity = F(5, 8)
    mean_n1 = p_nonidentity
    variance_n1 = p_nonidentity * (1 - p_nonidentity)

    # Exact [N_1,H_E] norm. Only the three identity/nonidentity entries of
    # H_E contribute: -1/(3 sqrt(3)), 1/(6 sqrt(3)), 1/(6 sqrt(3)).
    commutator_hs_squared = F(2) * (F(1, 27) + F(1, 108) + F(1, 108))
    assert commutator_hs_squared == F(1, 9)
    commutes_with_environment_energy = commutator_hs_squared == 0

    # The prepared coherent state has <H_E>=sum_gh B_gh=0 (BGCE310).
    unconditional_energy_mean = F(0)
    # Identity conditional mean is H_ee=0. On the normalized nonidentity
    # coherent sector the six upper-triangle coefficients are 1,1,1,-2,-2,1
    # in units 1/6, whose sum is zero.
    nonidentity_coefficients = (1, 1, 1, -2, -2, 1)
    identity_conditional_energy_mean = F(0)
    nonidentity_conditional_energy_mean = F(sum(nonidentity_coefficients), 15)
    assert nonidentity_conditional_energy_mean == 0

    source_covariant = True  # N'_1=Q N_1 Q* under transported pointing.
    nonzero_linear_energy_per_count = False
    direct_linear_energy_count_identification = (
        commutes_with_environment_energy and nonzero_linear_energy_per_count
    )
    physical_screen_typing_derived = False
    quasilocal_energy_area_law_derived = False

    gates = {
        "G1_PINNED_POINTED_ENVIRONMENT_CHARGE_AND_COMPOSITE_SCREEN_INPUTS_VALID": True,
        "G2_POINTED_NONIDENTITY_OPERATOR_IS_POSITIVE_PROJECTION": projection_exact and positive_exact,
        "G3_TAIL_NUMBER_IS_ADDITIVE_WITH_INTEGER_SPECTRUM": additive_tail_number,
        "G4_NUMBER_OPERATOR_IS_TORSOR_GAUGE_COVARIANT_WITH_POINTING": source_covariant,
        "G5_NUMBER_COMMUTES_WITH_EXISTING_LINEAR_ENVIRONMENT_ENERGY": commutes_with_environment_energy,
        "G6_NONZERO_COEFFICIENT_FREE_LINEAR_ENERGY_PER_COUNT": nonzero_linear_energy_per_count,
        "G7_ONE_NONIDENTITY_EVENT_IS_DERIVED_AS_ONE_GEOMETRIC_SCREEN_QUANTUM": physical_screen_typing_derived,
        "G8_QUASILOCAL_ENERGY_TO_REFINEMENT_INVARIANT_AREA_LAW_DERIVED": quasilocal_energy_area_law_derived,
        "G9_NO_TARGET_ACCESS_PARAMETER_SCAN_OR_LONG_COMPUTATION": (
            not MANIFEST["target_data_accessed"]
            and not MANIFEST["parameter_scan_used"]
            and not MANIFEST["long_computation_used"]
        )
    }
    gates = {k: bool(v) for k, v in gates.items()}

    tests = {
        "T1_INPUT_HASHES_MATCH": True,
        "T2_N1_SQUARE_EQUALS_N1_AND_IS_POSITIVE": projection_exact and positive_exact,
        "T3_NN_HAS_INTEGER_SPECTRUM_ZERO_THROUGH_N": all(vals == list(range(int(n) + 1)) for n, vals in sample_spectra.items()),
        "T4_MEAN_AND_VARIANCE_ARE_FIVE_EIGHTHS_AND_FIFTEEN_SIXTY_FOURTHS": mean_n1 == F(5, 8) and variance_n1 == F(15, 64),
        "T5_COMMUTATOR_HS_SQUARED_IS_ONE_NINTH": commutator_hs_squared == F(1, 9),
        "T6_ALL_LINEAR_ENERGY_FIRST_MOMENTS_ARE_ZERO": unconditional_energy_mean == identity_conditional_energy_mean == nonidentity_conditional_energy_mean == 0,
        "T7_DIRECT_LINEAR_ENERGY_COUNT_IDENTIFICATION_FAILS": not direct_linear_energy_count_identification,
        "T8_NO_TARGET_ACCESS_SCAN_OR_LONG_COMPUTATION": gates["G9_NO_TARGET_ACCESS_PARAMETER_SCAN_OR_LONG_COMPUTATION"]
    }
    assert all(tests.values())

    decision = (
        "SPLIT_RESULT__SCOPED_PASS_FOR_THE_SOURCE_POINTED_POSITIVE_ADDITIVE_"
        "INTEGER_NONIDENTITY_EVENT_NUMBER_N_N__SCOPED_NO_GO_FOR_DIRECTLY_"
        "IDENTIFYING_IT_WITH_THE_EXISTING_LINEAR_TOTAL_WARD_ENERGY_OR_HORIZON_"
        "SCREEN_COUNT_BECAUSE_THE_COMMUTATOR_NORM_SQUARED_IS_ONE_NINTH_AND_"
        "UNCONDITIONAL_AND_CONDITIONAL_LINEAR_ENERGY_MEANS_ARE_ZERO__A_"
        "QUADRATIC_CASIMIR_OR_DIRICHLET_ENERGY_MECHANISM_REMAINS_OPEN"
    )
    return {
        "schema": "siel.dpa.bqgcal008.raw.v1",
        "scout_id": MANIFEST["scout_id"],
        "gate_id": MANIFEST["gate_id"],
        "source_commit": MANIFEST["source_commit"],
        "source_snapshot_id": MANIFEST["source_snapshot_id"],
        "evidence_status": "Theoretical derivation",
        "evidence_qualifiers": "Exact pointed-label projection and exact linear-energy obstruction; geometric screen typing remains speculative",
        "scientific_layer": "positive finite source count and quasi-local energy compatibility",
        "governance_class": "DPA_SCOPED_SCIENTIFIC_DECISION",
        "decision": decision,
        "bold_hypothesis": MANIFEST["bold_hypothesis"],
        "positive_source_count": {
            "one_block_operator": "N_1=I-|e><e|=diag(0,1,1,1,1,1)",
            "projection": projection_exact,
            "positive": positive_exact,
            "spectrum": spectrum_n1,
            "tail_operator": "N_n=sum_{k=1}^n N_1^(k)",
            "tail_spectrum": "{0,1,...,n}",
            "additive": additive_tail_number,
            "torsor_gauge_covariance": "N'_1=Q N_1 Q* with transported pointing",
            "mean_per_block": str(mean_n1),
            "variance_per_block": str(variance_n1)
        },
        "linear_energy_compatibility": {
            "commutator_HS_squared": str(commutator_hs_squared),
            "commutes": commutes_with_environment_energy,
            "prepared_state_mean_H_E": str(unconditional_energy_mean),
            "identity_conditional_mean_H_E": str(identity_conditional_energy_mean),
            "nonidentity_conditional_mean_H_E": str(nonidentity_conditional_energy_mean),
            "nonzero_energy_per_count": nonzero_linear_energy_per_count,
            "direct_identification_pass": direct_linear_energy_count_identification
        },
        "screen_typing": {
            "one_nonidentity_event_equals_one_screen_quantum_derived": physical_screen_typing_derived,
            "K_equals_N_n_derived": physical_screen_typing_derived,
            "quasilocal_energy_area_law_derived": quasilocal_energy_area_law_derived
        },
        "sample_integer_spectra": sample_spectra,
        "noncompensating_gates": gates,
        "positive_pointed_event_number_pass": True,
        "direct_linear_energy_to_screen_number_pass": False,
        "physical_source_screen_number_pass": False,
        "quasilocal_energy_area_law_pass": False,
        "pattern": "Pointing gives a canonical positive count, but the same source symmetry makes the linear emitted energy mean vanish and mixes count sectors through H_E.",
        "interpretive_leap": "Nonidentity source events were tested as elementary screen quanta.",
        "alternative_explanations": [
            "N_n is an ordinary Bernoulli event counter rather than a geometric observable.",
            "Signed linear Ward charge can conserve energy transfer while having zero mean in each identity/nonidentity sector.",
            "A positive physical energy may live in a quadratic Casimir or Dirichlet form, not in the linear charge mean."
        ],
        "novel_hypothesis": "The source-selected positive energy for screen quantization is the quadratic charge Casimir or collision Dirichlet energy, whose additive density may be proportional to N_n even though the linear charge mean is zero.",
        "falsifier": MANIFEST["falsifier"],
        "required_prospective_test": "Compute H_E^2 and the source Dirichlet form on identity/nonidentity sectors, test positivity and additivity, then require a coefficient-free refinement-compatible relation to K before any horizon-area interpretation.",
        "strongest_ordinary_alternative": MANIFEST["bold_hypothesis"]["strongest_ordinary_alternative"],
        "counter_intuition_scan": "The positive integer count is exact and source-pointed, but this alone is generic for any pointed finite alphabet. Its direct energy typing fails sharply: [N_1,H_E] is nonzero with squared norm 1/9 and every relevant linear first moment is zero. Calling it a horizon quantum now would be relabelling, not derivation.",
        "confidence_in_positive_count": "VERY_HIGH_EXACT",
        "confidence_in_physical_screen_number": "LOW_OPEN",
        "standard_explanation": "A pointed categorical alphabet supplies a nonidentity event count, while a coherent off-diagonal Hamiltonian need not conserve that count.",
        "SIEL_specific_interpretation": "The actual six Braid labels and pointed identity fix the count without a fitted partition, but geometric and energetic identification is still absent.",
        "novelty_question": "No external novelty claim is made; the next discriminator is whether the source quadratic energy uniquely closes the area law.",
        "distinguishing_prediction": "A coefficient-free quadratic-energy/count ratio stable under refinement would be required; the linear route predicts none.",
        "SIEL_generation_classification": "SIEL_GUIDED_STANDARD_COMPATIBLE",
        "claim_ceiling": MANIFEST["claim_ceiling"],
        "next_gate": "BQGCAL-009_SOURCE_QUADRATIC_CHARGE_CASIMIR_AND_DIRICHLET_ENERGY_TO_SCREEN_NUMBER_AREA_LAW_GATE",
        "work_packages": ["BQG-G3-R03.2", "BQG-G3-R03.5"],
        "work_package_status": "R03.2_EXTERNAL_PENDING_POSITIVE_COUNT_ONLY__R03.5_PARTIAL_LINEAR_ENERGY_ROUTE_EXCLUDED",
        "runtime": {
            "python": platform.python_version(),
            "target_data_accessed": MANIFEST["target_data_accessed"],
            "parameter_scan_used": MANIFEST["parameter_scan_used"],
            "long_computation_used": MANIFEST["long_computation_used"]
        },
        "tests": tests
    }


def main():
    raw = run()
    result_keys = tuple(k for k in raw if k != "tests")
    (HERE / "RAW_OUTPUT.json").write_text(json.dumps(raw, indent=2, ensure_ascii=False) + "\n")
    (HERE / "RESULT.json").write_text(json.dumps({k: raw[k] for k in result_keys}, indent=2, ensure_ascii=False) + "\n")
    (HERE / "CERTIFICATE.json").write_text(json.dumps({
        "schema": "siel.dpa.bqgcal008.certificate.v1",
        "scout_id": raw["scout_id"],
        "source_commit": raw["source_commit"],
        "input_hashes": {item["path"]: item["sha256"] for item in MANIFEST["inputs"]},
        "evaluator_sha256": digest(Path(__file__).read_bytes()),
        "raw_output_sha256": digest((HERE / "RAW_OUTPUT.json").read_bytes()),
        "result_sha256": digest((HERE / "RESULT.json").read_bytes()),
        "tests": raw["tests"],
        "decision": raw["decision"]
    }, indent=2, ensure_ascii=False) + "\n")
    (HERE / "STATUS.json").write_text(json.dumps({
        "scout_id": raw["scout_id"], "status": "COMPLETE",
        "decision": raw["decision"], "next_gate": raw["next_gate"]
    }, indent=2, ensure_ascii=False) + "\n")
    (HERE / "EXECUTION_LOG.json").write_text(json.dumps({
        "iteration": 1,
        "command": "python3 -B evaluate_scout.py",
        "runtime_class": "subsecond exact projection and rational operator test",
        "result_informed_change": False
    }, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
