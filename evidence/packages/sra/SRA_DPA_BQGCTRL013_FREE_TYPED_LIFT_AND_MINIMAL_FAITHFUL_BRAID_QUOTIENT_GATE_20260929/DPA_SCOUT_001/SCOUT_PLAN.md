# BQGCTRL-013 — free typed lift and minimal faithful Braid quotient

## Parent question

Strengthen `BQGCTRL-011/012` by asking whether the same full product-cone
generation chain can be supplied by one coherent source that does not impose a
Braid relation, or whether the pointed-Braid source is forced by a universal
minimality condition.

## Pinned inputs

- SRA branch revision before this scout: `c45a07ce1994835e9b0c9f00bafff73b69eb6740`.
- `BQGCTRL-012` common-source product-functor result and raw output.
- `BQGCTRL-008` quantum-stage boundary result.
- `UB473` exact all-eight-sector Yang--Baxter path result and certificate.

Exact paths and SHA-256 values are fixed in `INPUT_MANIFEST.json`.

## Frozen source presentations

Let `P_free` be the free strict typed monoidal presentation on the already
declared source primitives:

- point;
- cap/cup;
- right-tail/history arrow;
- crossing generator `r` and its adjacent placements `r1,r2`;
- five-adic refinement;
- the fixed typed arrows used by the six `BQGCTRL-012` branch functors.

No Yang--Baxter relation is imposed in `P_free`. Therefore the source words

`wL = r1 r2 r1` and `wR = r2 r1 r2`

are distinct arrows in the free presentation.

Let `B_min` be the coequalizer quotient of `P_free` imposing `wL=wR`, together
with the already declared typing/point/cap/right-tail/refinement relations.
The crossing-generated part of `B_min` is the Braid presentation used by the
actual source.

Let `C_prod` be the product endpoint category of `BQGCTRL-012`, and let
`H_free:P_free->C_prod` assign each generator exactly the already pinned actual
source image. No endpoint, coefficient, target equation, branch interface or
observed datum is changed.

## Bold hypothesis

The full chain does not identify the syntax of its source category. A coherent
non-Braid free lift can reproduce the complete product-cone image, but only
nonfaithfully. After requiring a relation-minimal faithful source
representation, the Yang--Baxter quotient is forced by the exact equality of
the two three-crossing paths.

## Strongest ordinary alternative

The endpoint chain is a standard typed monoidal/module construction. The word
`Braid` records one efficient presentation, while an unequipped free source or
another redundant presentation can map to the same operators and fields.

## Noncompensating gates

1. `INPUT_INTEGRITY`: every pinned input hash and declared prior decision is
   verified.
2. `FREE_NONBRAID`: `wL` and `wR` remain distinct in `P_free`; no Braid
   relation is silently imported.
3. `TARGET_YBE`: their images are equal in `C_prod`, using the exact `UB473`
   Yang--Baxter certificate.
4. `FULL_CHAIN_MATCH`: assigning the same generator images reproduces every
   branch and interface of the `BQGCTRL-012` product functor, not one endpoint.
5. `NONFAITHFUL_WITNESS`: the distinct pair `(wL,wR)` has one target image, so
   `H_free` is not faithful.
6. `FAITHFUL_BOUNDARY`: any source functor with the same crossing image that is
   faithful on the crossing-generated subcategory must identify `wL=wR`.
7. `COEQUALIZER_MINIMALITY`: `H_free` factors uniquely through `B_min`, and
   every other factorization equalizing the same pair receives the canonical
   quotient map.

## Frozen controls

- `CTRL-FREE-TYPED-NONBRAID-LIFT`: coherent source, same typed generators and
  exact branch images, but no source-level YBE relation.
- `CTRL-FAITHFUL-YBE-BROKEN`: requires the same complete target image while
  keeping `wL!=wR` and remaining faithful on the crossing subcategory.
- `CTRL-MANUAL-MODULE-STACK`: retains the `BQGCTRL-011/012` boundary; endpoint
  modules without one generator assignment do not count as a source functor.

## Decision rule

- Universal source-ontology necessity is `NO-GO` if
  `CTRL-FREE-TYPED-NONBRAID-LIFT` reproduces the full chain.
- Minimal faithful Braid specificity is `PASS` if the free lift is necessarily
  nonfaithful, `CTRL-FAITHFUL-YBE-BROKEN` is impossible, and the coequalizer
  factorization is exact.
- It is `NO-GO` if a faithful YBE-broken source reproduces the same complete
  target functor.
- It is `OPEN` if any full-chain branch or required equality is unavailable.

## Falsifier

One faithful coherent source with `wL!=wR` and exactly the same complete
product-cone image falsifies the minimal faithful Braid boundary. Failure of
any `BQGCTRL-012` branch identity invalidates the full-chain match.

## Runtime and stopping condition

Exact word, quotient, hash and universal-property checks only. Stop after the
first complete theorem/counterexample certificate. No random search, parameter
fit, field solve, circuit execution or trajectory integration.

## Raw artifacts

- deterministic evaluator;
- raw JSON;
- result JSON;
- iteration ledger;
- validation script;
- Japanese audit report.

## Claim ceiling

At most: the actual pointed-Braid source simultaneously supplies the scoped
full chain and is the relation-minimal faithful presentation of its crossing
coherence, while unrestricted source ontology remains non-identifiable up to
nonfaithful lifts and observationally equivalent presentations. This is not
empirical gravity, physical necessity of Braid, confirmation, RPD adoption or
Official SIEL status.
