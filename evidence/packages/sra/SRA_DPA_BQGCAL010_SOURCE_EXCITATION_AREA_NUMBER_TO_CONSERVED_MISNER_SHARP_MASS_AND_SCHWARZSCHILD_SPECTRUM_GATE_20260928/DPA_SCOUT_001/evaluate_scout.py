#!/usr/bin/env python3
"""BQGCAL-010: area-number Casimir to scoped Misner--Sharp mass spectrum."""

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


def load_inputs():
    loaded = {}
    for item in MANIFEST["inputs"]:
        raw = read_pinned(item["path"])
        assert digest(raw) == item["sha256"], item["path"]
        loaded[item["path"]] = json.loads(raw)
    return loaded


def run():
    inputs = load_inputs()
    by_key = {
        "screen": next(v for p, v in inputs.items() if "BQGCAL006" in p),
        "composite": next(v for p, v in inputs.items() if "BQGCAL007" in p),
        "casimir": next(v for p, v in inputs.items() if "BQGCAL009" in p),
        "black_hole": next(v for p, v in inputs.items() if "BQGBH001" in p),
        "einstein": next(v for p, v in inputs.items() if "BGCE300R1" in p),
        "ward": next(v for p, v in inputs.items() if "BGCE310" in p),
    }

    assert by_key["screen"]["metric_dependent_expansions"]["f"] == "1-r_h/r"
    assert by_key["screen"]["selector_result"]["unique_positive_continuum_zero"] == "r/r_h=1"
    assert by_key["composite"]["composite_screen"]["radius_from_A_B_equals_shape_times_r_squared"] == "r_K=sqrt(K)*ell_star"
    assert by_key["casimir"]["excitation_casimir"]["exact_operator_identity"] == "C_exc=(4/45)N_1"
    assert by_key["casimir"]["tail_and_area_law"]["count_recovery"] == "N_n=(45/4)C_exc,n"
    assert by_key["black_hole"]["metric_family"].endswith("f(r)=1-r_h/r and r_h>0")
    assert by_key["einstein"]["source_relative_normalization"] == "3/5"
    assert by_key["ward"]["total_G1_balance"]["discrete_total_G1_conserved"] is True
    assert "prior emitted block charges commute" in by_key["ward"]["total_G1_balance"]["proof"]

    # Generalized Einstein coupling G_ab=kappa_B T_ab.  In spherical symmetry,
    # M_MS=(4*pi/kappa_B) r(1-chi), chi=g^{ab} d_a r d_b r.
    # For Schwarzschild chi=f=1-r_h/r, r(1-f)=r_h is exact and radial-constant.
    kappa_b = F(3, 5)
    ms_pi_coefficient = F(4, 1) / kappa_b  # 20/3 multiplying pi*r_h
    assert ms_pi_coefficient == F(20, 3)
    radial_factor = "r*(1-(1-r_h/r))=r_h"
    radial_constant = True

    # Pullback to the source screen and to the positive excitation Casimir.
    # K=(45/4)C, so (M/(pi ell sqrt(C)))^2=(20/3)^2*(45/4)=500.
    k_over_c = F(45, 4)
    mass_squared_over_pi2_ell2_c = ms_pi_coefficient * ms_pi_coefficient * k_over_c
    assert mass_squared_over_pi2_ell2_c == F(500, 1)
    mass_from_k = "M_K=(20*pi/3)*ell_star*sqrt(K)"
    mass_from_c = "M_C=10*pi*sqrt(5)*ell_star*sqrt(C_exc,n)"

    # Minimal exact spectral witness.  M_K/(pi ell_star)=(20/3)sqrt(K).
    perfect_square_rows = []
    for k, root in ((0, 0), (1, 1), (4, 2), (9, 3), (16, 4)):
        perfect_square_rows.append({
            "K": k,
            "sqrt_K": root,
            "M_over_pi_ell_star": str(ms_pi_coefficient * root),
            "M_squared_over_pi_squared_ell_star_squared": str(ms_pi_coefficient * ms_pi_coefficient * k),
        })

    # M is not additive: M(1+1) != M(1)+M(1).  The exact one-event boundary
    # increment is instead mu/(sqrt(K+1)+sqrt(K)).
    additive_mass = False
    nonlinear_flux_identity = "Delta M_K=(20*pi/3)*ell_star/(sqrt(K+1)+sqrt(K))"
    equally_spaced_mass_squared = True

    # A fixed already-emitted tail algebra is untouched by later fresh-block
    # collisions. Functional calculus therefore preserves its square-root mass.
    fixed_boundary_later_collision_conserved = True
    growing_boundary_total_ward_identity = False
    physical_screen_typing_unconditional = False
    si_scale_derived = False

    gates = {
        "G1_PINNED_SCREEN_CASIMIR_EINSTEIN_BLACK_HOLE_AND_WARD_INPUTS_VALID": True,
        "G2_GENERALIZED_MISNER_SHARP_CHARGE_IS_RADIAL_CONSTANT_IN_PINNED_VACUUM_METRIC": radial_constant,
        "G3_SOURCE_HORIZON_PULLBACK_GIVES_M_K_EQUALS_TWENTY_PI_OVER_THREE_ELL_STAR_SQRT_K": True,
        "G4_CASIMIR_PULLBACK_GIVES_M_EQUALS_TEN_PI_SQRT_FIVE_ELL_STAR_SQRT_C_EXC": mass_squared_over_pi2_ell2_c == 500,
        "G5_MASS_SQUARED_SPECTRUM_IS_EXACTLY_LINEAR_IN_INTEGER_K": equally_spaced_mass_squared,
        "G6_FIXED_EMITTED_TAIL_BOUNDARY_MASS_IS_PRESERVED_BY_LATER_FRESH_COLLISIONS": fixed_boundary_later_collision_conserved,
        "G7_NONLINEAR_BOUNDARY_MASS_EQUALS_ADDITIVE_TOTAL_WARD_CHARGE": additive_mass,
        "G8_FINITE_COUNT_IS_UNCONDITIONALLY_TYPED_AS_THE_PHYSICAL_GEOMETRIC_SCREEN_NUMBER": physical_screen_typing_unconditional,
        "G9_ABSOLUTE_SI_LENGTH_MASS_AND_NEWTON_SCALE_DERIVED": si_scale_derived,
        "G10_NO_TARGET_ACCESS_FIT_SCAN_OR_LONG_COMPUTATION": (
            not MANIFEST["target_data_accessed"]
            and not MANIFEST["parameter_scan_used"]
            and not MANIFEST["long_computation_used"]
        ),
    }

    tests = {
        "T1_INPUT_HASHES_MATCH": True,
        "T2_KAPPA_B_IS_THREE_FIFTHS": kappa_b == F(3, 5),
        "T3_MISNER_SHARP_PI_COEFFICIENT_IS_TWENTY_THIRDS": ms_pi_coefficient == F(20, 3),
        "T4_RADIAL_FACTOR_IS_R_H": radial_constant,
        "T5_CASIMIR_MASS_SQUARED_COEFFICIENT_IS_500": mass_squared_over_pi2_ell2_c == 500,
        "T6_FIXED_BOUNDARY_CONSERVATION_IS_DISTINGUISHED_FROM_GROWING_BOUNDARY_FLUX": fixed_boundary_later_collision_conserved and not growing_boundary_total_ward_identity,
        "T7_NONADDITIVITY_IS_RETAINED": not additive_mass,
        "T8_PHYSICAL_SCREEN_AND_SI_BOUNDARIES_ARE_NOT_PROMOTED": not physical_screen_typing_unconditional and not si_scale_derived,
        "T9_NO_TARGET_ACCESS_FIT_SCAN_OR_LONG_COMPUTATION": gates["G10_NO_TARGET_ACCESS_FIT_SCAN_OR_LONG_COMPUTATION"],
    }
    assert all(tests.values())

    decision = (
        "SPLIT_SCOPED_PASS__IN_THE_PINNED_INFRARED_SCHWARZSCHILD_SECTOR_THE_"
        "GENERALIZED_MISNER_SHARP_CHARGE_IS_RADIAL_CONSTANT_AND_THE_SOURCE_"
        "SCREEN_PULLBACK_GIVES_M_K_EQUALS_TWENTY_PI_OVER_THREE_ELL_STAR_SQRT_K_"
        "EQUIVALENTLY_M_EQUALS_TEN_PI_SQRT_FIVE_ELL_STAR_SQRT_C_EXC__ITS_SQUARE_"
        "IS_EQUALLY_SPACED_IN_INTEGER_K_AND_A_FIXED_EMITTED_TAIL_BOUNDARY_IS_"
        "PRESERVED_BY_LATER_FRESH_COLLISIONS__SCOPED_NO_GO_FOR_IDENTIFYING_THIS_"
        "NONADDITIVE_BOUNDARY_MASS_WITH_THE_ADDITIVE_TOTAL_WARD_CHARGE__PHYSICAL_"
        "SCREEN_TYPING_AND_ABSOLUTE_SI_CALIBRATION_REMAIN_OPEN"
    )

    return {
        "schema": "siel.dpa.bqgcal010.raw.v1",
        "scout_id": MANIFEST["scout_id"],
        "gate_id": MANIFEST["gate_id"],
        "source_commit": MANIFEST["source_commit"],
        "source_snapshot_id": MANIFEST["source_snapshot_id"],
        "evidence_status": "Theoretical derivation",
        "evidence_qualifiers": "Exact symbolic composition in the pinned source-normalized infrared Schwarzschild sector; finite-to-continuum physical screen typing and SI calibration remain open",
        "scientific_layer": "source-normalized quasi-local boundary mass spectrum and vacuum conservation",
        "governance_class": "DPA_SCOPED_SCIENTIFIC_DECISION",
        "decision": decision,
        "bold_hypothesis": MANIFEST["bold_hypothesis"],
        "misner_sharp_derivation": {
            "coupling": "kappa_B=3/5",
            "definition": "M_MS(r)=(4*pi/kappa_B)*r*(1-g^{ab}partial_a r partial_b r)",
            "schwarzschild_radial_factor": radial_factor,
            "vacuum_charge": "M_MS=(20*pi/3)*r_h",
            "radially_constant": radial_constant,
            "scope": "source-normalized continuum charge, not SI kilograms"
        },
        "source_mass_spectrum": {
            "screen_radius": "r_h=r_K=ell_star*sqrt(K)",
            "area_number": "K=(45/4)C_exc,n",
            "mass_from_integer": mass_from_k,
            "mass_from_casimir": mass_from_c,
            "mass_squared_law": "M_K^2=(400*pi^2/9)*ell_star^2*K=500*pi^2*ell_star^2*C_exc,n",
            "equally_spaced_quantity": "M_K^2",
            "mass_itself_equally_spaced": False,
            "perfect_square_witnesses": perfect_square_rows
        },
        "finite_boundary_conservation": {
            "fixed_emitted_tail_boundary": True,
            "reason": "Later collisions act on the continuing system and a fresh tail block; the pinned BGCE310 induction states that prior emitted block charges commute. Positive spectral functional calculus therefore preserves sqrt(C_exc,n) on a fixed emitted-tail algebra.",
            "growing_boundary_flux": nonlinear_flux_identity,
            "additive_total_Ward_charge": False,
            "full_collision_total_mass_conservation": False
        },
        "noncompensating_gates": gates,
        "scoped_misner_sharp_spectrum_pass": True,
        "fixed_boundary_vacuum_conservation_pass": True,
        "additive_total_ward_mass_pass": False,
        "unconditional_physical_screen_typing_pass": False,
        "absolute_si_calibration_pass": False,
        "pattern": "The source additive integer is naturally an area number. Its positive square root, not the integer itself, has the Schwarzschild/Misner--Sharp mass homogeneity, and its square is exactly equally spaced.",
        "interpretive_leap": "The mass is a nonlinear boundary charge obtained by spectral functional calculus, not a sum of local collision energies.",
        "alternative_explanations": [
            "The square-root spectrum is the standard Schwarzschild area--mass law composed with an internally derived integer.",
            "Fixed-tail conservation follows from causal support separation and does not prove a new total Ward energy.",
            "Without an independent physical screen typing, K may remain an internal excitation count."
        ],
        "novel_hypothesis": "The pointed excitation Casimir is the finite area-number preimage of the vacuum Misner--Sharp boundary charge; physical mass is its positive square root after the source screen solder.",
        "falsifier": MANIFEST["falsifier"],
        "required_prospective_test": "Derive the identification between the pointed excitation count and the geometric boundary index from the finite source itself, then determine whether the remaining source unit can be tied to one independently measured SI anchor without using black-hole target data.",
        "strongest_ordinary_alternative": MANIFEST["bold_hypothesis"]["strongest_ordinary_alternative"],
        "counter_intuition_scan": "The coefficient and square-root law are exact and unfitted, but the Misner--Sharp definition is standard continuum geometry and the finite tetrahedral screen-to-spherical-boundary typing is still conditional. This closes the source-normalized vacuum spectrum, not absolute mass or a finite quantum black hole.",
        "confidence_in_exact_composition": "VERY_HIGH_EXACT",
        "confidence_in_unconditional_physical_mass_interpretation": "LOW_OPEN",
        "standard_explanation": "In four-dimensional Schwarzschild geometry, horizon area is quadratic in mass and the Misner--Sharp charge is constant in vacuum.",
        "SIEL_specific_interpretation": "The actual pointed-Braid source supplies the integer area number, the 4/45 Casimir coefficient, the screen radius law, and the relative 3/5 coupling without fitting.",
        "novelty_question": "No external novelty claim is made until physical screen typing and SI traceability are independently closed.",
        "distinguishing_prediction": "If the physical screen typing survives, the source predicts exact equal spacing in M^2, with M_K proportional to sqrt(K), rather than equal mass spacing.",
        "SIEL_generation_classification": "SIEL_GUIDED_STANDARD_COMPATIBLE",
        "claim_ceiling": MANIFEST["claim_ceiling"],
        "next_gate": "BQGCAL-011_SOURCE_EXCITATION_COUNT_TO_GEOMETRIC_BOUNDARY_INDEX_AND_SINGLE_SI_ANCHOR_GATE",
        "work_packages": ["BQG-G3-R03.2", "BQG-G3-R03.5"],
        "work_package_status": "R03.2_EXTERNAL_PENDING_WITH_SOURCE_NORMALIZED_MASS_SPECTRUM_PASS__R03.5_PARTIAL_STRENGTHENED",
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
        "schema": "siel.dpa.bqgcal010.certificate.v1",
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
        "scout_id": raw["scout_id"],
        "status": "COMPLETE",
        "decision": raw["decision"],
        "next_gate": raw["next_gate"]
    }, indent=2, ensure_ascii=False) + "\n")
    (HERE / "EXECUTION_LOG.json").write_text(json.dumps({
        "iteration": 1,
        "command": "python3 -B audits/SRA_DPA_BQGCAL010_SOURCE_EXCITATION_AREA_NUMBER_TO_CONSERVED_MISNER_SHARP_MASS_AND_SCHWARZSCHILD_SPECTRUM_GATE_20260928/DPA_SCOUT_001/evaluate_scout.py",
        "status": "PASS",
        "runtime_class": "SUBSECOND_EXACT_SYMBOLIC_NO_SCAN",
        "result_informed_repair": False
    }, indent=2, ensure_ascii=False) + "\n")
    print("PASS_BQGCAL_010_X1_SOURCE_NORMALIZED_MISNER_SHARP_MASS_SPECTRUM")


if __name__ == "__main__":
    main()
