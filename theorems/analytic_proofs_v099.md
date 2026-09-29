# Self-contained analytic proofs for v0.99

This file closes only the theorem identifiers named below.  It does not turn a
premise supplied by another theorem into a proved fact.  Definitions and claim
ceilings are repeated so that each proof can be checked without consulting an
internal project ledger.

## V099-THE-11 — Four-component finite Ward telescope

**Hypotheses.** Let \(A\) be a unital algebra, let \(\Phi:A\to A\) be a linear
map, and for each \(\alpha\in\{0,1,2,3\}\) let
\(S_\alpha\in A\) and

\[
D_\alpha=S_\alpha-\Phi(S_\alpha).
\]

**Claim.** For every integer \(n\ge 1\),

\[
\sum_{k=0}^{n-1}\Phi^k(D_\alpha)
=S_\alpha-\Phi^n(S_\alpha).
\]

**Proof.** Linearity gives

\[
\sum_{k=0}^{n-1}\Phi^k(D_\alpha)
=\sum_{k=0}^{n-1}\bigl(\Phi^k(S_\alpha)-\Phi^{k+1}(S_\alpha)\bigr).
\]

All terms with powers \(1,\ldots,n-1\) cancel pairwise.  The remaining two
terms are \(S_\alpha-\Phi^n(S_\alpha)\).  The proof is independent of
\(\alpha\) and therefore applies to all four components.  It also applies
separately to every source sector in which the displayed definition of
\(D_\alpha\) is used. \(\square\)

**Claim ceiling.** This proof establishes the telescope after
\(D_\alpha=S_\alpha-\Phi(S_\alpha)\) is defined.  It does not establish that a
particular collision record physically selects that defect; that is the
separate content of V099-THE-10.

## V099-THE-45 — Minimal one-anchor theorem

**Hypotheses.** The source observables are dimensionless.  The declared
continuum class has one positive global rescaling parameter \(\lambda\).  A
time unit \(\tau\) transforms as \(\tau\mapsto\lambda\tau\), and the fixed
conversion constants \(c\) and \(\hbar\) are available.  No additional
dimensionful source scalar is supplied.

**Claim.** Zero independent dimensionful anchors cannot determine an absolute
scale, while one universal time anchor is sufficient to determine all units in
the declared class.

**Proof of necessity.** Every dimensionless source record is unchanged along
the orbit \(\tau\mapsto\lambda\tau\), \(\lambda>0\).  If a source-only rule
selected a unique absolute scale, it would have to distinguish two points of
this orbit using data that are identical at those points.  That is impossible.
Hence zero independent dimensionful anchors leave a one-parameter
non-identifiability.

**Proof of sufficiency.** Fix one physical value of \(\tau\).  Then
\(\ell=c\tau\) fixes length and \(E=\hbar/\tau\) fixes energy.  Products and
quotients give action \(E\tau=\hbar\), mass \(E/c^2\), four-volume
\(\ell^4\), stress \(E/\ell^3\), and every other declared quantity as a
unique monomial in \(\tau,c,\hbar\) times its already fixed dimensionless
source coefficient.  No positive rescaling freedom remains after \(\tau\) is
fixed. \(\square\)

**Claim ceiling.** This is a dimensional identifiability theorem.  It neither
predicts the numerical anchor nor proves that a proposed laboratory clock is
universal.  It also does not determine the physical value of Newton's constant
without the anchor.
