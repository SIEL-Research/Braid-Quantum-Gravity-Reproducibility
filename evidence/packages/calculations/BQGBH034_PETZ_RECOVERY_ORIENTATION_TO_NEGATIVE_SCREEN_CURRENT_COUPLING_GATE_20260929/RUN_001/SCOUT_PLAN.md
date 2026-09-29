# BQGBH-034 scouting plan

## Gate

`BQGBH-034_PETZ_RECOVERY_ORIENTATION_TO_NEGATIVE_SCREEN_CURRENT_COUPLING_GATE`

## North-star question

Do the already derived Petz/KMS adjoint, source-canonical time reversal and
reflected in/out walk uniquely orient the BGCE348 branch contrast as
`Petz-minus-raw=-D`, thereby supplying the negative radial reaction required by
BQGBH-032/033 without changing a coefficient or branch convention after the
required answer is known?

## Frozen hypothesis

BGCE348 supplies the exact conditional tangents

`dot F_raw=+D/2`, `dot F_Petz=-D/2`.

The candidate claim is stronger than the existence of the negative tangent. It
requires an existing source rule to select the ordered physical response

`response := Petz-minus-raw = -D`.

The proposed selectors are tested separately:

1. Petz/KMS adjointness or recovery direction;
2. the antiunitary time reversal `Theta`;
3. reflected in/out orientation of the source walk;
4. the prior-summed physical instrument.

## Noncompensating gates

1. All input hashes match.
2. Petz/KMS adjointness must define a directed physical response, not merely an
   adjoint paired with the raw map.
3. `Theta` must exchange or orient the raw/Petz record in the required order;
   invariance of the channel and reversal of modular time alone are
   insufficient.
4. The in/out reflection must type the KMS record; a separate reversible `Z2`
   cannot select its sign.
5. The prior-summed instrument must retain the negative first variation rather
   than cancel it.
6. No reversal of the frozen BGCE348 contrast convention is allowed unless one
   of gates 2--5 forces it.

## Decision rule

- `PASS` only if an existing source identity uniquely selects `-D` as the
  physical radial reaction.
- `SCOPED NO-GO` if all proposed selectors are reversible, separately typed,
  or give zero after physical averaging.
- A NO-GO excludes only this Petz/time-reversal orientation route. It does not
  exclude an irreversible source entropy-production or negative-gradient law.

## Counter-intuition scan

Calling a map "recovery" can suggest a causal arrow, but the finite formula in
BGCE341 is a KMS adjoint. Adjointness fixes a partner relative to a state; it
does not by itself state which ordered difference acts back on the radial
geometry. A physically meaningful minus sign must survive the source typing
and instrument prior.

## Stopping rule

Use the exact sign table and declared source identities only. No parameter
scan, continuum simulation or target Einstein equation.

## Claim ceiling

At most derive, or exclude within the frozen current grammar, the unique
negative radial branch orientation. No unconditional nonlinear interaction
action, collapse, evaporation, thermodynamics or empirical black-hole claim.
