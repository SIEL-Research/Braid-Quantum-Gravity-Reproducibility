# BQGBH-032 scouting plan

## Gate

`BQGBH-032_SOURCE_SCREEN_RELATIVE_PALATINI_INTERACTION_TO_REGULAR_BOUNCE_STATIONARITY_GATE`

## North-star question

Can the already source-derived signed screen and fixed-tail mass supply the
interaction variation missing from the complete static spherical six-face
Palatini action, without consulting a target Einstein tensor or fitting a
coefficient?

## Frozen inputs

- BQGBH-004: the actual source right tail separates a conserved fixed mass
  register from the active screen register.
- BQGBH-005: the active screen fixes
  `rho^2=X^2+ell_star^2` with `rho>0`.
- BQGBH-015: the signed screen is source-equivariantly embedded into the
  finite four-coframe and six-face module.
- BQGBH-031: the complete connection-eliminated static spherical action has
  natural variables `R,Y=RF` and edge kernel
  `2 C DeltaR DeltaY/h`.
- BGCE348/349: the raw/Petz branch contrast supplies a source-native local
  interaction variation only in the aligned four-score, block-local class;
  full ten-component nonlinear metric dependence and spatial-gradient
  dynamics are not supplied.
- BGCE371: in its aligned four-score identity-feedback class, the source
  Fisher action selects unit actuation scale and rejects scale two.

## Bold hypothesis fixed before evaluation

The source reference pair on each radial node is

`z_*=(rho, rho-r_h)`.

Use the exact Bregman remainder of the already derived quadratic Palatini
radial kernel about this source point:

`S_rel[z;z_*]=S_g[z]-S_g[z_*]-dS_g[z_*](z-z_*)`.

Because `S_g` is bilinear in the edge increments, this is exactly

`2 C sum_e Delta(R-rho)_e Delta(Y-rho+r_h)_e/h_e`.

The constant fixed-tail mass has zero edge difference, so the test reduces to

`2 C sum_e (DeltaR-Delta rho)(DeltaY-Delta rho)/h_e`.

This is not silently promoted to an unconditional source law.  The
interpretive leap being tested is that physical strong-curvature response is
the Palatini relative action about the typed source screen.  The algebraic
consequences and the absence of a fitted coefficient are tested exactly.

## Noncompensating gates

1. All pinned input hashes match.
2. Direct reuse of BGCE348/349 is rejected unless those records already supply
   full nonlinear radial metric dependence and spatial-gradient dynamics.
3. The Bregman remainder is derived algebraically from the frozen Palatini
   kernel; no coefficient is inserted after inspecting the throat residual.
4. Its finite Euler equations are the slope-divergence equations for
   `R-rho` and `Y-rho+r_h` on an arbitrary nonuniform connected chain.
5. The source pair `R=rho`, `Y=rho-r_h` is stationary at every internal node,
   not only at the three-node throat witness.
6. On the exact throat triplet, the interaction variation cancels the
   BQGBH-031 pure residual `2-2 sqrt(2)` with no fitted scalar.
7. Preserve the existing horizon rank, bounded-curvature and causal-complete
   results only within their previously declared source-metric scope.

## Decision rule

- `SPLIT CONDITIONAL SCOPED PASS / SCOPED NO-GO` if the relative action is
  uniquely fixed in the declared Bregman class and makes the source black
  bounce stationary, while direct BGCE348/349 reuse remains untyped.
- `NO-GO` if the exact Bregman remainder does not cancel the full finite Euler
  defect or requires a coefficient chosen from the answer.
- Do not call this unconditional Braid-only closure unless an existing source
  theorem independently selects the relative-Palatini prescription.

## Counter-intuition scan

For any quadratic action, subtracting its value and first derivative at a
chosen reference makes that reference stationary.  Therefore exact
stationarity alone is not evidence that the source selected this law.  The
scientific gain is narrower: the source supplies the reference pair, the
six-face Palatini kernel supplies the Hessian and normalization, and the
resulting interaction is unique inside the declared relative-action class.
The remaining task is to derive that relative prescription from the actual
branch-odd collision functional or another source theorem.

## Stopping rule

One exact symbolic derivation and the minimal throat witness.  No numerical
scan and no target Einstein/stress access.

## Claim ceiling

At most a coefficient-free, globally stationary regular black-bounce family
conditional on the source-relative Palatini prescription, plus a direct-route
NO-GO for using BGCE348/349 alone.  No unconditional source selection,
collapse, evaporation, thermodynamics, astrophysical identification or
empirical confirmation.
