#!/usr/bin/env python3
"""Exact type and chiral-projector gate for PUBLIC-RUN-BQGSTRAT-012."""

from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
MATRIX = json.loads((HERE / "SOURCE_MATRIX.json").read_text())


def archived(commit, path):
    return subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=ROOT)


def c(re=0, im=0):
    return (F(re), F(im))


ZERO = c()
ONE = c(1)
I = c(0, 1)


def ca(x, y):
    return (x[0] + y[0], x[1] + y[1])


def cs(x, y):
    return (x[0] - y[0], x[1] - y[1])


def cm(x, y):
    return (x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def cc(x):
    return (x[0], -x[1])


def mzero(n=6):
    return [[ZERO for _ in range(n)] for _ in range(n)]


def mid(n=6):
    out = mzero(n)
    for k in range(n):
        out[k][k] = ONE
    return out


def madd(a, b):
    return [[ca(a[r][s], b[r][s]) for s in range(len(a))] for r in range(len(a))]


def msub(a, b):
    return [[cs(a[r][s], b[r][s]) for s in range(len(a))] for r in range(len(a))]


def mscale(z, a):
    return [[cm(z, a[r][s]) for s in range(len(a))] for r in range(len(a))]


def mmul(a, b):
    n = len(a)
    out = mzero(n)
    for r in range(n):
        for s in range(n):
            value = ZERO
            for k in range(n):
                value = ca(value, cm(a[r][k], b[k][s]))
            out[r][s] = value
    return out


def mconj(a):
    return [[cc(x) for x in row] for row in a]


def main():
    checked = {}
    payloads = {}
    for source in MATRIX["sources"]:
        raw = archived(source["repository_commit"], source["path"])
        digest = hashlib.sha256(raw).hexdigest()
        assert digest == source["sha256"], source["path"]
        checked[f'{source["repository_commit"]}:{source["path"]}'] = digest
        payloads[source["path"]] = json.loads(raw)

    bg27 = payloads[MATRIX["sources"][0]["path"]]
    bg41 = payloads[MATRIX["sources"][1]["path"]]
    qbv = payloads[MATRIX["sources"][2]["path"]]
    old = payloads[MATRIX["sources"][3]["path"]]

    assert bg27["construction"]["Hodge_star"].startswith("unique star_h")
    assert bg27["decisions"]["four_dimensional_internal_Hodge_requires_new_geometry_input"] is False
    assert "inside the X29/X30 Lorentz carrier" in bg41["proved_no_go"]
    assert "address incidence and internal action commute" in qbv["gauge_typing"]

    # Ordered bivector basis: (K1,K2,K3,R1,R2,R3).  J maps K to R and
    # R to -K, the exact Lorentzian Hodge relation J^2=-I.
    ident = mid()
    J = mzero()
    for k in range(3):
        J[3 + k][k] = ONE
        J[k][3 + k] = c(-1)
    assert mmul(J, J) == mscale(c(-1), ident)

    pplus = mscale(c(F(1, 2)), msub(ident, mscale(I, J)))
    pminus = mscale(c(F(1, 2)), madd(ident, mscale(I, J)))
    assert madd(pplus, pminus) == ident
    assert mmul(pplus, pminus) == mzero()
    assert mmul(pplus, pplus) == pplus
    assert mmul(pminus, pminus) == pminus
    assert mconj(pplus) == pminus

    aplus = mmul(J, pplus)
    aminus = mmul(J, pminus)
    equal_completion = madd(aplus, aminus)
    assert equal_completion == J

    # A+ - A- = i I, hence -i(A+ - A-) is the independent Holst insertion I.
    holst = mscale(c(0, -1), msub(aplus, aminus))
    assert holst == ident

    # A dagger-real coefficient c=a+ib on + and conjugate(c) on - gives
    # a*J-b*I.  Two examples prove the independent real two-dimensional span.
    def dagger_real(a, b):
        coefficient = c(a, b)
        return madd(mscale(coefficient, aplus), mscale(cc(coefficient), aminus))

    assert dagger_real(1, 0) == J
    assert dagger_real(0, 1) == mscale(c(-1), ident)

    old_profile = old["exact_result"]["rank_profile"]
    assert old_profile == {"60": 1, "64": 12, "65": 12, "66": 600}

    type_gate = {
        "internal_lorentz_hodge_domain": "Lambda^2 of the X29/X30 Lorentz carrier",
        "cochain_polar_domain": "source-cylinder cell cochains tensored with an independent internal coefficient module",
        "same_operator": False,
        "commuting_factors": True,
        "dimension_80_collision_is_not_a_typed_identification": True,
    }
    source_selects_relative_holst_phase = False
    passed = equal_completion != J or source_selects_relative_holst_phase
    assert passed is False

    output = {
        "schema": "siel.public-calculation.bqgstrat012.raw.v1",
        "input_hashes_verified": checked,
        "type_gate": type_gate,
        "exact_internal_hodge": {
            "basis": ["K1", "K2", "K3", "R1", "R2", "R3"],
            "J_squared_equals_minus_identity": True,
            "Pplus_Pminus_projectors": True,
            "dagger_swaps_projectors": True,
        },
        "completion_theorem": {
            "palatini_insertion": "J",
            "chiral_insertions": ["J P_plus", "J P_minus"],
            "equal_dagger_completion": "J P_plus + J P_minus = J",
            "independent_real_partner": "-i(J P_plus - J P_minus) = I (Holst insertion)",
            "general_dagger_real_family": "(a+ib) J P_plus + (a-ib) J P_minus = a J - b I",
            "source_selects_relative_holst_phase": source_selects_relative_holst_phase,
        },
        "rank_consequence": {
            "equal_weight_profile": old_profile,
            "required_for_pass": "rank 64 on all 24 nonzero null-sheet sectors",
            "passed": passed,
            "all_sector_rerun_required": False,
            "reason": "The equal-weight completion is exactly the old real-space action, so its Hessian and rank profile are identical."
        },
        "decision": "NO_GO_SOURCE_DAGGER_CHIRAL_EQUAL_WEIGHT_COMPLETION__THE_TWO_CONJUGATE_CHIRAL_PIECES_RECONSTRUCT_THE_EXISTING_REAL_PALATINI_ACTION__A_NONPROPORTIONAL_HOLST_PARTNER_REQUIRES_AN_UNSELECTED_RELATIVE_PHASE",
        "incident_class": "SCIENTIFIC_OUTCOME",
        "primary_evidence_status": "Theoretical derivation / exact scoped no-go",
        "next_gate": "BQGSTRAT-013_SOURCE_PERFECT_BFV_SCHUR_COMPLEMENT_GATE",
        "claim_ceiling": "Excludes the declared coefficient-free equal-weight dagger/chiral completion. It does not exclude a source-perfect quasi-local Schur complement, a future typed phase law, matter-induced completion, generic singular/global continuation, Braid necessity or empirical gravity."
    }
    (HERE / "RAW_OUTPUT.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(output["decision"])


if __name__ == "__main__":
    main()

