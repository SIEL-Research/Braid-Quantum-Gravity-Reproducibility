# BQGBH-035 scouting plan

## Gate

`BQGBH-035_SOURCE_RELATIVE_ENTROPY_PRODUCTION_TO_NEGATIVE_PALATINI_GRADIENT_GATE`

## North-star question

Does the source-fixed active-screen/fixed-tail split place the radial source
current entirely in the positive Dirichlet eigenmode of the complete reduced
Palatini kernel, so that the already derived response-exact Bregman rule fixes
the negative reaction sign and unit coefficient without choosing a raw/Petz
branch or consulting a target metric equation?

## Frozen hypothesis

On one radial edge write

`r=Delta R`, `y=Delta Y`, `a=Delta rho`, with `Y=RF`.

The BQGBH-031 pure edge kernel, after removing the common positive factor
`C/h`, is

`k(r,y)=2 r y`.

Its matrix is `H=[[0,1],[1,0]]`.  The fixed right-tail mass and active screen
give the source reference displacement `p=a(1,1)`, because

`Delta(rho-r_h)=Delta rho`.

Thus `p` lies in the positive eigenspace of `H`, while the negative eigenspace
`(1,-1)` is not shifted.  Apply the BGCE254 response-exact/diagonal-zero
Bregman rule to the already fixed Palatini kernel on the actual reflected
source edge:

`B_k(x,p)=k(x)-k(p)-dk_p(x-p)`.

The claim passes only if this is exactly the BQGBH-032 relative kernel and its
cross term supplies the BQGBH-033 negative current with coefficient one.

## Noncompensating gates

1. All input hashes match.
2. The source fixed-tail/active-screen tangent is exactly `(1,1)`.
3. `(1,1)` and `(1,-1)` are respectively the positive and negative Palatini
   eigenmodes, and the source shifts only the positive mode.
4. The response-exact Bregman primitive is exactly `2(r-a)(y-a)`.
5. Its interaction part is exactly `-2a(r+y)+2a^2`, matching BQGBH-032.
6. Its Euler interaction covector is the exact negative of the BQGBH-033
   source current in both `R` and `Y` equations on arbitrary nonuniform edges.
7. The coefficient is inherited from the already fixed pure kernel; no scan,
   fit, target Einstein tensor or branch-order reversal is allowed.

## Decision rule

- `CLOSED_SCOPED` if all seven gates pass.
- `SCOPED NO-GO` if the source shift has a negative-mode component, the
  Bregman primitive differs from BQGBH-032, or a free sign/coefficient remains.

## Counter-intuition scan

The full Palatini quadratic form is indefinite, so it cannot be called an
entropy on the entire `(R,Y)` plane.  The claim is narrower: the actual source
screen displacement is confined to its positive one-dimensional eigenmode.
The untouched negative mode remains the conservative gravitational mode.

## Stopping rule

One exact two-by-two inertia calculation and one symbolic Bregman expansion.
No numerical scan or evolution.

## Claim ceiling

At most close the physical negative sign and unit coefficient of the
source-relative interaction in the complete static spherical reduced
six-face Palatini class.  No full nonspherical nonlinear action, collapse,
evaporation, thermodynamics or empirical black-hole claim.
