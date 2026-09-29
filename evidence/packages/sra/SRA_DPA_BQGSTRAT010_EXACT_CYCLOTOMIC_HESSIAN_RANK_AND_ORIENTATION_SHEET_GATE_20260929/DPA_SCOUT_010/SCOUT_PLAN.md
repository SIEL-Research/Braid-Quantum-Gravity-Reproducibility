# DPA-SCOUT-BQGSTRAT-010 plan

## Fixed object

- Source revision: `77d919f8f1148161eae9abcda782bc3ae7ef79f8`.
- Field: exact cyclotomic field `Q(zeta_5)` with `zeta_5^4+zeta_5^3+zeta_5^2+zeta_5+1=0`.
- Symbol: the conditional vacuum affine-plaquette Hessian constructed in `BQGSTRAT-009`.
- Sector set: all `5^4=625` momentum digits.

## Noncompensating gates

1. Reproduce the 80-coordinate symbol from the declared coframe and four GL4 link matrices.
2. Compute rank by exact Gaussian elimination over `Q(zeta_5)`; floating rank is not a decision input.
3. Cover all 625 sectors using only the exact spatial-permutation and cyclotomic-Galois orbit action.
4. Isolate every rank-loss orbit and its kernel dimension.
5. Probe the transverse crossing on each nonzero exceptional orbit without fitting.
6. Reject unconditional physical-component selection if opposite orientation sheets do not carry the same two-polarization corank.

## Claim ceiling

This scout classifies one explicit conditional affine-plaquette vacuum Hessian. It does not prove that this one-sided raw assembly is the unique source action, close the matter-coupled Hessian, derive Braid necessity, or establish global singular continuation.
