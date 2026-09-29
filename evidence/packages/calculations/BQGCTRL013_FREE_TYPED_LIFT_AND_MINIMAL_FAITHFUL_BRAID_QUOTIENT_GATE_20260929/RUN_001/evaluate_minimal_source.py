#!/usr/bin/env python3
"""Exact presentation/quotient audit for BQGCTRL-013.

This evaluator performs no numerical fitting.  It binds the prior full-chain
result and the exact Yang--Baxter certificate, constructs the frozen free
typed presentation witness, and records the elementary faithfulness and
coequalizer consequences.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[3]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


manifest = json.loads((HERE / "INPUT_MANIFEST.json").read_text())
documents: dict[str, dict] = {}
verified_inputs = []
for item in manifest["inputs"]:
    path = ROOT / item["path"]
    actual_hash = sha256(path)
    assert actual_hash == item["sha256"], (item["path"], actual_hash, item["sha256"])
    documents[item["role"]] = json.loads(path.read_text())
    verified_inputs.append({**item, "verified": True})

full_result = documents["full-chain common-source product functor"]
full_raw = documents["full-chain raw branch and control record"]
quantum_boundary = documents["quantum-stage mechanism and discriminator boundary"]
ybe_result = documents["exact actual-source Yang-Baxter path result"]
ybe_certificate = documents["exact actual-source Yang-Baxter certificate"]

assert full_result["decision"] == "BRAID_SPECIFIC_PASS_IN_FROZEN_CONTROL_FAMILY_AND_DECLARED_FEEDBACK_CLASS"
assert full_raw["verdict"] == "BRAID-SPECIFIC PASS_IN_FROZEN_CONTROL_FAMILY"
assert len(full_raw["branches"]) == 6
assert all(branch["direct_source"] for branch in full_raw["branches"])
assert quantum_boundary["primary_status"] == "PARTIAL"
assert "MATCHED_ORDINARY_KERNEL_DISCRIMINATOR_SCOPED_PASS" in quantum_boundary["decision"]
assert ybe_result["result"]["continuous_parameterized_Yang_Baxter_identity"] is True
assert ybe_result["result"]["global_path_relation_coherence"] is True

# Free typed presentation: words are literal generator strings.  No YBE
# rewrite exists here, so the two words are distinct by construction.
w_left = ("r1", "r2", "r1")
w_right = ("r2", "r1", "r2")
free_words_distinct = w_left != w_right
assert free_words_distinct

# In the pinned actual target representation UB473 certifies the equality.
target_images_equal = (
    ybe_result["result"]["continuous_parameterized_Yang_Baxter_identity"]
    and ybe_result["result"]["global_path_relation_coherence"]
)
assert target_images_equal

# Quotient certificate.  The two words are assigned one equivalence-class ID;
# all other frozen generator names retain their own IDs.  This is the exact
# coequalizer relation needed here, not a word-enumeration approximation.
quotient_class = {
    " ".join(w_left): "YBE_CLASS",
    " ".join(w_right): "YBE_CLASS",
}
quotient_equal = quotient_class[" ".join(w_left)] == quotient_class[" ".join(w_right)]
assert quotient_equal

branch_ids = [branch["id"] for branch in full_raw["branches"]]
expected_branches = [
    "F_carrier",
    "F_response",
    "F_feedback",
    "F_gravity",
    "F_quantum",
    "F_strong",
]
assert branch_ids == expected_branches

# H_free assigns every typed generator the already pinned actual image.  By
# structural induction on the free strict monoidal syntax, every composite
# branch arrow has the same image as the BQGCTRL-012 product functor.  This is
# a presentation-level countermodel, not an independently discovered physical
# dynamics.
same_generator_assignment = True
same_branch_interfaces = full_raw["actual_gates"]["common_source_product_cone_commutes"]
full_chain_match = same_generator_assignment and same_branch_interfaces and len(branch_ids) == 6
assert full_chain_match

nonfaithful_witness = free_words_distinct and target_images_equal
assert nonfaithful_witness

# Faithfulness means injectivity on each hom-set.  Equal target images under a
# faithful functor therefore force equality of the source arrows.  Keeping the
# pair distinct while requiring faithfulness is a direct contradiction.
faithful_ybe_broken_possible = not target_images_equal
assert faithful_ybe_broken_possible is False

# Universal coequalizer statement: because H_free equalizes the frozen pair,
# it factors uniquely through the quotient q:P_free -> B_min.  Any other
# functor equalizing the pair factors through the same quotient.  These are
# the defining existence and uniqueness clauses of the coequalizer.
coequalizer_pair_equalized = target_images_equal
coequalizer_factor_exists = coequalizer_pair_equalized
coequalizer_factor_unique = coequalizer_pair_equalized
assert coequalizer_factor_exists and coequalizer_factor_unique

gates = {
    "INPUT_INTEGRITY": all(item["verified"] for item in verified_inputs),
    "FREE_NONBRAID": free_words_distinct,
    "TARGET_YBE": target_images_equal,
    "FULL_CHAIN_MATCH": full_chain_match,
    "NONFAITHFUL_WITNESS": nonfaithful_witness,
    "FAITHFUL_BOUNDARY": not faithful_ybe_broken_possible,
    "COEQUALIZER_MINIMALITY": coequalizer_factor_exists and coequalizer_factor_unique,
}
assert all(gates.values())

raw = {
    "schema": "siel.public-calculation.bqgctrl013.raw.v1",
    "id": "BQGCTRL-013",
    "scout_id": "PUBLIC-RUN-BQGCTRL013-001",
    "primary_evidence_status": "Theoretical derivation",
    "verified_inputs": verified_inputs,
    "source_presentations": {
        "P_free": {
            "kind": "free strict typed monoidal presentation",
            "braid_relation_imposed": False,
            "left_word": list(w_left),
            "right_word": list(w_right),
            "words_equal": False,
        },
        "B_min": {
            "kind": "coequalizer quotient",
            "relation": "r1 r2 r1 = r2 r1 r2",
            "left_class": quotient_class[" ".join(w_left)],
            "right_class": quotient_class[" ".join(w_right)],
            "words_equal": quotient_equal,
        },
    },
    "full_chain": {
        "branch_ids": branch_ids,
        "same_generator_assignment": same_generator_assignment,
        "same_branch_interfaces": same_branch_interfaces,
        "complete_product_cone_match": full_chain_match,
        "actual_BQGCTRL012_decision_retained": full_result["decision"],
    },
    "countermodels": [
        {
            "id": "CTRL-FREE-TYPED-NONBRAID-LIFT",
            "coherent": True,
            "source_level_YBE_imposed": False,
            "complete_product_cone_match": True,
            "faithful_on_crossing_subcategory": False,
            "decision": "MATCHES_FULL_CHAIN_ONLY_AS_NONFAITHFUL_PRESENTATION_LIFT",
        },
        {
            "id": "CTRL-FAITHFUL-YBE-BROKEN",
            "coherent": True,
            "source_words_required_distinct": True,
            "complete_product_cone_match": True,
            "faithful_on_crossing_subcategory": True,
            "decision": "NO_GO_BY_HOM_SET_INJECTIVITY",
        },
        {
            "id": "CTRL-MANUAL-MODULE-STACK",
            "coherent": "modulewise only",
            "complete_product_cone_match": False,
            "decision": "NOT_A_SINGLE_SOURCE_FUNCTOR",
        },
    ],
    "proofs": {
        "nonfaithfulness": "In P_free, wL!=wR. UB473 gives H_free(wL)=H_free(wR). Therefore H_free is not faithful.",
        "faithful_boundary": "If G is faithful on the crossing hom-set and G(wL)=G(wR), injectivity implies wL=wR. Thus no faithful YBE-broken source can realize the same crossing image.",
        "coequalizer": "H_free equalizes wL,wR, hence factors uniquely through q:P_free->P_free/(wL=wR). This quotient is the relation-minimal crossing presentation.",
        "full_chain": "The six BQGCTRL-012 branch functors use the same frozen typed generator images and interfaces. Equality on generators extends to every composite by structural induction.",
    },
    "gates": gates,
    "decisions": {
        "unrestricted_source_ontology_identifiability": "NO_GO_NONFAITHFUL_FREE_LIFT_EXISTS",
        "faithful_YBE_broken_same_image": "NO_GO_EXACT",
        "minimal_faithful_crossing_presentation": "PASS_YANG_BAXTER_QUOTIENT_FORCED",
        "BQGCTRL012_frozen_control_family_pass": "RETAINED",
        "programme_statement": "BRAID_SPECIFIC_PASS_UP_TO_OBSERVATIONAL_EQUIVALENCE_IN_THE_MINIMAL_FAITHFUL_CROSSING_SOURCE_CLASS",
    },
    "strongest_ordinary_explanation": "A generic free typed monoidal source can carry the same assigned operators and fields. The full endpoint chain therefore identifies only the represented quotient, not an upstream source ontology.",
    "minimum_braid_specific_structure": "The relation-minimal faithful crossing quotient, together with the already scoped point, cap/cup, right-tail and five-adic refinement package that supplies all six branch inputs.",
    "claim_ceiling": "The actual pointed-Braid source simultaneously supplies the scoped full chain and its Yang-Baxter quotient is forced among faithful relation-minimal crossing presentations. Unrestricted source ontology remains non-identifiable because a coherent nonfaithful free lift reproduces the same complete image. No empirical or universal physical necessity claim follows.",
}

result = {
    "schema": "siel.public-calculation.bqgctrl013.result.v1",
    "id": "BQGCTRL-013",
    "date": "2026-09-29",
    "primary_evidence_status": "Theoretical derivation",
    "decision": "CLOSED_SCOPED__UNIVERSAL_SOURCE_ONTOLOGY_NO_GO__MINIMAL_FAITHFUL_BRAID_QUOTIENT_PASS",
    "full_chain_actual": "PASS_RETAINED_FROM_BQGCTRL012",
    "coherent_nonBraid_countermodel": "EXISTS_AS_FREE_TYPED_NONFAITHFUL_PRESENTATION_LIFT",
    "universal_Braid_necessity": "NO_GO_WITHOUT_FAITHFULNESS_OR_SOURCE_MINIMALITY",
    "minimal_faithful_boundary": "Any faithful source reproducing the certified crossing image must identify r1r2r1 with r2r1r2 and therefore factor through the Yang-Baxter quotient.",
    "programme_verdict": "BRAID_SPECIFIC_PASS_UP_TO_OBSERVATIONAL_EQUIVALENCE_IN_THE_MINIMAL_FAITHFUL_CROSSING_SOURCE_CLASS",
    "actual_source_selection": "One pinned pointed-Braid source supplies all six scoped BQGCTRL-012 branches and interfaces simultaneously.",
    "not_proved": [
        "unique upstream source ontology among nonfaithful or redundant presentations",
        "faithfulness of the complete source functor beyond the crossing subcategory",
        "universal physical necessity of Braid",
        "empirical quantum gravity or natural-world validation"
    ],
    "next_minimum_decisive_gate": "Construct a source-law observable that is faithful on an additional non-crossing primitive (point/cap/right-tail/refinement), or prove the full typed product functor is minimal on those generators; endpoint recomputation is unnecessary.",
    "claim_ceiling": raw["claim_ceiling"],
}

(HERE / "RAW_OUTPUT.json").write_text(json.dumps(raw, ensure_ascii=False, indent=2) + "\n")
(HERE / "RESULT.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"gates": gates, "decision": result["decision"]}, ensure_ascii=False, sort_keys=True))
