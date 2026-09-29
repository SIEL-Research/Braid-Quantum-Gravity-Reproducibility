# BGCE309R1 preregistered question

## Decision question

Do the existing source clock `G1` and three Fourier projectors select the four
regular tail copies and their group basepoint, or can the apparent selector be
removed as an environment-unitary gauge choice while preserving the reduced
GKSL channel?

## Frozen tests

1. Restrict `G1` and all three `P_chi` to every regular six-orbit in all eight
   source sectors and test literal equality or diagonal-sign marked unitary
   equivalence copy by copy.
2. Test whether the compressed clocks `P_chi G1 P_chi` split each rank-two
   Fourier sector into source-defined rank-one rays.
3. Test whether those six rays are permuted as the actual regular Braid labels.
4. Prove or refute basepoint/copy independence of the reduced Stinespring
   channel under environment-only unitary equivalence.

## Decision rule

- Full selector pass requires a unique physical copy and basepoint.
- Gauge pass requires all choices to give the same reduced channel even though
  no physical environment stress has yet been selected.
- Fail means neither a selector nor a choice-independent reduced construction
  exists.

## Runtime

Short exact integer/rational block checks; no scan.

## Revision provenance

BGCE309 stopped before producing a result because literal block equality was
too narrow for the signed source sectors.  BGCE309R1 is a fresh preregistration
whose declared test is marked unitary equivalence; no BGCE309 result is reused.
