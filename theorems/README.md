# Theorem traceability contract

The v0.99 manuscript contains 47 theorem environments, four propositions and
two corollaries. Every one of the 53 statements must appear exactly once in
`theorem_evidence_v099.json` and must close by one of three routes:

- `PUBLIC_PROOF`: a self-contained proof is included in this repository;
- `PUBLIC_CODE`: frozen public input, executable code, expected output and a
  verification command are included;
- `EXTERNAL_THEOREM_REDUCTION`: the manuscript statement is explicitly reduced
  to a cited external theorem after all model-specific hypotheses are checked.

`scripts/verify_theorem_coverage.py` fails if any statement is missing, points
to a nonexistent file, lacks a command for a code result, lacks a claim
ceiling, or retains a pending status. A passing source-level verifier does not
automatically close a downstream theorem.

The inventory is extracted mechanically from the English v0.99 source. The
evidence ledger is a scientific audit object and must be reviewed rather than
generated from theorem titles alone.
