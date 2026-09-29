# BGCE292 — BKM-horizontal connection curvature and local path-independence gate

## Frozen question

Does the BGCE287 first-order source-event-path BKM-horizontal lift integrate to
a locally path-independent finite conductance section over the ten-dimensional
metric-moment base?

## Source-native nonlinear completion under test

For positive microscopic edge rates `r_e`, use the event-path relative-entropy
Hessian already invoked by BGCE287:

```text
g_r(v,w) = sum_e v_e w_e / r_e.
```

Let `M` be the fixed 48-to-10 Braid event second-moment map. The unique
`g_r`-orthogonal horizontal right inverse is

```text
H(r)=D(r) M^T [M D(r) M^T]^{-1}.
```

At the common source rate this must reproduce the BGCE287 right inverse. No
coefficient, path ordering rule or new action may be added.

## Exact decision

Compute the Ehresmann curvature at the common-rate source anchor:

```text
F_ab = D X_b[X_a] - D X_a[X_b],
X_a(r)=H(r)e_a.
```

- `F_ab=0` for every base pair is necessary for local path independence and
  permits the finite-integrability route to continue.
- Any exact nonzero `F_ab` proves that the canonical nonlinear BKM-horizontal
  connection is non-flat; endpoint conductances depend on the chosen path.

The test is exact rational differentiation at one source anchor, not a scan.

## Claim boundary

Nonzero curvature refutes only path-independent integration of this canonical
BKM-horizontal connection. It does not refute the existence of a different
Braid-derived nonlinear selector or a path-dependent finite evolution law.
