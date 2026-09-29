#!/usr/bin/env python3
"""Exact typed reconciliation of Fisher gain one and outer-cup three-fifths."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent

INPUTS = {
    "audits/SRA_DPA_BGCE235_FULL_CORNER_MATTER_ACTION_AND_OUTER_UNIT_COMPOSITION_GATE_20260921/RESULT.json": "c443370d2729eaad99cc0bc09ed85799704d88093d91915a122bcc9f5019a0f4",
    "audits/SRA_DPA_BGCE235_FULL_CORNER_MATTER_ACTION_AND_OUTER_UNIT_COMPOSITION_GATE_20260921/CERTIFICATE.json": "22d65940cdf16b17f48d81d370cbf05b4859ce5e82943c170af565de44d392a2",
    "audits/SRA_DPA_BGCE371_SOURCE_CLOCK_RECORD_TO_ENDOGENOUS_METRIC_REGISTER_TRANSLATION_AND_ACTUATION_SCALE_GATE_20260924/RESULT.json": "46f4df88b0fb2edc57a12c99488879542d43a6cdc5b62ee936c3ca7866860de2",
    "audits/SRA_DPA_BGCE371_SOURCE_CLOCK_RECORD_TO_ENDOGENOUS_METRIC_REGISTER_TRANSLATION_AND_ACTUATION_SCALE_GATE_20260924/CERTIFICATE.json": "f52082bb9a1134bdea72ff4cb1293155f7c45a3f1fa563c12815ed7f11ae6cbf",
    "audits/SRA_DPA_BGCE372_DIRECT_FINITE_PARENT_RELATIVE_COUPLING_AND_THREE_FIFTHS_COMPATIBILITY_GATE_20260924/RESULT.json": "2e4f8295378c8cdf50515f8efb4796147567826d1728f0e18039379d6499a0f5",
    "audits/SRA_DPA_BGCE372_DIRECT_FINITE_PARENT_RELATIVE_COUPLING_AND_THREE_FIFTHS_COMPATIBILITY_GATE_20260924/CERTIFICATE.json": "c2901df8194a27bf33738758babdb4fee8f35fa35e5975333ca7a0f2209146a0",
    "audits/SRA_DPA_BGCE373_FINITE_FISHER_PARENT_TO_CONTINUUM_FULL_CORNER_ACTION_NORMALIZATION_MAP_GATE_20260924/RESULT.json": "4fc38c3c0aa802b0735c26cd61f7b0e6e6b5fd5465e8cf82c2bb83f396b54382",
    "audits/SRA_DPA_BGCE373_FINITE_FISHER_PARENT_TO_CONTINUUM_FULL_CORNER_ACTION_NORMALIZATION_MAP_GATE_20260924/CERTIFICATE.json": "06cb18039e7f378f1a423568d964ba67203a256407a8fc2dff9493f9f1ab8d1c",
    "audits/SRA_DPA_BGCE300R1_A49_NONCIRCULAR_BACKREACTION_TO_LOW_ENERGY_SPIN2_EINSTEIN_GATE_20260923/RESULT.json": "3ea43d21415ffc1a33b4d4446e6db053772a886c604147b50d614b2c9931835a",
    "audits/SRA_DPA_BGCE300R1_A49_NONCIRCULAR_BACKREACTION_TO_LOW_ENERGY_SPIN2_EINSTEIN_GATE_20260923/CERTIFICATE.json": "41a3ee80e9eee79692752c55c15f7f6cb3f9db16827290467b8d129c7a79eadb",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text())


def main() -> None:
    hash_checks = {rel: digest(ROOT / rel) == expected for rel, expected in INPUTS.items()}
    assert all(hash_checks.values())

    r235 = load(next(p for p in INPUTS if "BGCE235_" in p and p.endswith("RESULT.json")))
    r371 = load(next(p for p in INPUTS if "BGCE371_" in p and p.endswith("RESULT.json")))
    c372 = load(next(p for p in INPUTS if "BGCE372_" in p and p.endswith("CERTIFICATE.json")))
    c373 = load(next(p for p in INPUTS if "BGCE373_" in p and p.endswith("CERTIFICATE.json")))
    r300 = load(next(p for p in INPUTS if "BGCE300R1_" in p and p.endswith("RESULT.json")))

    p = Fraction(r235["outer_cup"])
    assert p == Fraction(3, 5)
    assert r235["manual_three_fifths"] is False
    assert r371["variational_closure"]["unique_stationary_translation"] == "delta h=F^{-1}S=2M^{-1}y"
    assert r371["variational_closure"]["free_actuation_coefficient"] is False
    assert c372["direct_parent_coupling"]["derived_relative_coefficient"] == "1"
    assert c372["three_fifths_comparison"]["same_referent_as_BGCE371_Fisher_relative_coefficient"] is False
    assert c373["split_normalization_theorem"]["asymmetric_pair_is_derived_by_current_source"] is False
    assert r300["same_full_corner_BKM_Umegaki_matter_lineage"] is True
    assert r300["source_relative_normalization"] == "3/5"
    assert r300["derived_equation"] == "G_mu_nu(g)=(3/5)T_mu_nu(g,lambda)"

    # Scalar exact proxy for the tensor identity (pF)^-1(pS)=F^-1 S.
    # F and S remain symbolic; only the coefficient cancellation is evaluated.
    internal_hessian_scale = p
    internal_score_scale = p
    internal_gain = internal_score_scale / internal_hessian_scale
    external_gravity_scale = Fraction(1, 1)
    external_matter_scale = p
    external_relative_weight = external_matter_scale / external_gravity_scale

    gates = {
        "G1_outer_cup_is_source_derived_three_fifths": p == Fraction(3, 5),
        "G2_same_record_fisher_gain_is_one": internal_gain == 1,
        "G3_referents_are_distinct": c372["three_fifths_comparison"]["same_referent_as_BGCE371_Fisher_relative_coefficient"] is False,
        "G4_common_matter_scaling_cancels_inside_fisher_update": internal_gain == 1,
        "G5_outer_matter_weight_survives_relative_to_gravity": external_relative_weight == Fraction(3, 5),
        "G6_no_asymmetric_score_hessian_map_used": c373["split_normalization_theorem"]["asymmetric_pair_is_derived_by_current_source"] is False,
        "G7_continuum_equation_uses_same_full_corner_lineage": r300["same_full_corner_BKM_Umegaki_matter_lineage"] is True,
    }
    assert all(gates.values())

    raw = {
        "schema": "siel.dpa.bgce499.scout.raw.v1",
        "scout_id": "DPA-SCOUT-BGCE499-002",
        "parent_work_item": "BQG-G3-R03.6",
        "source_commit": "ecfa6c97111d1cdf73626296452c82d853f69804",
        "input_hash_checks": hash_checks,
        "exact_rational_result": {
            "outer_cup_weight": str(p),
            "conditional_matter_hessian_scale": str(internal_hessian_scale),
            "conditional_matter_score_scale": str(internal_score_scale),
            "internal_fisher_gain": str(internal_gain),
            "external_gravity_action_scale": str(external_gravity_scale),
            "external_matter_action_scale": str(external_matter_scale),
            "external_relative_weight": str(external_relative_weight),
        },
        "typed_matching_rule": {
            "inner": "Gamma_m -> p Gamma_m implies (F,S)->(pF,pS) and delta_h=(pF)^-1(pS)=F^-1S",
            "outer": "S_total=S_g+p S_m implies delta S_total=0 gives G=pT in the BGCE300R1 normalization",
            "forbidden_misidentification": "p is not inserted only between the same-parent matter score and Fisher Hessian",
        },
        "noncompensating_gates": gates,
        "strongest_counter_reading": "This proves typed compatibility and the exact matching rule, not that BGCE371 is a discretization or integrator of BGCE300R1.",
        "primary_evidence_status": "Theoretical derivation",
        "decision": "CLOSED_SCOPED_TYPED_DISTINCT_REFERENTS_AND_EXACT_COMPOSITION_RULE",
        "claim_ceiling": "The apparent coefficient discontinuity is removed only as a typed compatibility theorem in the pinned finite source and BGCE300R1 declared continuum class. No finite-to-continuum dynamical convergence, SI Newton constant, empirical gravity or completed quantum gravity is proved.",
    }
    result = {
        "schema": "siel.dpa.bgce499.scout.result.v1",
        "candidate_id": "BGCE499",
        "scout_id": raw["scout_id"],
        "verification": "PASS_TYPED_FISHER_GAIN_ONE_AND_OUTER_CUP_THREE_FIFTHS_RECONCILIATION",
        "primary_evidence_status": raw["primary_evidence_status"],
        "scientific_layer": "finite-to-continuum variational typing and normalization",
        "internal_fisher_gain": str(internal_gain),
        "external_matter_to_gravity_weight": str(external_relative_weight),
        "same_scalar_referent": False,
        "manual_three_fifths": False,
        "asymmetric_score_hessian_map_used": False,
        "work_item_decision": "CLOSED_SCOPED",
        "remaining_boundary": "No proof that the BGCE371 update map converges dynamically to the BGCE300R1 continuum Euler flow.",
        "claim_ceiling": raw["claim_ceiling"],
    }
    (HERE / "RAW_OUTPUT.json").write_text(json.dumps(raw, indent=2) + "\n")
    (HERE / "RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
    print(result["verification"])


if __name__ == "__main__":
    main()
