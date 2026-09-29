#!/usr/bin/env python3
"""BGCE309R1: marked gauge-equivalence and torsor selector gate."""
from hashlib import sha256
import importlib.util
import itertools
from pathlib import Path
import json
import subprocess
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
REV = "7e877b0ccb5d03304d3a4200a3d0163b49a9036b"
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


def regular_orbits(group):
    maps = [np.argmax(np.abs(u), axis=0) for u in group]
    unseen = set(range(125))
    out = []
    while unseen:
        rep = min(unseen)
        orbit = sorted({int(mapping[rep]) for mapping in maps})
        unseen -= set(orbit)
        if len(orbit) == 6:
            out.append(orbit)
    return out


def main():
    sm = json.loads((HERE / "SOURCE_MATRIX.json").read_text())
    checked = {}
    for path, expected in sm["inputs_sha256"].items():
        actual = sha256(frozen(path)).hexdigest()
        assert actual == expected, (path, actual, expected)
        checked[f"{REV}:{path}"] = actual

    x123 = load("audits/SRA_DPA_BGCE123_A55_SELECTOR_FROM_COMMON_TEMPORAL_SPATIAL_RESPONSE_DETERMINANT_GATE_20260919/RAW_OUTPUT.json")
    x126 = load("audits/SRA_DPA_BGCE126_HYBRID_GKSL_AND_THREE_INNER_DERIVATIONS_LOCAL_METRIC_EVOLUTION_GATE_20260919/RAW_OUTPUT.json")
    r308 = load("audits/SRA_DPA_BGCE308_SOURCE_RIGHT_TAIL_REPEATED_INTERACTION_DILATION_AND_TOTAL_BALANCE_GATE_20260923/RESULT.json")
    assert x123["response_result"]["all_eight_identical"] is True
    assert x126["four_control_metric_differential"]["state_tangent_rank"] == 4
    assert r308["tail_register_capacity"]["native_regular_S3_registers_per_block"] == 4

    o14 = load_module("bgce309r1_o14", O14_PATH)
    survivors, projectors, _, _ = o14.reconstruct_actual_source()
    identity = np.eye(125, dtype=np.int64)
    expected_g = np.array([
        [15,-4,-7,0,0,-4], [-4,15,0,-4,-7,0],
        [-7,0,15,-4,-4,0], [0,-4,-4,15,0,-7],
        [0,-7,-4,0,15,-4], [-4,0,0,-7,-4,15]
    ], dtype=np.int64)
    expected_p = [
        np.diag([4,0,4,0,0,0]),
        np.diag([0,4,0,0,4,0]),
        np.diag([0,0,0,4,0,4])
    ]
    pair_positions = [(0,2), (1,4), (3,5)]
    sector_records = []
    for survivor in survivors:
        g_num, g_den, r1, r2 = o14.source_g1(survivor["R"].astype(np.int64))
        assert g_den == 6
        group = [identity, r1, r2, r1 @ r2, r2 @ r1, r1 @ r2 @ r1]
        orbits = regular_orbits(group)
        p3 = [np.kron(num, np.eye(5, dtype=np.int64)) for num, _ in projectors]
        copy_records = []
        for orbit in orbits:
            gblock = g_num[np.ix_(orbit, orbit)]
            pblocks = [p[np.ix_(orbit, orbit)] for p in p3]
            assert all(np.array_equal(a, b) for a, b in zip(pblocks, expected_p))
            sign_gauges = []
            for signs in itertools.product((1, -1), repeat=6):
                diagonal = np.diag(signs)
                if np.array_equal(diagonal @ gblock @ diagonal, expected_g):
                    sign_gauges.append(signs)
            assert len(sign_gauges) == 2

            rays = []
            for chi, (a, b) in enumerate(pair_positions, start=1):
                compressed = gblock[np.ix_([a,b],[a,b])]
                assert compressed[0,0] == 15 and compressed[1,1] == 15
                assert abs(int(compressed[0,1])) == 7 and compressed[0,1] == compressed[1,0]
                off_diagonal = int(compressed[0,1])
                for sign in (1, -1):
                    eigen_num = 15 + sign * off_diagonal
                    compressed_vector = np.array([1, sign], dtype=np.int64)
                    assert np.array_equal(compressed @ compressed_vector, eigen_num * compressed_vector)
                    vector = np.zeros(6, dtype=np.int64)
                    vector[a], vector[b] = 1, sign
                    q_num = np.outer(vector, vector)  # projector is q_num/2
                    assert np.array_equal(q_num @ q_num, 2 * q_num)
                    rays.append({"chi": chi, "sign": sign, "G1_eigenvalue": f"{eigen_num}/6", "projector_numerator": q_num})
            assert len(rays) == 6
            assert np.array_equal(sum((r["projector_numerator"] for r in rays), start=np.zeros((6,6), dtype=np.int64)), 2*np.eye(6, dtype=np.int64))

            # The six spectral rays are not the regular group basis: r2 sends
            # at least one ray to a superposition rather than another ray.
            r2block = r2[np.ix_(orbit, orbit)]
            qnums = [r["projector_numerator"] for r in rays]
            r2_permutes_all_rays = all(
                any(np.array_equal(r2block @ q @ r2block.T, target) for target in qnums)
                for q in qnums
            )
            assert r2_permutes_all_rays is False
            copy_records.append({
                "representative": orbit[0],
                "marked_G1_block_diagonal_sign_gauge_equivalent": True,
                "diagonal_sign_gauges_to_standard_block": len(sign_gauges),
                "marked_Pchi_blocks_identical": True,
                "six_rank_one_clock_Fourier_rays": True,
                "compressed_G1_numerator_eigenvalues": [8,22],
                "full_Braid_action_permutes_six_spectral_rays": False
            })
        assert len(copy_records) == 4
        sector_records.append({"mask": survivor["mask"], "copies": copy_records})
    assert len(sector_records) == 8

    selector = {
        "all_32_sector_copy_blocks_markedly_diagonal_sign_gauge_equivalent": True,
        "unique_copy_selected": False,
        "within_copy_Pchi_G1_spectral_rays": "six orthogonal rank-one rays labelled by three chi values and two clock eigenvalues 4/3 and 11/3",
        "spectral_rays_are_regular_group_label_basis": False,
        "unique_group_identity_selected": False,
        "physical_selector_gate": "FAIL"
    }
    gauge = {
        "regular_orbit_is_S3_torsor": True,
        "basepoint_change": "For b'=h b, the labelled Stinespring isometry changes by an environment-only unitary Q_h mapping |g b> to |g b'>.",
        "copy_change": "Any two regular copies are related by an environment-only isometry carrying their group-labelled bases.",
        "partial_trace_invariant_under_environment_unitary": True,
        "reduced_channel_independent_of_copy_and_basepoint": True,
        "copy_or_basepoint_is_physical_MMR_assumption_for_reduced_channel": False,
        "torsor_gauge_removes_selector_for_reduced_GKSL_channel": True,
        "environment_stress_independent_without_covariant_charge_transport": False
    }
    out = {
        "schema": "siel.dpa.bgce309r1.result.v1",
        "candidate_id": "BGCE309R1",
        "date": "2026-09-23",
        "source_revision": REV,
        "input_hashes_verified": checked,
        "primary_evidence_status": "Exact marked-block theorem plus environment-unitary torsor-gauge equivalence",
        "scientific_layer": "source selector, gauge equivalence, and reduced open quantum dynamics",
        "clock_Fourier_selector": selector,
        "torsor_gauge": gauge,
        "sector_records": sector_records,
        "BGCE308_tail_capacity_retained": True,
        "total_stress_Ward_derived": False,
        "decision": "SPLIT_PASS_SELECTOR_REMOVED_AS_REDUCED_CHANNEL_GAUGE__G1_AND_THE_THREE_FOURIER_PROJECTORS_RESTRICT_TO_MARKED_SIX_DIMENSIONAL_REPRESENTATIONS_ON_ALL_FOUR_REGULAR_COPIES_IN_ALL_EIGHT_SECTORS_WHICH_ARE_EXACTLY_EQUIVALENT_TO_ONE_STANDARD_BLOCK_BY_DIAGONAL_SIGN_UNITARIES_COMMUTING_WITH_ALL_PCHI_SO_NO_PHYSICAL_COPY_IS_SELECTED__THE_COMPRESSED_CLOCK_SPLITS_EACH_OF_THREE_RANK_TWO_FOURIER_SECTORS_INTO_SIX_ORTHOGONAL_RANK_ONE_RAYS_WITH_EIGENVALUES_4_OVER_3_AND_11_OVER_3_BUT_THE_FULL_BRAID_ACTION_DOES_NOT_PERMUTE_THESE_AS_THE_REGULAR_GROUP_BASIS_AND_NO_IDENTITY_BASEPOINT_IS_SELECTED__NEVERTHELESS_ANY_COPY_OR_BASEPOINT_CHANGE_IS_AN_ENVIRONMENT_ONLY_UNITARY_AND_LEAVES_THE_PARTIAL_TRACE_CHANNEL_EXACTLY_INVARIANT_SO_THIS_SELECTOR_IS_NOT_A_PHYSICAL_ASSUMPTION_FOR_THE_REDUCED_GKSL_CHANNEL__IT_REMAINS_UNRESOLVED_FOR_ENVIRONMENT_STRESS_AND_TOTAL_WARD_BALANCE",
        "counter_intuition_scan": {
            "ordinary_explanation": "Stinespring dilations are unique only up to environment isometries, so an unselected ancilla basis need not be a physical ambiguity of the reduced channel.",
            "SIEL_specific_part": "The fourfold regular multiplicity and six clock/Fourier rays are exact features of the actual pointed-Braid tail, not generic labels added afterward.",
            "strongest_counterpattern": "A torsor-gauge-covariant environment charge solving the one-collision G1 balance equation could make the same gauge removal valid for total conservation, not only the reduced channel.",
            "falsifier": "Two basepoint or copy choices producing different reduced channels, or a source mark uniquely selecting one physical copy/basepoint."
        },
        "next_gate": "BGCE310_TORSOR_GAUGE_COVARIANT_ENVIRONMENT_CHARGE_AND_TOTAL_G1_BALANCE_GATE",
        "runtime_class": "SUBSECOND_EXACT_MARKED_BLOCK_AND_GAUGE_EQUIVALENCE_AUDIT_NO_SCAN",
        "formal_E0_E1_E2": "NOT_CLAIMED__DPA_THEORETICAL_GATE_ONLY",
        "claim_ceiling": "BGCE309 removes copy/basepoint selection as a physical assumption for the reduced GKSL channel by exact environment-unitary equivalence. It does not yet make environment stress gauge-covariant, derive a total Ward identity, or close full finite Lorentzian Einstein backreaction."
    }
    # Remove raw matrices from the compact result records.
    (HERE / "RESULT.json").write_text(json.dumps(out, indent=2) + "\n")
    print(out["decision"])


if __name__ == "__main__":
    main()
