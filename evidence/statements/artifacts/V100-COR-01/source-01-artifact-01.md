# Self-contained analytic and reduction proofs for v1.0

This supplement is part of the public evidence graph for the v1.0 manuscript.
It closes only the identifiers named below.  Premises supplied by another
theorem remain separate dependencies in `theorem_evidence_v1.json`.

## V100-THE-11 — Four-component finite Ward telescope

**Hypotheses.** Let (A) be a unital algebra, let
\(\Phi:A\rightarrow A\) be linear, and, for each
\(\alpha\in\{0,1,2,3\}\), let

\[
D_\alpha=S_\alpha-\Phi(S_\alpha).
\]

**Claim.** For every integer (n\geq1),

\[
\sum_{k=0}^{n-1}\Phi^k(D_\alpha)
=S_\alpha-\Phi^n(S_\alpha).
\]

**Proof.** By linearity,

\[
\sum_{k=0}^{n-1}\Phi^k(D_\alpha)
=\sum_{k=0}^{n-1}
\left(\Phi^k(S_\alpha)-\Phi^{k+1}(S_\alpha)\right).
\]

The terms with powers (1,\ldots,n-1) cancel pairwise.  The two boundary
terms are (S_\alpha-\Phi^n(S_\alpha)).  The proof does not depend on
\(\alpha\), so it applies to all four components and separately to every
sector in which the displayed definition of (D_\alpha) holds. \(\square\)

**Ceiling.** This is the telescope conditional on the displayed definition.
The physical selection of that defect by the collision record is the separate
content of V100-THE-10.

## V100-THE-16 — Local regular source-perfect ADM/HDA--BFV parent

**Declared analytic domain.** Work on a common smooth interval on which the
source Palatini refinement tower has a unique gauge-fixed noncaustic stationary
branch, the transverse Hessian is nondegenerate after removal of the four gauge
directions, the boundary traces have the required Sobolev regularity, and the
rank-four constraint minor remains nonzero.  V100-THE-23 supplies strong
trajectory convergence on this interval; the finite-action and first-variation
limits are included in the vendored derivation package.

For fine level (m\) and coarse level (n\), define

\[
S_n^{\rm perf}(z_-,z_+)=
\lim_{m\to\infty}
\operatorname*{stat}_{R_{m,n}z_m^\partial=(z_-,z_+)}S_m[z_m].
\]

The hypotheses give existence of the stationary branch and convergence of the
action and first variation.  Stationarity with respect to an intermediate
boundary datum gives the exact discrete-Lagrangian composition law

\[
S_{02}^{\rm perf}=\operatorname*{stat}_{z_1}
\left(S_{01}^{\rm perf}+S_{12}^{\rm perf}\right),
\]

and nesting of the refinement maps gives
\(J_{n+1,n}^*S_{n+1}^{\rm perf}=S_n^{\rm perf}\).  These are precisely the
unit and composition identities of the local history groupoid.

Let (R_n\) denote the one clock and three spatial primitive history
refactorizations.  The perfect action is invariant under refactorization, so
differentiation in each of the four directions gives the off-shell identity

\[
R_n^\dagger\mathcal E(S_n^{\rm perf})=0.
\]

After Lorentz/torsion reduction the symplectic carrier has dimension twelve.
The saved exact rank certificate gives one scalar plus three vector generators
of rank four.  Constancy of that nonzero minor on an open neighborhood makes
the constraint surface coisotropic with a four-dimensional presymplectic
kernel.  The Lie algebroid of the history groupoid has the hypersurface
deformation brackets

\[
\{D[N],D[M]\}=D[[N,M]],\qquad
\{D[N],H[M]\}=H[\mathcal L_NM],
\]
\[
\{H[N],H[M]\}=
D[\gamma^{ij}(N\partial_jM-M\partial_jN)].
\]

Groupoid associativity supplies the higher coherence identities; equivalently,
the local BFV homological vector field squares to zero.  Functoriality of the
stationary construction intertwines the action, constraint surface,
presymplectic form, algebroid arrows and BFV differential under refinement.
Four regular first-class constraints therefore leave

\[
12-2\times4=4
\]

