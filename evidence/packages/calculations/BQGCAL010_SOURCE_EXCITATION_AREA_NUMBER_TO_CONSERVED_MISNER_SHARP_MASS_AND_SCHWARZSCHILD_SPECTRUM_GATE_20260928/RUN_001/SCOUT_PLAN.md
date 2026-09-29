# PUBLIC-RUN-BQGCAL-010-X1 plan

## Parent question

Can the source-derived excitation area number be mapped, without fitting or an
imported mass scale, to a conserved quasi-local mass in the already derived
Schwarzschild sector?

## Pinned source

- commit: `fdb714bece98c1dbc9a51d27a384d4315f16d22a`
- snapshot: `PUBLIC-SNAPSHOT-fdb714bece98`

## Bold hypothesis

The additive quantity `K=(45/4) C_exc` is an area number rather than a local
energy.  Its positive square root is a source-canonical boundary observable.
When the already derived source screen is placed at the marginal surface of the
already derived infrared Schwarzschild solution, this boundary observable is
the pullback of the generalized Misner--Sharp charge.

This changes the mechanism class from an additive local Ward-energy
identification to a nonlinear quasi-local boundary charge.  `C_exc`, the
pointing, the screen law, the relative coupling `kappa_B=3/5`, and the infrared
Schwarzschild solution are derived inputs.  Identifying the finite screen with
a physical spherical boundary remains conditional; SI calibration is not
assumed.

## Strongest ordinary alternative

The square-root relation is merely the standard Schwarzschild area--mass law
composed with an internally constructed integer.  Unless the finite count is
independently typed as a physical screen observable, the result is a
consistent pullback, not a Braid-only physical mass derivation.

## Exact endpoint

1. Derive the generalized Misner--Sharp charge from `kappa_B=3/5` and
   `f(r)=1-r_h/r`.
2. Pull it back along `r_h=ell_star sqrt(K)` and
   `K=(45/4) C_exc`.
3. Test fixed-boundary conservation under later fresh-tail collisions.
4. Test whether the resulting mass is additive and therefore identical to the
   finite total Ward charge.
5. Record the SI and physical-screen typing boundary.

## Falsifier and stopping rule

Reject the proposed boundary-mass mechanism if the Misner--Sharp charge is not
constant in the pinned vacuum metric, if the two source pullbacks disagree, if
the fixed emitted-tail algebra is not preserved by later collisions, or if a
fitted coefficient is required.  Stop after exact symbolic identities and a
minimal integer-spectrum witness; do not run a parameter scan.

## Retained raw artifacts

`INPUT_MANIFEST.json`, evaluator, raw output, result, certificate, execution
log, iteration ledger, status, and Japanese report.

## Claim ceiling

This scout may derive a source-normalized, fixed-boundary vacuum-conserved
Misner--Sharp/Schwarzschild mass spectrum by composing pinned source results.
It may not prove that the finite count is the unique physical screen number,
identify the nonlinear boundary mass with the additive total Ward energy,
derive SI mass or Newton's constant, or establish black-hole microphysics,
entropy, Hawking radiation, empirical gravity, or completed quantum gravity.
