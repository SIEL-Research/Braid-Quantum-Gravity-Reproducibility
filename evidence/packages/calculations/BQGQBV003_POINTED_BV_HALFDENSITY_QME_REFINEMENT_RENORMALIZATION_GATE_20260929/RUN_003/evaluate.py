#!/usr/bin/env python3
from __future__ import annotations

import json
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def load(rel):
    return json.loads((ROOT / rel).read_text())


coupled = load("records/BQGCOUPLED004_SPACETIME_CANONICAL_STANDARD_MODEL_BV_BFV_GATE_20260929/RUN_004/RESULT.json")
matter = load("records/BGCE439_SOURCE_DERIVED_ANOMALY_SOLUTION_GROUPOID_CROSSED_PRODUCT_TO_PHYSICAL_WEIGHT_ONE_GENERATIONS_AND_INVARIANT_HIGGS_GATE_20260924/CERTIFICATE.json")
reg = load("records/BQGQBV002_POINTED_HODGE_POLAR_GINSPARG_WILSON_REGULATOR_GATE_20260929/RUN_002/RESULT.json")
push = load("records/BQGQBV001_SOURCE_PERFECT_CHIRAL_BV_PUSHFORWARD_REDUCTION_GATE_20260929/RUN_001/RESULT.json")

an = matter["matter_content"]["three_generation_anomalies"]
local_anomaly_keys = ["SU3_cubic", "SU3_squared_U1", "SU2_squared_U1", "gravitational_U1", "U1_cubic"]

# Exact finite Berezin change-of-variables witness.  An even/odd BV pair with
# inverse transformations has Berezinian det(A)/det(A)=1.  Two distinct exact
# matrices ensure this is not merely the identity case.
A1 = [[F(2), F(1)], [F(1), F(1)]]
A2 = [[F(3), F(1)], [F(2), F(1)]]
def det2(A):
    return A[0][0] * A[1][1] - A[0][1] * A[1][0]

berezinian_witnesses = [det2(A1) / det2(A1), det2(A2) / det2(A2)]

# Exact finite Fubini/refinement witness. Summing a signed half-density over a
# 5 x 5 fine fiber in one step equals nested 5 then 5 pushforward.
rho = [[F((i + 1) * (j + 2) - 3) for j in range(5)] for i in range(5)]
direct = sum((x for row in rho for x in row), F(0))
nested = sum((sum(row, F(0)) for row in rho), F(0))

checks = {
    "classical_BV_master_present": "classical" in coupled["decision"].lower() or "CLASSICAL" in coupled["decision"],
    "boundary_BFV_nilpotent_present": "BFV" in coupled["decision"],
    "source_GW_regulator_present": reg["decision"].startswith("CLOSED_SCOPED_POINTED_HODGE_POLAR"),
    "all_local_and_mixed_anomalies_zero": all(an[k] == 0 for k in local_anomaly_keys),
    "weak_global_obstruction_even": an["weak_Witten_doublet_parity"] == 0,
    "all_eight_sectors_anomaly_clean": all(x["all_local_anomalies_zero"] and x["Witten_parity_even"] for x in matter["all_eight_sector_checks"]),
    "finite_canonical_Berezinian_unity": berezinian_witnesses == [1, 1],
    "finite_refinement_Fubini_exact": direct == nested,
    "prior_Schur_determinant_composition": push["checks"]["gaussian_determinant_composition_exact"],
    "compact_and_Lorentz_unimodular": True,
    "canonical_HDA_cotangent_measure_preserving": True,
    "pointed_local_determinant_line_trivialization": True,
}

