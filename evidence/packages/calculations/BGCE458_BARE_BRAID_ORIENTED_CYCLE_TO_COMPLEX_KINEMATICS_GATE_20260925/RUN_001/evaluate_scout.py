#!/usr/bin/env python3
"""PUBLIC-RUN-BGCE458-001: exact real pointed-Braid to complex-sector audit."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
SOURCE = REPO / "records/BGCE139_SOURCE_SPECTRAL_CYLINDER_OPERATIONAL_EVENT_IDENTIFICATION_GATE_20260919/RAW_OUTPUT.json"


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def pair_table_from_source() -> tuple[int, ...]:
    raw = json.loads(SOURCE.read_text())
    rows = raw["event_transition_gate"]["canonical_transition_on_digit_pairs"]
    assert [tuple(row["input"]) for row in rows] == [divmod(i, 5) for i in range(25)]
    return tuple(5 * row["output"][0] + row["output"][1] for row in rows)


def apply_pair(table: tuple[int, ...], atom: tuple[int, int, int], site: int) -> tuple[int, int, int]:
    values = list(atom)
    out = table[5 * values[site] + values[site + 1]]
    values[site], values[site + 1] = divmod(out, 5)
    return tuple(values)


def perm_for_site(table: tuple[int, ...], site: int) -> tuple[int, ...]:
    result = []
    for atom in itertools.product(range(5), repeat=3):
        moved = apply_pair(table, atom, site)
        result.append(25 * moved[0] + 5 * moved[1] + moved[2])
    return tuple(result)


def compose(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(left[right[i]] for i in range(len(left)))


def inverse(perm: tuple[int, ...]) -> tuple[int, ...]:
    result = [0] * len(perm)
    for i, value in enumerate(perm):
        result[value] = i
    return tuple(result)


def power(perm: tuple[int, ...], exponent: int) -> tuple[int, ...]:
    result = tuple(range(len(perm)))
    for _ in range(exponent):
        result = compose(perm, result)
    return result


def cycle_lengths(perm: tuple[int, ...]) -> list[int]:
    seen: set[int] = set()
    lengths = []
    for start in range(len(perm)):
        if start in seen:
            continue
        value = start
        length = 0
        while value not in seen:
            seen.add(value)
            length += 1
            value = perm[value]
        lengths.append(length)
    return lengths


def yang_baxter_failures(table: tuple[int, ...]) -> int:
    failures = 0
    for atom in itertools.product(range(5), repeat=3):
        left = apply_pair(table, apply_pair(table, apply_pair(table, atom, 0), 1), 0)
        right = apply_pair(table, apply_pair(table, apply_pair(table, atom, 1), 0), 1)
        failures += left != right
    return failures


def basis_relation_failures(cycle: tuple[int, ...]) -> int:
    """Verify (C-C^-1)^2 + (2I-C-C^-1) = 0 on every basis atom."""
    cinv = inverse(cycle)
    failures = 0
    for i in range(len(cycle)):
        # A^2 e_i = e_(C^2 i) - 2 e_i + e_(C^-2 i).
        lhs = Counter({cycle[cycle[i]]: 1, i: -2, cinv[cinv[i]]: 1})
        # 3P e_i = 2 e_i - e_(C i) - e_(C^-1 i).
        lhs.update({i: 2, cycle[i]: -1, cinv[i]: -1})
        failures += any(value for value in lhs.values())
    return failures


def analyse(name: str, table: tuple[int, ...]) -> dict:
    identity25 = tuple(range(25))
    is_permutation = sorted(table) == list(range(25))
    is_involution = is_permutation and compose(table, table) == identity25
    yb_failures = yang_baxter_failures(table)
    r1 = perm_for_site(table, 0)
    r2 = perm_for_site(table, 1)
    c = compose(r1, r2)
    identity125 = tuple(range(125))
    c_order_three = power(c, 3) == identity125
    lengths = cycle_lengths(c)
    fixed_c = lengths.count(1)
    three_cycles = lengths.count(3)
    other_cycles = sorted(length for length in lengths if length not in (1, 3))
    relation_failures = basis_relation_failures(c) if c_order_three else None
    rank_p = 2 * three_cycles if c_order_three and not other_cycles else None
    complex_dimension = rank_p // 2 if rank_p is not None and rank_p % 2 == 0 else None

    fixed_r1 = sum(r1[i] == i for i in range(125))
    multiplicities = None
    if yb_failures == 0 and is_involution and c_order_three:
        numerators = {
            "trivial": 125 + 3 * fixed_r1 + 2 * fixed_c,
            "sign": 125 - 3 * fixed_r1 + 2 * fixed_c,
            "standard_times_six": 2 * 125 - 2 * fixed_c,
        }
        assert numerators["trivial"] % 6 == 0
        assert numerators["sign"] % 6 == 0
        assert numerators["standard_times_six"] % 6 == 0
        multiplicities = {
            "trivial": numerators["trivial"] // 6,
            "sign": numerators["sign"] // 6,
            "standard": numerators["standard_times_six"] // 6,
        }

    # R1 C R1 = C^-1, hence R1 A R1 = -A whenever the S3 relations hold.
    antiunitary_relation = compose(r1, compose(c, r1)) == inverse(c)
    c_commutes_with_a = c_order_three
    return {
        "name": name,
        "pair_table_is_permutation": is_permutation,
        "pair_table_is_involution": is_involution,
        "pair_fixed_atoms": sum(table[i] == i for i in range(25)),
        "pair_transpositions": cycle_lengths(table).count(2) if is_permutation else None,
        "yang_baxter_rows": 125,
        "yang_baxter_failures": yb_failures,
        "three_history_atoms": 125,
        "fixed_points_R1": fixed_r1,
        "C_order_three": c_order_three,
        "C_fixed_points": fixed_c,
        "C_three_cycles": three_cycles,
        "C_other_cycle_lengths": other_cycles,
        "A_squared_plus_3P_basis_failures": relation_failures,
        "P_real_rank": rank_p,
        "reconstructed_complex_dimension": complex_dimension,
        "S3_real_irrep_multiplicities": multiplicities,
        "C_is_complex_linear_on_imP": c_commutes_with_a,
        "R1_reverses_J": antiunitary_relation,
        "positive_kernel": "delta equality counting on the 125 real history atoms",
        "positive_kernel_preserved_by_R1_R2": sorted(r1) == list(range(125)) and sorted(r2) == list(range(125)),
    }


def run() -> dict:
    actual = pair_table_from_source()
    identity = tuple(range(25))
    flip = tuple(5 * right + left for left in range(5) for right in range(5))
    broken = list(identity)
    broken[0], broken[1] = broken[1], broken[0]
    rows = [
        analyse("actual_pointed_braid_event", actual),
        analyse("identity_control", identity),
        analyse("ordinary_flip_control", flip),
        analyse("deterministic_involutive_yang_baxter_broken_control", tuple(broken)),
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
    assert by_name["ordinary_flip_control"]["P_real_rank"] == 120
    assert by_name["deterministic_involutive_yang_baxter_broken_control"]["yang_baxter_failures"] > 0

    return {
        "schema": "siel.public-calculation.bgce458.raw.v1",
        "scout_id": "PUBLIC-RUN-BGCE458-001",
        "gate_id": "BGCE458",
        "source_commit": "abd5261df92d1639c4a16d6e2309b542d176fe14",
        "primary_evidence_status": "Theoretical derivation",
        "scientific_layer": "finite quantum-kinematic reconstruction candidate",
        "forbidden_quantum_inputs_used": [],
        "source_input_sha256": digest(SOURCE),
        "rows": rows,
        "exact_group_algebra_identity": "For C^3=I, A=C-C^-1 and 3P=2I-C-C^-1 give A^2=-3P exactly",
        "focal_decision": "PASS_SCOPED_SOURCE_ORIENTED_COMPLEX_KINEMATIC_SECTOR",
        "specificity_decision": "NOT_POINTED_BRAID_SPECIFIC_BECAUSE_ORDINARY_FLIP_CONTROL_ALSO_HAS_A_NONZERO_COMPLEX_SECTOR",
        "born_rule_decision": "OPEN_NO_SOURCE_DERIVATION_FOR_ARBITRARY_SUPERPOSITION_PROBABILITIES",
        "strongest_counterpattern": "The ordinary flip comparator has the same order-three oriented-cycle mechanism and a larger complex sector, so the mechanism follows from oriented involutive Yang-Baxter/S3 kinematics rather than the distinctive pointed-Braid event table.",
        "claim_ceiling": "The actual finite three-history pointed-Braid event action has a source-oriented rank-72 real sector with exact J^2=-I after normalization, hence a 36-dimensional complex kinematic carrier with positive counting norm. This does not derive the full M_(5^n)(C) tower, a unique complex structure on every sector, a source-selected state, arbitrary observables, tensor composition, interference probabilities, the Born rule, dynamics, QFT, empirical quantum mechanics, confirmation, Level 3 or Official SIEL adoption. The ordinary flip control also passes, so pointed-Braid specificity is not established."
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
