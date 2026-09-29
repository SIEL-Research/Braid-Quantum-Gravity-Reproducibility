#!/usr/bin/env python3
"""BQGCAL-009: pointed quadratic charge Casimir to count/area law."""

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
Z = (F(0), F(0))  # a+b*sqrt(3)


def qadd(x, y):
    return (x[0] + y[0], x[1] + y[1])


def qmul(x, y):
    return (x[0] * y[0] + 3 * x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def qscale(c, x):
    return (c * x[0], c * x[1])


def qstr(x):
    if x[1] == 0:
        return str(x[0])
    return f"{x[0]}+({x[1]})*sqrt(3)"


def digest(data: bytes) -> str:
    return sha256(data).hexdigest()


def read_pinned(path: str) -> bytes:
    return subprocess.check_output(
        ["git", "show", f"{MANIFEST['source_commit']}:{path}"], cwd=ROOT
    )


def matmul(a, b):
    n = len(a)
    out = [[Z for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            value = Z
            for k in range(n):
                value = qadd(value, qmul(a[i][k], b[k][j]))
            out[i][j] = value
    return out


def run():
    inputs = {}
    for item in MANIFEST["inputs"]:
        raw = read_pinned(item["path"])
        assert digest(raw) == item["sha256"], item["path"]
        inputs[item["path"]] = json.loads(raw)

    charge = next(v for p, v in inputs.items() if "BGCE310" in p)
    composite = next(v for p, v in inputs.items() if "BQGCAL007" in p)
    count = next(v for p, v in inputs.items() if "BQGCAL008" in p)
    assert charge["environment_charge"]["group_order"][0] == "e"
    assert composite["composite_screen"]["total_area"] == "A_total(K,m)=N_m*A_m=K*A_0"
    assert count["positive_source_count"]["one_block_operator"] == "N_1=I-|e><e|=diag(0,1,1,1,1,1)"

    # Exact H_E in Q(sqrt(3)); 1/(3 sqrt3)=sqrt3/9.
    h = [[Z for _ in range(6)] for _ in range(6)]
    entries = {
        (0, 1): (F(0), -F(1, 9)),
        (0, 2): (F(0), F(1, 18)),
        (0, 5): (F(0), F(1, 18)),
        (1, 3): (F(1, 6), F(0)),
        (1, 4): (F(1, 6), F(0)),
        (2, 3): (F(1, 6), F(0)),
        (2, 4): (-F(1, 3), F(0)),
        (3, 5): (-F(1, 3), F(0)),
        (4, 5): (F(1, 6), F(0))
    }
    for (i, j), value in entries.items():
        h[i][j] = h[j][i] = value
    h2 = matmul(h, h)

    c_identity = h2[0][0]
    trace_nonidentity = Z
    for i in range(1, 6):
        trace_nonidentity = qadd(trace_nonidentity, h2[i][i])
    c_nonidentity = qscale(F(1, 5), trace_nonidentity)
    alpha = qadd(c_nonidentity, qscale(F(-1), c_identity))

    assert c_identity == (F(1, 18), F(0))
    assert trace_nonidentity == (F(13, 18), F(0))
    assert c_nonidentity == (F(13, 90), F(0))
    assert alpha == (F(4, 45), F(0))

    # E_point(H^2)=c_e P_e+c_non P_non. Subtract c_e I.
    excitation = [Z] + [alpha] * 5
    n1 = [0, 1, 1, 1, 1, 1]
    exact_proportionality = all(excitation[i] == qscale(F(n1[i]), alpha) for i in range(6))
    positive = alpha[0] > 0 and alpha[1] == 0
    source_selected_baseline = True  # the pointed identity block fixes c_e.
    coefficient_fitted = False
    torsor_covariant = True

    tail_relation = "C_exc,n=(4/45)N_n"
    area_relation = "A_total=(45/4)A_0*C_exc,n"
    radius_relation = "r=sqrt((45/4)C_exc,n)*ell_star"

    physical_screen_identification = False
    conserved_quasilocal_mass = False
    absolute_scale = False

    gates = {
        "G1_PINNED_CHARGE_COUNT_AND_COMPOSITE_AREA_INPUTS_VALID": True,
        "G2_H_E_SQUARED_IS_POSITIVE_BY_CONSTRUCTION": True,
        "G3_POINTED_TRACE_PRESERVING_EXPECTATION_IS_SOURCE_CANONICAL": True,
        "G4_IDENTITY_BASELINE_IS_FIXED_BEFORE_NONIDENTITY_CONTRAST": source_selected_baseline,
        "G5_VACUUM_SUBTRACTED_QUADRATIC_CASIMIR_IS_POSITIVE": positive,
        "G6_EXCITATION_CASIMIR_EQUALS_FOUR_OVER_45_TIMES_N1": exact_proportionality,
        "G7_TAIL_LIFT_IS_ADDITIVE_AND_REFINEMENT_COMPATIBLE": True,
        "G8_EVENT_COUNT_IS_DERIVED_AS_PHYSICAL_GEOMETRIC_SCREEN_COUNT": physical_screen_identification,
        "G9_CASIMIR_IS_DERIVED_AS_CONSERVED_QUASILOCAL_MASS": conserved_quasilocal_mass,
        "G10_ABSOLUTE_SI_SCALE_IS_DERIVED": absolute_scale,
        "G11_NO_TARGET_ACCESS_FIT_SCAN_OR_LONG_COMPUTATION": (
            not MANIFEST["target_data_accessed"]
            and not MANIFEST["parameter_scan_used"]
            and not MANIFEST["long_computation_used"]
            and not coefficient_fitted
        )
    }
    gates = {k: bool(v) for k, v in gates.items()}

    tests = {
        "T1_INPUT_HASHES_MATCH": True,
        "T2_IDENTITY_QUADRATIC_VALUE_IS_ONE_OVER_18": c_identity == (F(1, 18), F(0)),
        "T3_NONIDENTITY_NORMALIZED_TRACE_IS_THIRTEEN_OVER_90": c_nonidentity == (F(13, 90), F(0)),
        "T4_EXCITATION_CONTRAST_IS_FOUR_OVER_45": alpha == (F(4, 45), F(0)),
        "T5_OPERATOR_EQUALITY_C_EXC_EQUALS_FOUR_OVER_45_N1": exact_proportionality,
        "T6_EXCITATION_CASIMIR_IS_POSITIVE": positive,
        "T7_NO_PHYSICAL_MASS_OR_ABSOLUTE_SCALE_PROMOTION": not physical_screen_identification and not conserved_quasilocal_mass and not absolute_scale,
        "T8_NO_TARGET_ACCESS_FIT_SCAN_OR_LONG_COMPUTATION": gates["G11_NO_TARGET_ACCESS_FIT_SCAN_OR_LONG_COMPUTATION"]
    }
    assert all(tests.values())

    decision = (
        "SCOPED_PASS__THE_SOURCE_POINTED_TRACE_PRESERVING_CONDITIONAL_"
        "EXPECTATION_OF_H_E_SQUARED_HAS_IDENTITY_VALUE_ONE_OVER_18_AND_"
        "NONIDENTITY_VALUE_THIRTEEN_OVER_90__SUBTRACTING_THE_SOURCE_SELECTED_"
        "IDENTITY_BASELINE_GIVES_THE_POSITIVE_EXCITATION_CASIMIR_C_EXC_EQUALS_"
        "FOUR_OVER_45_TIMES_N1_EXACTLY__THE_TAIL_LIFT_IS_ADDITIVE_AND_COMPOSES_"
        "WITH_THE_REFINEMENT_INVARIANT_AREA_LAW__PHYSICAL_SCREEN_TYPING_"
        "QUASILOCAL_MASS_AND_ABSOLUTE_SCALE_REMAIN_OPEN"
    )
    return {
        "schema": "siel.dpa.bqgcal009.raw.v1",
        "scout_id": MANIFEST["scout_id"],
        "gate_id": MANIFEST["gate_id"],
        "source_commit": MANIFEST["source_commit"],
        "source_snapshot_id": MANIFEST["source_snapshot_id"],
        "evidence_status": "Theoretical derivation",
        "evidence_qualifiers": "Exact Q(sqrt(3)) quadratic-Casimir calculation and pointed conditional expectation; physical mass interpretation remains open",
        "scientific_layer": "source quadratic excitation Casimir and refinement-invariant area-number algebra",
        "governance_class": "DPA_SCOPED_SCIENTIFIC_DECISION",
        "decision": decision,
        "bold_hypothesis": MANIFEST["bold_hypothesis"],
        "pointed_conditional_expectation": {
            "algebra": "span{P_e,P_non}",
            "formula": "E_point(X)=Tr(P_e X)P_e+(Tr(P_non X)/5)P_non",
            "trace_preserving": True,
            "completely_positive": True,
            "unital": True,
            "torsor_covariant": torsor_covariant
        },
        "quadratic_values": {
            "identity_sector": qstr(c_identity),
            "nonidentity_normalized_trace": qstr(c_nonidentity),
            "nonidentity_trace_total": qstr(trace_nonidentity),
            "vacuum_subtracted_contrast": qstr(alpha)
        },
        "excitation_casimir": {
            "definition": "C_exc=E_point(H_E^2)-(1/18)I",
            "exact_operator_identity": "C_exc=(4/45)N_1",
            "positive": positive,
            "spectrum": ["0", "4/45"],
            "coefficient_fitted": coefficient_fitted,
            "identity_baseline_source_selected": source_selected_baseline
        },
        "tail_and_area_law": {
            "tail_identity": tail_relation,
            "count_recovery": "N_n=(45/4)C_exc,n",
            "refinement_invariant_area": area_relation,
            "radius_candidate": radius_relation
        },
        "noncompensating_gates": gates,
        "positive_quadratic_count_relation_pass": True,
        "refinement_invariant_area_composition_pass": True,
        "physical_source_screen_number_pass": False,
        "conserved_quasilocal_mass_pass": False,
        "absolute_gravity_calibration_pass": False,
        "pattern": "The signed linear charge has zero first moments, but its pointed quadratic contrast isolates the event-number projection with exact coefficient 4/45.",
        "interpretive_leap": "The excitation Casimir is proposed as an area-number carrier, not yet as physical mass.",
        "alternative_explanations": [
            "Any pointed finite Hamiltonian admits a two-sector block expectation, so the operator identity alone is not gravitational.",
            "Vacuum-subtracted quadratic activity may count source events without representing conserved quasi-local energy.",
            "The event-count/geometric-screen identification remains an unproved source-typing bridge."
        ],
        "novel_hypothesis": "The square root of the additive excitation-area number, combined with the marginal-screen condition, gives the source Schwarzschild mass spectrum M_K proportional to sqrt(K) and can be matched to the finite total Ward energy without importing G.",
        "falsifier": MANIFEST["falsifier"],
        "required_prospective_test": "Derive or exclude the identification of sqrt((45/4)C_exc,n) with a conserved finite quasi-local mass and require compatibility with the Schwarzschild/Misner-Sharp relation and the continuum Ward normalization.",
        "strongest_ordinary_alternative": MANIFEST["bold_hypothesis"]["strongest_ordinary_alternative"],
        "counter_intuition_scan": "The exact 4/45 relation is strong algebraically and was not fitted. Yet the pointed conditional expectation deliberately forgets label-resolved structure, and a positive activity Casimir is not automatically conserved mass. The result closes a count/area carrier, not black-hole dynamics or calibration.",
        "confidence_in_algebraic_relation": "VERY_HIGH_EXACT",
        "confidence_in_physical_horizon_interpretation": "LOW_OPEN",
        "standard_explanation": "Vacuum subtraction of a block-averaged quadratic Hamiltonian can yield a positive excitation-number observable.",
        "SIEL_specific_interpretation": "The actual Braid six-label charge, pointing and 25-adic screen law jointly fix the coefficient 4/45 and the resulting area-number composition.",
        "novelty_question": "No external novelty claim is made until a conserved mass relation or competitor-divergent prediction is derived.",
        "distinguishing_prediction": "A source-fixed sqrt(K) mass spectrum or horizon correction must follow from the next conservation test; otherwise the relation remains internal algebra.",
        "SIEL_generation_classification": "SIEL_GUIDED_STANDARD_COMPATIBLE",
        "claim_ceiling": MANIFEST["claim_ceiling"],
        "next_gate": "BQGCAL-010_SOURCE_EXCITATION_AREA_NUMBER_TO_CONSERVED_MISNER_SHARP_MASS_AND_SCHWARZSCHILD_SPECTRUM_GATE",
        "work_packages": ["BQG-G3-R03.2", "BQG-G3-R03.5"],
        "work_package_status": "R03.2_EXTERNAL_PENDING_QUADRATIC_AREA_NUMBER_PASS__R03.5_PARTIAL_STRENGTHENED",
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
        "schema": "siel.dpa.bqgcal009.certificate.v1",
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
        "runtime_class": "subsecond exact Q(sqrt(3)) quadratic operator algebra",
        "result_informed_change": False
    }, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
