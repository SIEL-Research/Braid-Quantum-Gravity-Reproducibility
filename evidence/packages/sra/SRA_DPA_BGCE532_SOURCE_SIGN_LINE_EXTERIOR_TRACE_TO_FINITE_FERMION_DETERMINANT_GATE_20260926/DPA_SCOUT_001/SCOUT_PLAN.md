# BGCE532 scout plan

- Scout: `DPA-SCOUT-BGCE532-001`
- Parent: `BQG-G3-R03.7`
- Source commit: `cf07f1d993a8c12e3b50afeac2e5cc8eb4205f92`
- Source snapshot: `DPA-SNAPSHOT-cf07f1d993a8`
- Evidence class: exact `Theoretical derivation`

## North-star fields

- North-star claim: the finite fermion determinant used conditionally in BGCE530 is selected by the same Braid-derived sign-line, typed matter and CTP trace structures, rather than by an independently assumed Grassmann action.
- Closest prior result: BGCE530 derives three source-weighted Yukawa strengths and proves a unique nonzero Higgs radius conditional on the finite odd Gaussian determinant.
- Current missing link: remove the explicit odd-Gaussian-action assumption and fix the determinant plus sign and effective-action minus sign from existing finite source structures.
- Directness: `direct`.

## Bold hypothesis

- Interpretive leap: do not introduce a Grassmann path integral. Pull the already source-derived permutation sign line back along the BGCE439 total Boolean parity, apply its exterior/Fock functor to the finite odd matter carrier, and use the ordinary closed-contour trace already selected by the CTP parent.
- Source status:
  - `DERIVED`: GRADEDSEC-196R/BGCE406 sign representation and determinant line; BGCE321/322/325 ordinary finite CTP trace/log-partition structure; BGCE439 degree-one matter and degree-zero scalar; BGCE526/530 positive typed one-particle Yukawa operator.
  - `NEW COMPOSITION TO BE TESTED`: the parity pullback sends every BGCE439 degree-one matter factor to the existing sign representation while keeping degree-zero Higgs factors even. No coefficient, phase, target mass or new cocycle may be chosen.
- New composition rule: for the branch-paired positive one-particle operator `A(H)=M_H* M_H=|H|^2 M* M`, define the matter marginal by the ordinary exterior trace `Z_m(H)=Tr_(Lambda E) Lambda(A(H))`. Then test whether functoriality forces `Z_m=det(I+A)` and `S_eff=S_H-log Z_m`.
- Strongest ordinary alternative: the rapidity sign line may be a separate statistics object with no source-selected action on the BGCE439 derived matter extension. If the pullback is not canonical, or if CTP gluing permits a supertrace instead of the recorded ordinary trace, the determinant remains an extra matter law.
- Counter-intuition: BGCE518 already excludes deriving a Koszul sign from the local Yukawa star count. BGCE406 also excludes using the sign line to select internal chirality or the exact 163R field algebra. BGCE532 must preserve both NO-GOs; it may use the sign only as universal particle statistics after chirality and matter typing have independently been derived.

## Exact endpoint, falsifier and stopping rule

Core discriminator A:

1. prove or refute that total Boolean parity plus the fixed sign character selects a unique symmetric braiding on degree-one matter and the ordinary exterior functor up to natural isomorphism;
2. prove or refute the exact finite identity `Tr_(Lambda E) Lambda(A)=det(I+A)` for the typed positive mode operator;
3. prove or refute that ordinary CTP marginalization forces `S_eff=S_H-log Z_m`, while a parity-inserted supertrace would give a different, non-selected `det(I-A)`;
4. verify that forward/reverse CTP pairing selects `A=M_H* M_H>=0`, with the opposite ordering giving the same determinant by Sylvester's identity.

Validity-critical B:

- preserve BGCE406's no-go for internal chirality selection and same-163R transfer;
- preserve BGCE518's no-go for a local star-derived two-cocycle;
- require no target-data fit, no observed mass, no inserted negative Higgs quadratic and no manually selected determinant sign.

Falsify the route if the parity pullback has more than one sign choice after the existing sign character is fixed, if the CTP record does not select ordinary trace, if `A` is not positive/gauge invariant/branch neutral, or if the exterior trace is not the BGCE530 determinant.

Stop after the categorical uniqueness, trace identity, sign audit, and preservation of prior NO-GOs. Do not calculate the numerical Higgs radius or compare with observed masses.

## Claim ceiling

A PASS may remove BGCE530's explicit finite odd-Gaussian-action assumption inside the already declared source-derived sign-line + anomaly-solution-groupoid + ordinary-CTP-trace class. It cannot establish the unchanged raw source alone, same-163R local field equivalence, observed Yukawa values, absolute fermion masses, CKM/PMNS mixing, running, empirical Standard Model physics or completed quantum gravity.

Commands:

```text
python3 audits/SRA_DPA_BGCE532_SOURCE_SIGN_LINE_EXTERIOR_TRACE_TO_FINITE_FERMION_DETERMINANT_GATE_20260926/DPA_SCOUT_001/evaluate_scout.py
python3 audits/SRA_DPA_BGCE532_SOURCE_SIGN_LINE_EXTERIOR_TRACE_TO_FINITE_FERMION_DETERMINANT_GATE_20260926/DPA_SCOUT_001/verify.py
```
