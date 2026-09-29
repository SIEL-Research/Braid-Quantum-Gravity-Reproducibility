# BGCE291 — stress/Ward independent rederivation and scope red-team gate

## Frozen question

Does BGCE290 actually remove the last Braid-only stress/Ward bridge, or does it
only construct an algebraically valid rank-ten source-to-metric candidate and
then promote a pointwise coframe identity to an unproved active curved Markov
transport?

The audit must independently decide four noncompensating gates:

1. **Source typing:** the ten `a_A` must be the independent dual sources of the
   ten symmetric functionals built from the fixed four-operator source frame.
2. **Physical solder selection:** the normalized Hadamard carrier map must do
   more than provide one invertible `Sym2` intertwiner. Existing source
   principles must select it as the off-shell physical metric solder; `S4`
   covariance alone is insufficient if multiple invertible intertwiners exist.
3. **Active transport:** the source record must provide an integrable finite
   curved conductance/Markov transport, not only a first-order connection or
   the algebraic identity `H=S^T K+KS`.
4. **Action identity:** the varied covariant BKM action must be the same action
   derived from the finite Braid source. Conditional minimal coupling or a
   standard sigma-model Noether identity does not by itself establish a
   Braid-derived Hilbert stress/Ward package.

## Exact short tests

- Recompute the rank of the BGCE290 `Sym2(U)` map.
- Compute the exact dimension of the commutant of the `S4` action on
  `Sym2(R^4)`. Dimension greater than one falsifies uniqueness from `S4`
  equivariance alone.
- Compare BGCE290's promoted booleans with the explicit scope fields of
  BGCE267, BGCE268, BGCE284, BGCE285, BGCE286 and BGCE287.
- No numerical scan and no new action are allowed.

## Decision rule

`FULL_PASS` requires all four gates. If the algebraic rank-ten solder survives
but physical selection, nonlinear active transport or action identity remains
open, issue a partial reversal: retain the solder as a canonical candidate,
restore Hilbert stress/Ward to conditional status, and identify the shortest
missing theorem.

## Forbidden promotions

- Carrier compatibility to an off-shell spacetime metric functor.
- Pointwise coframe solvability to finite active Markov dynamics.
- First-order horizontal lift to nonlinear integrability.
- Conditional minimal coupling to a Braid-only action theorem.
- A standard Noether identity to Einstein dynamics or empirical gravity.
