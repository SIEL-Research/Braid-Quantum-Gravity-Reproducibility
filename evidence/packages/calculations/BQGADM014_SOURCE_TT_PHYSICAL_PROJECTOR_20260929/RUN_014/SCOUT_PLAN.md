# PUBLIC-RUN-BQGADM-014 — source-axis physical projector gate

## Parent question

Can the missing finite physical projector from the BQGADM-012 four-dimensional
physical phase quotient to the BQGEULER-004 two-polarization carrier be
constructed directly from the existing source spatial coframe, Palatini
symplectic form and rank-four constraint symbols, without importing a target
Einstein/Fierz-Pauli action, choosing a gauge by hand, fitting a coefficient or
adding a BKM law?

## Pinned source

- Repository: `SIEL-Research/Braid-Quantum-Gravity-Reproducibility`
- Commit: `65c5c4f9e7084357d228b3014f189623cc4c1540`
- public calculation snapshot: `PUBLIC-SNAPSHOT-65c5c4f9e708`
- Reservoir SHA-256:
  `150757e2372bb50c2689248faabd4900a76e631b603fe65a6cfb5ca75833a8f4`

Every scientific input is read with `git show` from that commit and checked
against `SOURCE_MATRIX.json` before the endpoint is inspected.

## Bold hypothesis

The source-selected flat spatial coframe and each of its three nonzero
incidence axes already determine a unique transverse-tracefree projector on
the six symmetric spatial metric coordinates. Applying that same projector to
the conjugate six momentum coordinates gives a rank-four phase projector. It
annihilates all four Hamiltonian gauge directions, lands in the four-constraint
surface, is symplectic on its image, and commutes exactly with source
refinement because it acts only on the internal tensor factor.

This changes the mechanism class from a manually supplied physical basis or a
new BKM horizontal law to a source-canonical coisotropic reduction built from
objects already derived by BQGADM-006.

## Strongest ordinary alternative

The familiar TT projector may merely be a convenient continuum gauge choice.
Dimension two and helicity counting do not prove that it is selected by the
finite Braid source, that it kills the actual Palatini gauge distribution, or
that it intertwines refinement. A projector passing only the standard
continuum formula but failing any one of those exact finite tests is rejected.

## Noncompensating endpoints

For each of the three source-selected nonzero axes:

1. the six-coordinate TT map is idempotent and has rank two;
2. the twelve-coordinate phase map is idempotent and has rank four;
3. the four BQGADM-006 constraint rows annihilate the projected phase;
4. the projector annihilates the four Hamiltonian gauge vectors computed from
   the actual pulled-back Palatini symplectic form;
5. the constraint symbol is first class at the flat source anchor;
6. the pulled-back symplectic form has rank four on the projector image;
7. the phase projector is self-adjoint with respect to the actual symplectic
   form;
8. its image is exactly the quotient representative: the constraint surface
   is the direct sum of the gauge image and the projector image;
9. the map is the unique orthogonal projector onto the source-axis transverse
   tracefree subspace;
10. tensor-factor separation proves exact commutation with the BQGEULER-004
    child-constant refinement and scalar hierarchical generator.

## Falsifier and stopping rule

Any failed endpoint gives `NO-GO` for the proposed source-axis projector.
Stop without repair if a coefficient, target Einstein/Fierz-Pauli equation,
manual polarization basis, new action or new BKM metric is required. A pass is
limited to the flat-anchor linearized source-axis and hierarchical two-copy
scope. Arbitrary finite momentum directions, a nonlinear moving projector and
off-shell commutation with the full ten-component nonlinear update remain open
unless separately derived.

## Deterministic evaluator

```text
python3 records/BQGADM014_SOURCE_TT_PHYSICAL_PROJECTOR_20260929/RUN_014/evaluate_projector.py
```

Retain the source matrix, exact rational matrices, all endpoint booleans,
machine-readable result, evaluator hash, execution environment and every
attempt.

## Claim ceiling

At most an exact source-derived physical phase projector and refinement/
hierarchical-wave intertwiner on the flat time-gauge anchor for the three
source-selected nonzero spatial axes. No nonlinear moving projector, arbitrary
finite Fourier direction theorem, exact commutation with the nonlinear
BQGEULER-010 update, global/strong-curvature result, empirical gravity,
confirmation, RPD adoption, Level 3 or Official SIEL statement.
