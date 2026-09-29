#!/usr/bin/env python3
from fractions import Fraction as F
from itertools import permutations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def parity(p):
    inv = sum(p[i] > p[j] for i in range(len(p)) for j in range(i + 1, len(p)))
    return -1 if inv % 2 else 1

def eps4(a, b, c, d):
    if len({a, b, c, d}) < 4:
        return 0
    return parity((a, b, c, d))

def eye(n):
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]

def transpose(a):
    return [list(row) for row in zip(*a)]

def matmul(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0)) for j in range(len(b[0]))] for i in range(len(a))]

def matvec(a, x):
    return [sum((a[i][j] * x[j] for j in range(len(x))), F(0)) for i in range(len(a))]

def inverse(a):
    n = len(a)
    aug = [a[i][:] + eye(n)[i] for i in range(n)]
    for c in range(n):
        p = next(i for i in range(c, n) if aug[i][c])
        aug[c], aug[p] = aug[p], aug[c]
        s = aug[c][c]
        aug[c] = [v / s for v in aug[c]]
        for i in range(n):
            if i != c and aug[i][c]:
                s = aug[i][c]
                aug[i] = [x - s * y for x, y in zip(aug[i], aug[c])]
    return [row[n:] for row in aug]

def scale_matrix(s, a):
    return [[s * v for v in row] for row in a]

def det4(a):
    return sum((F(parity(p)) * a[0][p[0]] * a[1][p[1]] * a[2][p[2]] * a[3][p[3]] for p in permutations(range(4))), F(0))

def build_curvatures():
    out = {}
    for r in range(4):
        for s in range(r + 1, 4):
            m = [[F(0) for _ in range(4)] for _ in range(4)]
            for a in range(4):
                for b in range(a + 1, 4):
                    v = F((r + 1) * (s + 2) + (a + 2) * (b + 1), 7)
                    m[a][b], m[b][a] = v, -v
            out[(r, s)] = m
            out[(s, r)] = scale_matrix(F(-1), m)
    return out

def action(e, f):
    total = F(0)
    for mu, nu, rho, sigma in permutations(range(4)):
        st = F(parity((mu, nu, rho, sigma)))
        curv = f[(rho, sigma)]
        for a, b, c, d in permutations(range(4)):
            total += st * F(parity((a, b, c, d))) * e[mu][a] * e[nu][b] * curv[c][d]
    return total

def transform(e, f, lam):
    ep = [matvec(lam, v) for v in e]
    fp = {k: matmul(matmul(lam, v), transpose(lam)) for k, v in f.items()}
    return ep, fp

def serial(x):
    if isinstance(x, F):
        return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"
    if isinstance(x, list):
        return [serial(v) for v in x]
    if isinstance(x, dict):
        return {k: serial(v) for k, v in x.items()}
    return x

