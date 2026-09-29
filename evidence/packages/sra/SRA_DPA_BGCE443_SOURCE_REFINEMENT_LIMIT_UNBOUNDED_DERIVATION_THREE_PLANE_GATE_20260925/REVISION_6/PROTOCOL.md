# BGCE443 Revision 6 all-n and reconstructable-retention protocol

Status: `AWAITING_INDEPENDENT_E0_REVIEW`

Revision 6 is the append-only repair of the R5 independent E0 failure. No focal evaluator exists
and no focal outcome has been accessed.

## Frozen focal target, still unimplemented

The later focal evaluator retains the R5 source target: ordered seeds `h_a=i[G1,P_chi_a]`, all
range-three windows with coefficient one, OCBFH014 signed transport, eventual stabilization on each
fixed local algebra, exact three-row rank, bounded-inner exclusion from action growth, and the
finite-range closability hypotheses in `CLOSABILITY_THEOREM.md`. It must run the same unsigned-swap
comparator and retain source-resolved raw data in all eight sectors.

## R6 all-order witness

For each Pauli seed `h` and unitary partner `k`, the constructor retains the exact 2x2 matrices and
checks `h*=h`, `h^2=I`, `k*k=I`, `{h,k}=0`, and a nonzero `+1` eigenvector `v` of `h`. With
`N=n-2`, it then derives for every integer `n>=3`:

- `P_n v_n = N v_n`;
- `A_n P_n A_n^* = -P_n`;
- `[P_n,A_n]v_n = -2N A_n v_n`; and
- the triangle upper bound is also `2N`.

Thus the action norm is exactly `2(n-2)` for all `n>=3`, not an extrapolation from four samples.
The retained integer polynomials are checked independently by `validate_retention.py`. The bounded
telescoping control has the all-order identity
`sum_(x=0)^(n-2)(h_x-h_(x+1))=h_0-h_(n-1)` and constant action upper bound four.

## Reconstructable retention

Sparse Gaussian-integer matrices retain:

1. every rank derivation row;
2. local seeds, partners and eigenvectors;
3. signed/unsigned adjacent-swap generators;
4. signed/unsigned order-six implementers;
5. all 32 frozen matrix-unit observables and commutator actions; and
6. closability local terms and star-defect matrices.

The validator rebuilds ranks and minors, swap relations, implementers, observables, commutators,
hashes, variance endpoints, all-n action identities, closability predicates and all eight decisions.
`test_retention_mutations.py` must reject altered decisions, false relation certificates, a false
rank determinant, fabricated action hashes, and altered raw action entries even when aggregate
hashes are recomputed.

## Stop rule

Source fidelity, all-n growth, rank, raw reconstruction, closability and access isolation are
noncompensating. No focal evaluator may be created or run before an exact-revision independent E0
PASS. A later focal PASS remains a scoped source-seeded refinement-limit derivation carrier, not a
completed gravitational first-class constraint algebra by itself.
