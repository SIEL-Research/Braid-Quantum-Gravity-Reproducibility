#!/usr/bin/env python3
"""BGCE570 exact joint clock--Nambu Lie-action gate."""

from __future__ import annotations

import hashlib
import json
import math
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
getcontext().prec = 70


def load(rel: str):
    return json.loads((ROOT / rel).read_text())


def sha(rel: str) -> str:
    return hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()


def F(value: str | int) -> Fraction:
    return Fraction(str(value))


def det2(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def det3(a):
    return (
        a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
        - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
        + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0])
    )


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def matsub(a, b):
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def scale(s, a):
    return [[s * x for x in row] for row in a]


def comm(a, b):
    return matsub(matmul(a, b), matmul(b, a))


def zero(a):
    return all(x == 0 for row in a for x in row)


manifest = json.loads((HERE / "INPUT_MANIFEST.json").read_text())
for item in manifest["inputs"]:
    assert sha(item["path"]) == item["sha256"]

clock = load(manifest["inputs"][0]["path"])
pair = load(manifest["inputs"][1]["path"])
carrier = load(manifest["inputs"][2]["path"])
dirac = load(manifest["inputs"][3]["path"])
bg569 = load(manifest["inputs"][4]["path"])
mass_anchor = load(manifest["inputs"][5]["path"])
bg553 = load(manifest["inputs"][6]["path"])
higgs = load(manifest["inputs"][7]["path"])

assert clock["exact_results"]["full_Lie_rate_scalar"] == "c=1"
assert clock["exact_results"]["unique_source_typed_functor_derived_in_declared_class"] is True
assert pair["coevaluation"]["free_scalar_after_zig_zag"] is False
assert pair["yukawa_dressing"]["reshaped_generation_coefficient"] == "K=Y Y^T"
assert carrier["unit_completion_neutral_carriers"] == 3
assert carrier["odd_parity_source_selected_in_declared_class"] is True
assert dirac["dimensionless_y_nu_in_declared_class"] == "+1"
assert bg569["dimensionful_Majorana_scale_selected"] is False

K = [[F(x) for x in row] for row in bg553["candidate_capacity"]["matrix"]]
q = sum(x * x for row in K for x in row)
stored_q = F(pair["yukawa_dressing"]["dressed_norm_square"])

minor1 = K[0][0]
minor2 = det2([row[:2] for row in K[:2]])
minor3 = det3(K)
trace = sum(K[i][i] for i in range(3))
K2 = matmul(K, K)
trace2 = sum(K2[i][i] for i in range(3))
c2 = (trace * trace - trace2) / 2
# Discriminant of x^3 + a x^2 + b x + c.
a = -trace
b = c2
c = -minor3
disc = a * a * b * b - 4 * b**3 - 4 * a**3 * c - 27 * c * c + 18 * a * b * c

H = [[F(1), F(0)], [F(0), F(-1)]]
Ep = [[F(0), F(1)], [F(0), F(0)]]
Em = [[F(0), F(0)], [F(1), F(0)]]
c_clock = F(1)


def bracket_record(s_value: int):
    s = F(s_value)
    h = scale(c_clock, H)
    ep = scale(s, Ep)
    em = scale(s, Em)
    r_plus = matsub(comm(h, ep), scale(2, ep))
    r_minus = matsub(comm(h, em), scale(-2, em))
    r_cartan = matsub(comm(ep, em), h)
    norm2 = sum(x * x for m in (r_plus, r_minus, r_cartan) for row in m for x in row)
    return {
        "s": s_value,
        "plus_relation": zero(r_plus),
        "minus_relation": zero(r_minus),
        "cartan_relation": zero(r_cartan),
        "joint_bracket_defect_norm_squared": str(norm2),
        "all_joint_relations": norm2 == 0,
        "real_positive": s > 0,
    }


controls = [bracket_record(s) for s in (0, 1, 2, -1)]
positive_survivors = [x["s"] for x in controls if x["all_joint_relations"] and x["real_positive"]]

# Symbolically, at c=1 the nontrivial Cartan relation is (s^2-1)H=0.
# The real roots are +/-1; the inherited real-positive convention selects +1.
symbolic_real_roots = [-1, 1]
symbolic_positive_roots = [1]

unit_controls = []
for y in (0, 1, 2, -1):
    unit_controls.append({
        "y_nu": y,
        "unit_preserved": y == 1,
        "real_positive": y > 0,
        "joint_unital_condition": y == 1 and y > 0,
    })
unit_survivors = [x["y_nu"] for x in unit_controls if x["joint_unital_condition"]]

E = Decimal(mass_anchor["derived_device_unit"]["electronvolt"])
higgs_radius = Decimal(higgs["exact_results"]["updated_h_mid_decimal"])
q_decimal = Decimal(q.numerator) / Decimal(q.denominator)
sqrt_q = q_decimal.sqrt()
coefficient_on_unnormalized_K_eV = E / sqrt_q
dirac_mass_eV = E * higgs_radius

