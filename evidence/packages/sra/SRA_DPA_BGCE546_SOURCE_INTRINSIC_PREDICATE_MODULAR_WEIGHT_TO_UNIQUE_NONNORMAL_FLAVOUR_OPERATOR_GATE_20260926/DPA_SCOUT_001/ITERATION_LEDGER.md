# BGCE546 iteration ledger

| Attempt | Code/configuration | Inputs inspected | Result | Next change | Change class |
|---|---|---|---|---|---|
| `001-FROZEN` | `evaluate_scout.py` as frozen before first run | Commit-pinned BGCE416/433/509/530/532/544 records | Not run | Execute once and retain exact output | Initial frozen bold-hypothesis scout |
| `001-ATTEMPT-1` | Frozen evaluator SHA before repair | No scientific output inspected | `FAILED_IMPLEMENTATION`: Python rejected an unparenthesized generator in the matrix-product helper before input verification or endpoint calculation | Parenthesize the generator; no hypothesis, endpoint, input or threshold change | Syntax-only defect repair |
| `001-REPAIRED` | Matrix-product helper syntax repaired | Same pinned records | Not run | Execute repaired evaluator once | Implementation repair only |
| `001-ATTEMPT-2` | Repaired evaluator; scientific design unchanged | Same pinned records | PASS: selector rank `3`, normality-commutator rank `3`, positive full-rank mass operator and strictly positive cubic discriminant | Stop and report; calculate unfitted singular-value ratios at BGCE548 | Outcome run, no hypothesis change |
