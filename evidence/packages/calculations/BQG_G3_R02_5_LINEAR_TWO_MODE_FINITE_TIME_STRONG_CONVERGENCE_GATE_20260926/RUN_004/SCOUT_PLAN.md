# PUBLIC-RUN-BQGEULER-004 — linear two-mode finite-time strong convergence gate

- Parent work package: `BQG-G3-R02.5`
- Evidence class: bounded public calculation exact theoretical scout
- Pinned source commit: `ffbcedd69722e3cc3f46b982652dba500ee01554`
- Scope: flat-anchor linearized two-mode wave dynamics only

## Parent question

Do the refinement-compatible BGCE452/BGCE456 spatial wave operators, after restricting to two configuration modes, converge strongly in the wave-energy norm on every finite time interval? If so, does the present source also identify those two slots with the physical ADM/Fierz–Pauli quotient?

## Bold hypothesis

`PUBLIC_HYPOTHESIS`: exact refinement intertwining and positivity make the two-polarization wave trajectories strongly convergent without an additional numerical limit argument.

## Strongest ordinary alternative

The theorem closes only an abstract two-copy hierarchical wave carrier. The current sources may still lack a refinement-natural physical ADM projector and smooth Fierz–Pauli principal-symbol identification, so the word `physical` may remain unlicensed.

## Exact endpoints

1. Construct the inductive-limit positive operator from the finite hierarchical operators.
2. Prove that the finite wave group is the restriction of the limit wave group.
3. Prove uniform-in-time strong convergence in the mean-zero wave-energy norm.
4. Verify that the argument applies to two passive polarization copies and to the BGCE456 actual-metric form by its exact form bounds.
5. Separately test whether the pinned source supplies a physical-projector refinement intertwiner and smooth Fierz–Pauli generator identity.

The physical claim passes only if all five endpoints pass. A pass of endpoints 1–4 with endpoint 5 open is a scoped hierarchical theorem, not physical ADM convergence.

## Falsifiers and stopping rule

- Any failed input hash, loss of positivity/self-adjointness, failed refinement intertwining, non-dense energy truncation, or nonzero good-intertwiner residual falsifies the hierarchical convergence claim.
- Missing physical-projector/refinement or smooth-symbol identity blocks the physical ADM claim noncompensatingly.
- Stop after one exact symbolic evaluation and validation. Do not tune a projector or insert a continuum Laplacian.

## Evaluator and retained artifacts

- Command: `python3 records/BQG_G3_R02_5_LINEAR_TWO_MODE_FINITE_TIME_STRONG_CONVERGENCE_GATE_20260926/RUN_004/evaluate_scout.py`
- Retain: plan, input manifest, evaluator, raw output, result, validator, iteration ledger, report, status and certificate.

## Claim ceiling

At most an exact strong wave-trajectory convergence theorem for two copies of the pinned hierarchical source-cylinder carrier, plus an explicit boundary on physical ADM/Fierz–Pauli identification. No nonlinear Euler convergence, finite nonlinear HDA, empirical gravity, confirmation, RPD adoption, Level 3 or Official SIEL statement.
