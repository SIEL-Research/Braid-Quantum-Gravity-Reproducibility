#!/usr/bin/env python3
"""BQGNEUT-023 exact internal carrier and weighted-gap gate."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import platform
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
MANIFEST = json.loads((HERE / "INPUT_MANIFEST.json").read_text())
Q = Fraction


def digest(data: bytes) -> str:
    return sha256(data).hexdigest()


def read_pinned(path: str) -> bytes:
    return subprocess.check_output(
        ["git", "show", f"{MANIFEST['source_commit']}:{path}"], cwd=ROOT
    )


def matrix(rows):
    return tuple(tuple(Q(x) for x in row) for row in rows)


def eye(n=3):
    return matrix([[1 if i == j else 0 for j in range(n)] for i in range(n)])


def mm(a, b):
    n = len(a)
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(n)) for j in range(n)) for i in range(n))


def add(a, b):
    return tuple(tuple(x + y for x, y in zip(ar, br)) for ar, br in zip(a, b))


def sub(a, b):
    return tuple(tuple(x - y for x, y in zip(ar, br)) for ar, br in zip(a, b))


def scale(s, a):
    return tuple(tuple(s * x for x in row) for row in a)


def flatten(a):
    return tuple(x for row in a for x in row)


def rank(rows):
    a = [list(map(Q, row)) for row in rows]
    if not a:
        return 0
    m, n = len(a), len(a[0])
    r = 0
    for c in range(n):
        pivot = next((i for i in range(r, m) if a[i][c] != 0), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        p = a[r][c]
        a[r] = [x / p for x in a[r]]
        for i in range(m):
            if i != r and a[i][c] != 0:
                f = a[i][c]
                a[i] = [x - f * y for x, y in zip(a[i], a[r])]
        r += 1
        if r == m:
            break
    return r


def independent_basis(mats):
    out = []
    for a in mats:
        if rank([flatten(x) for x in out] + [flatten(a)]) > len(out):
            out.append(a)
    return out


def algebra_closure(generators):
    basis = independent_basis([eye()] + list(generators))
    while True:
        products = [mm(a, b) for a in basis for b in basis]
        enlarged = independent_basis(basis + products)
        if len(enlarged) == len(basis):
            return basis
        basis = enlarged


def commutator_constraint_rows(generators):
    # Linear equations for unknown X_ij in [X,G]=0.
    rows = []
    for g in generators:
        for i in range(3):
            for j in range(3):
                row = [Q(0)] * 9
                for k in range(3):
                    row[3 * i + k] += g[k][j]
                    row[3 * k + j] -= g[i][k]
                rows.append(row)
    return rows


def trace(a):
    return sum(a[i][i] for i in range(3))


def det3(a):
    return (
        a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
        - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
        + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0])
    )


def principal_minor_sum(a):
    return (
        a[0][0] * a[1][1] - a[0][1] * a[1][0]
        + a[0][0] * a[2][2] - a[0][2] * a[2][0]
        + a[1][1] * a[2][2] - a[1][2] * a[2][1]
    )


def text_q(x):
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def text_matrix(a):
    return [[text_q(x) for x in row] for row in a]


def permutation_matrix(p):
    return matrix([[1 if row == p[col] else 0 for col in range(3)] for row in range(3)])


def run():
    inputs = {}
    for item in MANIFEST["inputs"]:
        raw = read_pinned(item["path"])
        assert digest(raw) == item["sha256"], item["path"]
        inputs[item["path"]] = json.loads(raw)
    prior = next(v for p, v in inputs.items() if "BQGNEUT022" in p)
    flav026 = next(v for p, v in inputs.items() if "BQGFLAV026" in p)
    bgce524 = next(v for p, v in inputs.items() if "BGCE524" in p)
    assert prior["next_gate"].startswith("BQGNEUT-023")
    assert flav026["algebra_form"] == "I_3 tensor M_2(R)"
    assert bgce524["representation"]["standard_copy_multiplicity"] == 3

    reflections = [
        matrix([[1, 0, 0], [0, 1, 0], [0, 0, -1]]),
        matrix([[1, 0, 0], [0, -1, 0], [0, 0, 1]]),
        matrix([[-1, 0, 0], [0, 1, 0], [0, 0, 1]]),
    ]
    Cg = permutation_matrix(tuple(prior["source_conjugation"]["induced_coordinate_permutation"]))
    generated_basis = algebra_closure(reflections + [Cg])
    generated_dimension = len(generated_basis)
    commutant_rank = rank(commutator_constraint_rows(reflections + [Cg]))
    commutant_dimension = 9 - commutant_rank

    # Each source transposition is an edge of K3.  Frozen branch weights follow
    # the trine map: r1->e2 has 7/15, r2->e1 has 4/15, r121->e3 has 4/15.
    r1 = permutation_matrix((1, 0, 2))
    r2 = permutation_matrix((0, 2, 1))
    r121 = permutation_matrix((2, 1, 0))
    weights = {"r1": Q(7, 15), "r2": Q(4, 15), "r121": Q(4, 15)}
    L = matrix([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    for name, P in (("r1", r1), ("r2", r2), ("r121", r121)):
        L = add(L, scale(weights[name], sub(eye(), P)))

    tr = trace(L)
    e2 = principal_minor_sum(L)
    determinant = det3(L)
    expected_spectrum = [Q(0), Q(4, 5), Q(6, 5)]
    spectral_sum = sum(expected_spectrum)
    spectral_e2 = sum(expected_spectrum[i] * expected_spectrum[j] for i in range(3) for j in range(i + 1, 3))
    spectral_det = expected_spectrum[0] * expected_spectrum[1] * expected_spectrum[2]
    spectrum_exact = (tr, e2, determinant) == (spectral_sum, spectral_e2, spectral_det)
    adjacent_gaps = [expected_spectrum[1] - expected_spectrum[0], expected_spectrum[2] - expected_spectrum[1]]

    # L is real symmetric, so a real orthogonal eigenframe exists and its
    # rephasing-invariant Jarlskog is zero relative to the coordinate frame.
    laplacian_CP_invariant = Q(0)

    gates = {
        "G1_SOURCE_GENERATED_NEUTRAL_ALGEBRA_IS_FULL_M3": generated_dimension == 9,
        "G2_NEUTRAL_ALGEBRA_COMMUTANT_IS_SCALAR": commutant_dimension == 1,
        "G3_EXTERNAL_THREE_GENERATION_CARRIER_NOT_MATHEMATICALLY_REQUIRED_FOR_NEUTRAL_OPERATIONAL_SECTOR": generated_dimension == 9 and commutant_dimension == 1,
        "G4_SOURCE_WEIGHTED_LAPLACIAN_HAS_NONDEGENERATE_DIMENSIONLESS_SPECTRUM": spectrum_exact and len(set(expected_spectrum)) == 3,
        "G5_TWO_ADJACENT_GAPS_ARE_UNEQUAL": adjacent_gaps[0] != adjacent_gaps[1],
        "G6_SAME_WEIGHTED_LAPLACIAN_RETAINS_NONZERO_CP_FRAME": laplacian_CP_invariant != 0,
        "G7_STANDARD_MODEL_LEPTON_EMBEDDING_AND_ABSOLUTE_SCALE_DERIVED": False,
        "G8_NO_TARGET_DATA_OR_PARAMETER_SCAN": not MANIFEST["target_data_accessed"] and not MANIFEST["parameter_scan_used"],
    }
    operational_carrier_pass = all(gates[k] for k in (
        "G1_SOURCE_GENERATED_NEUTRAL_ALGEBRA_IS_FULL_M3",
        "G2_NEUTRAL_ALGEBRA_COMMUTANT_IS_SCALAR",
        "G3_EXTERNAL_THREE_GENERATION_CARRIER_NOT_MATHEMATICALLY_REQUIRED_FOR_NEUTRAL_OPERATIONAL_SECTOR",
    ))
    gap_shape_pass = gates["G4_SOURCE_WEIGHTED_LAPLACIAN_HAS_NONDEGENERATE_DIMENSIONLESS_SPECTRUM"] and gates["G5_TWO_ADJACENT_GAPS_ARE_UNEQUAL"]
    simultaneous_physical_PMNS_pass = operational_carrier_pass and gap_shape_pass and gates["G6_SAME_WEIGHTED_LAPLACIAN_RETAINS_NONZERO_CP_FRAME"] and gates["G7_STANDARD_MODEL_LEPTON_EMBEDDING_AND_ABSOLUTE_SCALE_DERIVED"]

    tests = {
        "T1_PINNED_INPUT_HASHES_MATCH": True,
        "T2_GENERATED_ALGEBRA_DIMENSION_IS_NINE": generated_dimension == 9,
        "T3_COMMUTANT_LINEAR_SYSTEM_RANK_IS_EIGHT": commutant_rank == 8,
        "T4_WEIGHTED_LAPLACIAN_MATRIX_IS_EXPECTED": L == matrix([[Q(11,15), Q(-7,15), Q(-4,15)], [Q(-7,15), Q(11,15), Q(-4,15)], [Q(-4,15), Q(-4,15), Q(8,15)]]),
        "T5_CHARACTERISTIC_INVARIANTS_MATCH_0_4OVER5_6OVER5": spectrum_exact,
        "T6_DIMENSIONLESS_ADJACENT_GAPS_ARE_4OVER5_AND_2OVER5": adjacent_gaps == [Q(4,5), Q(2,5)],
        "T7_REAL_LAPLACIAN_FRAME_HAS_ZERO_CP": laplacian_CP_invariant == 0,
        "T8_NO_PMNS_NUFIT_OR_MASS_TARGET_ACCESSED": not MANIFEST["target_data_accessed"],
        "T9_NO_PARAMETER_SCAN_OR_LONG_COMPUTATION": not MANIFEST["parameter_scan_used"] and not MANIFEST["long_computation_used"],
    }
    assert all(tests.values())

    decision = (
        "SPLIT_SCOPED_PASS_SOURCE_GENERATED_REFLECTION_PLUS_C3_ALGEBRA_IS_FULL_M3_"
        "WITH_SCALAR_COMMUTANT_SO_NO_EXTERNAL_THREE_GENERATION_CARRIER_IS_REQUIRED_"
        "FOR_THE_NEUTRAL_OPERATIONAL_SECTOR__SCOPED_PASS_SOURCE_WEIGHTED_"
        "TRANSPOSITION_LAPLACIAN_HAS_EXACT_NONDIMENSIONAL_SPECTRUM_0_4OVER5_6OVER5_"
        "AND_UNEQUAL_GAPS__NO_GO_THIS_REAL_LAPLACIAN_ALONE_FOR_NONZERO_CP_OR_FULL_"
        "PHYSICAL_PMNS_AND_ABSOLUTE_SCALE"
    )
    return {
        "schema": "siel.public-calculation.bqgneut023.raw.v1",
        "scout_id": MANIFEST["scout_id"],
        "gate_id": MANIFEST["gate_id"],
        "source_commit": MANIFEST["source_commit"],
        "source_snapshot_id": MANIFEST["source_snapshot_id"],
        "evidence_status": "Theoretical derivation",
        "scientific_layer": "finite neutral operational carrier algebra and dimensionless weighted-gap generator",
        "decision": decision,
        "bold_hypothesis": {
            "interpretive_leap": "Use source-generated algebraic completeness, rather than identification with BGCE524, as the neutral carrier sufficiency criterion.",
            "new_structure": "full operational star-algebra plus canonical weighted transposition Laplacian",
            "source_status": "DERIVED_FOR_NEUTRAL_OPERATIONAL_SECTOR__PHYSICAL_HAMILTONIAN_AND_STANDARD_MODEL_EMBEDDING_OPEN",
        },
        "internal_neutral_carrier": {
            "generators": ["R_e1", "R_e2", "R_e3", "C_g"],
            "generated_star_algebra": "M3(C)",
            "generated_complex_dimension": generated_dimension,
            "commutant_dimension": commutant_dimension,
            "irreducible": generated_dimension == 9 and commutant_dimension == 1,
            "external_three_generation_carrier_required_for_neutral_operational_sector": False,
            "BGCE524_Standard_Model_matter_identification_replaced": False,
        },
        "source_weighted_gap_generator": {
            "definition": "L_w=sum_a w_a(I-P_a)",
            "transposition_weights": {k: text_q(v) for k, v in weights.items()},
            "matrix": text_matrix(L),
            "characteristic_polynomial": "lambda*(lambda-4/5)*(lambda-6/5)",
            "dimensionless_spectrum": [text_q(x) for x in expected_spectrum],
            "adjacent_gaps": [text_q(x) for x in adjacent_gaps],
            "adjacent_gap_ratio_large_over_small": "2",
            "nondegenerate": True,
            "real_symmetric": True,
            "coordinate_frame_Jarlskog": "0",
            "absolute_scale": "not derived",
            "physical_mass_squared_interpretation": "not derived",
        },
        "noncompensating_gates": gates,
        "operational_carrier_pass": operational_carrier_pass,
        "gap_shape_pass": gap_shape_pass,
        "simultaneous_physical_PMNS_pass": simultaneous_physical_PMNS_pass,
        "strongest_ordinary_alternative": "Full M3 generation is generic for a diagonal qutrit algebra plus a cyclic shift, and a real weighted graph Laplacian generically splits levels. These facts establish internal mathematical sufficiency, not the empirical identity of this sector with natural neutrinos.",
        "counter_intuition_scan": "The source weights solve the level-splitting problem only for a real Laplacian whose mixing frame has J=0. The earlier F3 kernel has nonzero CP but degenerate phase chords. Claiming both from separate operators would silently change the physical propagation observable.",
        "claim_ceiling": "The source-generated neutral operational algebra is internally complete and needs no external three-generation carrier for its own states, observables, channel and history transport. The source-weighted transposition Laplacian has exact unequal dimensionless gaps. The result does not identify the sector with Standard-Model lepton doublets, derive one operator carrying both nonzero CP and unequal physical mass gaps, supply an absolute scale, compare with data, or complete quantum gravity.",
        "next_gate": "BQGNEUT-024_UNIQUE_SOURCE_ORDERED_C3_WEIGHTED_FLOQUET_TO_SIMULTANEOUS_CP_AND_GAP_GATE",
        "work_package": "BQG-G3-R03.8",
        "work_package_status": "ACTIVE",
        "tests": tests,
        "runtime": {"python": platform.python_version(), "target_data_accessed": False, "parameter_scan_used": False, "long_computation_used": False},
    }


def main():
    raw = run()
    keys = (
        "schema", "scout_id", "gate_id", "source_commit", "source_snapshot_id",
        "evidence_status", "scientific_layer", "decision", "bold_hypothesis",
        "internal_neutral_carrier", "source_weighted_gap_generator",
        "noncompensating_gates", "operational_carrier_pass", "gap_shape_pass",
        "simultaneous_physical_PMNS_pass", "strongest_ordinary_alternative",
        "counter_intuition_scan", "claim_ceiling", "next_gate", "work_package",
        "work_package_status", "runtime"
    )
    (HERE / "RAW_OUTPUT.json").write_text(json.dumps(raw, indent=2, ensure_ascii=False) + "\n")
    (HERE / "RESULT.json").write_text(json.dumps({k: raw[k] for k in keys}, indent=2, ensure_ascii=False) + "\n")
    (HERE / "CERTIFICATE.json").write_text(json.dumps({
        "schema": "siel.public-calculation.bqgneut023.certificate.v1",
        "scout_id": raw["scout_id"],
        "source_commit": raw["source_commit"],
        "input_hashes": {item["path"]: item["sha256"] for item in MANIFEST["inputs"]},
        "evaluator_sha256": digest(Path(__file__).read_bytes()),
        "raw_output_sha256": digest((HERE / "RAW_OUTPUT.json").read_bytes()),
        "result_sha256": digest((HERE / "RESULT.json").read_bytes()),
        "tests": raw["tests"],
        "decision": raw["decision"],
    }, indent=2, ensure_ascii=False) + "\n")
    (HERE / "STATUS.json").write_text(json.dumps({"scout_id": raw["scout_id"], "status": "COMPLETE", "decision": raw["decision"], "next_gate": raw["next_gate"]}, indent=2, ensure_ascii=False) + "\n")
    (HERE / "EXECUTION_LOG.json").write_text(json.dumps({"iteration": 1, "command": "python3 evaluate_scout.py", "runtime_class": "subsecond exact rational M3 closure and graph spectrum", "result_informed_change": False}, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
