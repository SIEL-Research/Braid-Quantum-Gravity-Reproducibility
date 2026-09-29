# BGCE530 scout plan

- Scout: `PUBLIC-RUN-BGCE530-001`
- Parent: `BQG-G3-R03.7`
- Source commit: `b4aa9f5fa215a0d2c8b048471e53bdec05e240bf`
- Source snapshot: `PUBLIC-SNAPSHOT-b4aa9f5fa215`
- Evidence class: exact `Theoretical derivation`

## North-star fields

- North-star claim: the same finite Braid-derived matter packet supplies both species-dependent normalized Yukawa strengths and a stable nonzero Higgs vacuum without target-mass fitting.
- Closest prior result: BGCE526 derives the common generation operator `Y=abs(X-2I)` with relative spectrum `5:4:2`; BGCE528 proves ordinary Hilbert--Schmidt cycle counting remains species-independent.
- Current missing link: a source-selected nontracial kinetic metric that survives normalization, plus a source-derived finite odd action whose exact determinant changes the zero-vacuum result.
- Directness: `direct`.

## Bold hypothesis after repeated NO-GOs

- Interpretive leap: physical normalization is set by the source-selected compact-central shadow of `omega_can`, not by the tracial Hilbert--Schmidt metric. The derived odd matter parity then permits a finite Gaussian fermion integral whose determinant is the missing sign-changing Higgs contribution.
- New structure and source status:
  - `DERIVED`: BGCE318 `omega_can`, BGCE396 compact-central block weights, BGCE430 typed up/down/lepton cycles, BGCE439 odd matter/even scalar grading, BGCE516 positive quartic, and BGCE526 `Y`.
  - `EXPLICIT BOLD DERIVED-EXTENSION ASSUMPTION`: use the `omega_Z`-weighted GNS norm as the physical fermion/scalar kinetic normalization and use the canonically normalized finite odd Gaussian action. The Braid source has not yet been proved to select this full fermionic functional as its unique matter action.
- New composition rule: normalize every Morita edge with the star-compatible half-density KMS form `||A||^2_(omega,1/2)=Tr(omega_Z^(1/2) A* omega_Z^(1/2) A)`. On `Hom(b,a)` its scalar coefficient is `sqrt(w_a w_b)`, so a closed block cycle `(a,b,c)` has normalized cubic strength squared `1/(w_a w_b w_c)`. Tensor it with BGCE526 `Y`. For the scalar radius `r`, integrate the finite odd quadratic form exactly and add its normalized `-log det(I+r^2 M*M)` to the existing positive quartic.
- Strongest ordinary alternative: the nontracial weights may merely be modular bookkeeping; choosing their GNS form as the physical kinetic action and Grassmann determinant may be an additional matter law, not a Braid-only consequence.
- Counter-intuition: unlike the raw `32:45:60` count, the block-weight products may survive normalization, but a nonzero minimum produced by a standard fermion determinant is only conditional until the finite odd Gaussian parent is derived from the collision action itself.
- Exact falsifier:
  1. FAIL weighted splitting if the three typed cycle products are equal, the typed cycle-to-block map is absent, or compact-central weighting is not positive.
  2. FAIL conditional vacuum if the determinant-corrected radial derivative has no positive root, more than one positive root, or the potential is unbounded below.
  3. Do not call the vacuum unconditional unless the finite odd Gaussian action is already source-selected.
- Minimum decisive test: exact rational block-weight products, exact typed cycle map, and monotonicity proof for the determinant-corrected radial equation; no coefficient scan, fit, observed mass input or long numerical optimization.
- Stopping condition: stop after weighted cycle splitting, metric-compatible Higgs real-structure check, determinant existence/uniqueness/boundedness, and classification of the remaining assumption.
- Claim ceiling: a PASS may establish source-weighted species splitting and a conditional unique nonzero Higgs radius in the declared finite Gaussian derived extension. It cannot establish observed Yukawa values, absolute masses, CKM/PMNS mixing, neutrino content, running, empirical Standard Model physics or completed quantum gravity.

## Condition classes

- A: exact inequality of the three typed `omega_Z`-normalized cycle strengths.
- A: exact existence and uniqueness of a nonzero minimum after the finite odd determinant.
- B: positivity/faithfulness of `omega_Z`, typed cycle identity, boundedness of the total radial potential, and compatibility of the two Higgs routes with a metric-preserving anti-linear involution.
- C: comparison with observed mass ratios. Not executed.
- D: CKM/PMNS mixing and absolute SI calibration. Not part of this scout.

## Protocol deviation disclosure

Before this file was written, a scratch exact-arithmetic command evaluated the three rational weight products and their relative inverse products. The inspected values are preserved as attempt `0000` in `ITERATION_LEDGER.md`. No fit, scan, determinant root or work-package decision was inspected. The formal evaluator and its full endpoints are frozen by this plan before execution.

Before formal execution, the initially written left-GNS expression `Tr(omega_Z A* A)` was replaced by the half-density KMS form above because the left form assigns different norms to `A` and `A*` between unequal-weight blocks. This is a pre-execution definition correction, not a response to an inspected endpoint; it is recorded as attempt `0000a`.

Commands:

```text
python3 records/BGCE530_SOURCE_STATE_WEIGHTED_KINETIC_METRIC_AND_FINITE_FERMION_DETERMINANT_HIGGS_GATE_20260926/RUN_001/evaluate_scout.py
python3 records/BGCE530_SOURCE_STATE_WEIGHTED_KINETIC_METRIC_AND_FINITE_FERMION_DETERMINANT_HIGGS_GATE_20260926/RUN_001/verify.py
```
