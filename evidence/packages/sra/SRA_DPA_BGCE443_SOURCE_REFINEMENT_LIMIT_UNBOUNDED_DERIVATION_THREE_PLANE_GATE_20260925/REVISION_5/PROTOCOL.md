# BGCE443 Revision 5 common-endpoint prospective protocol

Status: `AWAITING_INDEPENDENT_E0_REVIEW`

Revision 5 preserves the R3 source typing and the R4 explicit-operator requirement, while repairing
the four defects identified by the R4 independent E0 audit. No actual BGCE443 focal evaluator
exists and no focal value has been accessed.

## Actual focal construction, frozen but unimplemented

- Ordered seeds are `h_a=i[G1,P_chi_a]`, `a=1,2,3`, typed by the exact BGCE075 ordered map to
  `(g01,g02,g03)` and BGCE117 all-stage transport.
- Order `n` contains every range-three window `x in {0,...,n-3}` exactly once, with coefficient one.
- Signed transport is the OCBFH014 actual signed Braid action. The focal evaluator must use the
  lexicographically first shortest adjacent-generator word and verify word independence with the
  existing relation engine.
- `P_a^(n)=sum_x tau_x(h_a)`.
- Compatibility means eventual stabilization on each fixed local algebra `A_m` for `n>=m+2`.
- Rank is computed by one general exact-minor routine for ranks zero through three. No control may
  bypass that routine.
- Bounded-inner exclusion uses norm-one observables and exact action-norm lower bounds. Implementer
  norm growth alone is not an endpoint.
- Closability instantiates the hypotheses in `CLOSABILITY_THEOREM.md`; a prose label is never a
  truth input.

## Exact unsigned comparator

The comparator replaces each actual signed adjacent Braid implementer by the canonical unsigned
tensor swap while preserving the adjacent word, matrix dimension, windows and ordered seeds. It
constructs both matrices and retains the commutator action of each on the same frozen matrix-unit
basis. Implementer difference is not accepted as an action difference.

Generic carrier existence and Braid-transport specificity are separate decisions. The unsigned
side is allowed to pass. If both sides pass the carrier endpoints but raw actions are identical,
transport specificity is `NO_GO`; it may not be forced to pass.

## Non-focal Revision 5 witness

`exact_witness_constructor.py` constructs Pauli operators, finite implementers, canonical signed
and unsigned adjacent swaps, raw commutator actions and controls. The same functions compute:

1. rank-three positive, rank-two, rank-one and rank-zero cases;
2. eventual stabilization and normalized-trace variance growth;
3. exact linear action growth for three positive directions;
4. a telescoping bounded negative through the same action-growth classifier;
5. positive, bounded-positive and non-self-adjoint negative closability endpoints; and
6. signed/unsigned relation certificates, carrier decisions and 16 retained raw-action rows per
   transport.

The frozen witness must equal a fresh replay byte-for-byte. `validate_retention.py` independently
checks typed row variants, cardinalities, exact residuals, hash formats and decision reconstruction.

## Source access and stop rule

The later focal evaluator may read only the six hash-bound paths in `INPUT_ALLOWLIST.json` through
`access_guard.py`. The guard must reject denylisted prior outcomes, traversal, absolute paths,
symlinks, unlisted paths and hash mismatch before returning bytes.

Source fidelity, stabilization, growth, rank, bounded-inner exclusion, closability and retention
are noncompensating. No focal evaluator may be created or run before a revision-matched independent
E0 PASS.

A later focal PASS would establish only a source-seeded refinement-limit derivation carrier at the
declared scope. It would not establish first-class constraints, diffeomorphism gravity, empirical
gravity, RPD adoption or Official SIEL adoption.
