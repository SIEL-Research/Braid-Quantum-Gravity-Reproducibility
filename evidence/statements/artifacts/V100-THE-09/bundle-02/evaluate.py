#!/usr/bin/env python3
"""BGCE308: source right-tail repeated interaction and total balance gate."""
from collections import Counter
from hashlib import sha256
import importlib.util
from pathlib import Path
import json
import subprocess
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
REV = "59d75db606f84605e191af4adcbe0e4c3f4aa4f0"
O14_PATH = ROOT / "projects/active/discovery_partner/formal_checks/ocbfh014_source_native_refinement_naturality_check.py"


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

    x125 = load("audits/SRA_DPA_BGCE125_REYNOLDS_PROJECTION_CP_SEMIGROUP_FOR_AFFINE_SCALAR_FLOW_GATE_20260919/RAW_OUTPUT.json")
    r127 = load("audits/SRA_DPA_BGCE127_BRAID_INTERVAL_QUASILOCAL_NET_AND_OVERLAP_LOCALITY_GATE_20260919/RESULT.json")
    x127 = load("audits/SRA_DPA_BGCE127_BRAID_INTERVAL_QUASILOCAL_NET_AND_OVERLAP_LOCALITY_GATE_20260919/RAW_OUTPUT.json")
    r266 = load("audits/SRA_DPA_BGCE266_REFINEMENT_CLOCK_TO_UNIQUE_EVENT_SEMIGROUP_AND_IR_OS_CONTINUATION_GATE_20260922/RESULT.json")
    r307 = load("audits/SRA_DPA_BGCE307_SOURCE_GKSL_STINESPRING_DILATION_TO_TOTAL_STRESS_WARD_GATE_20260923/RESULT.json")
    assert x125["reynolds_channel"]["actual_unitary_count"] == 6
    assert r127["status"].startswith("PASS_EXACT_X63_INTERVAL_QUASILOCAL_NET")
    assert x127["hybrid_generator_locality"]["right_tail_refinement_naturality"] is True
    assert x127["hybrid_generator_locality"]["translated_copy_at_every_interval_derived"] is False
    assert x127["state_overlap"]["one_compatible_product_tail_family_exists"] is True
    assert x127["state_overlap"]["unique_global_state_selected_by_net"] is False
    assert r266["source_fixed_event_OS_rate"] == "2*pi/3"
    assert r307["fixed_time_source_labelled_Stinespring"]["environment_dimension"] == 6

    o14 = load_module("bgce308_o14", O14_PATH)
    survivors, _, _, _ = o14.reconstruct_actual_source()
    identity = np.eye(125, dtype=np.int64)
    sector_records = []
    for survivor in survivors:
        _, _, r1, r2 = o14.source_g1(survivor["R"].astype(np.int64))
        group = [identity, r1, r2, r1 @ r2, r2 @ r1, r1 @ r2 @ r1]
        maps = [np.argmax(np.abs(u), axis=0) for u in group]
        unseen = set(range(125))
        orbits = []
        while unseen:
            representative = min(unseen)
            orbit = sorted({int(mapping[representative]) for mapping in maps})
            unseen -= set(orbit)
            orbits.append(orbit)
        histogram = Counter(map(len, orbits))
        assert histogram == Counter({1: 17, 3: 28, 6: 4})
        regular = [orbit for orbit in orbits if len(orbit) == 6]

        # Pointed numerator on three strands.  P is the rank-one cap with
        # P^2=5P.  On each regular orbit, (I+P) tensor I restricts exactly to
        # I_6 and has no coupling to its complement.  Reynolds neutralization
        # therefore restricts to 6 I_6: both give uniform group-label weight.
        cap = survivor["P"].astype(np.int64)
        assert np.array_equal(cap @ cap, 5 * cap)
        pointed = np.kron(np.eye(25, dtype=np.int64) + cap, np.eye(5, dtype=np.int64))
        neutral = sum((u @ pointed @ u.T for u in group), start=np.zeros_like(pointed))
        all_indices = set(range(125))
        orbit_records = []
        for orbit in regular:
            complement = sorted(all_indices - set(orbit))
            pblock = pointed[np.ix_(orbit, orbit)]
            nblock = neutral[np.ix_(orbit, orbit)]
            assert np.array_equal(pblock, np.eye(6, dtype=np.int64))
            assert np.array_equal(nblock, 6 * np.eye(6, dtype=np.int64))
            assert not np.any(pointed[np.ix_(orbit, complement)])
            assert not np.any(neutral[np.ix_(orbit, complement)])
            orbit_records.append({
                "representative": orbit[0],
                "basis_indices": orbit,
                "pointed_restriction": "I_6",
                "neutral_restriction": "6 I_6",
                "identity_label_selected": False,
                "q_one_quarter_weights_selected": False
            })
        sector_records.append({
            "mask": survivor["mask"],
            "three_strand_dimension": 125,
            "orbit_histogram": {"1": 17, "3": 28, "6": 4},
            "regular_register_copies": 4,
            "regular_register_total_dimension": 24,
            "regular_orbits": orbit_records
        })
    assert len(sector_records) == 8
    common = [{k: v for k, v in row.items() if k != "mask"} for row in sector_records]
    assert all(row == common[0] for row in common)

    capacity = {
        "source_tail_dimension_per_three_strands": 125,
        "exact_orbit_decomposition": "17*1 + 28*3 + 4*6 = 125",
        "native_regular_S3_registers_per_block": 4,
        "unbounded_supply_from_infinite_right_tail": True,
        "external_Hilbert_space_required": False,
        "capacity_gate": "PASS"
    }
    selection = {
        "pointed_state_restriction_each_regular_orbit": "uniform I_6",
        "neutral_state_restriction_each_regular_orbit": "uniform 6 I_6",
        "affine_pointed_neutral_family_selects_group_identity": False,
        "required_q_one_quarter_weights": ["3/8", "1/8", "1/8", "1/8", "1/8", "1/8"],
        "required_weights_source_selected": False,
        "four_regular_copies_uniquely_selected": False,
        "basepoint_within_regular_orbit_selected": False,
        "state_selection_gate": "FAIL"
    }
    dynamics = {
        "existing_marked_generator_extension": "L_n tensor identity_tail",
        "existing_tail_is_fresh_but_interacting": False,
        "translated_collision_copy_at_each_block_derived": False,
        "source_shift_or_reset_protocol_derived": False,
        "controlled_six_Braid_unitary_realized_by_declared_local_boundary_word": False,
        "repeated_interaction_semigroup_derived": False,
        "environment_G1_balance_current_derived": False,
        "total_stress_Ward_derived": False
    }
    out = {
        "schema": "siel.dpa.bgce308.result.v1",
        "candidate_id": "BGCE308",
        "date": "2026-09-23",
        "source_revision": REV,
        "input_hashes_verified": checked,
        "primary_evidence_status": "Exact eight-sector orbit decomposition and source-state restriction audit",
        "scientific_layer": "source-native environment capacity, state selection, repeated interaction, and total balance",
        "tail_register_capacity": capacity,
        "tail_state_selection": selection,
        "collision_and_balance": dynamics,
        "sector_records": sector_records,
        "BGCE307_fixed_time_dilation_retained": True,
        "BGCE300R1_low_energy_Einstein_result_retained": True,
        "decision": "SPLIT_PASS_NATIVE_ENVIRONMENT_CAPACITY_ONLY__EVERY_ACTUAL_THREE_STRAND_RIGHT_TAIL_BLOCK_DECOMPOSES_EXACTLY_AS_17_TRIVIAL_PLUS_28_THREE_ORBITS_PLUS_4_REGULAR_SIX_ORBITS_SO_THE_SOURCE_CONTAINS_FOUR_NATIVE_SIX_LABEL_BRAID_REGISTERS_PER_BLOCK_AND_AN_UNBOUNDED_SUPPLY_IN_THE_INFINITE_TAIL__BUT_THE_POINTED_CAP_STATE_RESTRICTS_TO_I6_AND_ITS_REYNOLDS_NEUTRALIZATION_TO_6I6_ON_EVERY_REGULAR_ORBIT_SO_NEITHER_SELECTS_ONE_OF_THE_FOUR_COPIES_AN_IDENTITY_BASEPOINT_OR_THE_REQUIRED_THREE_EIGHTHS_PLUS_FIVE_ONE_EIGHTH_PREPARATION__THE_EXISTING_GENERATOR_TENSORS_WITH_IDENTITY_ON_THE_TAIL_AND_NO_TRANSLATED_COLLISION_SHIFT_RESET_ENVIRONMENT_BALANCE_OR_TOTAL_WARD_LAW_IS_DERIVED__FULL_FINITE_BACKREACTION_REMAINS_OPEN",
        "counter_intuition_scan": {
            "ordinary_explanation": "An infinite tensor tail has enough room for ancillas, but capacity alone does not specify their state, coupling or conservation bookkeeping.",
            "SIEL_specific_part": "The six-label registers are actual free orbits of the pointed-Braid action and occur with the same fourfold multiplicity in all eight sectors; the source pointed/neutral states provably remain uniform on them.",
            "strongest_counterpattern": "The already source-derived clock and three Fourier marks may jointly select one regular-orbit copy and an identity basepoint, converting capacity into a collision register without an external label.",
            "falsifier": "A frozen source identity showing that the pointed/cap or neutral state alone has weights 3/8 and 1/8 on a uniquely selected regular orbit, or an existing translated collision law acting nontrivially on successive tail blocks."
        },
        "next_gate": "BGCE309_SOURCE_CLOCK_FOURIER_MARK_TO_REGULAR_ORBIT_BASEPOINT_AND_COLLISION_SELECTOR_GATE",
        "runtime_class": "SUBSECOND_EXACT_ORBIT_AND_INTEGER_BLOCK_AUDIT_NO_SCAN",
        "formal_E0_E1_E2": "NOT_CLAIMED__DPA_THEORETICAL_GATE_ONLY",
        "claim_ceiling": "BGCE308 proves that the source right tail contains an unbounded supply of native six-label Braid registers, but it does not derive the nonuniform ancilla state, register/basepoint selector, repeated collision law, environment balance current, total Ward identity or full finite Lorentzian quantum backreaction."
    }
    (HERE / "RESULT.json").write_text(json.dumps(out, indent=2) + "\n")
    print(out["decision"])


if __name__ == "__main__":
    main()
