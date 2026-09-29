# BGCE443 Revision 3 prospective protocol

Status: `AWAITING_INDEPENDENT_E0_REVIEW`

The exact producer revision is the Git commit selected and recorded by the independent E0 reviewer
after this complete directory is committed. The E0 record must bind to that audited commit and to
hashes of every file in this directory. No packet file declares a parent commit as its own revision,
and no self-referential commit hash is required.

## Source-typed construction

For each of the eight actual sectors, use the ordered local Hermitian seeds

`h_a=i[G1,P_chi_a]`, `a=1,2,3`.

Their ordered direction labels are bound to the exact BGCE075 map from
`([G1,P_chi_1],[G1,P_chi_2],[G1,P_chi_3])` to `(g01,g02,g03)` and to BGCE117's
all-stage transport. BGCE386 Hadamard signs are not refinement-position coefficients.

For order `n>=3`, let `X_n={0,...,n-3}` be every consecutive three-strand window in pointed
left-to-right order. `tau_x` is OCBFH014's word-independent transport of the marked base window
to `x`; the implementation must use the lexicographically first shortest adjacent-generator word
and verify equality against every reduced word enumerated by the OCBFH014 relation engine.

Define with the counting measure on `X_n`

`P_a^(n)=sum_{x in X_n} tau_x(h_a)`.

Every coefficient is exactly one. No Hadamard window sign, fitted scale, periodic choice,
`25^r`, manual `3/5`, endpoint normalization or post-outcome basis choice is permitted.

## Algebraic local core and all-order stabilization

The carrier is the pointed UHF inductive system `A_n=M_5(C)^(tensor n)` with
`j_n(A)=A tensor I_5`. The local core is `D=union_{m>=1} A_m`, using lexicographically ordered
matrix units `E_uv^(m)` and explicit support metadata.

For `A in A_m`, only windows with `x<=m-1` can overlap its support. Therefore

`i[P_a^(n),A]` is exactly constant for all `n>=m+2`.

Revision 3 does not require the false stronger statement that finite-volume derivations
intertwine on every full `A_n` at each adjacent order. The primary compatibility endpoint is the
above all-order eventual-stabilization theorem plus exact checks on the frozen finite witness set.

## Noncompensating primary endpoints

1. **Source fidelity:** all inputs match the allowlist; every window is present once; every
   coefficient is one; forbidden artifacts are not opened.
2. **Eventual stabilization:** symbolic support proof gives threshold `n>=m+2`, and all retained
   finite witness rows have zero residual at and after that threshold.
3. **Implementer growth:** with normalized product trace and centered `h_a`, define exact overlap
   covariances `gamma_a(d)=tau(h_a tau_d(h_a))`, `d=0,1,2`. For `n>=5`, verify the exact variance
   identity
   `tau((P_a^(n))^2)=(n-2)gamma_a(0)+2(n-3)gamma_a(1)+2(n-4)gamma_a(2)`.
   PASS requires exact positive slope `C_a=gamma_a(0)+2gamma_a(1)+2gamma_a(2)>0` in every sector.
   Then `||P_a^(n)||>=sqrt(tau((P_a^(n))^2))` proves unbounded growth without fitting.
4. **Spatial rank:** the three stabilized derivation superoperator rows restricted to the complete
   ordered base-cell matrix-unit core have exact rank three in each sector.
5. **Bounded-inner exclusion:** each `P_a^(n)` is Hermitian and trace-centered. Positive unbounded
   variance forces unbounded spectral diameter. The minimum norm of a finite-volume implementer
   modulo scalars is half that diameter, excluding any uniformly bounded compatible implementer.
   The implementation must also retain the exact action-growth witness used by the common harness.
6. **Closability:** cite and instantiate the bounded finite-range interaction theorem on the UHF
   quasi-local algebra, with domain `D`, range three, uniform local bound `||h_a||`, and the
   constructed strongly continuous automorphism group. The source-specific obligations are
   boundedness, self-adjointness and translation covariance of every local term.

Every endpoint must pass independently in all eight sectors. No endpoint can rescue another.

## Controls

- zero-seed negative;
- exact rank-two direction negative;
- bounded-inner negative with zero action-growth certificate;
- nonclosable-domain negative;
- matched non-Braid transport obtained by replacing every signed adjacent Braid action by the
  canonical unsigned tensor-factor swap on the same `M_5^(tensor n)`. It preserves dimension,
  window set, seed spectrum/norm and Coxeter word-independence. Its result is not forced to fail;
- single-direction control, which must report rank one and never three.

All controls and the positive synthetic witness use `witness_harness.py` and the same row schema.
The witness harness tests endpoint discrimination only; it is not the focal source evaluator.

The decision has two nonconflated layers. The six primary endpoints decide existence of a
source-seeded refinement-limit carrier. Braid-transport specificity additionally requires the
actual signed transport to differ on a frozen raw endpoint from the unsigned-swap comparator.
If both pass identically, report at most
`SCOPED_PASS_SOURCE_SEEDED_GENERIC_REFINEMENT / NO_GO_BRAID_TRANSPORT_SPECIFICITY`; never rescue it
as a Braid-specific PASS.

## Retention and isolation

The focal constructor, if later authorized, may read only paths and hashes listed in
`INPUT_ALLOWLIST.json`. It must abort if a requested path matches the denylist. Raw focal output
must follow `RETENTION_SCHEMA.json` and retain per-sector, per-order, per-window, per-basis and
per-control rows before aggregates.

## Stop rule and claim ceiling

No focal evaluator may be created or run before a revision-matched independent E0 PASS. A later
PASS may establish only three source-seeded compatible closable unbounded derivations on this
declared unit-counting refinement carrier. Braid-transport specificity is a separate comparator
decision and may fail while the generic carrier passes. The packet does not establish a BGCE386 solder, cotangent
moment maps, clock-spatial closure, a finite first-class gravity algebra, diffeomorphism gravity,
empirical gravity, RPD adoption or Official SIEL adoption.
