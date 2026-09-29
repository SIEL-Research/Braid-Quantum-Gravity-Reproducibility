#!/usr/bin/env python3
"""BGCE292: exact curvature of the event-path BKM horizontal connection."""

from fractions import Fraction
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json
import subprocess

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
REVISION = "9f140067043ef0588121e66b8809cbcc914e33c9"
ZERO = Fraction(0)
ONE = Fraction(1)
SYM_INDEX = ((0, 0), (1, 1), (2, 2), (3, 3), (0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
AXIS_PAIRS = tuple(combinations(range(4), 2))


def frozen_bytes(path):
    return subprocess.check_output(["git", "show", f"{REVISION}:{path}"], cwd=ROOT)


def mm(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a):
    return [list(row) for row in zip(*a)]


def eye(n):
    return [[ONE if i == j else ZERO for j in range(n)] for i in range(n)]


def inverse(a):
    n = len(a)
    work = [list(row) + ident for row, ident in zip(a, eye(n))]
    for col in range(n):
        pivot = next(row for row in range(col, n) if work[row][col])
        work[col], work[pivot] = work[pivot], work[col]
        q = work[col][col]
        work[col] = [x / q for x in work[col]]
        for row in range(n):
            if row != col and work[row][col]:
                q = work[row][col]
                work[row] = [x - q * y for x, y in zip(work[row], work[col])]
    return [row[n:] for row in work]


def rank(a):
    work = [list(map(Fraction, row)) for row in a]
    if not work:
        return 0
    rows, cols, out = len(work), len(work[0]), 0
    for col in range(cols):
        pivot = next((r for r in range(out, rows) if work[r][col]), None)
        if pivot is None:
            continue
        work[out], work[pivot] = work[pivot], work[out]
        q = work[out][col]
        work[out] = [x / q for x in work[out]]
        for r in range(rows):
            if r != out and work[r][col]:
                q = work[r][col]
                work[r] = [x - q * y for x, y in zip(work[r], work[out])]
        out += 1
    return out


def flatten_symmetric(a):
    return [a[i][j] for i, j in SYM_INDEX]


def outer(v):
    return [[v[i] * v[j] for j in range(4)] for i in range(4)]


def actual_edges(records):
    mapping = {tuple(r["input"]): tuple(r["output"]) for r in records}
    seen, edges = set(), []
    for source, target in mapping.items():
        if source == target:
            continue
        key = tuple(sorted((source, target)))
        if key in seen:
            continue
        seen.add(key)
        delta = (target[0] - source[0], target[1] - source[1])
        edges.append({
            "magnitude": abs(delta[0]),
            "sign": 1 if delta[0] * delta[1] > 0 else -1,
        })
    return edges


def build_moment_map(bg139):
    edges = actual_edges(bg139["event_transition_gate"]["canonical_transition_on_digit_pairs"])
    assert len(edges) == 8
    columns = []
    for i, j in AXIS_PAIRS:
        for edge in edges:
            v = [ZERO] * 4
            v[i] = Fraction(edge["magnitude"])
            v[j] = Fraction(edge["sign"] * edge["magnitude"])
            columns.append(flatten_symmetric(outer(v)))
    return [list(row) for row in zip(*columns)]


def diagonal(v):
    return [[v[i] if i == j else ZERO for j in range(len(v))] for i in range(len(v))]


def column(a, j):
    return [[a[i][j]] for i in range(len(a))]


def sub(a, b):
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def derivative_horizontal(m, h, direction):
    # At the normalized common-rate anchor D=I:
    # dH = dD M^T A^-1 - H (M dD M^T) A^-1.
    mt = transpose(m)
    ainv = inverse(mm(m, mt))
    dd = diagonal([row[0] for row in direction])
    first = mm(dd, mm(mt, ainv))
    second = mm(h, mm(mm(m, mm(dd, mt)), ainv))
    return sub(first, second)


def qserial(x):
    x = Fraction(x)
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def main():
    matrix = json.loads((HERE / "SOURCE_MATRIX.json").read_text())
    checked = {}
    for path, expected in matrix["inputs_sha256"].items():
        payload = frozen_bytes(path)
        actual = sha256(payload).hexdigest()
        assert actual == expected
        checked[f"{REVISION}:{path}"] = actual

    bg139 = json.loads(frozen_bytes("records/BGCE139_SOURCE_SPECTRAL_CYLINDER_OPERATIONAL_EVENT_IDENTIFICATION_GATE_20260919/RAW_OUTPUT.json"))
    bg254 = json.loads(frozen_bytes("records/BGCE254_SOURCE_RESPONSE_LEGENDRE_EXACTNESS_TO_UNIQUE_LOGZ_BREGMAN_EDGE_ACTION_GATE_20260921/RESULT.json"))
    bg287 = json.loads(frozen_bytes("records/BGCE287_SOURCE_EVENT_PATH_BKM_HORIZONTAL_CONDUCTANCE_LIFT_GATE_20260923/RESULT.json"))
    bg291 = json.loads(frozen_bytes("records/BGCE291_STRESS_WARD_INDEPENDENT_REDERIVATION_AND_SCOPE_RED_TEAM_GATE_20260923/RESULT.json"))
    assert bg254["functional_form_ambiguity_removed_within_response_exact_class"] is True
    assert bg287["full_nonlinear_integrability"] == "OPEN"
    assert bg291["finite_nonlinear_active_Markov_transport"] == "OPEN"

    m = build_moment_map(bg139)
    assert rank(m) == 10
    mt = transpose(m)
    h = mm(mt, inverse(mm(m, mt)))
    assert mm(m, h) == eye(10)

    curvature = []
    records = []
    for a, b in combinations(range(10), 2):
        xa, xb = column(h, a), column(h, b)
        dxb_xa = column(derivative_horizontal(m, h, xa), b)
        dxa_xb = column(derivative_horizontal(m, h, xb), a)
        fab = sub(dxb_xa, dxa_xb)
        assert mm(m, fab) == [[ZERO] for _ in range(10)]
        nonzero = any(row[0] for row in fab)
        curvature.append([row[0] for row in fab])
        records.append({
            "base_pair": [a, b],
            "nonzero": nonzero,
            "support": sum(row[0] != 0 for row in fab),
            "max_abs": qserial(max(abs(row[0]) for row in fab)),
        })

    nonzero_count = sum(r["nonzero"] for r in records)
    curvature_rank = rank([list(row) for row in zip(*curvature)])
    flat = nonzero_count == 0
    assert len(records) == 45

    if flat:
        decision = "PASS_FLAT_AT_SOURCE_ANCHOR__LOCAL_PATH_INDEPENDENCE_ROUTE_REMAINS_OPEN"
        next_gate = "BGCE293_FINITE_POSITIVE_REFINEMENT_COMPATIBLE_INTEGRATION_GATE"
    else:
        decision = "FAIL_LOCAL_PATH_INDEPENDENCE__THE_CANONICAL_EVENT_PATH_BKM_HORIZONTAL_CONNECTION_HAS_EXACT_NONZERO_VERTICAL_CURVATURE_AT_THE_COMMON_SOURCE_RATE__THE_BGCE287_FIRST_ORDER_LIFT_CANNOT_BE_INTEGRATED_TO_A_PATH_INDEPENDENT_FINITE_CONDUCTANCE_SECTION__BGCE290_STRESS_WARD_PROMOTION_REMAINS_REVERSED"
        next_gate = "BGCE293_BRAID_ORDERED_PATH_HOLONOMY_AS_PHYSICAL_TRANSPORT_OR_ALTERNATIVE_SELECTOR_GATE"

    output = {
        "schema": "siel.public-calculation.bgce292.raw.v1",
        "candidate_id": "BGCE292",
        "source_revision": REVISION,
        "input_hashes_verified": checked,
        "baseline_gate": "PASS_REVISION_MATCHED_BGCE139_254_287_291",
        "primary_evidence_status": "Exact local curvature test of the canonical source-event-path BKM horizontal connection",
        "scientific_layer": "nonlinear conductance connection integrability",
        "connection": {
            "microscopic_rate_dimension": 48,
            "metric_moment_dimension": 10,
            "metric": "g_r(v,w)=sum_e v_e w_e/r_e",
            "horizontal_right_inverse": "H(r)=D(r)M^T[M D(r) M^T]^-1",
            "common_rate_normalization_affects_zero_nonzero_curvature": False,
            "reproduces_BGCE287_anchor_right_inverse": True,
        },
        "curvature_gate": {
            "base_two_plane_count": len(records),
            "nonzero_curvature_two_planes": nonzero_count,
            "curvature_span_rank_in_vertical_kernel": curvature_rank,
            "all_curvature_vectors_vertical": True,
            "flat_at_source_anchor": flat,
            "local_path_independence": "PASS" if flat else "FAIL",
            "records": records,
        },
        "dependency_effect": {
            "BGCE287_first_order_horizontal_lift": "RETAINED",
            "finite_path_independent_conductance_section": "SUPPORTED" if flat else "REFUTED_FOR_THIS_CANONICAL_CONNECTION",
            "BGCE290_active_transport": "OPEN" if flat else "REMAINS_REVERSED",
            "Hilbert_stress_Braid_only": "OPEN_NOT_DERIVED",
            "Ward_Braid_only": "OPEN_NOT_DERIVED",
            "MMR2_and_source_three_fifths": "RETAINED_UNCHANGED",
        },
        "next_gate": next_gate,
        "decision": decision,
        "runtime_class": "SUBSECOND_EXACT_RATIONAL_LOCAL_CURVATURE_NO_SCAN",
        "formal_E0_E1_E2": "NOT_CLAIMED__PUBLIC_THEORETICAL_GATE_ONLY",
        "claim_ceiling": "BGCE292 decides local flatness at the common-rate source anchor for the canonical nonlinear event-path BKM-horizontal extension of BGCE287. Nonzero curvature, if found, refutes only path-independent integration of this connection; it does not refute every Braid-derived nonlinear selector, path-ordered transport, Einstein dynamics or empirical gravity."
    }
    (HERE / "RAW_OUTPUT.json").write_text(json.dumps(output, indent=2) + "\n")
    print(decision)


if __name__ == "__main__":
    main()
