# DPA-SCOUT-BQGCAL-009-X1 plan

## Question

Does the source-canonical pointed conditional expectation of `H_E^2`, after subtracting the identity-sector vacuum value, yield a positive additive Casimir exactly proportional to the integer event number and hence to the refinement-invariant area label?

## Pinned source

- Commit: `b1db38f07a60ea7e3cf925e1f540f6f4599546d8`
- Snapshot: `DPA-SNAPSHOT-b1db38f07a60`
- Inputs: `INPUT_MANIFEST.json`

## Endpoints

1. Reconstruct `H_E` exactly in `Q(sqrt(3))`.
2. Compute `H_E^2` and the trace-preserving pointed expectation onto `span{P_e,P_non}`.
3. Subtract the identity-sector baseline selected before inspecting the nonidentity coefficient.
4. Require exact positivity and operator proportionality to `N_1`.
5. Lift additively to the tail and compose only algebraically with the BQGCAL-007 area law.

No target data, coefficient fitting, scan or long computation.

## Command

`python3 -B evaluate_scout.py`

## Claim ceiling

Quadratic excitation-Casimir/count/area algebra only; physical quasi-local mass and absolute calibration remain open.