physical phase dimensions, or two configuration modes. \(\square\)

**Ceiling.** This is a perfect-action theorem on the stated local regular
noncaustic branch.  It does not assert an ultralocal closed form for the raw
finite-cell action, continuation through caustics or singularities, or a
global existence theorem.

## V100-THE-23 — Local regular ten-component metric--Euler convergence

Let (A\leq B\) index the ten symmetric metric components and set

\[
D_\tau^2g_{AB,h}^n-L_h(g_h^n)g_{AB,h}^n=N^{\rm src}_{AB,h},
\]
\[
L_h(g)u(x)=\frac1{25h^2}
\sum_{\delta\in C_5^3\setminus\{0\}}
c_\delta(g)\,[u(x+h\delta)-u(x)].
\]

The exact source moment is
\(\sum_\delta c_\delta\delta_i\delta_j=50A_{ij}(g)\).  Taylor's
second-order factor (1/2\) therefore forces the normalization (1/25\):

\[
\frac12\frac1{25}
\sum_\delta c_\delta\delta_i\delta_j=A_{ij}(g).
\]

The reverse-edge equality (c_\delta=c_{-\delta}\) cancels all odd spatial
moments.  The centered source-clock difference cancels odd temporal terms, and
the source five-digit fourth-jet rule controls the ten components uniformly.
For a smooth exact solution (U\), Taylor's theorem thus gives

\[
\|E_hI_hU-I_hE(U)\|_{H^{s-1}}
\leq C_T(h^2+\tau_h^2).
\]

The centered discrete divergence has operator norm (O(h^{-1})\).  The
continuum Bianchi identity together with V100-THE-07 and V100-THE-11 cancels
the zeroth-order divergence, leaving

\[
\|B_hE_hI_hU\|_{H^{s-2}}
\leq C_T\left(h+\frac{\tau_h^2}{h}\right).
\]

The positive conductances of V100-THE-21, positive dual Hessian and saved
strict CFL margin (3.3912913508957665<4\) persist on a sufficiently small
compact regular metric neighborhood.  The discrete energy estimate followed
by the standard Gronwall inequality then gives

\[
\sup_{0\leq t\leq T}
\|J_hU_h(t)-U(t)\|_{H^{s-1}}
\leq C_T\left(\eta_h+h+\frac{\tau_h^2}{h}\right).
\]

For (\tau_h=O(h)\) and consistent initial data (\eta_h\to0\), the right-hand
side tends to zero.  The principal tensor is the actual inverse spatial metric
because of the exact second-moment identity above, and the subsidiary defect is
\(O(h)\). \(\square\)

**Ceiling.** The theorem is local in time and conditional on the declared
regularity, positivity and CFL neighborhood.  It does not give exact finite-
mesh constraint preservation, a fully coupled matter principal system, or
continuation through singular/rank-loss branches.

## V100-COR-01 — Massless spin two: checked reduction

**Model hypotheses.** V100-THE-08 supplies the Einstein--Hilbert metric
variation on the declared local conservative infrared branch.  Expand on a
flat background, (g_{\mu\nu}=\eta_{\mu\nu}+h_{\mu\nu}), retain terms through
quadratic order in (h\), and quotient by the linearized diffeomorphism action

\[
h_{\mu\nu}\mapsto h_{\mu\nu}
+\partial_\mu\xi_\nu+\partial_\nu\xi_\mu.
\]

**Reduction.** The quadratic Einstein--Hilbert density differs by a boundary
term from the massless Fierz--Pauli density

\[
\mathcal L_{\rm FP}=
-\tfrac12\partial_\lambda h_{\mu\nu}\partial^\lambda h^{\mu\nu}
+\partial_\mu h^{\mu\nu}\partial^\lambda h_{\lambda\nu}
-\partial_\mu h^{\mu\nu}\partial_\nu h
+\tfrac12\partial_\lambda h\partial^\lambda h.
\]

The ten components of a symmetric four-tensor are reduced by four first-class
linear constraints and four gauge directions, leaving two configuration
degrees of freedom.  V100-THE-17 independently realizes the corresponding
rank-two physical projector on every nonzero source momentum, and
V100-THE-18 verifies the scalar principal symbol times (I_2).  Thus the
external Fierz--Pauli reduction hypotheses are explicitly matched rather than
assumed by name.

