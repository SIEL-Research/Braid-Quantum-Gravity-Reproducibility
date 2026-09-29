#!/usr/bin/env python3
"""BGCE307: source GKSL Stinespring dilation to total stress/Ward gate."""
from fractions import Fraction
from hashlib import sha256
import importlib.util
from pathlib import Path
import json
import subprocess
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
REV = "b168bb94e266dbe96614e67aa8ea636f352ce1b1"
O14_PATH = ROOT / "public-inputs/formal_checks/ocbfh014_source_native_refinement_naturality_check.py"


def frozen(path):
    return subprocess.check_output(["git", "show", f"{REV}:{path}"], cwd=ROOT)


def load(path):
    return json.loads(frozen(path))


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def main():
    sm = json.loads((HERE / "SOURCE_MATRIX.json").read_text())
    checked = {}
    for path, expected in sm["inputs_sha256"].items():
        actual = sha256(frozen(path)).hexdigest()
        assert actual == expected, (path, actual, expected)
        checked[f"{REV}:{path}"] = actual

    x125 = load("records/BGCE125_REYNOLDS_PROJECTION_CP_SEMIGROUP_FOR_AFFINE_SCALAR_FLOW_GATE_20260919/RAW_OUTPUT.json")
    x126 = load("records/BGCE126_HYBRID_GKSL_AND_THREE_INNER_DERIVATIONS_LOCAL_METRIC_EVOLUTION_GATE_20260919/RAW_OUTPUT.json")
    r266 = load("records/BGCE266_REFINEMENT_CLOCK_TO_UNIQUE_EVENT_SEMIGROUP_AND_IR_OS_CONTINUATION_GATE_20260922/RESULT.json")
    r295 = load("records/BGCE295_FINITE_BRAID_ACTION_TO_CONTINUUM_HILBERT_VARIATION_IDENTITY_GATE_20260923/RESULT.json")
    r300 = load("records/BGCE300R1_A49_NONCIRCULAR_BACKREACTION_TO_LOW_ENERGY_SPIN2_EINSTEIN_GATE_20260923/RESULT.json")
    r306 = load("records/BGCE306_SOURCE_GKSL_EVENT_CLOCK_TO_FINITE_BACKREACTION_TRANSFER_GATE_20260923/RESULT.json")

    assert x125["reynolds_channel"]["actual_unitary_count"] == 6
    assert x125["semigroup"]["formula"] == "T_t=E+exp(-t)(I-E)"
    assert x125["semigroup"]["CPTP_for_t_nonnegative"] is True
    assert x126["all_stage_transport"]["all_finite_stages"] is True
    assert r266["source_fixed_event_OS_rate"] == "2*pi/3"
    assert r295["Ward_source_derived_in_declared_class"] is True
    assert r300["full_finite_Lorentzian_quantum_backreaction"] is False
    assert r306["stress_Ward_transfer"]["direct_finite_GKSL_to_BGCE300R1_backreaction"] is False

    # At the source crossing q=1/4, combine q*Id with the identity element in
    # the six-element Reynolds average.  The exact group probabilities are
    # p_e=3/8 and p_g=1/8 for the other five elements.
    q = Fraction(1, 4)
    p_identity = q + (1-q) / 6
    p_other = (1-q) / 6
    probabilities = [p_identity] + [p_other] * 5
    assert probabilities == [Fraction(3, 8)] + [Fraction(1, 8)] * 5
    assert sum(probabilities) == 1

    o14 = load_module("bgce307_o14", O14_PATH)
    survivors, _, _, _ = o14.reconstruct_actual_source()
    identity = np.eye(125, dtype=np.int64)
    sector_records = []
    for survivor in survivors:
        g_num, g_den, r1, r2 = o14.source_g1(survivor["R"].astype(np.int64))
        group = [identity, r1, r2, r1 @ r2, r2 @ r1, r1 @ r2 @ r1]
        assert len(group) == 6
        assert all(np.array_equal(u.T @ u, identity) for u in group)

        # Exact Kraus/Stinespring normalization: sum_g p_g U_g^*U_g=I.
        normalization_num = sum(
            (p.numerator * (8 // p.denominator)) * (u.T @ u)
            for p, u in zip(probabilities, group)
        )
        assert np.array_equal(normalization_num, 8 * identity)

        # The Reynolds adjoint does not conserve the source clock observable.
        # E^*(G1)-G1 = defect_num/(6*g_den), with g_den=6 here.
        defect_num = sum((u.T @ g_num @ u for u in group), start=np.zeros_like(g_num)) - 6 * g_num
        assert np.any(defect_num)
        defect_frobenius_num_sq = int(np.sum(defect_num * defect_num))
        defect_hs_sq = Fraction(defect_frobenius_num_sq, (6 * g_den) ** 2)
        assert defect_frobenius_num_sq == 23328
        assert defect_hs_sq == 18
        sector_records.append({
            "mask": survivor["mask"],
            "group_register_dimension": 6,
            "fixed_time_controlled_Braid_unitary": True,
            "Stinespring_isometry_exact": True,
            "G1_adjoint_generator_defect_nonzero": True,
            "G1_defect_Hilbert_Schmidt_norm_squared": str(defect_hs_sq),
            "G1_defect_nonzero_entries": int(np.count_nonzero(defect_num))
        })
    assert len(sector_records) == 8
    common = [{k: v for k, v in row.items() if k != "mask"} for row in sector_records]
    assert all(row == common[0] for row in common)

    fixed_time = {
        "channel": "T_t=q Id+(1-q)E, q=exp(-gamma t)",
        "exact_witness_q": "1/4",
        "group_probabilities_at_witness": ["3/8", "1/8", "1/8", "1/8", "1/8", "1/8"],
        "environment": "C[S3] group register labelled by the six actual Braid unitaries",
        "environment_dimension": 6,
        "controlled_unitary": "W=sum_g U_g tensor |g><g|",
        "environment_state": "|psi_t>=sum_g sqrt(p_t(g))|g>",
        "partial_trace_reproduces_channel": True,
        "all_eight_actual_sectors": True,
        "new_fitted_coefficient": False
    }

    autonomous = {
        "single_finite_environment_fixed_initial_state_and_time_independent_H_total": False,
        "theorem": "A finite-dimensional autonomous unitary reduction has matrix elements that are finite sums of phases. If such a function converges as t tends to infinity, all nonzero-frequency coefficients vanish and it is constant. The nonconstant channel E+exp(-gamma t)(I-E) converges to E, so it cannot have such a realization.",
        "required_for_exact_full_semigroup": "an infinite ancilla/Fock environment or repeated fresh-ancilla reset",
        "required_structure_source_selected": False,
        "fixed_time_dilation_is_autonomous_semigroup_dilation": False
    }

    conservation = {
        "system_source_clock_observable": "G1",
        "Reynolds_adjoint_generator_fixes_G1": False,
        "all_eight_G1_defect_HS_norm_squared": "18",
        "trivial_environment_Hamiltonian_can_balance_G1": False,
        "source_environment_Hamiltonian_or_stress_present": False,
        "total_system_environment_Ward_identity_derived": False,
        "probability_norm_conservation_upgraded_to_stress_conservation": False,
        "finite_Einstein_backreaction_bridge_closed": False
    }

    out = {
        "schema": "siel.public-calculation.bgce307.result.v1",
        "candidate_id": "BGCE307",
        "date": "2026-09-23",
        "source_revision": REV,
        "input_hashes_verified": checked,
        "primary_evidence_status": "Exact fixed-time dilation theorem, exact eight-sector conservation defect, and finite-autonomous-dilation no-go",
        "scientific_layer": "open quantum dynamics, closed-system dilation, and total stress/Ward conservation",
        "fixed_time_source_labelled_Stinespring": fixed_time,
        "full_semigroup_autonomous_dilation": autonomous,
        "sector_records": sector_records,
        "total_conservation": conservation,
        "BGCE300R1_low_energy_Einstein_result_retained": True,
        "decision": "SPLIT_PASS_FIXED_TIME_DILATION_ONLY__THE_SIX_ACTUAL_BRAID_UNITARIES_GIVE_AN_EXACT_SOURCE_LABELLED_SIX_DIMENSIONAL_STINESPRING_DILATION_OF_EACH_REYNOLDS_SEMIGROUP_CHANNEL_AND_AT_Q_ONE_QUARTER_THE_GROUP_WEIGHTS_ARE_EXACTLY_THREE_EIGHTHS_PLUS_FIVE_TIMES_ONE_EIGHTH__BUT_NO_SINGLE_FINITE_ENVIRONMENT_WITH_FIXED_STATE_AND_AUTONOMOUS_HAMILTONIAN_CAN_REALIZE_THE_NONCONSTANT_EXPONENTIALLY_RELAXING_SEMIGROUP_FOR_ALL_TIMES__MOREOVER_THE_REYNOLDS_ADJOINT_GENERATOR_CHANGES_G1_WITH_EXACT_HS_DEFECT_SQUARED_18_IN_ALL_EIGHT_SECTORS__NO_SOURCE_ENVIRONMENT_STRESS_OR_TOTAL_WARD_BALANCE_IS_PRESENT__FINITE_EINSTEIN_BACKREACTION_REMAINS_OPEN",
        "counter_intuition_scan": {
            "ordinary_explanation": "Every finite-dimensional CPTP map has a Stinespring dilation, but a relaxing Markov semigroup needs an effectively inexhaustible environment and total energy bookkeeping.",
            "SIEL_specific_part": "Here the dilation labels and controlled unitaries are not arbitrary: they are the six actual pointed-Braid actions, and the failure to conserve the same source clock G1 is exact and identical across all eight sectors.",
            "strongest_counterpattern": "The already source-native infinite right-tail refinement may itself provide the fresh ancilla chain, avoiding an externally postulated bath.",
            "falsifier": "A finite autonomous fixed-environment dilation of the full nonconstant relaxation semigroup, or exact vanishing of the computed G1 adjoint defect."
        },
        "next_gate": "BGCE308_SOURCE_RIGHT_TAIL_REPEATED_INTERACTION_DILATION_AND_TOTAL_BALANCE_GATE",
        "runtime_class": "SUBSECOND_EXACT_INTEGER_RATIONAL_OPERATOR_CHECK_NO_SCAN",
        "formal_E0_E1_E2": "NOT_CLAIMED__PUBLIC_THEORETICAL_GATE_ONLY",
        "claim_ceiling": "BGCE307 derives an exact source-labelled Stinespring dilation for each finite-time Reynolds channel and proves an exact nonzero G1 conservation defect, but it does not derive an autonomous full-semigroup environment, environment stress, total Ward identity or full finite Lorentzian quantum backreaction."
    }
    (HERE / "RESULT.json").write_text(json.dumps(out, indent=2) + "\n")
    print(out["decision"])


if __name__ == "__main__":
    main()
