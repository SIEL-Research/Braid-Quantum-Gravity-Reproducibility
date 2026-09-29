# BQGBH-037 scouting plan

## Gate

`BQGBH-037_SOURCE_MAXIMAL_ATLAS_INEXTENDIBILITY_AND_GLOBAL_CAUSAL_STRUCTURE_GATE`

## Frozen question

Does the selected static spherical finite Palatini solution admit a canonical
source-maximal, non-quotiented global atlas whose complete causal development
is globally hyperbolic and inextendible, without adding a target Einstein
equation, fitted coefficient, periodic time identification, or external matter
law?

## Fixed inputs

- BQGBH-003 source-reflected bi-infinite radial line;
- BQGBH-031 complete static spherical six-face Palatini action;
- BQGBH-035 source selection of the relative action and unit reaction;
- BQGBH-036 selected global solution and horizon-complete local atlas.

All input hashes are fixed in `INPUT_MANIFEST.json` before evaluation.

## Exact tests

1. classify the throat and horizon graph for `r_h/ell_star <,=,> 1`;
2. determine whether source provenance selects the universal non-quotient atlas
   over periodic identifications;
3. show that every causal geodesic can cross every finite-`X` horizon/bounce and
   cannot reach either asymptotic end at finite affine parameter;
4. construct a Cauchy block-time on the non-quotient Carter--Penrose tiling;
5. apply the standard completeness/inextendibility theorem only after tests 3
   and 4 pass;
6. separate static maximality from collapse, evaporation, rotation, charge and
   empirical identification.

## Controls and failure conditions

- A one-chart EF argument is insufficient.
- Bounded curvature alone is insufficient for inextendibility.
- A periodic time quotient is rejected unless the source identifies distinct
  event indices.
- If global hyperbolicity or timelike completeness is not proved, absolute
  inextendibility remains `OPEN`.
- Literature is used only to compare the derived causal classification, never
  to select the source action or metric.

## Primary literature comparison fixed before evaluation

- Simpson and Visser, *Black-bounce to traversable wormhole*,
  arXiv:1812.07114 / JCAP 02 (2019) 042.
- Lobo et al., *Novel black-bounce spacetimes: wormholes, regularity, energy
  conditions, and causal structure*, arXiv:2009.12057.
- Galloway, Ling and Sbierski, *Timelike completeness as an obstruction to
  C0-extensions*, arXiv:1704.00353.

Accessed 2026-09-29.

## Claim ceiling

At most: static spherical source-maximal non-quotient analytic development,
global causal classification and an inextendibility theorem for that selected
continuum solution. No dynamical formation, evaporation, thermodynamics,
rotation, charge, generic nonspherical strong-curvature, or empirical claim.
