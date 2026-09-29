# BQGBH-033 scouting plan

## Gate

`BQGBH-033_SOURCE_SCREEN_WALK_CURRENT_TO_RELATIVE_PALATINI_EULER_COVECTOR_GATE`

## North-star question

Does the actual reflected active-screen walk generate the exact finite source
current whose divergence is required by BQGBH-032, before a target metric
equation or fitted coefficient is consulted?  Does the existing raw/Petz
grading also select the physical minus sign needed for backreaction?

## Frozen hypothesis

On the signed source chain define

`rho=ell_star sqrt(J)`, `X=ell_star Sigma sqrt(J-I)`.

For every oriented source edge `e=(k,k+1)`, use the source-normalized screen
current

`j_e=Delta rho_e / Delta X_e`.

At each internal node, its signed divergence is

`Q_k=j_(k-1/2)-j_(k+1/2)`.

The BQGBH-031 pure Palatini Euler covector evaluated on `R=rho` is exactly the
same expression.  The BQGBH-032 interaction covector must therefore be
`-Q_k` for both natural variables `R` and `Y`.

Interpret the oriented edge currents as normalized Heisenberg coboundaries of
the actual BQGBH-003 in/out unitary walk.  Compare the available raw/Petz
branch signs from BGCE348 without changing their prior or branch order after
seeing the answer.

## Noncompensating gates

1. All input hashes match.
2. The active-screen walk and signed coordinate supply both oriented adjacent
   edges, including the reflected throat.
3. The current divergence equals the pure Palatini Euler covector on an
   arbitrary nonuniform chain by exact coefficient identity.
4. At the source throat the current is `2-2 sqrt(2)` and the required
   interaction is its exact negative.
5. Record separately what raw, Petz, raw-minus-Petz, Petz-minus-raw and the
   unconditioned average supply.
6. Do not call the negative coupling derived unless an existing source rule
   selects Petz-minus-raw, rather than merely making both orderings available.

## Decision rule

- PASS the source-current shape if gates 1--4 hold.
- PASS the sign only if the frozen source records uniquely select the negative
  branch ordering needed by BQGBH-032.
- Otherwise return a split result and move the sign-selection question to the
  next gate.

## Counter-intuition scan

Every scalar field on a one-dimensional chain has an edge gradient and a node
divergence.  The nontrivial source-specific content is that `rho`, `X`, the
two orientations, the throat reflection and the finite Palatini radial
variables were derived from one pointed-Braid chain.  Equality of two
discrete divergences does not by itself select the sign with which one sector
acts on the other.

## Stopping rule

One exact algebraic identity and the exact throat witness.  No scan.

## Claim ceiling

At most derive the required finite interaction-current shape from the actual
source walk and isolate the remaining branch-sign law.  No unconditional
relative action, collapse, evaporation, thermodynamics or empirical claim.