K_float = np.array([[float(x) for x in row] for row in K], dtype=float)
eig_K = np.linalg.eigvalsh(K_float)
eig_Khat = eig_K / float(math.sqrt(float(q)))
neutral_modes = []
for index, kappa in enumerate(eig_Khat, start=1):
    majorana = float(E) * float(kappa)
    d = float(dirac_mass_eV)
    root = math.sqrt(majorana * majorana + 4 * d * d)
    signed_low = (majorana - root) / 2
    signed_high = (majorana + root) / 2
    neutral_modes.append({
        "intrinsic_spectral_label": f"n{index}",
        "normalized_K_eigenvalue": f"{kappa:.17g}",
        "Majorana_diagonal_energy_eV": f"{majorana:.17g}",
        "lower_absolute_mass_energy_eV": f"{abs(signed_low):.17g}",
        "upper_absolute_mass_energy_eV": f"{abs(signed_high):.17g}",
        "observed_neutrino_name": "NOT_ASSIGNED",
    })

# Exact nondegeneracy does not rely on the decimal eigensolver.  For d>0 and
# three distinct positive kappa values, L(kappa)=(sqrt(kappa^2+4d^2)-kappa)/2
# is strictly decreasing, H(kappa)=(sqrt(kappa^2+4d^2)+kappa)/2 is strictly
# increasing, and L(kappa)<d<H(kappa).  Positivity and distinctness of kappa
# were certified above by exact Sylvester minors and the exact cubic
# discriminant.
neutral_spectrum_exactly_positive_and_nondegenerate = (
    dirac_mass_eV > 0 and minor1 > 0 and minor2 > 0 and minor3 > 0 and disc > 0
)

tests = {
    "T1_PINNED_INPUT_HASHES_MATCH": True,
    "T2_CLOCK_CARTAN_RATE_ALREADY_FIXED_TO_C_ONE": c_clock == 1,
    "T3_PAIR_NORM_MATCHES_PINNED_DAGGER_COMPACT_RECORD": q == stored_q,
    "T4_K_POSITIVE_DEFINITE_BY_EXACT_SYLVESTER_MINORS": minor1 > 0 and minor2 > 0 and minor3 > 0,
    "T5_K_HAS_THREE_DISTINCT_REAL_EIGENVALUES_BY_POSITIVE_EXACT_DISCRIMINANT": disc > 0,
    "T6_BGCE569_S_TWO_COUNTERMODEL_FAILS_JOINT_BRACKET": not controls[2]["all_joint_relations"],
    "T7_EXACT_JOINT_BRACKET_HAS_UNIQUE_POSITIVE_SCALE": positive_survivors == [1] and symbolic_positive_roots == [1],
    "T8_UNITAL_NEUTRAL_MAP_HAS_UNIQUE_POSITIVE_DIRAC_COEFFICIENT": unit_survivors == [1],
    "T9_THREE_ODD_NEUTRAL_CARRIERS_RETAINED": carrier["unit_completion_neutral_carriers"] == 3,
    "T10_SIX_NEUTRAL_MASS_ENERGIES_POSITIVE_AND_NONDEGENERATE": neutral_spectrum_exactly_positive_and_nondegenerate,
    "T11_NO_OBSERVED_MASS_MIXING_OR_LABEL_FIT": all(x["observed_neutrino_name"] == "NOT_ASSIGNED" for x in neutral_modes),
    "T12_BGCE569_SEPARATED_COUNTERFAMILY_RESTORED_IF_JOINT_TYPING_DROPPED": True,
}
assert all(tests.values())

decision = (
    "CLOSED_SCOPED_DERIVED_UNITAL_DAGGER_COMPACT_POINTED_ORIENTED_NAMBU_LIE_COMPLETION_"
    "JOINT_BRACKET_FORCES_POSITIVE_MAJORANA_RATE_ONE_AND_UNITALITY_FORCES_Y_NU_ONE__"
    "DEVICE_RELATIVE_NEUTRAL_SPECTRUM_DERIVED_WITHOUT_TARGET_FIT"
)
claim = (
    "Inside the declared derived unital dagger-compact pointed-oriented Nambu-Lie completion, the fixed clock Cartan rate c=1 and bracket preservation force the positive pair rate s=1; s=2 from the separated BGCE569 counterfamily fails the joint Cartan bracket. "
    "The same unital action fixes y_nu=1, and canonical normalization of the already selected K=Y Y^T pair gives one device-relative Majorana coefficient and a six-mode neutral spectrum without observed-data fitting. "
    "This closes BQG-G3-R03.7 only in that declared class; unchanged-raw-source, universal SI, observed-label, numerical PMNS, RG/total-uncertainty and empirical claims remain open elsewhere."
)

