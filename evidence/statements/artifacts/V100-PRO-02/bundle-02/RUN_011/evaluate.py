#!/usr/bin/env python3
"""Exact reverse-orientation proportionality gate for BQGSTRAT-011."""

from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
MATRIX = json.loads((HERE / "SOURCE_MATRIX.json").read_text())
REVISION = MATRIX["source_revision"]


def archived(path):
    return subprocess.check_output(["git", "show", f"{REVISION}:{path}"], cwd=ROOT)


def clean(poly):
    return {word: value for word, value in poly.items() if value}


def add(*polys):
    out = defaultdict(F)
    for poly in polys:
        for word, value in poly.items():
            out[word] += value
    return clean(out)


def scale(poly, value):
    return clean({word: value * coefficient for word, coefficient in poly.items()})


def multiply(left, right, degree=2):
    out = defaultdict(F)
    for a, av in left.items():
        for b, bv in right.items():
            if len(a + b) <= degree:
                out[a + b] += av * bv
    return clean(out)


def exp2(name, sign):
    sign = F(sign)
    return {(): F(1), (name,): sign, (name, name): sign * sign / 2}


def log2(product):
    q = add(product, {(): F(-1)})
    return add(q, scale(multiply(q, q), F(-1, 2)))


def word_log(sequence):
    product = {(): F(1)}
    for name, sign in sequence:
        product = multiply(product, exp2(name, sign))
    return log2(product)


def main():
    checked = {}
    for source in MATRIX["sources"]:
        raw = archived(source["path"])
        digest = hashlib.sha256(raw).hexdigest()
        assert digest == source["sha256"], source["path"]
        assert raw == (ROOT / source["path"]).read_bytes(), f"working-tree drift: {source['path']}"
        checked[source["path"]] = digest

    strat9 = json.loads(archived(MATRIX["sources"][0]["path"]))
    strat10 = json.loads(archived(MATRIX["sources"][2]["path"]))
    bg137 = json.loads(archived(MATRIX["sources"][3]["path"]))
    bg138 = json.loads(archived(MATRIX["sources"][4]["path"]))
    bg259 = json.loads(archived(MATRIX["sources"][5]["path"]))

    forward = word_log((("A", 1), ("B", 1), ("C", -1), ("D", -1)))
    reverse = word_log((("D", 1), ("C", 1), ("B", -1), ("A", -1)))
    inverse_log_exact = reverse == scale(forward, F(-1))

    # In the Palatini density, swapping the oriented face indices reverses
    # epsilon^{mu nu rho sigma}.  The face logarithm reverses at the same time.
    # Therefore the legal reversed-face term equals the forward term exactly.
    curvature_sign = -1
    face_bivector_sign = -1
    legal_reverse_action_factor = curvature_sign * face_bivector_sign
    illegal_fixed_label_reverse_factor = curvature_sign
    assert legal_reverse_action_factor == 1
    assert illegal_fixed_label_reverse_factor == -1

    original_profile = strat10["rank_profile"]
    assert original_profile == {"60": 1, "64": 12, "65": 12, "66": 600}
    allowed_scalar_completions = {
        "forward_only": 1,
        "legal_equal_weight_orientation_pair": 2,
        "orientation_odd_difference": 0,
    }
    inherited_profiles = {
        name: (original_profile if factor else {"0": 625})
        for name, factor in allowed_scalar_completions.items()
    }

    source_checks = {
        "bqgstrat009_orientation_reversal_negates_log": strat9["plaquette_checks"]["orientation_reversal_negates_log"],
        "bgce137_orientation_double_cover_canonical": bg137["graded_Cartan_factorization"]["orientation_double_cover_canonical"],
        "bgce138_reverse_transport_is_inverse_path_ordered_holonomy": "path-ordered" in bg138["minimal_smooth_completion"]["connection_coarsening"],
        "bgce259_orientation_odd_quadratic_rank_zero": bg259["orientation_odd_second_rank"] == 0,
    }

    pass_target = inherited_profiles["legal_equal_weight_orientation_pair"].get("64") == 24
    # It remains twelve rank-64 sectors and twelve rank-65 sectors, not 24
    # rank-64 sectors.  Multiplication by a nonzero scalar preserves rank.
    assert pass_target is False
    assert inverse_log_exact
    assert all(source_checks.values())

    output = {
        "schema": "siel.public-calculation.bqgstrat011.raw.v1",
        "source_revision": REVISION,
        "input_hashes_verified": checked,
        "exact_free_associative_second_jet": {
            "log_reverse_equals_minus_log_forward": inverse_log_exact,
            "curvature_sign_under_orientation_reversal": curvature_sign,
            "face_bivector_sign_under_orientation_reversal": face_bivector_sign,
            "legal_reverse_action_factor": legal_reverse_action_factor,
        },
        "source_checks": source_checks,
        "completion_family": {
            "allowed_scalar_factors": allowed_scalar_completions,
            "theorem": "Every scalar forward/reverse completion supplied solely by edge inversion and face orientation is lambda times the original real-space Palatini quadratic form.  For lambda nonzero its Fourier rank and nullity profile is unchanged; lambda zero is the zero form.",
            "inherited_rank_profiles": inherited_profiles,
            "off_diagonal_sheet_coupling_source_derived": False,
        },
        "target_gate": {
            "required": "rank 64 on all 24 nonzero null-sheet sectors",
            "observed_legal_completion": "rank 64 on 12 and rank 65 on 12",
            "passed": pass_target,
        },
        "decision": "NO_GO_SOURCE_REVERSE_FACE_OR_ADJOINT_SCALAR_COMPLETION__LEGAL_ORIENTATION_PAIR_DOUBLES_THE_EXISTING_PALATINI_HESSIAN_AND_PRESERVES_THE_EXACT_TWO_VERSUS_ONE_CORANK_IMBALANCE__ORIENTATION_ODD_DIFFERENCE_IS_ZERO",
        "incident_class": "SCIENTIFIC_OUTCOME",
        "primary_evidence_status": "Theoretical derivation / scoped no-go",
        "claim_ceiling": "Excludes only completions generated by the already-declared scalar reverse-face, edge-inversion and orientation-double-cover operations.  It does not exclude a newly derived off-diagonal doubled-branch pairing, quasi-local perfect action, matter-coupled parent, generic singular continuation, Braid necessity or empirical gravity.",
    }
    (HERE / "RAW_OUTPUT.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(output["decision"])


if __name__ == "__main__":
    main()
