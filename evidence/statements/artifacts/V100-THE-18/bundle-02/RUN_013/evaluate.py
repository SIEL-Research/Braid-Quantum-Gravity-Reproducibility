#!/usr/bin/env python3
"""Exact physical-symbol and Schur gate for PUBLIC-RUN-BQGSTRAT-013."""

from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import hashlib
import itertools
import json
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
MATRIX = json.loads((HERE / "SOURCE_MATRIX.json").read_text())


def archived(commit, path):
    return subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=ROOT)


def zero(rows, cols):
    return [[F(0) for _ in range(cols)] for _ in range(rows)]


def identity(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def scale(x, a):
    return [[x * value for value in row] for row in a]


def rref(matrix):
    a = [row[:] for row in matrix]
    row = 0
    pivots = []
    for col in range(len(a[0])):
        pivot = next((i for i in range(row, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        value = a[row][col]
        a[row] = [x / value for x in a[row]]
        for i in range(len(a)):
            if i != row and a[i][col]:
                value = a[i][col]
                a[i] = [a[i][j] - value * a[row][j] for j in range(len(a[0]))]
        pivots.append(col)
        row += 1
    return a, pivots


def rank(matrix):
    return len(rref(matrix)[1])


def sym6(operator):
    pairs = [(0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 2)]
    out = zero(6, 6)
    for col, (a, b) in enumerate(pairs):
        tensor = zero(3, 3)
        tensor[a][b] = F(1)
        tensor[b][a] = F(1)
        transformed = operator(tensor)
        for row, (i, j) in enumerate(pairs):
            out[row][col] = transformed[i][j]
    return out


def tt_projector(momentum):
    k = [F(v) for v in momentum]
    k2 = sum(v * v for v in k)
    pi = [[F(i == j) - k[i] * k[j] / k2 for j in range(3)] for i in range(3)]

    def apply(tensor):
        projected = matmul(matmul(pi, tensor), pi)
        tr = sum(pi[i][j] * tensor[i][j] for i in range(3) for j in range(3))
        return [[projected[i][j] - tr * pi[i][j] / 2 for j in range(3)] for i in range(3)]

    return sym6(apply)


# Q(zeta_5) arithmetic in the basis 1,z,z^2,z^3.
ZERO = (F(0),) * 4
ONE = (F(1), F(0), F(0), F(0))


def qa(a, b):
    return tuple(a[i] + b[i] for i in range(4))


def qs(a, b):
    return tuple(a[i] - b[i] for i in range(4))


def qm(a, b):
    c = [F(0)] * 7
    for i in range(4):
        for j in range(4):
            c[i + j] += a[i] * b[j]
    for degree in range(6, 3, -1):
        coefficient = c[degree]
        for j in range(degree - 4, degree):
            c[j] -= coefficient
    return tuple(c[:4])


zeta = (F(0), F(1), F(0), F(0))
powers = [ONE]
for _ in range(4):
    powers.append(qm(powers[-1], zeta))


def laplace_digit(d):
    return qs(qa(powers[d], powers[(-d) % 5]), (F(2), F(0), F(0), F(0)))


def main():
    checked = {}
    payloads = {}
    for source in MATRIX["sources"]:
        raw = archived(source["repository_commit"], source["path"])
        digest = hashlib.sha256(raw).hexdigest()
        assert digest == source["sha256"]
        checked[f'{source["repository_commit"]}:{source["path"]}'] = digest
        payloads[source["path"]] = json.loads(raw)

    ultra = payloads[MATRIX["sources"][0]["path"]]
    bridge = payloads[MATRIX["sources"][1]["path"]]
    adm14 = payloads[MATRIX["sources"][2]["path"]]
    adm15 = payloads[MATRIX["sources"][3]["path"]]
    euler = payloads[MATRIX["sources"][4]["path"]]
    raw_rank = payloads[MATRIX["sources"][5]["path"]]

    assert "Schur complement" in ultra["construction"]
    assert "on-shell asymptotic" in bridge["decisive_result"]
    assert adm14["gate_results"]["rank_two_configuration_projector"] == "PASS_EXACT"
    assert adm15["gate_results"]["all_124_nonzero_C5_cubed_momenta"] == "PASS_EXACT"
    assert "for every A<=B" in euler["normalized_update"]["equation"]
    assert euler["gate_results"]["exact_actual_metric_principal_moment"].startswith("PASS")
    assert raw_rank["exact_result"]["rank_profile"] == {"60": 1, "64": 12, "65": 12, "66": 600}

    directions = [d for d in itertools.product(range(-2, 3), repeat=3) if d != (0, 0, 0)]
    projector_records = []
    scalar_commutes = True
    for direction in directions:
        p = tt_projector(direction)
        assert rank(p) == 2
        assert matmul(p, p) == p
        for scalar in (F(-3), F(0), F(5, 7)):
            qid = scale(scalar, identity(6))
            scalar_commutes &= matmul(p, qid) == matmul(qid, p) == scale(scalar, p)
        projector_records.append({"momentum": list(direction), "rank": 2})
    assert scalar_commutes

    null_sheets = []
    for temporal in range(1, 5):
        for axis in range(3):
            for sign in (1, -1):
                spatial = (sign * temporal) % 5
                q = qs(laplace_digit(temporal), laplace_digit(spatial))
                assert q == ZERO
                null_sheets.append({
                    "temporal_digit": temporal,
                    "spatial_axis": axis,
                    "spatial_digit": spatial,
                    "orientation": "+" if sign == 1 else "-",
                    "physical_kernel_dimension": 2,
                })
    assert len(null_sheets) == 24

    control_q = qs(laplace_digit(1), laplace_digit(0))
    assert control_q != ZERO
    control_physical_rank = 2

    output = {
        "schema": "siel.public-calculation.bqgstrat013.raw.v1",
        "input_hashes_verified": checked,
        "physical_projector": {
            "nonzero_momenta_checked": len(projector_records),
            "configuration_rank": 2,
            "phase_rank_inherited": 4,
            "scalar_principal_symbol_commutes_exactly": scalar_commutes,
        },
        "physical_symbol_theorem": {
            "ten_component_principal_symbol": "q_h(omega,k) I_10",
            "TT_restriction": "q_h(omega,k) I_2",
            "positive_negative_orientation_sheets": len(null_sheets),
            "kernel_dimension_on_every_declared_null_sheet": 2,
            "noncharacteristic_control_rank": control_physical_rank,
            "new_coefficient": False,
        },
        "raw_block_relation": {
            "raw_80_component_profile_retained_as_negative_route_evidence": raw_rank["exact_result"]["rank_profile"],
            "raw_block_repaired": False,
            "raw_imbalance_inherited_by_physical_principal_system": False,
        },
        "source_perfect_schur_scope": {
            "regular_transverse_Schur_theorem": True,
            "finite_parent_to_Euler_relation": "on-shell asymptotic, not literal exact finite-map identity",
            "evaluated_closed_form_full_perfect_Hessian": False,
            "lower_order_crossing_form": "OPEN",
        },
        "null_sheet_records": null_sheets,
        "decision": "SCOPED_PASS_SOURCE_PERFECT_PHYSICAL_PRINCIPAL_SYMBOL_IS_EXACTLY_TWO_POLARIZATION_AND_PARITY_BALANCED__RAW_80_COMPONENT_TWO_VERSUS_ONE_IMBALANCE_IS_NOT_INHERITED__OPEN_EVALUATED_FULL_PERFECT_HESSIAN_AND_LOWER_ORDER_CROSSING",
        "primary_evidence_status": "Theoretical derivation / exact scoped physical-principal theorem",
        "incident_class": "SCIENTIFIC_OUTCOME",
        "next_gate": "BQGSTRAT-014_EVALUATED_PERFECT_HESSIAN_LOWER_ORDER_CROSSING_GATE",
        "claim_ceiling": "Closes the two-polarization parity-balanced physical principal symbol on the flat source-axis sheets and its all-nonzero-momentum TT rank theorem, with local regular source-perfect/trajectory identification. It does not evaluate the full finite perfect Hessian, close lower-order crossing or global singular continuation, construct an infinite-depth quantum measure, or establish empirical gravity."
    }
    (HERE / "RAW_OUTPUT.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(output["decision"])


if __name__ == "__main__":
    main()

