# BQGBH-036 scouting plan

## Gate

`BQGBH-036_GLOBAL_LOG_BRANCH_AND_MAXIMAL_EXTENSION_FROM_THE_SELECTED_STATIC_SPHERICAL_FINITE_ACTION_GATE`

## North-star question

Does the BQGBH-031/035 selected finite static spherical six-face action produce
a globally regular two-ended black-bounce geometry with a horizon-complete
analytic atlas?  Is a global matrix-logarithm branch actually required once
the Palatini connection, rather than the holonomy logarithm, is treated as the
primary field?

## Frozen construction

Use the action-selected solution

`R(X)=sqrt(X^2+ell_star^2)`, `Y=R-r_h`, `F=Y/R=1-r_h/R`

on the bi-infinite reflected source line `X in R`.

The primary horizon-regular charts are

`g_in=-F dv^2+2 dv dX+R^2 dOmega^2`,

`g_out=-F du^2-2 du dX+R^2 dOmega^2`.

For every simple horizon `X_s`, introduce a local Kruskal patch from
`dr_star/dX=1/F` and signed `kappa_s=F'(X_s)/2`.

For the finite Cartan sector use the BQGBH-031 connection-first equations

`v_e=Delta R_e/h_e`, `U_e=-Delta Y_e/h_e`,

fix the Lorentz gauge zero mode locally, and form holonomies by ordered
exponentiation.  Do not recover a connection by taking matrix logarithms.

## Noncompensating gates

1. All input hashes match.
2. The selected finite Euler solution holds on every edge of an arbitrary
   nonuniform bi-infinite source chain.
3. `R>=ell_star`, both `X -> +/- infinity` ends are asymptotically flat, and
   all curvature building blocks remain finite.
4. The no-horizon, degenerate-horizon and two-simple-horizon regimes are
   classified without fitted thresholds.
5. The single ingoing EF chart is adversarially checked using both radial null
   families; any finite-affine endpoint at `v=infinity` must be reported.
6. Outgoing EF and local Kruskal patches must extend every such endpoint with
   a smooth nondegenerate metric coefficient.
7. The throat is an interior regular surface, not a chart boundary.
8. The connection-first action must define every finite edge holonomy without
   a matrix-log branch; reverse-edge inversion and refinement-by-composition
   must remain available.

## Decision rule

- `CLOSED_SCOPED` for the source-maximal horizon-complete static spherical
  atlas if gates 1--8 pass.
- Preserve separately whether one EF chart alone is complete.
- Do not claim absolute uniqueness or global analytic inextendibility unless
  the audit proves them; a horizon-complete universal analytic development is
  a narrower claim.

## Counter-intuition scan

Smooth metric coefficients in one EF chart do not imply that every geodesic
has finite coordinates there.  Conversely, a divergent EF coordinate at a
regular horizon is not a physical singularity if a source-compatible chart
extends the geodesic.  A global logarithm of all Lorentz holonomies is also not
needed in a connection-first Palatini formulation.

## Stopping rule

Exact horizon roots, one null-geodesic witness, local series at each horizon,
and the bounded connection equations.  No long integration or parameter scan.

## Claim ceiling

At most establish the horizon-complete, two-ended, causally extendible static
spherical analytic development selected by the finite action and remove the
matrix-log obligation in that sector.  No dynamical collapse, evaporation,
thermodynamics, rotation, charge, arbitrary nonspherical maximality or
empirical black-hole claim.
