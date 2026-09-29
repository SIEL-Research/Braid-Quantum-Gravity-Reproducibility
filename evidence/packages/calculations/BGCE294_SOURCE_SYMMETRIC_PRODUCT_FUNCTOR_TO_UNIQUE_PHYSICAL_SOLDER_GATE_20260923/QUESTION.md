# BGCE294 — source symmetric-product functor to unique physical solder gate

## Frozen question

Does the nine-dimensional `S4`-equivariant freedom found by BGCE291 survive
once a solder is required to preserve the actual source type: ten metric
functionals generated as the symmetric square of four source-carrier labels?

## Gates

1. Reconfirm the unrestricted `S4` commutant dimension.
2. Impose only clock/grading/event spectral tensors and measure the residual
   freedom; these constraints must not be overstated.
3. Use the committed BGCE141 construction to determine whether the ten sources
   are a bilinear `Sym2` object, and the committed BGCE268 `U` to fix the
   underlying four-carrier map.
4. Require carrier-functoriality:

```text
T(v symmetric-product w)=U(v) symmetric-product U(w).
```

   Test exact uniqueness on the ten spanning rank-one tensors `e_i^2` and
   `(e_i+e_j)^2`.
5. Separate a uniqueness theorem inside this existing typed class from a claim
   that every conceivable non-functorial physical solder is impossible.

No coefficient fitting, numerical scan or new matter action is allowed.

## Decision

- Full pass in the source-typed class requires affine solution dimension zero
  after the product-functorial constraints and exact recovery of `Sym2(U)`.
- If the product constraint is not already encoded by the source construction,
  report it as a new assumption and keep physical solder open.

## Claim boundary

This gate can select the metric solder. It cannot by itself prove equality of
the finite Braid action variation with the continuum BKM Hilbert variation,
Ward conservation, Einstein dynamics or empirical gravity.