**External theorem.** M. Fierz and W. Pauli, *On relativistic wave equations
for particles of arbitrary spin in an electromagnetic field*, Proc. Roy. Soc.
A **173** (1939), 211--232,
<https://doi.org/10.1098/rspa.1939.0140>.
An open modern constraint classification covering the same massless
spin-two degree-of-freedom reduction is A. Naruko, R. Kimura and D. Yamauchi,
*On Lorentz-invariant spin-2 theories*, <https://arxiv.org/abs/1812.10886>.

**Ceiling.** The reduction is local, quadratic and flat-background.  It does
not prove nonlinear global propagation or empirical graviton detection.

## V100-THE-44 — Global inextendibility: checked reduction

**Model hypotheses.** The vendored BQGBH-037 package verifies, for the selected
non-quotient static branch, global hyperbolicity and timelike geodesic
completeness.  The metric is smooth and time oriented.

**Reduction.** The cited inextendibility theorem states that a smooth,
timelike geodesically complete, globally hyperbolic spacetime is
\(C^0\)-inextendible.  Each hypothesis is represented by an explicit gate in
the BQGBH-037 result.  Applying the theorem therefore gives
\(C^0\)-inextendibility; analytic inextendibility follows because an analytic
extension would in particular be continuous.

**External theorem.** G. J. Galloway, E. Ling and J. Sbierski,
*Timelike completeness as an obstruction to \(C^0\)-extensions*,
Commun. Math. Phys. **359** (2018), 937--949,
<https://doi.org/10.1007/s00220-017-3019-2>.

**Ceiling.** This reduction concerns the selected static maximal cover.  It
does not establish collapse, evaporation, rotation or generic nonspherical
strong-curvature evolution.

## V100-THE-45 — Minimal one-anchor theorem

**Hypotheses.** Source observables are dimensionless.  The declared continuum
class has one positive global rescaling parameter \(\lambda\).  A time unit
\(\tau\) transforms as \(\tau\mapsto\lambda\tau\), and the fixed conversion
constants (c) and \(\hbar\) are available.  No additional dimensionful
source scalar is supplied.

**Necessity.** Every dimensionless source record is constant on the orbit
\(\tau\mapsto\lambda\tau\).  A source-only rule selecting one absolute scale
would have to distinguish points on that orbit from identical data, which is
impossible.  Hence zero independent dimensionful anchors leave a one-parameter
non-identifiability.

**Sufficiency.** Fix one physical value of \(\tau\).  Then
\(\ell=c\tau\) fixes length and \(E=\hbar/\tau\) fixes energy.  Every declared
unit is a unique monomial in \(\tau,c,\hbar\) multiplied by its already fixed
dimensionless source coefficient.  No positive rescaling freedom remains.
\(\square\)

**Ceiling.** This proves dimensional identifiability.  It neither predicts the
anchor's numerical value nor proves that a proposed laboratory clock is
universal.

## V100-THE-47 — Countermodel to universal objectivist primacy

Define the target thesis precisely as

> Every reproducible invariant public structure requires a primitive,
> perspective-neutral public structure of the same explanatory role.

Let the inputs of the v1.0 construction be the explicitly declared finite
standpoint-bearing source, its pointing, crossing, cap/cup and source-dagger
relations.  V100-THE-01--V100-THE-44 construct, within their stated scopes,
public invariant carriers, transformation laws, quantum operations,
conservation laws and gravitational structures from those relational inputs.
The public carriers are outputs of the construction and are not included as
primitive perspective-neutral inputs.

The target thesis is universal.  A single well-defined construction satisfying
its antecedent and falsifying its asserted necessity is a countermodel.  The
displayed construction therefore refutes that universal necessity thesis.
\(\square\)

**Ceiling.** This does not refute realism, mind-independent constraints,
measurement objectivity or the practical norm of intersubjective replication.
It refutes only the explicitly defined claim of *universal explanatory
priority* for primitive perspective-neutral structure.  The result is a
mathematical/interpretive countermodel, not an empirical psychology result.
