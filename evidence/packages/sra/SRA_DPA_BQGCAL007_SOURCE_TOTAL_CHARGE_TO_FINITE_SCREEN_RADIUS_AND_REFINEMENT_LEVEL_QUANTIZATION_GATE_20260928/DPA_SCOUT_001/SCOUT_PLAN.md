# DPA-SCOUT-BQGCAL-007-X1 plan

## Parent question

Can the existing source total Ward/energy charge select a finite Braid-screen radius and one refinement level, without target data or an external gravity scale?

## Pinned source

- Commit: `21f08ae4fdcc8ee92794ad2ce00b9f34a28e5e3d`
- Snapshot: `DPA-SNAPSHOT-21f08ae4fdcc`
- Hash-bound inputs: `INPUT_MANIFEST.json`

## Bold hypothesis

The physical horizon is not one elementary cell at level `m`. The full screen contains `N_m=K 25^m` descendants, so `m` is a resolution coordinate and the physical area is refinement invariant. A distinct positive additive count `K`, if source-derived, would quantize area and radius.

## Ordinary alternative

This is standard discretization invariance. The current total charge supplies neither a positive count operator nor a physical energy-area relation, so no black-hole quantum number has yet been derived.

## Endpoints and stopping rule

1. Verify that the existing total charge is transported through every refinement and therefore has no `m` dependence.
2. Prove that an `m`-blind charge functional cannot select exactly one positive radius from `r_m=ell_star 5^{-m}`.
3. Verify exact 25-child area conservation and derive `A_total(K,m)=K A_0` and `r_K=sqrt(K) ell_star`.
4. Decide whether the existing charge is already a positive integer screen-count operator.

Stop after these exact algebraic endpoints. No numerical search, measured `G`, mass data or long computation is permitted.

## Command and retained artifacts

`python3 -B evaluate_scout.py`

Retain manifest, evaluator, raw output, result, certificate, status, execution log, iteration ledger, verifier and report.

## Claim ceiling

The scout may decide only the existing-charge-to-unique-level route and the refinement-invariant composite-screen law. Absolute calibration and physical black-hole quantization remain outside scope.
