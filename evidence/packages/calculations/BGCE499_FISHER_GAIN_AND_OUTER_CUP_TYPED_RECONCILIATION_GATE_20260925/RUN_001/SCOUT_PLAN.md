# PUBLIC-RUN-BGCE499-001 — Fisher gain / outer-cup typed reconciliation

## Parent question

Can `BQG-G3-R03.6` be closed without changing either the finite Fisher result
`1` or the continuum full-corner routing result `3/5`?

Pinned source commit: `ecfa6c97111d1cdf73626296452c82d853f69804`.

## Bold hypothesis

The two numbers have different variational types.

- `1` is the internal unit Newton/Fisher gain obtained when the gradient and
  Hessian of one record action are compared.
- `3/5` is the source-derived outer-cup weight of the full-corner matter
  action relative to the separately typed gravity action.

Therefore multiplying the matter action by `3/5` scales its score and Hessian
together, leaving the internal Fisher gain equal to `1`, while the same weight
survives between the gravity and matter first variations and yields
`G=(3/5)T`.

This changes the mechanism class from an asymmetric score/Hessian map to a
typed two-level variational composition. It introduces no new coefficient.

## Strongest ordinary alternative

The finite record action and continuum matter action are merely different
models with no derived relation. Then the algebra below shows only that the
numbers need not conflict; it does not identify a finite-to-continuum dynamics.

## Exact endpoint and noncompensating gates

1. The pinned BGCE235 source gives the full-corner outer-cup weight `p=3/5`.
2. The pinned BGCE371/372 source gives the same-record Fisher gain `1`.
3. The pinned BGCE372/373 source says the two are not the same referent and
   forbids an untyped asymmetric score-only insertion.
4. Exact algebra proves `(pF)^{-1}(pS)=F^{-1}S` for nonzero `p`.
5. Exact first-variation typing proves that
   `delta(S_g+p S_m)=0` gives `G=pT`, while no `p` is inserted between the
   matter score and matter Hessian.
6. BGCE300R1 already records the same full-corner matter lineage and
   `G=(3/5)T` in its declared continuum class.

All six gates must pass.

## Falsifier and stopping condition

The hypothesis fails if a pinned source identifies the BGCE235 cup with the
BGCE371 Fisher gain, if the continuum matter sector is not the same full-corner
lineage, if internal common scaling changes the stationary update, or if the
outer first variation does not retain `p` relative to gravity.

Stop after the exact rational/type check. No coefficient scan, long numerical
run, target-Einstein fitting, MMR/CGR insertion, or new physical axiom is
allowed.

## Execution

```text
python3 -B records/BGCE499_FISHER_GAIN_AND_OUTER_CUP_TYPED_RECONCILIATION_GATE_20260925/RUN_001/evaluate_scout.py
python3 -B records/BGCE499_FISHER_GAIN_AND_OUTER_CUP_TYPED_RECONCILIATION_GATE_20260925/RUN_001/verify.py
```

Retained raw artifact: `RAW_OUTPUT.json`.

## Claim ceiling

At most this scout may prove a typed compatibility and exact matching rule:
unit Fisher gain internally, `3/5` relative matter weight externally, in the
pinned finite source and BGCE300R1 declared continuum class. It cannot prove
that BGCE371 is a discretization or numerical integrator of BGCE300R1, cannot
derive SI Newton's constant, and cannot establish empirical or completed
quantum gravity.
