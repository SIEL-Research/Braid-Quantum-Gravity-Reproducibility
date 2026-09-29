# PUBLIC-RUN-BQGSTRAT-011 plan

## Parent question

Can the canonical orientation double cover and reverse-edge rule already present
in the source complete the `BQGSTRAT-010` single-orientation Palatini symbol so
that both cyclotomic null sheets carry two additional kernel directions?

## Pinned inputs

- Source revision: `66461357b07465ae85bb276079331a107fd3cd60`.
- `BQGSTRAT-009`: exact affine-plaquette second jet and reverse-orientation law.
- `BQGSTRAT-010`: exact `Q(zeta_5)` rank profile.
- `BGCE137`: canonical two-sheet orientation cover.
- `BGCE138`: inverse/reverse-edge transport through path-ordered holonomy.
- `BGCE259`: retained boundary that an orientation-even quadratic form does not
  acquire a new principal sign from forward/reverse duplication alone.

All inputs are hash-bound in `SOURCE_MATRIX.json`.

## Frozen hypothesis and ordinary alternative

**Bold hypothesis.** The source orientation double cover supplies the missing
reverse face without a new coefficient.  On a reversed oriented face,
`P_bar=P^{-1}`, hence `log(P_bar)=-log(P)`, while the Palatini face bivector also
changes sign.  Their product may therefore give a canonical second sheet.

**Strongest ordinary alternative.** The two signs cancel exactly, so the
reverse-sheet term is only another copy of the original action.  Its Hessian is
a scalar multiple of the old Hessian and cannot alter any rank or corank.

## Exact endpoint and falsifier

1. Verify the source records and their hashes at the pinned revision.
2. Verify, in the exact degree-two free-associative plaquette algebra, that the
   reversed boundary word has logarithm `-log(P)`.
3. Apply the antisymmetric Palatini face weight.  A legal orientation reversal
   must reverse both the boundary word and the face orientation.
4. Classify every scalar forward/reverse completion.  If its Hessian is a
   nonzero scalar multiple of the `BQGSTRAT-010` Hessian, the rank profile must
   remain `60 x1, 64 x12, 65 x12, 66 x600`; a zero scalar gives the zero form.
5. PASS only if a source-derived legal completion produces rank 64 on both
   null sheets without a fitted coefficient, manual symmetrization, a target
   Einstein equation, or a new off-diagonal sheet coupling.  Otherwise prove
   the reverse-sheet-only route NO-GO.

The exact falsifier of the ordinary alternative is a source-authorized reverse
term that is not proportional to the original real-space Palatini quadratic
form and has exact rank 64 on both sheets.

## Evaluator, retained artifacts and stopping rule

- Evaluator: `evaluate.py`.
- Command: `python3 evaluate.py` from this directory.
- Retain: this plan, source matrix, evaluator, attempt ledger, raw output,
  result, verifier and report.
- Stop after the exact proportionality/rank theorem decides the gate.  Do not
  run a numerical parameter scan.

## Claim ceiling

This scout decides only whether the already-declared scalar reverse-face or
adjoint completion can repair the `BQGSTRAT-010` two-versus-one null-sheet
corank imbalance.  It does not exclude a newly derived off-diagonal doubled
branch pairing, a different quasi-local perfect action, matter coupling,
generic singular continuation, Braid necessity, empirical gravity,
confirmation, RPD adoption or Official SIEL adoption.
