# BGCE443 Revision 7 actual-source focal E0 request

Status: `AWAITING_INDEPENDENT_E0_REVIEW`

Bind review to the exact commit containing this directory. Do not run `evaluate.py` and do not
create or inspect `RESULT.json` or `RAW_OUTPUT.json`. Confirm prospectively:

1. only the hash-bound actual-source snapshot and R6 E0 record are readable through the guard;
2. all eight sectors and all 24 ordered `h_a=i[G1,P_chi_a]` matrices come from the frozen snapshot;
3. canonical tensor refinement and signed Braid support transport are explicitly separated rather
   than silently identified;
4. the exact product-state energy-density gap proves an all-`n` spectral-diameter/derivation-norm
   lower bound without finite-sample extrapolation or coefficient fitting;
5. rank three is computed from exact retained matrices through the same function in every sector;
6. self-adjoint finite-range local terms, uniform local bounds and canonical stabilization meet the
   declared closability bridge;
7. signed and unsigned support transports use the same `[2,1,0]` word and specificity is decided by
   a retained raw commutator-action witness, not implementer difference alone;
8. generic carrier and Braid specificity cannot compensate for one another;
9. raw output is sufficient to reconstruct every sector/direction decision; and
10. no focal result has been accessed.

Missing or failed E0 blocks execution. A PASS authorizes exactly one run of this frozen evaluator.
