# BGCE443 Revision 7 actual-source binding preflight

Status: `FOCAL_EVALUATOR_FROZEN__AWAITING_INDEPENDENT_E0`

Revision 6 passed independent semantic E0, but its six-file focal allowlist contains only aggregate
BGCE075/BGCE117/BGCE386/BGCE442 results and the OCBFH014 producer/certificate. Those aggregates do
not themselves contain the eight exact signed relations or the 24 ordered local commutator
matrices required by an actual-source evaluator. Importing the OCBFH014 producer would read
transitive non-allowlisted dependencies and would violate the R6 guard contract.

Revision 7 therefore performs no BGCE443 endpoint evaluation. It runs the canonical OCBFH014
source reconstruction once as a source-only producer and freezes `ACTUAL_SOURCE_SNAPSHOT.json`.
The snapshot retains:

- all eight masks `[0,5,8,13,16,21,24,29]`;
- each exact 25x25 signed relation;
- each exact 125x125 `G1` numerator with denominator six;
- all three exact spatial projector numerators with denominator four and ranks `8,4,4`; and
- all 24 exact antisymmetric commutator numerators, with
  `h_a=i*commutator_numerator/24`.

All matrices use sparse integer entries. `scientific_outcome_computed=false`; no growth, rank,
closability, comparator or final decision is evaluated here. A byte-exact fresh replay must equal
the frozen snapshot and verify the two canonical OCBFH014 source hashes plus its own producer hash.

## Frozen bold hypothesis and endpoints

OCBFH014 distinguishes product-preserving pointed tensor refinement from Braid transport of marked
support. R7 therefore does not define physical windows by repeatedly braiding the local operator.
It uses the canonical finite-range refinement
`h_x=I^x tensor h tensor I`, while the actual signed Braid support transport is compared against
the unsigned canonical swap as a separate specificity endpoint.

For each exact `h_a=i C_a/24`, every canonical order-`n` implementer is
`P_a^(n)=sum_(x=0)^(n-3) h_(a,x)`. The evaluator deterministically scans the frozen 85 one-site
Gaussian vectors `e_j` and `e_j+(+1,-1,+i,-i)e_k`. Two product states with exact local energy-density
gap `Delta_a>0` imply for every integer `n>=3` that the spectral diameter, hence the norm of the
inner derivation on the finite algebra, is at least `(n-2)Delta_a`. This excludes a bounded inner
limit without fitting a coefficient or extrapolating finite samples.

The exact local direction rank is the rank of the three retained commutator numerators. Hermiticity,
finite range, a finite Frobenius norm bound, canonical stabilization and the standard finite-range
thermodynamic-limit bridge supply the closability gate. Signed versus unsigned block transport uses
the same shortest adjacent word `[2,1,0]`; the evaluator retains the first raw matrix-unit action
witness when the two transported actions differ.

Generic carrier and Braid specificity are separate decisions. A generic PASS with specificity
NO-GO remains a scoped generic refinement result. Even a full BGCE443 PASS does not yet construct
moment maps or the first-class clock-spatial bracket.

`evaluate.py` is now frozen against only the snapshot and the R6 E0 record. No result or raw output
exists. A new revision-matched independent E0 is mandatory before the one allowed execution; the
R6 PASS cannot authorize an evaluator whose input contract changed.
