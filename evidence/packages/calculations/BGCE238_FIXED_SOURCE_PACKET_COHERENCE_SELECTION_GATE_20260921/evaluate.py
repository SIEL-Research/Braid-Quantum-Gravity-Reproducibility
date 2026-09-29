#!/usr/bin/env python3
"""BGCE238: exact fixed-source packet coherence selection."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
from typing import Any
import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MATRIX = json.loads((HERE / "SOURCE_MATRIX.json").read_text())
REVISION = MATRIX["source_revision"]
EIGENVALUES = (-7, -5, -4, -1, 7)
FUNCTIONALS = (
    ("F00", 0, 0), ("F01", 0, 1), ("F02", 0, 2), ("F03", 0, 3),
    ("F11", 1, 1), ("F12", 1, 2), ("F13", 1, 3),
    ("F22", 2, 2), ("F23", 2, 3), ("F33", 3, 3),
)
PARTITIONS = (
    ("012", ((0, 1, 2),)),
    ("01|2", ((0, 1), (2,))),
    ("02|1", ((0, 2), (1,))),
    ("12|0", ((1, 2), (0,))),
    ("0|1|2", ((0,), (1,), (2,))),
)


def load_module(name: str, relative: str):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def verify_sources() -> dict[str, str]:
    checked = {}
    for relative, expected in MATRIX["inputs_sha256"].items():
        archived = subprocess.check_output(["git", "show", f"{REVISION}:{relative}"], cwd=ROOT)
        assert archived == (ROOT / relative).read_bytes(), f"source drift: {relative}"
        actual = hashlib.sha256(archived).hexdigest()
        assert actual == expected, relative
        checked[relative] = actual
    return checked


def same_rational(left, right) -> bool:
    return np.array_equal(left[0] * right[1], right[0] * left[1])


def build_output() -> dict[str, Any]:
    checked = verify_sources()
    prior234 = json.loads((ROOT / "records/BGCE234_INTERSECTION_CONDITIONED_MATTER_COMPRESSION_PRESERVATION_GATE_20260921/RESULT.json").read_text())
    prior235 = json.loads((ROOT / "records/BGCE235_FULL_CORNER_MATTER_ACTION_AND_OUTER_UNIT_COMPOSITION_GATE_20260921/RESULT.json").read_text())
    prior236 = json.loads((ROOT / "records/BGCE236_EVENT_EFFECT_TO_COMPRESSION_INSTRUMENT_UNIQUENESS_GATE_20260921/RESULT.json").read_text())
    prior237 = json.loads((ROOT / "records/BGCE237_SOURCE_PARTITION_RETRACTION_MATTER_SELECTION_GATE_20260921/RESULT.json").read_text())
    assert prior234["compression"] == "F_A^cap=P F_A P"
    assert prior234["fitted_coefficient"] is False
    assert prior235["full_nontrivial_corner_matter_action_derived_given_compression_candidate"] is True
    assert prior236["existing_source_uniquely_selects_A_to_PAP"] is False
    assert prior237["all_eight_surviving_partitions"] == [name for name, _ in PARTITIONS]

    bgce237 = load_module(
        "bgce238_bgce237",
        "records/BGCE237_SOURCE_PARTITION_RETRACTION_MATTER_SELECTION_GATE_20260921/evaluate.py",
    )
    bgce141 = load_module(
        "bgce238_bgce141",
        "records/BGCE141_SOURCE_MARK_CHARGE_CYLINDER_CURRENT_TO_DOUBLED_METRIC_STRESS_FUNCTOR_GATE_20260919/evaluate.py",
    )
    authoritative141 = json.loads((ROOT / "records/BGCE141_SOURCE_MARK_CHARGE_CYLINDER_CURRENT_TO_DOUBLED_METRIC_STRESS_FUNCTOR_GATE_20260919/RAW_OUTPUT.json").read_text())
    assert bgce141.build_output() == authoritative141

    bgce191 = load_module(
        "bgce238_bgce191",
        "records/BGCE191_FULL_W_CROSSING_NATURALITY_BARE_MARKED_DISCRIMINATOR_20260920/evaluate.py",
    )
    marker_packets, _ = bgce191.setup()
    marker_by_mask = {mask: p2 for mask, _, p2 in marker_packets}
    ub476 = load_module(
        "bgce238_ub476",
        "records/UB476_BRAID_CASIMIR_SECTION_FREE_SAME_ENERGY_C5_BACKREACTION_GATE/evaluate.py",
    )
    source_manifest = ub476.load(ub476.INPUTS["ub475_source_manifest"])
    commit = source_manifest["commit"]
    ob011 = ub476.git_json(commit, "records/OB011_FULL_EIGHT_SECTOR_TIME_PARITY_CLOCK_ACTION/RESULT.json")
    ob013 = ub476.git_json(commit, "records/OB013_CANONICAL_COMMUTING_TIME_SPACE_QUOTIENT/RESULT.json")
    _, spatial_projectors = ub476.quotient_projectors(ob011, ob013)
    ub443 = load_module(
        "bgce238_ub443",
        "records/UB443_TYPED_SIGNED_SURVIVOR_GAUGE_OR_OBSERVABLE_GATE/evaluate.py",
    )
    survivors, endpoint_j = ub443.build_survivors()
    endpoint25 = np.kron(endpoint_j, np.eye(5, dtype=np.int64))

    records = []
    for survivor in survivors:
        mask = survivor["mask"]
        marker = ub443.partial_trace_second(
            endpoint25 @ survivor["F"] @ endpoint25 @ survivor["H"] @ survivor["R"]
        )
        atom_pairs = [
            bgce237.lift_middle_atom(ub443.spectral_projector_numerator(marker, EIGENVALUES, value))
            for value in EIGENVALUES[:3]
        ]
        full_p = ub476.combine([(Fraction(1), atom) for atom in atom_pairs])
        assert same_rational(full_p, (np.kron(marker_by_mask[mask], np.eye(5, dtype=np.int64)), 2))

        bundle = bgce141.build_metric_bundle(ub476, survivor, spatial_projectors)
        original_packet = [("H_cap", bundle["generator"])] + [
            (name, bundle["transformed"][row][column])
            for name, row, column in FUNCTIONALS
        ]
        fixed_packet = []
        for name, operator in original_packet:
            p_num, p_den = full_p
            op_num, op_den = operator
            fixed_packet.append((
                name,
                ub476.normalize(p_num @ op_num @ p_num, p_den * op_den * p_den),
            ))

        partition_records = []
        for partition_name, partition in PARTITIONS:
            blocks = [
                ub476.combine([(Fraction(1), atom_pairs[index]) for index in block])
                for block in partition
            ]
            fixed_count = 0
            first_changed = None
            for operator_name, operator in fixed_packet:
                retracted = bgce237.block_retraction(ub476, operator, blocks)
                if same_rational(retracted, operator):
                    fixed_count += 1
                    continue
                residual = ub476.combine([(Fraction(1), operator), (Fraction(-1), retracted)])
                first_changed = {
                    "operator": operator_name,
                    "cross_block_residual_rank": bgce237.modular_rank(residual[0]),
                    "cross_block_residual_nonzero": bool(np.any(residual[0])),
                }
                # A single exact changed source operator excludes no-retuning.
                break
            partition_records.append({
                "partition": partition_name,
                "fixed_operators_checked_before_stop": fixed_count,
                "fixes_entire_fixed_packet": fixed_count == len(fixed_packet),
                "first_changed_operator": first_changed,
            })
        records.append({"mask": mask, "partitions": partition_records})

    summary = []
    for partition_name, _ in PARTITIONS:
        items = [
            next(item for item in record["partitions"] if item["partition"] == partition_name)
            for record in records
        ]
        summary.append({
            "partition": partition_name,
            "fixes_packet_in_all_eight": all(item["fixes_entire_fixed_packet"] for item in items),
            "changes_packet_in_all_eight": all(not item["fixes_entire_fixed_packet"] for item in items),
            "first_changed_operators": [
                None if item["first_changed_operator"] is None else item["first_changed_operator"]["operator"]
                for item in items
            ],
            "first_residual_ranks": [
                0 if item["first_changed_operator"] is None else item["first_changed_operator"]["cross_block_residual_rank"]
                for item in items
            ],
        })

    admissible = [item["partition"] for item in summary if item["fixes_packet_in_all_eight"]]
    unique = admissible == ["012"] and all(
        item["changes_packet_in_all_eight"] for item in summary if item["partition"] != "012"
    )
    if unique:
        decision = (
            "PASS_FIXED_SOURCE_PACKET_UNIQUELY_SELECTS_FULL_CORNER_WITHIN_COMPLETE_SOURCE_ATOM_PARTITION_CLASS__"
            "NONTRIVIAL_DEPHASINGS_RETUNE_SOURCE_COHERENCE__INSTRUMENT_UNIQUENESS_NOT_REQUIRED_FOR_MATTER_ACTION__"
            "MMR2_CLOSED_IN_FIXED_SOURCE_EVENT_CONDITIONED_MODEL"
        )
        next_gate = "BGCE239_MMR2_CLOSURE_DEPENDENCY_PROPAGATION_TO_SOURCED_EINSTEIN_GATE"
    else:
        decision = (
            "FAIL_FIXED_SOURCE_PACKET_DOES_NOT_UNIQUELY_SELECT_FULL_CORNER__"
            "CROSS_ATOM_COHERENCE_RECOVERABILITY_LAW_STILL_REQUIRED"
        )
        next_gate = "BGCE239_SOURCE_COHERENCE_RECOVERABILITY_LAW_GATE"

    return {
        "schema": "siel.public-calculation.bgce238.raw.v1",
        "candidate_id": "BGCE238",
        "source_revision": REVISION,
        "input_hashes_verified": checked,
        "baseline_gate": "PASS_BGCE141_EXACT_RAW_REGENERATION_BGCE191_UB443_PROJECTORS_AND_BGCE234_237_ASSERTIONS",
        "endpoint_provenance": "NOT_ISSUED_BY_PUBLIC__THEORETICAL_EXACT_ALGEBRAIC_AUDIT_ONLY",
        "primary_evidence_status": "Theoretical derivation with exact source-identity witnesses",
        "scientific_layer": "fixed event-conditioned matter packet and source-coherence preservation",
        "fixed_packet": {
            "operators": ["H_cap"] + [name for name, _, _ in FUNCTIONALS],
            "definition": "H_cap=P G1 P and F_A_cap=P F_A P",
            "operator_count": 11,
            "retuning_allowed": False,
        },
        "sector_records": records,
        "partition_summary": summary,
        "admissible_partitions_preserving_exact_packet_all_eight": admissible,
        "full_corner_uniquely_selected": unique,
        "scope_correction": {
            "BGCE236_instrument_nonuniqueness_retained": True,
            "unique_post_event_state_update_needed_for_BGCE235_action": False,
            "reason": "BGCE235 uses the fixed corner algebra and fixed compressed source operators, not a unique CP state-update instrument. A dephasing instrument may coexist as a measurement update, but replacing the source packet by its dephased image is a different matter model.",
            "BGCE237_rank_result_retained": True,
            "BGCE237_overstrong_inference_corrected": "Equal rank after operator replacement does not establish equal source identity.",
        },
        "MMR_effect": {
            "MMR2_fixed_source_event_conditioned_model": "CLOSED" if unique else "OPEN",
            "MMR2_braid_only_removed_within_declared_fixed_model": unique,
            "remaining_full_corner_nondemolition_law_for_matter_action": False if unique else True,
            "state_update_instrument_uniqueness": "NOT_REQUIRED_AND_NOT_CLAIMED",
            "outer_P_and_three_fifths": "INHERITED_BGCE235_NO_MANUAL_COEFFICIENT" if unique else "CONDITIONAL",
        },
        "counter_intuition_scan": {
            "tempting_failure": "Because every partition keeps Hessian rank 10, all five are equally valid realizations of the same matter source.",
            "refutation": "The nontrivial partitions obtain rank 10 only after replacing at least one fixed compressed source operator by a dephased operator. They preserve dimension, not the source packet.",
            "ordinary_explanation": "A linear projection can preserve the number of independent observables while changing every observable's off-block entries.",
            "falsifier": "Any nontrivial source-atom partition that fixes H_cap and all ten F_A_cap exactly in every sector defeats unique full-corner selection.",
        },
        "next_gate": next_gate,
        "decision": decision,
        "claim_ceiling": (
            "BGCE238 selects the full corner only within the complete five-element partition-retraction class generated by the three marked source atoms, under exact preservation of the already fixed event-conditioned source packet. "
            "It does not prove uniqueness of arbitrary CP instruments or arbitrary source subalgebras. It closes MMR2 for the fixed source event-conditioned matter model, subject to a dependency propagation audit before upgrading the final sourced Einstein claim. No empirical gravity, natural-sector selection, completed quantum gravity, ontology, subjectivity or consciousness is established."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    output = build_output()
    if args.write:
        (HERE / "RAW_OUTPUT.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({
        "decision": output["decision"],
        "admissible_partitions": output["admissible_partitions_preserving_exact_packet_all_eight"],
        "partition_summary": output["partition_summary"],
        "scope_correction": output["scope_correction"],
        "MMR": output["MMR_effect"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
