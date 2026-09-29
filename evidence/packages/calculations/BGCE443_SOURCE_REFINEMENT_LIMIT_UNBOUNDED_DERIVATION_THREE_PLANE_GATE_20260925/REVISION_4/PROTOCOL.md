# BGCE443 Revision 4 exact-constructor prospective protocol

Status: `AWAITING_INDEPENDENT_E0_REVIEW`

Revision 4 retains the R3 source-typing correction but replaces every flag-fed semantic witness by
an explicit operator constructor. No actual BGCE443 focal evaluator exists and no focal value has
been accessed.

## Actual focal construction, frozen but unimplemented

- Ordered seeds: `h_a=i[G1,P_chi_a]`, `a=1,2,3`, typed by the exact BGCE075 ordered map to
  `(g01,g02,g03)` and BGCE117 all-stage transport.
- Order `n` windows: every `x in {0,...,n-3}` exactly once.
- Signed transport: OCBFH014 actual signed Braid action, using the lexicographically first shortest
  adjacent-generator word and verifying equality over all reduced words enumerated by its relation
  engine.
- Implementer: `P_a^(n)=sum_x tau_x(h_a)` with coefficient one.
- Compatibility: eventual stabilization on `A_m` for `n>=m+2`, not full-algebra adjacent-order
  intertwining.
- Growth: exact overlap covariances and the frozen variance identity, with positive all-order slope.
- Rank: exact rank three of stabilized derivation rows on the ordered base-cell matrix-unit core.
- Bounded-inner exclusion: construct norm-one local observables whose action norm has an exact
  unbounded lower bound. Implementer norm growth alone is insufficient.
- Closability: instantiate every hypothesis in `CLOSABILITY_THEOREM.md`.

## Exact unsigned comparator

For the same canonical adjacent word, replace each actual signed Braid generator on adjacent
five-dimensional tensor factors by the canonical unsigned tensor-factor swap. Preserve matrix
dimension, window set, seed matrices, seed spectra/norms and word set. Run both transports through
the same endpoint code and retain raw action hashes and differences.

Carrier existence and transport specificity are separate decisions. If both actual and unsigned
transport pass the carrier endpoints without a frozen raw difference, report
`SCOPED_PASS_SOURCE_SEEDED_GENERIC_REFINEMENT / NO_GO_BRAID_TRANSPORT_SPECIFICITY`.

## Non-focal semantic witness

`exact_witness_constructor.py` starts from explicit Pauli matrices, constructs finite implementers,
commutators and controls, and computes rather than accepts:

1. eventual stabilization residuals;
2. normalized-trace variance growth;
3. a nonzero exact minor for three derivation rows;
4. norm-one observables with linear action-norm growth;
5. a bounded telescoping interaction negative;
6. a non-self-adjoint star-derivation/closability-hypothesis negative;
7. signed and unsigned transports with matching invariants, carrier PASS on both sides, and a
   nonzero raw-action difference; and
8. a single-direction rank-one control.

No endpoint residual, growth slope, rank, closability flag or comparator decision is an input to
the constructor. The frozen `WITNESS_RESULT.json` must equal a fresh replay byte-for-byte.

## Source access and retention

`access_guard.py` rejects absolute paths, traversal, symlinks, non-allowlisted paths, denylisted
R1/R2 artifacts and hash mismatch before reading bytes. Its negative tests are mandatory.

The later focal evaluator may read only `INPUT_ALLOWLIST.json` through that guard. Raw output must
conform to `RETENTION_SCHEMA.json`; aggregates alone cannot support a decision.

## Noncompensation and stop rule

Source fidelity, stabilization, growth, rank, action-growth bounded-inner exclusion and closability
are noncompensating. The unsigned comparator cannot be forced to fail. No focal evaluator may be
created or run before a revision-matched independent E0 PASS.

Even a later focal PASS establishes at most a source-seeded refinement-limit derivation carrier at
the declared scope. BGCE386 soldering, moment maps, clock-spatial closure, first-class gravity,
diffeomorphism gravity, empirical gravity, RPD adoption and Official SIEL adoption remain separate.
