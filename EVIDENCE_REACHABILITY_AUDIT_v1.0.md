# v1.0 Evidence-Reachability Audit

Audit date: 2026-09-30
Decision: **PASS — PUBLIC EVIDENCE REACHABILITY CLOSED**

## Gate

Every theorem-like statement in the English v1.0 manuscript must have a
reader-visible route that terminates in at least one of the following:

1. repository-local executable code with frozen result artifacts;
2. a repository-local analytic proof;
3. a checked reduction to a named external theorem whose hypotheses are stated.

The gate fails if a statement is missing, if an evidence path is absent, if a
declared dependency is absent, if a frozen artifact has changed, or if a
vendored canonical verifier fails.

## Result

The manuscript contains 53 theorem-like statements:

- 47 theorems;
- 4 propositions;
- 2 corollaries.

All 53 are present in `THEOREM_EVIDENCE_INDEX_v1.0.md` and terminate as follows:

- 46 in repository-local executable evidence;
- 5 in repository-local analytic proofs;
- 2 in checked external-theorem reductions.

The package validation additionally reports:

- 47 canonical vendored verifiers passed;
- 4 public adapters passed for packages whose historical verifier depended on
  the private SRA checkout or Git graph;
- 11 supporting dependency packages were present and hash-checked;
- 1 historical failed implementation was retained and explicitly excluded from
  the canonical endpoint;
- no private Git history is required by the public validation path.

The external source audit resolved and checked the two E016 DOI records, the
open Fierz--Pauli reduction source, and the cited inextendibility theorem.

## Reproduction boundary

This decision closes **evidence reachability**. It means that a third party can
start from the paper, locate each theorem-like statement in the public index,
and reach inspectable code, data, proof, or an explicit external reduction
without access to a private research checkout.

It does **not** mean that all 53 statements have been independently reproduced
by a third party, that every mathematical construction has an independent
implementation, or that the quantum-gravity interpretation has been
experimentally confirmed. Registered reproducibility refers only to the E016
frozen rerun and its two DOI records.

## Machine checks

The release gate is implemented by:

```text
python scripts/verify_manifest.py
python scripts/verify_source.py
python scripts/verify_theorem_coverage_v1.py
python scripts/verify_evidence_integrity.py
python scripts/verify_vendored_packages.py
python -m unittest discover -s tests -v
```

The public repository CI executes the same fail-closed command set on every
push and pull request. The first clean-checkout public run passed all steps.
