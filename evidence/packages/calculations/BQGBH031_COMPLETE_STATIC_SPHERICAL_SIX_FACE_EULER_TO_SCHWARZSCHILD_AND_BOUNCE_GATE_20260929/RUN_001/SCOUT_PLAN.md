# BQGBH-031 scouting plan

## Gate

`BQGBH-031_ACTUAL_CONNECTION_REDUCED_RADIAL_PALATINI_EULER_AND_BLACK_BOUNCE_GATE`

## North-star question

After all static spherical connection components and Lorentz gauge zero modes
are treated, what finite Euler family is selected by the actual complete
six-face Palatini action? Does it include the source regular black-bounce, or
only the vacuum Schwarzschild branch?

## Frozen exact test

1. Compute the remaining time--radial, time--tangent and intrinsic-screen
   contractions from the BQGBH-027 EF coframe.
2. Combine them with BQGBH-030's radial--tangent null block.
3. Use the exact edge midpoint identity
   `Delta J = 2 Rbar Delta R` to quotient the Lorentz connection zero mode.
4. Eliminate the non-gauge connection pair and derive the complete static
   spherical reduced edge action.
5. Derive its finite Euler equations in natural variables `R,Y=RF`.
6. Test the entire affine Schwarzschild family and the BQGBH-005 regular
   bounce throat without a target fit.

## Decision rule

- PASS Schwarzschild if both finite Euler divergences vanish identically on
  arbitrary nonuniform source edges for affine `R` and `Y`.
- PASS regular bounce only if the exact throat slopes of
  `R^2=X^2+ell_star^2` satisfy the same source-free Euler equation.
- If Schwarzschild passes and the bounce fails, record a split result and
  require a separately source-derived interaction stress. Do not alter the
  pure action after inspecting the defect.

## Counter-intuition scan

Ordinary spherical vacuum Palatini gravity is expected to select the
Schwarzschild family and reject a smooth bounce without matter. Such a split
is a consistency result, not Braid-specific singularity resolution. The
pointed source becomes decisive only if it supplies the missing interaction
from its own finite collision structure.

## Claim ceiling

The gate may derive an exact finite static spherical vacuum black-hole family
and a pure-action bounce NO-GO. It does not yet derive the required interior
stress, global regular black hole, collapse, evaporation, thermodynamics or
empirical gravity.