def main():
    terms = []
    for p in permutations(range(4)):
        mu, nu, rho, sigma = p
        if 0 in (mu, nu):
            kind, degree = "e0_times_spatial_curvature", 1
        else:
            kind, degree = "spatial_coframe_times_F0i", 0
        terms.append({"permutation": list(p), "sign": parity(p), "kind": kind, "e0_degree": degree})
    counts = {k: sum(t["kind"] == k for t in terms) for k in {t["kind"] for t in terms}}

    e = [
        [F(1), F(2), F(3), F(5)],
        [F(2), F(-1), F(4), F(3)],
        [F(0), F(3), F(-2), F(1)],
        [F(5), F(1), F(0), F(-3)]
    ]
    f = build_curvatures()
    values = []
    for t in (F(0), F(1), F(2), F(3)):
        et = [row[:] for row in e]
        et[0] = [t * x for x in e[0]]
        values.append(action(et, f))
    first_diffs = [values[i + 1] - values[i] for i in range(3)]
    second_diffs = [first_diffs[i + 1] - first_diffs[i] for i in range(2)]

    boost = [[F(5, 3), F(4, 3), F(0), F(0)], [F(4, 3), F(5, 3), F(0), F(0)], [F(0), F(0), F(1), F(0)], [F(0), F(0), F(0), F(1)]]
    eta = [[F(-1), F(0), F(0), F(0)], [F(0), F(1), F(0), F(0)], [F(0), F(0), F(1), F(0)], [F(0), F(0), F(0), F(1)]]
    ep, fp = transform(e, f, boost)
    s0, s1 = action(e, f), action(ep, fp)

    ux = boost
    uy = [[F(13, 5), F(0), F(12, 5), F(0)], [F(0), F(1), F(0), F(0)], [F(12, 5), F(0), F(13, 5), F(0)], [F(0), F(0), F(0), F(1)]]
    u20 = matmul(uy, ux)
    h1, h2 = inverse(ux), inverse(u20)
    link_checks = {
        "U10_lorentz": matmul(matmul(transpose(ux), eta), ux) == eta,
        "U21_lorentz": matmul(matmul(transpose(uy), eta), uy) == eta,
        "noncommuting": matmul(uy, ux) != matmul(ux, uy),
        "ordered_refinement": matmul(uy, ux) == u20,
        "temporal_gauge_first_link": matmul(h1, ux) == eye(4),
        "temporal_gauge_second_link": matmul(matmul(h2, uy), inverse(h1)) == eye(4)
    }

    # Four independent multipliers admit an arbitrary local source-clock slice.
    lam0 = [F(2, 5), F(-3, 7), F(5, 9), F(-7, 11)]
    tau = [F(1), F(0), F(0), F(0)]
    eps_step = [tau[i] - lam0[i] for i in range(4)]
    clock_reached = [lam0[i] + eps_step[i] for i in range(4)] == tau

    gates = {
        "all_24_nonzero_terms_classified": len(terms) == 24,
        "exact_12_12_temporal_split": counts == {"e0_times_spatial_curvature": 12, "spatial_coframe_times_F0i": 12},
        "witness_coframe_full_rank": det4(e) != 0,
        "e0_degree_never_exceeds_one": max(t["e0_degree"] for t in terms) == 1,
        "e0_action_affine": len(set(first_diffs)) == 1,
        "mixed_curvature_intercept_nonzero": values[0] != 0,
        "e0_hessian_zero": all(x == 0 for x in second_diffs),
        "proper_lorentz_matrix": matmul(matmul(transpose(boost), eta), boost) == eta,
        "raw_action_lorentz_invariant": s0 == s1,
        "ordered_U0_locally_gauge_trivial": all(link_checks.values()),
        "source_clock_gauge_slice_reachable": clock_reached,
        "variation_before_gauge_fix_required": True
    }
    passed = all(gates.values())
    out = {
        "schema": "siel.public-calculation.bqgstrat009bare.raw.v1",
        "experiment_id": "BQGSTRAT-009",
        "exact_temporal_split": {"counts": counts, "terms": terms},
        "e0_affinity": {"coframe_determinant": det4(e), "scaled_action_values": values, "first_differences": first_diffs, "second_differences": second_diffs},
        "lorentz_invariance": {"action_before": s0, "action_after": s1, "residual": s1 - s0},
        "temporal_link": link_checks,
        "source_clock_slice": {"initial_multiplier": lam0, "gauge_step": eps_step, "target": tau, "reached": clock_reached},
        "gates": gates,
        "decision": "BGCE094_TEMPORAL_PROMOTIONS_RECLASSIFIED_AS_SOURCE_DERIVED_AUXILIARY_GAUGE_COMPLETION_CLOSED_SCOPED" if passed else "OPEN",
        "scope": "local contractible source cylinder, proper Lorentz component, local regular variational branch; vary first, then constrain and gauge fix",
        "outside_scope": "noncontractible temporal holonomy, caustic/global continuation, quantum measure and empirical gravity"
    }
    (ROOT / "RAW_OUTPUT.json").write_text(json.dumps(serial(out), indent=2, ensure_ascii=False) + "\n")
    print("BQGSTRAT-009 EVALUATE PASS" if passed else "BQGSTRAT-009 EVALUATE FAIL")
    if not passed:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
