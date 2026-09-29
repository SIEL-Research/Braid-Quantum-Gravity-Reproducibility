# DPA-SCOUT-BGCE443-001 append-only iteration ledger

## Attempt 0001 — retained pre-policy ad-hoc algebra probe

- Input: the same R7 source snapshot.
- Code path: imported R7 helper functions and called `exact_rank` without invoking R7 `main()`.
- Outcome: `FAILED_IMPLEMENTATION` before a scientific result.
- First divergence: `exact_rank` flattened a 3-by-15625 array and reused flattened indices as column
  indices, raising `IndexError: index 16145 is out of bounds for axis 0 with size 15625`.
- Result/raw artifact: none.
- Consequence: R7 remains unexecuted. Attempt 0002 replaces rank with sparse exact Gaussian
  elimination and uses a new scout identity; this is result-informed debugging only at the crash
  boundary, not an inspected scientific endpoint.

## Attempt 0002 — frozen exact scout

- Evaluator: `evaluate_scout.py` (hash recorded in `SCOUT_FREEZE.json`).
- Change: correct sparse exact rank; direct matrix-unit commutator witness avoids brute-force 625
  dense matrix multiplications per candidate observable.
- Input and decision gates: fixed in `SCOUT_PLAN.md` and `SCOUT_FREEZE.json` before execution.
- Outcome: `OPEN`; evaluator exited normally.
- Result SHA-256: `b5c326d21b6e3066a2d4ad2572a81bf2a27af8eae6a09478a1379469f1530804`.
- Raw SHA-256: `eded02d256a2566e129479b7a7f428cb1f744211cfc4439f8e8d2799bc2e2809`.
- Passed: all eight signed relation checks, rank three in all eight sectors, exact matrix Jacobi in
  all eight sectors.
- Failed: the homogeneous family `v tensor v tensor v` had zero energy gap in all 24 directions;
  same-word signed and unsigned support transport induced identical actions in all 24 directions.
- Interpretation: the first null is a symmetry-induced non-discriminating witness family, not a
  no-go for unboundedness. The second null is consistent with covariant support transport and does
  not test whether signed sectors change the local generator relative to unsigned mask zero.

## Attempt 0003 — source-entry product witness and sector comparator

- Result-informed changes disclosed before execution:
  1. construct a non-homogeneous product-state witness from the first exact nonzero matrix entry and
     frozen phase order `(+1,-1,+i,-i)`; complex conjugation supplies the opposite energy;
  2. test Braid specificity by raw local-generator action against unsigned sector `mask=0` for each
     of the seven nonzero masks, rather than treating transport covariance as a specificity failure.
- Unchanged: source snapshot, all-eight relation gate, exact rank-three gate, all-`n` expectation-gap
  theorem, exact Jacobi gate and claim ceiling.
- Outcome: `CLOSED_SCOPED`.
- Result SHA-256: `4e1dc270df54cc9d9ba7edb0095d8dac6292302879baab87c4883dc821f85a76`.
- Raw SHA-256: `dd9cfb3e55f4053d697e33e518dce3659a3e04a818557d23ab9f278d47bfed46`.
- All five noncompensating gates passed: eight relation checks, eight rank-three checks, 24
  constructive positive gaps, 21 signed-sector raw-action witnesses against unsigned mask zero,
  and eight exact Jacobi checks.
- Every constructive local gap equals `2/3`, giving the all-order lower bound
  `(2/3)(n-2)` for every integer `n>=3`.
