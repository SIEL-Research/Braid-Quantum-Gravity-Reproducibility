# DPA-SCOUT-BQGSTRAT-013 plan

## Frozen hypothesis

The physical parent is not the raw `BQGSTRAT-010` 80-component ultralocal
block.  The normalized ten-component source metric-Euler principal operator is
scalar on the symmetric-tensor factor, while the source TT projector acts only
on that factor.  They therefore commute, and the physical configuration symbol
must be `q_h(omega,k) I_2`.

## Pinned evidence

- `BQGULTRA-002`: exact finite-depth stationary composition and Hessian Schur
  complement on every regular transverse branch.
- `BQGADM-013`: the source-perfect parent and metric-Euler trajectory share a
  scoped on-shell asymptotic bridge, but are not literally the same finite map.
- `BQGADM-014/015`: source-derived rank-two configuration and rank-four phase
  projectors, all 124 nonzero momenta, refinement naturality.
- `BQGEULER-010`: the same normalized scalar principal operator acts on all ten
  metric components; the nonprincipal source term is separately typed.
- `BQGSTRAT-010`: the raw single-orientation 80-component block has the exact
  `2 versus 1` exceptional-sheet imbalance.

## Exact endpoint

1. Verify all source hashes and claim ceilings.
2. Reconstruct the exact source TT projector for all 124 nonzero `C5^3`
   momenta and verify rank two.
3. Prove `P(q I_6)=(q I_6)P=qP`; hence the physical restriction is `q I_2`.
4. On the flat source-axis stencil use the exact fifth-root symbol
   `q=(z0+z0^-1-2)-(zi+zi^-1-2)` and verify all 24 nonzero sheets `di=+/-d0`
   have physical kernel dimension two.
5. Verify a noncharacteristic control sector has physical rank two.
6. Use the `BQGULTRA-002` Schur theorem only on the regular transverse branch.
   Do not claim an evaluated closed-form full perfect Hessian at the
   characteristic point.

## Decision rule

PASS scoped if the physical principal symbol is exactly scalar on two TT
polarizations and both orientation sheets have kernel dimension two, without a
new coefficient, target equation, Holst phase or fitted term.  Keep the literal
evaluated full source-perfect Hessian and lower-order crossing form OPEN unless
they are present in the pinned artifacts.

## Claim ceiling

This gate can close parity-balanced physical characteristics and show that the
raw-block imbalance is not inherited by the physical principal system.  It
cannot turn the discarded raw block into a valid parent or prove global
post-caustic continuation, the full evaluated perfect Hessian, infinite-depth
quantum measure or empirical gravity.

