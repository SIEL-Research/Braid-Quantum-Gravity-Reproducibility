#!/usr/bin/env python3
"""Attempt-0003 exact runner with the disclosed flip-control rank correction."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
FROZEN = HERE / "evaluate_scout.py"
SPEC = importlib.util.spec_from_file_location("bgce458_frozen_attempt_0001", FROZEN)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)
MODULE.REPO = HERE.parents[2]
MODULE.SOURCE = MODULE.REPO / "audits/SRA_DPA_BGCE139_SOURCE_SPECTRAL_CYLINDER_OPERATIONAL_EVENT_IDENTIFICATION_GATE_20260919/RAW_OUTPUT.json"


def run() -> dict:
    actual = MODULE.pair_table_from_source()
    identity = tuple(range(25))
    flip = tuple(5 * right + left for left in range(5) for right in range(5))
    broken = list(identity)
    broken[0], broken[1] = broken[1], broken[0]
    rows = [
        MODULE.analyse("actual_pointed_braid_event", actual),
        MODULE.analyse("identity_control", identity),
        MODULE.analyse("ordinary_flip_control", flip),
        MODULE.analyse("deterministic_involutive_yang_baxter_broken_control", tuple(broken)),
    ]
    by_name = {row["name"]: row for row in rows}
    focal = by_name["actual_pointed_braid_event"]
    assert focal["pair_table_is_involution"]
    assert focal["pair_fixed_atoms"] == 9
    assert focal["pair_transpositions"] == 8
    assert focal["yang_baxter_failures"] == 0
    assert focal["C_order_three"]
    assert focal["A_squared_plus_3P_basis_failures"] == 0
    assert focal["P_real_rank"] == 72
    assert focal["reconstructed_complex_dimension"] == 36
    assert focal["S3_real_irrep_multiplicities"] == {"trivial": 49, "sign": 4, "standard": 36}
    assert focal["R1_reverses_J"]
    assert by_name["identity_control"]["P_real_rank"] == 0
    # Disclosed Attempt-0002 correction: 40 three-cycles each contribute a
    # two-real-dimensional nontrivial plane, hence rank 80 rather than 120.
    assert by_name["ordinary_flip_control"]["C_three_cycles"] == 40
    assert by_name["ordinary_flip_control"]["P_real_rank"] == 80
    assert by_name["deterministic_involutive_yang_baxter_broken_control"]["yang_baxter_failures"] > 0

    return {
        "schema": "siel.dpa.bgce458.raw.v1",
        "scout_id": "DPA-SCOUT-BGCE458-001",
        "gate_id": "BGCE458",
        "attempt": "0003",
        "source_commit": "abd5261df92d1639c4a16d6e2309b542d176fe14",
        "primary_evidence_status": "Theoretical derivation",
        "scientific_layer": "finite quantum-kinematic reconstruction candidate",
        "forbidden_quantum_inputs_used": [],
        "source_input_sha256": MODULE.digest(MODULE.SOURCE),
        "rows": rows,
        "exact_group_algebra_identity": "For C^3=I, A=C-C^-1 and 3P=2I-C-C^-1 give A^2=-3P exactly",
        "focal_decision": "PASS_SCOPED_SOURCE_ORIENTED_COMPLEX_KINEMATIC_SECTOR",
        "specificity_decision": "NOT_POINTED_BRAID_SPECIFIC_BECAUSE_ORDINARY_FLIP_CONTROL_ALSO_HAS_A_NONZERO_COMPLEX_SECTOR",
        "born_rule_decision": "OPEN_NO_SOURCE_DERIVATION_FOR_ARBITRARY_SUPERPOSITION_PROBABILITIES",
        "strongest_counterpattern": "The ordinary flip comparator has the same order-three oriented-cycle mechanism and a nonzero complex sector, so the mechanism follows from oriented involutive Yang-Baxter/S3 kinematics rather than the distinctive pointed-Braid event table.",
        "claim_ceiling": "The actual finite three-history pointed-Braid event action has a source-oriented rank-72 real sector with exact J^2=-I after normalization, hence a 36-dimensional complex kinematic carrier with positive counting norm. This does not derive the full M_(5^n)(C) tower, a unique complex structure on every sector, a source-selected state, arbitrary observables, tensor composition, interference probabilities, the Born rule, dynamics, QFT, empirical quantum mechanics, confirmation, Level 3 or Official SIEL adoption. The ordinary flip control also passes, so pointed-Braid specificity is not established."
    }


print(json.dumps(run(), indent=2, sort_keys=True))
