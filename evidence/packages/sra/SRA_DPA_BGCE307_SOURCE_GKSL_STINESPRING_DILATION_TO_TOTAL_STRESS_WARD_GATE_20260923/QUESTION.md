# BGCE307 preregistered question

## Decision question

Can the actual six-element pointed-Braid Reynolds semigroup be lifted to a
source-labelled unitary system-environment dynamics whose **total** conserved
stress/Ward current closes the missing BGCE306 finite-backreaction bridge?

## Frozen tests

1. Construct the exact group-register Stinespring dilation of
   `T_t=q I+(1-q)E`, using the six actual Braid unitaries and the source crossing
   `q=1/4` as an exact rational witness.
2. Decide whether this fixed-time dilation is a single autonomous finite-
   environment unitary realization of the full relaxing semigroup for every
   `t>=0`.
3. Test exact conservation of the source clock observable `G1` under the
   Reynolds adjoint generator in all eight actual sectors.
4. Require a source-derived environment Hamiltonian/stress and a total Ward
   identity before declaring finite Einstein backreaction.

## Pass / fail rule

- **Full pass:** one source-selected autonomous dilation supplies total
  stress/Ward conservation and reproduces the complete semigroup.
- **Split pass:** exact source-labelled fixed-time dilation exists, but the
  autonomous environment or total stress/Ward law is absent.
- **Fail:** even the exact finite-time channel lacks a source-labelled unitary
  dilation.

## Runtime

Short exact integer/rational operator checks; no parameter scan.