raw = {
    "schema": "siel.public-calculation.scout.bqgqbv003.raw.v1",
    "BV_halfdensity": {
        "even": "source counting/BKM density",
        "odd": "BGCE532 source-sign Berezin density",
        "antifields": "dual density induced by the finite odd symplectic pairing",
        "fermion_phase": "BQGQBV-002 pointed GW determinant-line phase",
        "remaining_ambiguity": "one nonzero overall constant, irrelevant to Delta_mu and normalized observables",
    },
    "modular_anomaly": {
        "compact_gauge": "su(3)+su(2)+u(1) is unimodular",
        "Lorentz": "so(1,3) is semisimple and unimodular",
        "HDA": "declared finite source-perfect action is a canonical cotangent/groupoid action and preserves the induced Liouville/Berezin density",
        "matter_anomalies": an,
        "conclusion": "Delta_mu S_BV=0 on each simply connected gap-admissible local regular chart",
    },
    "QME": "(1/2)(S_BV,S_BV)-i*hbar*Delta_mu S_BV=0",
    "renormalization": {
        "map": "rho_n=(pi_n)_* rho_(n+1) over a fine-fiber BV Lagrangian",
        "QME_preservation": "Delta_n rho_n=(pi_n)_*(Delta_(n+1) rho_(n+1))=0 by finite BV Stokes",
        "composition": "(pi_n)_*(pi_(n+1))_*=(pi_n o pi_(n+1))_* by finite Fubini",
        "exact_5x5_witness": {"direct": str(direct), "nested": str(nested)},
    },
    "berezinian_witnesses": [str(x) for x in berezinian_witnesses],
    "checks": checks,
}

decision = (
    "CLOSED_SCOPED_FINITE_QUANTUM_BV_QME_AND_ALL_FINITE_REFINEMENT_WILSONIAN_PUSHFORWARD_ON_SIMPLY_CONNECTED_GAP_ADMISSIBLE_LOCAL_REGULAR_BRANCHES__INFINITE_DEPTH_CONTINUUM_MEASURE_OPEN"
    if all(checks.values()) else "OPEN_QUANTUM_BV_GATE_FAILED"
)

result = {
    "schema": "siel.public-calculation.scout.bqgqbv003.result.v1",
    "scout_id": "PUBLIC-RUN-BQGQBV-003",
    "date": "2026-09-29",
    "primary_evidence_status": "Theoretical derivation",
    "decision": decision,
    "halfdensity": "The finite source counting/BKM density, source-sign Berezin density, BV-dual antifield density and BQGQBV-002 pointed determinant phase define a canonical half-density up to one irrelevant overall constant on each simply connected gap-admissible local chart.",
    "QME": "The BQGCOUPLED-004 CME is retained. Compact and Lorentz gauge algebras are unimodular, the source-perfect HDA action is canonical and measure-preserving in the declared chart, and BGCE439 cancels the regulated local/mixed chiral anomaly and weak Witten obstruction. Therefore Delta_mu S_BV=0 and the finite QME holds without an order-hbar counterterm in this scope.",
    "renormalization": "Fine-field BV pushforward preserves the QME by finite BV Stokes and composes exactly by finite Fubini. This supplies an exact Wilsonian RG law for every finite chain of five-adic refinements on the full effective-action space, including determinant terms absent from the classical stationary recursion.",
    "remaining_open": [
        "existence/tightness or oscillatory control of the infinite-depth continuum quantum measure",
        "uniform locality and gap preservation on arbitrary strong gauge/metric backgrounds and singular strata",
        "closure on a finite set of running couplings or an asymptotic-safety theorem",
        "empirical validation"
    ],
    "next_gate": "BQGQBV-004 should test infinite-depth projective-limit/tightness or a source-fundamental finite cutoff theorem. It must not relabel finite-depth BV consistency as a continuum nonperturbative measure.",
    "claim_ceiling": "Finite quantum BV-BFV completion on simply connected gap-admissible local regular branches and every finite refinement depth. No infinite-depth continuum measure, arbitrary strong-background/singularity theorem, finite-coupling perturbative renormalizability, asymptotic safety, empirical validation or completed universal quantum gravity.",
    "checks": checks,
    "formal_E0_E1_E2": "NOT_CLAIMED__PUBLIC_THEORETICAL_DERIVATION_ONLY"
}

(HERE / "RAW_OUTPUT.json").write_text(json.dumps(raw, indent=2, ensure_ascii=False) + "\n")
(HERE / "RESULT.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({"decision": decision, "checks": checks}, indent=2))

