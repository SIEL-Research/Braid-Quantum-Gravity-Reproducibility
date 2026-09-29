# DPA-SCOUT-BGCE443-001 attempt 0003 amendment

Status: `FROZEN_BEFORE_OUTCOME`

Attempt 0002 established exact rank three and Jacobi but showed that its two witness endpoints were
mis-specified. This amendment preserves that result and changes only the two failed witnesses.

## Product-state witness

For each nonzero real antisymmetric commutator numerator `C`, scan its nonzero upper-triangle matrix
entries in lexical order. Decode the two basis triples, place the frozen phases
`(+1,-1,+i,-i)` on differing local factors, and retain the first product state with nonzero exact
expectation of `iC/24`. Its complex conjugate has the opposite energy. The two expectations prove a
strict local gap and hence the all-`n` lower bound `(n-2) Delta` without coefficient fitting or
finite-size extrapolation. Failure to find a witness is `OPEN`, not `NO-GO`.

## Braid specificity witness

Sector `mask=0` is the unsigned reference. For each of the seven nonzero signed masks and all three
directions, compare the raw local commutator action against the matching mask-zero direction. Retain
the first matrix-unit action witness. The attempt-0002 equality under same-word support transport is
retained as a covariance observation, not used as the specificity endpoint.

All five noncompensating gates and the claim ceiling from `SCOUT_PLAN.md` otherwise remain fixed.
