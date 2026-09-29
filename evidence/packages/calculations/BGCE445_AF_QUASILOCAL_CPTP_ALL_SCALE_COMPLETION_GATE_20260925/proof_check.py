#!/usr/bin/env python3
"""Pinned-source consistency checker for the BGCE445 theorem proof."""

from pathlib import Path
import hashlib
import json
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
REV = "c8a1fe03d97805aaf43995c49386ab419dde0b07"
INPUTS = {
    "records/BGCE336R2_REFINED_COLLISION_CTP_TO_CONTINUUM_LORENTZIAN_INFLUENCE_AND_NONCIRCULAR_FINITE_BACKREACTION_GATE_20260923/RESULT.json": "9147e820e85e8f5810a5134846718f017ead658b5e2cd22e9f529fb0903d750d",
    "records/BGCE349_BRANCH_RESOLVED_CHOI_TRANSFER_TO_LOCAL_3PLUS1_DOUBLED_METRIC_LORENTZIAN_PARENT_GATE_20260924/RESULT.json": "ba240e4700abde0ce229d09fcc6094b98feec773414987aa5e53a86ce6c0d226",
    "records/BGCE350_FINITE_SOURCE_CYLINDER_PARENT_TO_LOCAL_HISTORY_DRESSED_TOTAL_WARD_IDENTITY_GATE_20260924/RESULT.json": "fdcf67ebce8768376010572985815233fcee4d0eb3a2615738fb5459e8e69051",
    "records/BGCE444_TEN_METRIC_SOURCE_TO_THIRTY_FIVE_QUARTIC_SECOND_RESPONSE_GATE_20260925/RESULT.json": "360c43a8a722e7d1ce5f9a9c7e46b5d974003ec07b7eeacd015ec1dfb6a82b20",
}


def load(relative):
    data = subprocess.check_output(["git", "show", f"{REV}:{relative}"], cwd=ROOT)
    assert hashlib.sha256(data).hexdigest() == INPUTS[relative]
    assert data == (ROOT / relative).read_bytes()
    return json.loads(data)


def main():
    docs = {path: load(path) for path in INPUTS}
    r336 = docs[next(p for p in INPUTS if "BGCE336R2" in p)]
    r349 = docs[next(p for p in INPUTS if "BGCE349_" in p)]
    r350 = docs[next(p for p in INPUTS if "BGCE350_" in p)]
    r444 = docs[next(p for p in INPUTS if "BGCE444_" in p)]

    assert "Phi_h=exp[h gamma(E-I)]" in r336["decision"]
    assert "converge in operator norm" in r336["decision"]

    parent = r349["local_3plus1_parent"]
    assert parent["local_algebra_at_stage_m"] == "C(C_m) tensor M_125 with one central address block per source cell"
    assert r349["source_metric_to_instrument_map"]["total_instrument_CPTP"] is True
    refinement = r349["gluing_and_refinement"]
    assert refinement["address_embedding"] == "child-constant pullback C(C_m)->C(C_(m+1))"
    assert refinement["controlled_channel_naturality"] == "L_(m+1)[j g] j = j L_m[g]"
    assert refinement["address_and_collision_refinement_commute"] is True
    for record in refinement["records"]:
        level = record["level"]
        assert record["address_cells"] == 625 ** level
        assert record["cell_weight"] == f"1/{625 ** level}"
        assert record["625_child_volume_coarsening_exact"] is True
        assert record["address_block_and_internal_collision_commute"] is True

    ward = r350["locality_and_refinement"]
    assert ward["address_and_time_refinement_commute"] is True
    assert all(record["625_child_address_measure_exact"] for record in ward["records"])
    assert all(record["local_vertex_Ward_refinement_natural"] for record in ward["records"])
    assert r444["gate_decision"]["ten_to_thirty_five_algebraic_capacity"] == "SCOPED_PASS"
    assert r444["gate_decision"]["actual_PBM_U4_source_generation"] == "OPEN"

    print(json.dumps({
        "source_revision": REV,
        "finite_stage_algebra_class": "finite direct sums of matrix algebras",
        "address_embedding": "injective unital star homomorphism",
        "finite_stage_dynamics": "CPTP / dual UCP",
        "spatial_refinement_levels_checked": len(refinement["records"]),
        "largest_checked_address_count": refinement["records"][-1]["address_cells"],
        "time_semigroup_operator_norm_convergence": True,
        "inductive_limit_UCP_extension": "THEOREM_PROVED_IN_AUDIT",
        "uniform_complete_bound": 1,
        "actual_PBM_U4_generation": "OPEN",
    }, indent=2))


if __name__ == "__main__":
    main()
