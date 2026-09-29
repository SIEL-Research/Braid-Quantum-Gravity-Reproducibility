#!/usr/bin/env python3
"""BGCE259: oriented Braid coborder versus causal grading insertion."""

from fractions import Fraction as F
from itertools import permutations
from pathlib import Path
from typing import Any
import hashlib
import json
import subprocess
import time


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MATRIX = json.loads((HERE / "SOURCE_MATRIX.json").read_text())
REVISION = MATRIX["source_revision"]


def load(relative: str) -> dict[str, Any]:
    return json.loads((ROOT / relative).read_text())


def verify_sources() -> dict[str, str]:
    checked = {}
    for relative, expected in MATRIX["inputs_sha256"].items():
        archived = subprocess.check_output(["git", "show", f"{REVISION}:{relative}"], cwd=ROOT)
        assert archived == (ROOT / relative).read_bytes(), f"source drift: {relative}"
        actual = hashlib.sha256(archived).hexdigest()
        assert actual == expected, relative
        checked[relative] = actual
    return checked


def rank(a):
    w = [row[:] for row in a]
    r = 0
    for c in range(len(w[0])):
        p = next((i for i in range(r, len(w)) if w[i][c]), None)
        if p is None:
            continue
        w[r], w[p] = w[p], w[r]
        q = w[r][c]
        w[r] = [x / q for x in w[r]]
        for i in range(len(w)):
            if i != r and w[i][c]:
                q = w[i][c]
                w[i] = [x - q * y for x, y in zip(w[i], w[r])]
        r += 1
    return r


def parity(p):
    inversions = sum(p[i] > p[j] for i in range(4) for j in range(i + 1, 4))
    return 1 if inversions % 2 == 0 else -1


def pair_moments(mapping, reverse_edge=False):
    first = [0, 0]
    second = [[0, 0], [0, 0]]
    for index, output in enumerate(mapping):
        source = divmod(index, 5)
        delta = [output[i] - source[i] for i in range(2)]
        if reverse_edge:
            delta = [-x for x in delta]
        for i in range(2):
            first[i] += delta[i]
            for j in range(2):
                second[i][j] += delta[i] * delta[j]
    return first, second


def chart_aggregate(moment2, wanted_parity=None):
    total = [[0 for _ in range(4)] for _ in range(4)]
    charts = 0
    for order in permutations(range(4)):
        if wanted_parity is not None and parity(order) != wanted_parity:
            continue
        charts += 1
        for site in range(3):
            left, right = order[site], order[site + 1]
            total[left][left] += moment2[0][0]
            total[left][right] += moment2[0][1]
            total[right][left] += moment2[1][0]
            total[right][right] += moment2[1][1]
    return charts, total


def normalize(a, denominator):
    return [[F(x, denominator) for x in row] for row in a]