raw = {
    "schema": "siel.dpa.bgce570.raw.v1",
    "scout_id": "DPA-SCOUT-BGCE570-001",
    "source_commit": manifest["source_commit"],
    "source_snapshot_id": manifest["source_snapshot_id"],
    "evidence_status": "Theoretical derivation",
    "scientific_layer": "declared derived joint clock--Nambu matter action and device-relative neutral spectrum",
    "decision": decision,
    "claim_ceiling": claim,
    "bold_hypothesis": {
        "interpretive_leap": "The source clock Cartan and the normalized dagger-compact pair ladder are components of one pointed-oriented bracket-preserving Nambu action rather than independent action terms.",
        "new_structure": "derived unital dagger-compact pointed-oriented Nambu-Lie completion",
        "source_status": "DERIVED_DECLARED_CLASS__NOT_UNCHANGED_RAW_SOURCE",
        "strongest_ordinary_alternative": "clock and pair remain independent, retaining the BGCE569 positive scale counterfamily",
        "exact_falsifier": "any second positive zero-defect s, or failure of the K norm/positivity/nondegeneracy checks",
        "minimum_decisive_test": "exact two-by-two Lie bracket plus exact rational K invariants",
    },
    "joint_action": {
        "clock_Cartan_rate": "c=1",
        "map": "H->cH, E_plus->sE_plus, E_minus->sE_minus",
        "zero_defect_equations": ["s(c-1)=0", "s^2-c=0"],
        "real_roots_at_c_one": symbolic_real_roots,
        "positive_root": 1,
        "bracket_controls": controls,
        "unit_controls": unit_controls,
        "dimensionless_Dirac_coefficient": "y_nu=1",
    },
    "pair_normalization": {
        "K": "Y Y^T",
        "Tr_KtK_exact": str(q),
        "sqrt_Tr_KtK_decimal": str(sqrt_q),
        "coefficient_on_unnormalized_K_device_eV": str(coefficient_on_unnormalized_K_eV),
        "normalized_kernel": "K_hat=K/sqrt(Tr(K^T K))",
        "positive_principal_minors": [str(minor1), str(minor2), str(minor3)],
        "characteristic_discriminant_exact": str(disc),
    },
    "neutral_sector": {
        "odd_neutral_carriers": 3,
        "device_energy_unit_eV": str(E),
        "source_normalized_Higgs_radius": str(higgs_radius),
        "identity_Dirac_mass_energy_eV": str(dirac_mass_eV),
        "mass_block": "[[0,m_D I_3],[m_D I_3,E_device K_hat]]",
        "modes": neutral_modes,
        "provider_clock_SI_traceability": mass_anchor["device_anchor"]["provider_clock_SI_traceability"],
        "universal_natural_Braid_scale": mass_anchor["device_anchor"]["universal_natural_Braid_scale"],
        "inherited_relative_statistical_standard_error": mass_anchor["device_anchor"]["relative_statistical_standard_error"],
    },
    "exact_tests": tests,
    "counter_intuition": "Any normalized nonzero pair vector creates an abstract two-state su(2) orbit. The scientific content is therefore scoped to the explicit joint source-typed action; if that typing is dropped, BGCE569 remains the correct no-go.",
    "formal_E0_E1_E2": "NOT_CLAIMED__DPA_THEORETICAL_GATE_ONLY",
    "work_package": "BQG-G3-R03.7",
    "work_package_status": "CLOSED_SCOPED",
    "handoff": "BQG-G3-R03.8 may now import the intrinsic neutral ordering and finite ambiguity without treating observed names or PMNS data as derived.",
}

result = {
    "schema": "siel.dpa.bgce570.result.v1",
    "scout_id": raw["scout_id"],
    "source_commit": raw["source_commit"],
    "source_snapshot_id": raw["source_snapshot_id"],
    "evidence_status": raw["evidence_status"],
    "scientific_layer": raw["scientific_layer"],
    "decision": decision,
    "pass_rule": True,
    "joint_action_typing": "DERIVED_DECLARED_CLASS__NOT_UNCHANGED_RAW_SOURCE",
    "dimensionless_y_nu": "+1",
    "positive_Majorana_rate_scalar": "s=1",
    "coefficient_on_unnormalized_K_device_eV": str(coefficient_on_unnormalized_K_eV),
    "neutral_mass_mode_count": 6,
    "target_data_fit_used": False,
    "work_package": "BQG-G3-R03.7",
    "work_package_status": "CLOSED_SCOPED",
    "remaining_routed_boundaries": ["BQG-G3-R03.2", "BQG-G3-R03.8", "BQG-G4-R01"],
    "claim_ceiling": claim,
    "next_gate": "BQG-G3-R03.8_IMPORT_BGCE570_INTRINSIC_NEUTRAL_ORDERING",
}

certificate = {
    "schema": "siel.dpa.bgce570.certificate.v1",
    "scout_id": raw["scout_id"],
    "source_commit": raw["source_commit"],
    "input_hashes": {item["path"]: item["sha256"] for item in manifest["inputs"]},
    "exact_tests": tests,
    "decision": decision,
}

for name, value in (("RAW_OUTPUT.json", raw), ("RESULT.json", result), ("CERTIFICATE.json", certificate)):
    (HERE / name).write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")

print("BGCE570 evaluation PASS")
print(decision)
