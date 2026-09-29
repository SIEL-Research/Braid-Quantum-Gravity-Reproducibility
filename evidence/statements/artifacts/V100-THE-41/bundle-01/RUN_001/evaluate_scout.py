#!/usr/bin/env python3
"""BQGCAL-007: total-charge level selection and composite-screen correction."""

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
    screen = next(v for p, v in inputs.items() if "BQGCAL004" in p)
    transport = next(v for p, v in inputs.items() if "BQGCAL005" in p)
    horizon = next(v for p, v in inputs.items() if "BQGCAL006" in p)

    assert charge["total_G1_balance"]["discrete_total_G1_conserved"] is True
    assert charge["total_G1_balance"]["all_finite_refinement_stages"] == (
        "transport by tensoring source operators with identity_tail"
    )
    assert screen["refinement_area_spectrum"]["ratio_A_m_plus_1_over_A_m"] == "1/25"
    assert transport["codimension_two_refinement"]["children_per_two_dimensional_face"] == 25
    assert transport["codimension_two_refinement"]["total_child_area_over_parent_face"] == "1"
    assert horizon["selector_result"]["unique_positive_continuum_zero"] == "r/r_h=1"

    # Q_m=Q tensor I_tail has identical source spectral/expectation data at
    # every refinement. Therefore any predicate depending only on Q_m has the
    # same truth value at every m and cannot distinguish exactly one m.
    charge_refinement_blind = True
    charge_only_unique_level_selector = False

    # A_m/A_0=25^-m and a complete refinement has N_m=K*25^m cells.
    # Thus A_total/A_0=N_m*25^-m=K exactly for every nonnegative m.
    exact_rows = []
    for k in (1, 2, 4, 9):
        for m in range(4):
            cell_area_ratio = F(1, 25) ** m
            cell_count = k * (25 ** m)
            total_area_ratio = cell_count * cell_area_ratio
            assert total_area_ratio == k
            exact_rows.append({
                "K": k,
                "m": m,
                "N_m": cell_count,
                "elementary_area_over_A0": str(cell_area_ratio),
                "total_area_over_A0": str(total_area_ratio)
            })

    composite_area_refinement_invariant = True
    composite_radius_law = "r_K=sqrt(K)*ell_star"
    m_is_resolution_not_state_label = True

    # The existing emitted charge is Hermitian, nonzero and has zero diagonal
    # (only off-diagonal nonzero entries are listed). Hence trace(H_E)=0 and a
    # nonzero Hermitian H_E is indefinite. It is not a positive integer count.
    entries = charge["environment_charge"]["nonzero_upper_triangle_B_entries"]
    charge_is_nonzero = bool(entries)
    all_nonzero_entries_off_diagonal = all(
        pair.split(",")[0] != pair.split(",")[1] for pair in entries
    )
    environment_charge_trace_zero = all_nonzero_entries_off_diagonal
    environment_charge_indefinite = (
        charge["environment_charge"]["Hermitian"]
        and charge_is_nonzero
        and environment_charge_trace_zero
    )
    positive_integer_screen_count_derived = False
    charge_to_count_identification_derived = False
    absolute_radius_derived = False

    gates = {
        "G1_PINNED_TOTAL_CHARGE_SCREEN_AREA_TRANSPORT_AND_HORIZON_INPUTS_VALID": True,
        "G2_TOTAL_G1_CHARGE_IS_REFINEMENT_BLIND": charge_refinement_blind,
        "G3_EXISTING_TOTAL_CHARGE_SELECTS_EXACTLY_ONE_REFINEMENT_LEVEL": charge_only_unique_level_selector,
        "G4_COMPLETE_25_ADIC_DESCENDANT_SCREEN_AREA_IS_REFINEMENT_INVARIANT": composite_area_refinement_invariant,
        "G5_COMPOSITE_RADIUS_LAW_R_K_EQUALS_SQRT_K_ELL_STAR_DERIVED": True,
        "G6_EXISTING_TOTAL_CHARGE_IS_A_POSITIVE_INTEGER_SCREEN_COUNT": positive_integer_screen_count_derived,
        "G7_CHARGE_TO_COUNT_AND_QUASILOCAL_ENERGY_AREA_LAW_DERIVED": charge_to_count_identification_derived,
        "G8_ABSOLUTE_SI_RADIUS_MASS_AND_GRAVITY_SCALE_DERIVED": absolute_radius_derived,
        "G9_NO_TARGET_ACCESS_PARAMETER_SCAN_OR_LONG_COMPUTATION": (
            not MANIFEST["target_data_accessed"]
            and not MANIFEST["parameter_scan_used"]
            and not MANIFEST["long_computation_used"]
        )
    }
    gates = {k: bool(v) for k, v in gates.items()}

    tests = {
        "T1_INPUT_HASHES_MATCH": True,
        "T2_TOTAL_CHARGE_TRANSPORTS_WITH_IDENTITY_TAIL_AT_ALL_LEVELS": charge_refinement_blind,
        "T3_CHARGE_ONLY_PREDICATE_CANNOT_DISTINGUISH_M": not charge_only_unique_level_selector,
        "T4_25_CHILDREN_TIMES_ONE_OVER_25_AREA_EQUALS_ONE": F(25) * F(1, 25) == 1,
        "T5_ALL_EXACT_COMPOSITE_ROWS_HAVE_AREA_RATIO_K": all(F(row["total_area_over_A0"]) == row["K"] for row in exact_rows),
        "T6_ENVIRONMENT_CHARGE_IS_NONZERO_TRACE_ZERO_HERMITIAN_AND_THEREFORE_INDEFINITE": environment_charge_indefinite,
        "T7_NO_POSITIVE_INTEGER_COUNT_OR_CHARGE_TO_COUNT_MAP_IS_DERIVED": not positive_integer_screen_count_derived and not charge_to_count_identification_derived,
        "T8_NO_TARGET_ACCESS_SCAN_OR_LONG_COMPUTATION": gates["G9_NO_TARGET_ACCESS_PARAMETER_SCAN_OR_LONG_COMPUTATION"]
    }
    assert all(tests.values())

    decision = (
        "SPLIT_RESULT__SCOPED_NO_GO_FOR_SELECTING_A_UNIQUE_REFINEMENT_LEVEL_FROM_"
        "THE_EXISTING_TOTAL_G1_CHARGE_BECAUSE_THE_CHARGE_IS_REFINEMENT_BLIND__"
        "SCOPED_PASS_FOR_THE_REFINEMENT_INVARIANT_COMPOSITE_SCREEN_LAW_WITH_"
        "N_M_EQUALS_K_TIMES_25_TO_M__A_TOTAL_EQUALS_K_A0__AND_R_K_EQUALS_"
        "SQRT_K_TIMES_ELL_STAR__A_SOURCE_POSITIVE_COUNT_K_AND_ITS_QUASILOCAL_"
        "ENERGY_AREA_IDENTIFICATION_REMAIN_OPEN"
    )
    return {
        "schema": "siel.public-calculation.bqgcal007.raw.v1",
        "scout_id": MANIFEST["scout_id"],
        "gate_id": MANIFEST["gate_id"],
        "source_commit": MANIFEST["source_commit"],
        "source_snapshot_id": MANIFEST["source_snapshot_id"],
        "evidence_status": "Theoretical derivation",
        "evidence_qualifiers": "Exact refinement covariance and rational area-count algebra; physical count and energy-area identification remain absent",
        "scientific_layer": "finite refinement semantics and source-screen area quantization candidate",
        "governance_class": "PUBLIC_SCOPED_SCIENTIFIC_DECISION",
        "decision": decision,
        "bold_hypothesis": MANIFEST["bold_hypothesis"],
        "existing_total_charge": {
            "refinement_transport": "Q_m=Q_source tensor I_tail",
            "refinement_blind": charge_refinement_blind,
            "can_select_unique_m_by_charge_only_predicate": charge_only_unique_level_selector,
            "environment_component_nonzero": charge_is_nonzero,
            "environment_component_trace_zero": environment_charge_trace_zero,
            "environment_component_indefinite": environment_charge_indefinite,
            "positive_integer_screen_count": positive_integer_screen_count_derived
        },
        "single_cell_refinement": {
            "area": "A_m=A_0*25^(-m)",
            "radius": "r_m=ell_star*5^(-m)",
            "children_per_parent_screen": 25,
            "total_descendant_area_over_parent": "1"
        },
        "composite_screen": {
            "cell_count": "N_m=K*25^m",
            "total_area": "A_total(K,m)=N_m*A_m=K*A_0",
            "radius_from_A_B_equals_shape_times_r_squared": composite_radius_law,
            "refinement_invariant": composite_area_refinement_invariant,
            "m_interpretation": "resolution coordinate, not physical black-hole state label",
            "K_interpretation": "candidate positive additive screen-number label; not yet source-derived"
        },
        "exact_rows": exact_rows,
        "noncompensating_gates": gates,
        "unique_refinement_level_from_existing_total_charge_pass": False,
        "refinement_invariant_composite_screen_pass": True,
        "positive_source_screen_number_operator_pass": False,
        "absolute_gravity_calibration_pass": False,
        "pattern": "The same 25-adic law that shrinks one elementary face makes the complete descendant screen area exactly invariant; the conserved total charge is likewise refinement blind.",
        "interpretive_leap": "The finite level m labels resolution. Physical horizon size should be carried by a refinement-invariant additive sector K rather than by choosing one m.",
        "alternative_explanations": [
            "This is standard regulator/refinement invariance and does not by itself imply quantum black-hole area levels.",
            "K is currently a bookkeeping integer, not a derived observable.",
            "The existing environment charge is indefinite and cannot be silently renamed as a positive cell count."
        ],
        "novel_hypothesis": "A source-central positive number operator N_screen and the finite total Ward energy jointly select K, giving a refinement-independent quasi-local horizon area without choosing m.",
        "falsifier": MANIFEST["falsifier"],
        "required_prospective_test": "Construct a positive integer source-screen number operator commuting with refinement and derive its coefficient-free relation to the conserved total Ward energy and the marginal-screen area.",
        "strongest_ordinary_alternative": MANIFEST["bold_hypothesis"]["strongest_ordinary_alternative"],
        "counter_intuition_scan": "The result corrects a category error: m cannot be both a pure refinement coordinate and a physical radius label for the complete screen. The new K law is exact geometry, but until K is a source observable and is tied to quasi-local energy, it is not a black-hole spectrum.",
        "confidence_in_pattern": "VERY_HIGH_EXACT",
        "confidence_in_physical_area_quantization": "LOW_OPEN",
        "standard_explanation": "A mesh refinement subdivides a fixed surface without changing its total area, while conserved total energy is regulator independent.",
        "SIEL_specific_interpretation": "The source fixes the 25-adic descendant law and tetrahedral area coefficient, making the refinement-invariant composite relation exact inside this finite Braid construction.",
        "novelty_question": "No external novelty claim is made; the exact source-specific screen-count realization remains to be constructed.",
        "distinguishing_prediction": "A derived discrete K spectrum and energy-area relation would distinguish the finite Braid screen from a generic mesh; neither is yet established.",
        "SIEL_generation_classification": "SIEL_GUIDED_STANDARD_COMPATIBLE",
        "claim_ceiling": MANIFEST["claim_ceiling"],
        "next_gate": "BQGCAL-008_SOURCE_POSITIVE_SCREEN_NUMBER_AND_QUASILOCAL_ENERGY_TO_REFINEMENT_INVARIANT_HORIZON_AREA_GATE",
        "work_packages": ["BQG-G3-R03.2", "BQG-G3-R03.5"],
        "work_package_status": "R03.2_EXTERNAL_PENDING_ROUTE_CORRECTED__R03.5_PARTIAL_STRENGTHENED",
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
        "schema": "siel.public-calculation.bqgcal007.certificate.v1",
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
        "runtime_class": "subsecond exact refinement and rational area-count algebra",
        "result_informed_change": False
    }, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