def sub(a, b):
    return [[x - y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def encode(a):
    return [[str(x) for x in row] for row in a]


def build_output() -> dict[str, Any]:
    started = time.perf_counter()
    checked = verify_sources()
    bg133 = load("records/BGCE133_X63_BOUNDARY_TO_FIXED_J_AFFINE_CYCLE_ROUTING_GATE_20260919/RESULT.json")
    bg134 = load("records/BGCE134_MARKED_WORD_TO_A3_AFFINE_CLOSURE_FUNCTOR_GATE_20260919/RESULT.json")
    bg137 = load("records/BGCE137_DISCRETE_S4_CHART_TRANSITION_VERSUS_NEAR_IDENTITY_CARTAN_CONNECTION_FACTORING_GATE_20260919/RESULT.json")
    bg139_raw = load("records/BGCE139_SOURCE_SPECTRAL_CYLINDER_OPERATIONAL_EVENT_IDENTIFICATION_GATE_20260919/RAW_OUTPUT.json")
    bg139 = load("records/BGCE139_SOURCE_SPECTRAL_CYLINDER_OPERATIONAL_EVENT_IDENTIFICATION_GATE_20260919/RESULT.json")
    bg254 = load("records/BGCE254_SOURCE_RESPONSE_LEGENDRE_EXACTNESS_TO_UNIQUE_LOGZ_BREGMAN_EDGE_ACTION_GATE_20260921/RESULT.json")
    bg256 = load("records/BGCE256_BRAID_INDUCED_EVENT_TRANSITION_COBORDER_TO_NEIGHBOR_COUPLING_LAW_GATE_20260921/RESULT.json")
    bg258 = load("records/BGCE258_SOURCE_CAUSAL_GRADING_TIMES_EVENT_MOMENT_TO_UNIQUE_NULL_GRAM_PARENT_KINETIC_GATE_20260921/RESULT.json")

    assert bg133["result"]["raw_endpoint_action_involutive"] is True
    assert bg134["result"]["inverse_word_equals_r_inverse"] is True
    assert bg137["graded_Cartan_factorization"]["A4_orientation_orbits"] == 2
    assert bg139["event_transition"]["involutive"] is True
    assert bg254["unique_response_exact_edge_functional"].startswith("Umegaki")
    assert bg256["S4_averaged_Q4_rank"] == 4
    assert bg258["K_evt_signature"] == [3, 1, 0]

    records = bg139_raw["event_transition_gate"]["canonical_transition_on_digit_pairs"]
    mapping = [tuple(record["output"]) for record in records]
    inverse_mapping = [None] * 25
    for source_index, output in enumerate(mapping):
        output_index = 5 * output[0] + output[1]
        inverse_mapping[output_index] = divmod(source_index, 5)
    assert all(value is not None for value in inverse_mapping)
    assert inverse_mapping == mapping

    forward_first, forward_second = pair_moments(mapping)
    reverse_first, reverse_second = pair_moments(mapping, reverse_edge=True)
    assert forward_first == reverse_first == [0, 0]
    assert forward_second == reverse_second == [[28, -20], [-20, 28]]
    odd_first = [x - y for x, y in zip(forward_first, reverse_first)]
    odd_second = sub(forward_second, reverse_second)
    assert odd_first == [0, 0]
    assert odd_second == [[0, 0], [0, 0]]

    even_count, even_raw = chart_aggregate(forward_second, 1)
    odd_count, odd_raw = chart_aggregate(forward_second, -1)
    all_count, all_raw = chart_aggregate(forward_second)
    assert (even_count, odd_count, all_count) == (12, 12, 24)
    q_even = normalize(even_raw, 12 * 25)
    q_odd = normalize(odd_raw, 12 * 25)
    q_all = normalize(all_raw, 24 * 25)
    q_parity = normalize(sub(even_raw, odd_raw), 24 * 25)
    stored_q4 = [[F(x) for x in row] for row in bg256["S4_averaged_Q4"]]
    assert q_all == stored_q4
    assert q_even == q_odd == stored_q4
    assert all(x == 0 for row in q_parity for x in row)

    k_evt = [[F(x) for x in row] for row in bg258["K_evt"]]
    assert k_evt != stored_q4
    assert k_evt != q_parity
    # Since M_forward=M_reverse, every scalar combination is a scalar multiple
    # of Q4.  No scalar multiple of positive Q4 equals indefinite K_evt.
    scalar_forward_reverse_combination_can_equal_k = False

    orientation_generates_grading = False
    decision = (
        "FAIL_FORWARD_REVERSE_EVENT_SECOND_MOMENTS_IDENTICAL_AND_ORIENTATION_ODD_COBORDER_ZERO__"
        "FAIL_A4_EVEN_ODD_CHART_MOMENTS_IDENTICAL_AND_PARITY_SIGNED_HAAR_MOMENT_ZERO__"
        "FULL_MARKED_WORD_RETAINS_ORIENTATION_BUT_ACTUAL_QUADRATIC_EDGE_ACTION_ERASES_IT__"
        "CAUSAL_GRADING_INSERTION_NOT_DERIVED"
    )
    return {
        "schema": "siel.public-calculation.bgce259.raw.v1",
        "candidate_id": "BGCE259",
        "source_revision": REVISION,
        "preregistered_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "input_hashes_verified": checked,
        "baseline_gate": "PASS_REVISION_MATCHED_ACTUAL_EVENT_MAP_ORIENTATION_FUNCTOR_AND_FROZEN_K_EVT",
        "endpoint_provenance": "NOT_ISSUED_BY_PUBLIC__THEORETICAL_EXACT_ORIENTATION_MOMENT_GATE_ONLY",
        "primary_evidence_status": "Exact theoretical no-go for orientation-only quadratic action selection",
        "scientific_layer": "marked Braid orientation, graph principal symbol and variational action selection",
        "forward_reverse_gate": {
            "actual_event_map_involutive": True,
            "inverse_mapping_equals_forward_mapping": True,
            "forward_first_moment": forward_first,
            "reverse_first_moment": reverse_first,
            "orientation_odd_first_moment": odd_first,
            "forward_second_moment": forward_second,
            "reverse_second_moment": reverse_second,
            "orientation_odd_second_moment": odd_second,
            "orientation_odd_second_rank": rank([[F(x) for x in row] for row in odd_second]),
        },
        "chart_parity_gate": {
            "even_chart_count": even_count,
            "odd_chart_count": odd_count,
            "Q_even": encode(q_even),
            "Q_odd": encode(q_odd),
            "Q_even_equals_Q_odd_equals_Q4": True,
            "parity_signed_Haar_moment": encode(q_parity),
            "parity_signed_rank": rank(q_parity),
        },
        "principal_action_gate": {
            "Umegaki_BKM_quadratic_term_edge_reversal_even": True,
            "reason": "A divergence and its reversed divergence have the same diagonal BKM Hessian; orientation asymmetry begins beyond the principal quadratic term.",
            "every_scalar_forward_reverse_combination_is_scalar_Q4": True,
            "scalar_forward_reverse_combination_can_equal_K_evt": scalar_forward_reverse_combination_can_equal_k,
            "K_evt_target": encode(k_evt),
            "orientation_generates_J_ray_insertion": orientation_generates_grading,
        },
        "dependency_effect": {
            "BGCE134_full_word_orientation_retained": True,
            "BGCE258_algebraic_Lorentz_carrier_retained": True,
            "orientation_only_action_selection_route_closed": True,
            "action_level_parent_kinetic_derived": False,
            "off_shell_metric_variation_derived": False,
            "Ward_derived": False,
            "SDPC_complete": False,
            "unconditional_sourced_Einstein_derived": False,
        },
        "counter_intuition_scan": {
            "tempting_success": "Because the full marked word distinguishes forward from inverse, its edge action must remember the causal sign.",
            "refutation": "The actual event map is involutive and the principal Dirichlet term is quadratic, so displacement reversal squares away the word orientation. The A4 parity split cancels for the same reason.",
            "ordinary_explanation": "A reversible graph Dirichlet form is orientation-even; a Lorentzian principal symbol requires more than orienting its edges.",
            "SIEL_specific_interpretation": "Braid history retains orientation at the affine-word level, but the current relative-entropy coarse graining discards it before the continuum principal symbol.",
            "falsifier": "A retained source phase or branch pairing whose exact second variation is nonzero, Lorentzian, and equals J_ray Q4 without fitted mode weights.",
        },
        "decision": decision,
        "next_gate": "BGCE260_MARKED_BRAID_PHASE_OR_DOUBLED_BRANCH_PAIRING_TO_J_RAY_QUADRATIC_PRINCIPAL_SYMBOL_GATE",
        "elapsed_seconds": time.perf_counter() - started,
        "formal_E0_E1_E2": "NOT_CLAIMED__THEORETICAL_EXACT_ORIENTATION_MOMENT_GATE_ONLY",
        "claim_ceiling": "BGCE259 proves that the retained forward/reverse event orientation and canonical A4 chart parity cannot generate the BGCE258 causal grading in the quadratic principal edge action: all orientation-odd second moments vanish while the orientation-even moment is the positive Q4. It does not refute a distinct retained complex phase or doubled-branch pairing with a nonzero Lorentzian Hessian, and does not derive a parent kinetic action, Ward conservation, SDPC or an unconditional sourced Einstein equation.",
    }


if __name__ == "__main__":
    output = build_output()
    (HERE / "RAW_OUTPUT.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    print(output["decision"])
    print(f"elapsed_seconds={output['elapsed_seconds']:.6f}")
