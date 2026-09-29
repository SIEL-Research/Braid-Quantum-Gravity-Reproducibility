# Finite-range UHF dynamics theorem used by BGCE443 R4

Let `A_loc=union_n M_d(C)^(tensor n)` be the algebraic local core of the one-sided UHF
quasi-local algebra. Let a translation-covariant interaction assign a bounded self-adjoint
operator `Phi(X)` to every interval `X` of length at most `R`, with a uniform bound `J`, and with
only finitely many translated intervals meeting any fixed site.

For local `A`, define

`delta(A)=i sum_{X intersect supp(A) nonempty} [Phi(X),A]`.

The sum is finite. Finite-volume Hamiltonians `H_L=sum_{X subset L} Phi(X)` define
`alpha_t^L=Ad(exp(i t H_L))`. For every local `A` and bounded time interval, the nested-commutator
series is Cauchy uniformly as `L` exhausts the half-chain. At commutator depth `k`, only intervals
within distance `k(R-1)` of the original support occur; the number and norm of terms are bounded by
a constant depending only on `R`, `J` and the original support times a factorial growth. The series
therefore converges on a nonzero time interval. Composition extends it to every finite time.

The limit `alpha_t(A)=lim_L alpha_t^L(A)` is isometric, multiplicative, star-preserving and obeys
the group law on the dense local core, so it extends uniquely to a strongly continuous
one-parameter automorphism group of the quasi-local C-star algebra. Its closed generator extends
`delta`; hence `delta` is closable.

For BGCE443 R4 the focal proof obligation is to record, in every actual sector:

1. self-adjointness of each local `h_a`;
2. the exact finite interaction range `R=3`;
3. a finite exact bound for `||h_a||`;
4. word-independent translated local terms;
5. the support-overlap count entering the finite nested-commutator bound.

The non-focal toy witness is stronger and simpler: its translated one-site Pauli terms commute, so
the finite-volume evolution factorizes explicitly and the strong limit on every local observable is
eventually constant.
