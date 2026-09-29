# Source-affine plaquette second-jet and child-split theorem

## Statement

Conditional on the BGCE094 off-shell temporal fields, the existing BGCE138
metric-affine completion and BGCE097 face-log prescription canonically define
the raw finite-depth Palatini second jet on one source five-adic parent. No
target Einstein equation, fitted coefficient or new action term is required.

## Plaquette two-jet

Let the four positively parameterized edge logarithms of an oriented face be
`A,B,C,D`, with the top and left edges traversed backwards. In the common
identity log branch,

`P=exp(A) exp(B) exp(-C) exp(-D)`.

Through total degree two,

`log P = L + Q + O(3)`, where

`L=A+B-C-D`

and

`Q=(1/2) sum_(i<j) [Z_i,Z_j]`, `Z=(A,B,-C,-D)`.

This follows exactly by multiplying the truncated exponentials and applying
`log(1+X)=X-X^2/2+O(3)`. Orientation reversal gives `-log P`. For a constant
connection, `C=A,D=B`, the linear term cancels and the quadratic term is
`[A,B]`.

## Source child split

BGCE137--138 fixes one refinement parent as the `n=5` cubical four-grid. Its
incidence numbers are:

- vertices: `6^4=1296`, with `256` interior and `1040` boundary;
- oriented positive edges: `4*5*6^3=4320`, with `1280` interior and `3040`
  boundary;
- oriented positive faces: `6*5^2*6^2=5400`, with `2400` interior and `3000`
  boundary;
- four-cells: `5^4=625`.

For the BGCE138 raw coframe/GL4 coordinates, this gives `24576` interior field
coordinates and `65280` boundary field coordinates before gauge/BFV reduction.
These dimensions are bookkeeping for the raw sparse Hessian, not physical
degrees of freedom.

## Flat critical relation and second variation

At the committed anchor `bar e=3 I_4`, `bar Gamma=0`, every plaquette is the
identity and every face log vanishes. Hence the coframe first variation of the
vacuum Palatini block vanishes. The connection first variation is the cubical
incidence adjoint applied to the constant bivector `epsilon bar e bar e`; all
interior edge coefficients cancel pairwise. With boundary fields fixed, the
flat anchor is therefore an interior stationary point of the conditional
vacuum block.

Writing `f=delta e`, `a=delta Gamma`, and denoting the linear and quadratic
parts of the face log by `D a` and `Q(a,a)`, the exact quadratic action is

`delta^2 S = C sum epsilon epsilon [2 bar e f (D a) + bar e bar e Q(a,a)]`.

The raw Hessian `H` is the bilinear form represented by this expression.
Let `I` be the interior vertex/link coordinates and `B` the boundary ones from
the source incidence split. Then

`K_ii = H|_(I x I)`, `K_ib = H|_(I x B)`.

Thus these blocks are now well-defined sparse exact forms whose entries are
fixed by integer incidence, Levi-Civita signs, the source anchor `3 I_4` and
the declared overall Palatini normalization. Their rank is not evaluated in
this theorem.

## Provenance label

The refinement-natural source mark is the ordered sequence of four spectral
digits at each epoch together with the BGCE137 orientation sheet. Deleting the
newest four digits is the parent map. This supplies a typed ordered-history
label for a relation component, but BQGSTRAT-005 prevents treating the coarse
endpoint alone as a unique selector. Injectivity against actual connected
components can be tested only after the sparse rank-loss block is evaluated.

## Boundary

The construction is standard local lattice gauge/Palatini mathematics on a
source-selected complex. It closes the missing construction input, not Braid
necessity, an actual clean caustic, a unique outgoing branch or global
continuation. BGCE094's off-shell temporal promotions remain conditional.
