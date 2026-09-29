# PUBLIC-RUN-BQGSTRAT-009 frozen plan

- Date: `2026-09-29`
- Snapshot: `162680b8b2c0b45d2ceaa6baef6a1f00d9af7cc5`
- Evidence status: `Theoretical derivation`
- Parent: `BQG-G3-R01.5 / BQG-G3-R02.5`

## Claim under test

The missing finite Palatini second jet is the ordinary second differential of
structures already present in the source packet:

1. `U_e=Pexp integral_e Gamma` on the BGCE138 identity component;
2. the principal oriented face log used by BGCE097;
3. the source-selected five-adic four-cube and its incidence boundary;
4. the BGCE138 flat anchor `e=3 I_4, Gamma=0`.

Together they should define the raw `K_ii/K_ib` bilinear forms without adding a
new physical coefficient.

## Bold hypothesis

BQGSTRAT-008 found no *inference* from the first jet to the second jet. The
missing construction is nevertheless already latent as the two-jet of the
committed `Pexp/log` discretization. The source complex supplies the missing
boundary/interior index split.

## Strongest ordinary alternative

This is standard lattice gauge/Palatini geometry. Even if the construction
passes, it does not prove that Braid is necessary, that the resulting Hessian
has a physical clean rank loss, or that the ordered source mark selects a
unique outgoing branch.

## Noncompensating gates

1. Reproduce the oriented four-edge plaquette logarithm through degree two in
   exact noncommutative algebra.
2. Verify reversal gives the negative face log and the constant-connection
   specialization gives `[A,B]`.
3. Derive the depth-one `5^4` cubical boundary/interior incidence counts from
   the source refinement, not by importing a target lattice size.
4. Verify the linear face incidence annihilates every interior edge at the
   flat constant-coframe anchor.
5. State the exact second variation and raw `K_ii/K_ib` restrictions.
6. Preserve the BGCE094 temporal-promotion condition and leave actual rank,
   crossing and component selection open until the sparse Hessian is evaluated.

## Exact endpoint

PASS requires all five algebra/incidence/stationarity checks and an explicit
second-variation formula. FAIL if any identity fails. A PASS constructs the
previously missing input; it does not itself locate a caustic.

## Deterministic evaluator

`evaluate.py` uses exact `Fraction` coefficients in the truncated free
associative algebra and exhaustive combinatorial incidence on one `n=5`
source parent. No floating-point arithmetic, parameter fit or long sweep is
used.

## Retained artifacts

Plan, source matrix, theorem, evaluator, raw output, result, report, status and
append-only iteration ledger.

## Claim ceiling

At most a conditional source-compatible construction of the raw finite-depth
Palatini second jet and its canonical child split. No evaluated rank loss,
crossing form, unique relation component, global continuation, unconditional
Braid-only temporal provenance, quantum BV result or empirical claim.
