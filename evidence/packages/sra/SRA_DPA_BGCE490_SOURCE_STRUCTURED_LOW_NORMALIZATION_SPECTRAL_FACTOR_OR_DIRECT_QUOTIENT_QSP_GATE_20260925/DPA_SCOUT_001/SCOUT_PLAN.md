# BGCE490 scouting plan

## Question

Can source structure reduce the enormous BGCE488 Lagrange normalization before
amplitude amplification?

## Bold hypothesis

Use the canonical Halmos block encoding from BGCE478 as a rotation walk.  If
`A=H/alpha`, `D=sqrt(I-A^2)`, `BE(H)=[[A,D],[D,-A]]`, and
`R=Z BE(H)`, then functional calculus gives

`<0|R^k|0>=T_k(A)`.

Transform the canonical finite-spectrum target polynomial into its unique
Chebyshev coefficients and LCU-select the powers `R^k`.  This preserves the
exact target values but may drastically reduce coefficient one-norm.

## Checks

- reconstruct all 32 compressed controls from the pinned source at 70 digits;
- solve the Chebyshev interpolation system without empirical fitting;
- verify every spectral target and every scalar walk identity;
- compare success probability directly with BGCE488;
- apply BGCE489 exact phase matching and record total query cost;
- preserve the boundary between typed circuit closure and bare-word/hardware
  realization.
