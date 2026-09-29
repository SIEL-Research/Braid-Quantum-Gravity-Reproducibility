#!/usr/bin/env python3
"""DPA-SCOUT-BGCE459-001: exact source gluing to Born probability gate."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]

INPUTS = {
    "bgce139_raw": (
        "audits/SRA_DPA_BGCE139_SOURCE_SPECTRAL_CYLINDER_OPERATIONAL_EVENT_IDENTIFICATION_GATE_20260919/RAW_OUTPUT.json",
        "ddf630fbaff1ae4e72c778f47dc2bed6906da0a8aa17d4e6a98d2c96791955e9",
    ),
    "bgce458_raw": (
        "audits/SRA_DPA_BGCE458_BARE_BRAID_ORIENTED_CYCLE_TO_COMPLEX_KINEMATICS_GATE_20260925/DPA_SCOUT_001/RAW_OUTPUT.json",
        "0db4d8cb8cb92cc5defadda23b84a1e1f59c5b66cdf1b8c971e57e60103a5c5a",
    ),
    "bgce458_result": (
        "audits/SRA_DPA_BGCE458_BARE_BRAID_ORIENTED_CYCLE_TO_COMPLEX_KINEMATICS_GATE_20260925/DPA_SCOUT_001/RESULT.json",
        "ea9874a062e2c90e9cdcd26cc7c22834f8c59d9abc67d895076099e43dd8a7d3",
    ),
    "ocbfh017": (
        "projects/active/discovery_partner/formal_checks/ocbfh017_source_cup_trace_necessity_certificate_v1.json",
        "54c20f4c0df9d757746fdafff522e84a63225b68224c4a35ad0939732de2e517",
    ),
    "captower194r": (
        "projects/active/discovery_partner/formal_checks/disc008_captower194r_coherent_brauer_cap_tower_v1.json",
        "98011b7f02fbbc99a8cf34f7a8eb837135c784baf5a3b498c6dacc8d29bafe14",
    ),
    "ocbfh007": (
        "projects/active/discovery_partner/formal_checks/ocbfh007_reciprocal_crossing_parallelogram_quadratic_origin_certificate_v1.json",
        "a891e2db7642ba5870a774ffc89c9991f40bc4a740b8309d2a6ae1b40fd7aa41",
    ),
}


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def load_verified_inputs() -> dict[str, dict]:
    loaded = {}
    for name, (relative, expected) in INPUTS.items():
        path = REPO / relative
        actual = digest(path)
        assert actual == expected, (name, actual, expected)
        loaded[name] = json.loads(path.read_text())
    return loaded


def load_bgce458_module():
    path = REPO / "audits/SRA_DPA_BGCE458_BARE_BRAID_ORIENTED_CYCLE_TO_COMPLEX_KINEMATICS_GATE_20260925/DPA_SCOUT_001/evaluate_scout.py"
    spec = importlib.util.spec_from_file_location("bgce458_frozen", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    module.REPO = REPO
    module.SOURCE = REPO / INPUTS["bgce139_raw"][0]
    return module


def canonical_cycles(perm: tuple[int, ...], length: int) -> list[tuple[int, ...]]:
    seen = set()
    cycles = []
    for start in range(len(perm)):
        if start in seen:
            continue
        orbit = []
        value = start
        while value not in seen:
            seen.add(value)
            orbit.append(value)
            value = perm[value]
        if len(orbit) == length:
            minimum = min(orbit)
            while orbit[0] != minimum:
                orbit = orbit[1:] + orbit[:1]
            cycles.append(tuple(orbit))
    return sorted(cycles)


def norm_squared(vector: dict[int, int]) -> int:
    return sum(value * value for value in vector.values())


def add_scaled(left: dict[int, int], right: dict[int, int], scale: int) -> dict[int, int]:
    result = dict(left)
    for key, value in right.items():
        result[key] = result.get(key, 0) + scale * value
        if result[key] == 0:
            del result[key]
    return result


def cycle_difference(cycle: tuple[int, ...]) -> dict[int, int]:
    return {cycle[0]: 1, cycle[1]: -1}


def restrict(vector: dict[int, int], support: set[int]) -> dict[int, int]:
    return {key: value for key, value in vector.items() if key in support}


def power_weight_probability(first_amplitude: int, second_amplitude: int, exponent: int) -> Fraction:
    return Fraction(abs(first_amplitude) ** exponent, abs(first_amplitude) ** exponent + abs(second_amplitude) ** exponent)


def parallelogram_record(exponent: int) -> dict:
    # u=(1,1), v=(1,-1); q_r(z)=sum |z_i|^r.
    left = 2 ** exponent + 2 ** exponent
    right = 2 * (1 + 1) + 2 * (1 + 1)
    return {"exponent": exponent, "left": left, "right": right, "passes": left == right}


def run() -> dict:
    data = load_verified_inputs()
    bgce458 = load_bgce458_module()
    table = bgce458.pair_table_from_source()
    r1 = bgce458.perm_for_site(table, 0)
    r2 = bgce458.perm_for_site(table, 1)
    c = bgce458.compose(r1, r2)
    cycles = canonical_cycles(c, 3)
    assert len(cycles) == 36
    assert bgce458.power(c, 3) == tuple(range(125))

    baseline = data["bgce458_raw"]
    focal = next(row for row in baseline["rows"] if row["name"] == "actual_pointed_braid_event")
    assert focal["reconstructed_complex_dimension"] == 36
    assert focal["P_real_rank"] == 72
    assert data["bgce458_result"]["born_rule"].startswith("OPEN")

    cup = data["ocbfh017"]
    assert cup["decision"]["normalized_trace_from_source_cap_marginal"] == "PASS_EXACT"
    assert cup["decision"]["unique_cup_compatible_split_observation"] == "PASS_EXACT"
    assert cup["decision"]["forced_by_split_and_comoving_covariance_alone"] == "REFUTED_EXACT"
    cap_tower = data["captower194r"]
    theorem = cap_tower["all_n_diagram_quotient_theorem"]
    assert theorem["status"] == "PASS_ALL_N_DIAGRAM_QUOTIENT_ISOMETRY_THEOREM"
    assert theorem["source_assumptions"]["dagger_errors"] == {
        "ordinary_F_minus_F_star": 0,
        "ordinary_P_minus_P_star": 0,
        "source_F_minus_F_star": 0,
        "source_P_minus_P_star": 0,
    }

    first_cycle, second_cycle = cycles[:2]
    x = cycle_difference(first_cycle)
    y = cycle_difference(second_cycle)
    psi = add_scaled(x, y, 2)
    effect_psi = restrict(psi, set(first_cycle))
    assert norm_squared(x) == 2
    assert norm_squared(y) == 2
    assert norm_squared(psi) == 10
    assert effect_psi == x
    born = Fraction(norm_squared(effect_psi), norm_squared(psi))
    assert born == Fraction(1, 5)

    # The selected orbit is C-invariant. Its diagonal support projector therefore
    # commutes with C, A=C-C^-1, P, and J=A/sqrt(3); it is self-adjoint for delta counting.
    assert {c[index] for index in first_cycle} == set(first_cycle)
    assert not set(first_cycle).intersection(second_cycle)

    controls = {
        "r1": {
            "probability": str(power_weight_probability(1, 2, 1)),
            "parallelogram": parallelogram_record(1),
        },
        "r2": {
            "probability": str(power_weight_probability(1, 2, 2)),
            "parallelogram": parallelogram_record(2),
        },
        "r4": {
            "probability": str(power_weight_probability(1, 2, 4)),
            "parallelogram": parallelogram_record(4),
        },
    }
    assert controls["r2"]["probability"] == str(born)
    assert controls["r2"]["parallelogram"]["passes"]
    assert controls["r1"]["probability"] != str(born)
    assert controls["r4"]["probability"] != str(born)
    assert not controls["r1"]["parallelogram"]["passes"]
    assert not controls["r4"]["parallelogram"]["passes"]
    previous = data["ocbfh007"]["norm_blind_reciprocal_return_gate"]
    assert not previous["parallelogram_witnesses"]["l1"]["parallelogram_identity"]
    assert previous["parallelogram_witnesses"]["l2_squared"]["parallelogram_identity"]

    return {
        "schema": "siel.dpa.bgce459.raw.v1",
        "scout_id": "DPA-SCOUT-BGCE459-001",
        "gate_id": "BGCE459",
        "attempt": "0001",
        "source_commit": "0de3fde9ca4d2f896eac3c63f948641da104843b",
        "primary_evidence_status": "Theoretical derivation",
        "scientific_layer": "finite source-dagger projective probability reconstruction",
        "forbidden_inputs_used": [],
        "input_hashes_verified": len(INPUTS),
        "complex_carrier": {
            "real_history_atoms": 125,
            "C_three_cycles": len(cycles),
            "P_real_rank": focal["P_real_rank"],
            "complex_dimension": focal["reconstructed_complex_dimension"],
            "state_space": "nonzero rays in H=im(P), with complex scalar action aI+bJ derived from J^2=-I",
        },
        "source_gluing": {
            "atom_kernel": "delta equality counting",
            "dagger": "source reversal; cap and evaluation are certified adjoints",
            "extension_uniqueness": "Sesquilinearity fixes h(sum a_i e_i, sum b_j e_j)=sum conjugate(a_i)b_j delta_ij coefficient by coefficient; normalization removes the common loop scale.",
            "born_functional": "p(E|psi)=h(Epsi,Epsi)/h(psi,psi)=h(psi,Epsi)/h(psi,psi) for a dagger projector E",
            "cup_trace_status": cup["decision"]["normalized_trace_from_source_cap_marginal"],
            "all_stage_closure_status": theorem["status"],
        },
        "exact_two_orbit_witness": {
            "first_C_cycle": list(first_cycle),
            "second_C_cycle": list(second_cycle),
            "state": "psi=x+2y with x,y equal-norm mean-zero vectors on disjoint actual C three-cycles",
            "source_orbit_effect": "E is the first-cycle support projector restricted to H; it is self-adjoint and commutes with C,A,P,J",
            "closure_numerator": norm_squared(effect_psi),
            "closure_denominator": norm_squared(psi),
            "probability": str(born),
        },
        "power_law_controls": controls,
        "weak_axiom_boundary": "Normalized r=1 and r=4 weights remain positive, coordinate-symmetric, phase-blind and product-multiplicative; only the pinned linear dagger closure/parallelogram requirement excludes them. Weak symmetry alone does not derive Born.",
        "observable_scope": "Source cylinder sums invariant under C give self-adjoint complex-linear projectors. The full algebra of all complex self-adjoint operators is not shown to be generated by the pointed Braid.",
        "focal_decision": "PASS_SCOPED_SOURCE_DAGGER_GLUE_UNIQUELY_GIVES_NORMALIZED_SQUARED_NORM_ON_RECONSTRUCTED_FINITE_CARRIER",
        "specificity_decision": "NOT_POINTED_BRAID_SPECIFIC_BECAUSE_THE_SOURCE_CAP_AND_ORIENTED_S3_MECHANISM_HAVE_ORDINARY_FLIP_CONTROLS",
        "strongest_counterpattern": "Without the already certified cup-compatible dagger closure, r=1 and r=4 normalized power laws survive the weaker probability symmetries. The squared rule is forced only inside the fixed source/Brauer observation branch.",
        "claim_ceiling": "BGCE459 establishes a finite normalized squared-norm probability law for arbitrary rays of the BGCE458 reconstructed carrier and source-typed dagger projectors by composing the source equality-counting kernel, reversal, certified cap/evaluation adjunction, and cup-compatible observation. It does not show that every self-adjoint operator is generated by the pointed Braid, provide general physical tensor composition or dynamics, distinguish the actual event table from ordinary flip, recover empirical quantum mechanics, or establish confirmation, Level 3, or Official SIEL adoption.",
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
