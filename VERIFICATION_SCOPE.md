# Verification scope for release v1.0

## Executable now

The source verifier checks all eight declared sectors and requires, without
floating-point tolerances:

1. orthogonality and involution of each crossing operator;
2. the Yang--Baxter identity on the full `5^3` basis;
3. preservation of the distinguished point;
4. the endpoint involution and cup/cap relation;
5. the source-Hamiltonian minimal polynomial;
6. the exact Brauer-projector identities;
7. the marker characteristic polynomial;
8. all eight distinct three-character labels.

The command exits nonzero if any equality fails or if the reconstructed result
differs from `expected/source_verification_v099.json`.

## Paper-wide evidence map

The v1.0 inventory contains 47 theorems, four propositions and two corollaries.
Every one of those 53 statements has a local evidence locator in
`THEOREM_EVIDENCE_INDEX_v1.0.md`, except the two CKM entries, which resolve to
their public DOI-1 and DOI-2 archives. The local coverage verifier fails on a
missing statement, locator, proof heading, executable package or claim ceiling.

The evidence classes are not interchangeable:

- `PUBLIC_CODE` preserves executable calculation material and an adjudicated
  result;
- `PUBLIC_PROOF` supplies a self-contained analytic proof with dependencies and
  ceiling stated;
- `EXTERNAL_THEOREM_REDUCTION` states the external theorem and checks its model
  hypotheses explicitly.

The gate proves reachability, not independent replication. Historical audit
packages may contain failed implementation attempts; these are retained rather
than rewritten. Scientific conclusions remain bounded by the theorem-specific
claim ceilings.
