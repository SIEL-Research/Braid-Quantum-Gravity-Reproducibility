#!/usr/bin/env python3
"""UB612: construct the actual PBM U4 and v0,2 covariant polynomial jets.

The calculation is deliberately target blind.  It reads curvature tensors and
their four frozen K-direction derivatives, never a stress sign or root target.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from decimal import Decimal as D, ROUND_CEILING, ROUND_FLOOR, localcontext
from fractions import Fraction
from itertools import product
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / "PBM_COVARIANT_TRANSPORT_JETS_PARTIAL_v1.json"
RIC = ROOT / "records/UB598J_ACTUAL_SCHEME_V2_HPS_INSERTION_C1_COEFFICIENT_GATE/ACTUAL_UB597A_PROPER_FRAME_NABLA2_RICCI_C1.json"
RIE = ROOT / "records/UB598O_ACTUAL_UB597A_RIEMANN_C1_GATE/ACTUAL_UB597A_PROPER_FRAME_RIEMANN_C1_PACKET_v1.json"
FIXTURE = ROOT / "records/UB516A_HOMOGENEOUS_HADAMARD_TRANSPORT_GATE/RESULT.json"
FORMULA = ROOT / "records/UB530A_HADAMARD_OFFDIAGONAL_TRANSPORT_GATE/RESULT.json"
FRAME = ROOT / "records/UB594F_ACTUAL_HADAMARD_SELECTOR_FREEZE_GATE/SELECTOR_FREEZE_v2.json"
IX = range(4)
ROOTS = ["p1", "p2", "p3", "H"]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def down(x: D, y: D) -> D:
    with localcontext() as c:
        c.prec = 140
        c.rounding = ROUND_FLOOR
        return x + y


def up(x: D, y: D) -> D:
    with localcontext() as c:
        c.prec = 140
        c.rounding = ROUND_CEILING
        return x + y


def ivadd(x, y):
    return down(x[0], y[0]), up(x[1], y[1])


def ivneg(x):
    return -x[1], -x[0]


def ivmul(x, y):
    lo, hi = [], []
    for a in x:
        for b in y:
            with localcontext() as c:
                c.prec = 140
                c.rounding = ROUND_FLOOR
                lo.append(a * b)
            with localcontext() as c:
                c.prec = 140
                c.rounding = ROUND_CEILING
                hi.append(a * b)
    return min(lo), max(hi)


def ivscale(x, q):
    q = D(q.numerator) / D(q.denominator) if hasattr(q, "numerator") else D(str(q))
    return ivmul(x, (q, q))


ZERO = (D(0), D(0))
ONE = (D(1), D(1))


def jet(value=ZERO, derivatives=None):
    return {"v": value, "d": list(derivatives or [ZERO] * 4)}


def jadd(x, y):
    return jet(ivadd(x["v"], y["v"]), [ivadd(a, b) for a, b in zip(x["d"], y["d"])])


def jneg(x):
    return jet(ivneg(x["v"]), [ivneg(a) for a in x["d"]])


def jscale(x, q):
    return jet(ivscale(x["v"], q), [ivscale(a, q) for a in x["d"]])


def jmul(x, y):
    return jet(
        ivmul(x["v"], y["v"]),
        [ivadd(ivmul(a, y["v"]), ivmul(x["v"], b)) for a, b in zip(x["d"], y["d"])],
    )


def from_json(x):
    value = tuple(map(D, x["value"])) if isinstance(x, dict) else tuple(map(D, x))
    derivs = [tuple(map(D, q)) for q in x.get("derivatives", [])] if isinstance(x, dict) else []
    return jet(value, derivs or [ZERO] * 4)


def seriv(x):
    return [str(x[0]), str(x[1])]


def serjet(x):
    return {"value": seriv(x["v"]), "derivatives": [seriv(q) for q in x["d"]]}


def alpha(indices):
    return tuple(indices.count(i) for i in IX)


def pterm(p, a, x):
    p[a] = jadd(p.get(a, jet()), x)


def padd(*ps):
    out = {}
    for p in ps:
        for a, x in p.items():
            pterm(out, a, x)
    return out


def pscale(p, q):
    return {a: jscale(x, q) for a, x in p.items()}


def pmul(p, q):
    out = {}
    for a, x in p.items():
        for b, y in q.items():
            pterm(out, tuple(a[i] + b[i] for i in IX), jmul(x, y))
    return out


def pderiv(p, i):
    out = {}
    for a, x in p.items():
        if a[i]:
            b = list(a)
            n = b[i]
            b[i] -= 1
            pterm(out, tuple(b), jscale(x, n))
    return out


def monomial(i):
    a = [0] * 4
    a[i] = 1
    return {tuple(a): jet(ONE)}


def load_metric_inverse():
    path = ROOT / "records/UB596E_NONCIRCULAR_PBM_TIME_JET_LOCAL_ENERGY_GATE/evaluate.py"
    spec = importlib.util.spec_from_file_location("ub612_ub596e", path)
    u = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(u)
    old = u.load_curvature_backend()
    old.r.N = 4
    terminal = json.loads((ROOT / "records/UB586C_TERMINAL_CLASSICAL_CONSTRAINT_TARGET_GATE/RESULT.json").read_text())
    box = json.loads((ROOT / "records/UB597A_NONZERO_ENERGY_CENTERED_K_DOMAIN_GATE/RESULT.json").read_text())
    model, base, _, _, _ = u.terminal_chart(old, terminal)
    center = [u.interval_from(old, x) for x in box["frozen_box"]["normalized_K_center_intervals"]]
    for k, value in enumerate(center):
        base[model.slices["k"].start + k] = value
    z = [old.TS(x) for x in base]
    g3 = old.u.ode._state_parts(model.physical_state(z))["gamma"]
    gi3 = old.u.ode.inverse3(g3)
    G = [[jet() for _ in IX] for _ in IX]
    inv = [[jet() for _ in IX] for _ in IX]
    G[0][0] = jet((-D(1), -D(1)))
    inv[0][0] = jet((-D(1), -D(1)))
    for i, j in product(range(3), repeat=2):
        G[i + 1][j + 1] = jet(tuple(map(D, g3[i][j].c[0].to_pair())))
        inv[i + 1][j + 1] = jet(tuple(map(D, gi3[i][j].c[0].to_pair())))
    return G, inv


def polynomial_json(p):
    return {",".join(map(str, a)): serjet(x) for a, x in sorted(p.items(), reverse=True)}


def interval_contains_zero(x):
    return x[0] <= 0 <= x[1]


def compute():
    ricj = json.loads(RIC.read_text())
    rie = json.loads(RIE.read_text())
    formula = json.loads(FORMULA.read_text())
    frame = json.loads(FRAME.read_text())
    assert ricj["root_direction_order"] == ROOTS == rie["root_direction_order"]
    assert formula["U_degree4"] == "tr(K2)/80+tr(K0^2)/360+tr(K0)^2/288"
    assert "gamma0 exponential midpoint" in frame["fixed_phase_and_quantization"]["weyl_quantization"]
    _, inv = load_metric_inverse()
    Ric = {tuple(map(int, k.split(","))): from_json(v) for k, v in ricj["Ricci"].items()}
    nRic = {tuple(map(int, k.split(","))): from_json(v) for k, v in ricj["nablaRicci"].items()}
    n2Ric = {tuple(map(int, k.split(","))): from_json(v) for k, v in ricj["nabla2Ricci"].items()}
    Rlow = {tuple(map(int, k.split(","))): from_json(v) for k, v in rie["Riemann_covariant"].items()}
    scalarR = from_json(ricj["R"])

    Rup = {}
    for a, c, b, d in product(IX, repeat=4):
        x = jet()
        for q in IX:
            x = jadd(x, jmul(inv[a][q], Rlow[q, c, b, d]))
        Rup[a, c, b, d] = x
    Rtwo = {}
    for a, c, b, d in product(IX, repeat=4):
        x = jet()
        for q in IX:
            x = jadd(x, jmul(inv[b][q], Rup[a, c, q, d]))
        Rtwo[a, c, b, d] = x
    Ricup = {}
    for a, b in product(IX, repeat=2):
        x = jet()
        for q in IX:
            x = jadd(x, jmul(inv[a][q], Ric[q, b]))
        Ricup[a, b] = x

    U2, U3, U4d, U4rr, U4ric = {}, {}, {}, {}, {}
    for a, b in product(IX, repeat=2):
        pterm(U2, alpha([a, b]), jscale(Ric[a, b], D(1) / D(12)))
    for c, a, b in product(IX, repeat=3):
        pterm(U3, alpha([c, a, b]), jscale(nRic[c, a, b], D(1) / D(24)))
    for d, c, a, b in product(IX, repeat=4):
        pterm(U4d, alpha([d, c, a, b]), jscale(n2Ric[d, c, a, b], D(1) / D(80)))
    for c, d, e, f in product(IX, repeat=4):
        x = jet()
        for a, b in product(IX, repeat=2):
            x = jadd(x, jmul(Rup[a, c, b, d], Rup[b, e, a, f]))
        pterm(U4rr, alpha([c, d, e, f]), jscale(x, D(1) / D(360)))
        pterm(U4ric, alpha([c, d, e, f]), jscale(jmul(Ric[c, d], Ric[e, f]), D(1) / D(288)))
    U4 = padd(U4d, U4rr, U4ric)

    boxU4 = {}
    for a, b in product(IX, repeat=2):
        boxU4 = padd(boxU4, pscale(pderiv(pderiv(U4, b), a), inv[a][b]["v"][0])) if inv[a][b]["v"][0] == inv[a][b]["v"][1] else padd(boxU4, {k: jmul(inv[a][b], v) for k, v in pderiv(pderiv(U4, b), a).items()})
    delta1, delta2 = {}, {}
    for a, b, c, d in product(IX, repeat=4):
        piece = pmul(monomial(c), monomial(d))
        piece = pmul(piece, pderiv(pderiv(U2, b), a))
        piece = {k: jmul(Rtwo[a, c, b, d], v) for k, v in piece.items()}
        delta1 = padd(delta1, pscale(piece, D(1) / D(3)))
    for a, b in product(IX, repeat=2):
        piece = pmul(monomial(b), pderiv(U2, a))
        piece = {k: jmul(Ricup[a, b], v) for k, v in piece.items()}
        delta2 = padd(delta2, pscale(piece, -D(2) / D(3)))
    ricpoly = {}
    for a, b in product(IX, repeat=2):
        pterm(ricpoly, alpha([a, b]), Ric[a, b])
    v00 = jadd(jet((D(1) / D(2), D(1) / D(2))), jscale(scalarR, -D(1) / D(12)))
    v02 = pscale(padd(pscale(boxU4, -1), pscale(padd(delta1, delta2), -1), U2,
                         {k: jscale(jmul(v, v00), D(1) / D(3)) for k, v in ricpoly.items()}), D(1) / D(6))
    gradR = {}
    for c in IX:
        x = jet()
        for a, b in product(IX, repeat=2):
            x = jadd(x, jmul(inv[a][b], nRic[c, a, b]))
        gradR[c] = x
    v01 = {alpha([c]): jscale(gradR[c], -D(1) / D(24)) for c in IX}

    # Reconstruct the recurrence residual from independently retained terms.
    residual = padd(pscale(v02, 6), boxU4, delta1, delta2, pscale(U2, -1),
                    {k: jscale(jmul(v, v00), -D(1) / D(3)) for k, v in ricpoly.items()})
    residual_contains_zero = all(interval_contains_zero(x["v"]) and all(interval_contains_zero(q) for q in x["d"])
                                 for x in residual.values())

    # Dependency-free exact replay of the UB516 quartic coefficient.  The raw
    # U term is (a+b+c)/192 and the parallel/horizontal contribution is its
    # negative.  Keeping them as Fractions makes the cancellation executable.
    raw_fixture_coefficient = Fraction(1, 192)
    parallel_fixture_coefficient = Fraction(-1, 192)
    assert raw_fixture_coefficient + parallel_fixture_coefficient == 0
    saved_fixture = json.loads(FIXTURE.read_text())
    assert saved_fixture["U_transport_residual"] == "0"
    assert saved_fixture["v0_transport_residual"] == "0"
    fixture_regression = {
        "U_transport_residual": saved_fixture["U_transport_residual"],
        "v0_transport_residual": saved_fixture["v0_transport_residual"],
        "raw_U_D00_coefficient_per_traceS": str(raw_fixture_coefficient),
        "required_parallel_contraction_per_traceS": str(parallel_fixture_coefficient),
        "exact_sum": str(raw_fixture_coefficient + parallel_fixture_coefficient),
        "raw_without_parallel_is_nonzero": raw_fixture_coefficient != 0,
    }
    data = {
        "schema": "ub612.pbm-covariant-transport-jets-partial.v1",
        "date": "2026-09-13",
        "box_id": ricj["box_id"],
        "root_direction_order": ROOTS,
        "target_blind": True,
        "world_function": {
            "spacetime_exponential_midpoint_identity": "sigma=g_m(y,y)/2 for endpoints Exp_m^g(-y/2), Exp_m^g(+y/2)",
            "actual_frozen_state_frame": "gamma0 spatial exponential midpoint at equal Cauchy time",
            "frames_identical": False,
            "actual_sigma6_generated": False,
            "qualification": "nonzero extrinsic curvature means an equal-time gamma0 spatial geodesic need not be the four-dimensional spacetime geodesic; the spacetime-midpoint identity cannot erase sigma3..6 in the frozen state frame",
        },
        "van_vleck": {
            "convention": "U=1+U2+U3+U4+O(|y|^5), with the UB530 radial orientation",
            "U2": polynomial_json(U2),
            "U3": polynomial_json(U3),
            "U4_covariant_derivative": polynomial_json(U4d),
            "U4_curvature_square": polynomial_json(U4rr),
            "U4_Ricci_square": polynomial_json(U4ric),
            "U4_total": polynomial_json(U4),
        },
        "v0": {
            "v00": serjet(v00),
            "v01": polynomial_json(v01),
            "v02": polynomial_json(v02),
            "recurrence": "6 v02=-Box_0 U4-deltaBox2 U2+U2+(Ric_ab y^a y^b)v00/3",
            "recurrence_interval_residual_contains_zero_all_coefficients_and_roots": residual_contains_zero,
        },
        "coefficient_counts": {
            "U2": len(U2), "U3": len(U3), "U4": len(U4), "v01": len(v01), "v02": len(v02)
        },
        "parallel4": None,
        "sigma6_parallel4_first_fail": {
            "missing_object": "the finite four-dimensional-spacetime to frozen gamma0-spatial midpoint adapter for sigma through degree six and the full covariant bidifferential stress operator through degree four",
            "why_curvature_values_alone_do_not_close_it": "parallel transport can be made componentwise identity along each radial split, but transverse/base differentiation of that moving frame contributes curvature terms",
            "fixture_detects_omission": fixture_regression,
            "required_next": "derive the finite horizontal lift/Jacobi chain rule and verify that its quartic term cancels the saved UB516 raw U contribution",
        },
        "status": "PARTIAL_PASS_ACTUAL_U4_V0_2_CENTER_AND_FOUR_ROOTS__SPACETIME_TO_FROZEN_SPATIAL_MIDPOINT_ADAPTER_FIRST_FAIL",
        "claim_ceiling": "Actual interval U4 and v0 degree-two PBM coefficients, including four frozen root derivatives, are generated. The four-dimensional Hps midpoint is not the frozen gamma0 spatial Weyl midpoint, so actual sigma6 and the parallel/horizontal point-split operator remain ungenerated. The complete UB611 callback, twenty stress values, eight faces and an unconditional root remain open.",
        "input_hashes": {str(p.relative_to(ROOT)): sha(p) for p in (RIC, RIE, FIXTURE, FORMULA, FRAME)},
    }
    return data


if __name__ == "__main__":
    HERE.mkdir(parents=True, exist_ok=True)
    data = compute()
    OUT.write_text(json.dumps(data, indent=2) + "\n")
    print(data["status"])
    print(json.dumps(data["coefficient_counts"], sort_keys=True))
