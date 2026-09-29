# Public provenance

## Scientific object

The initial executable object is the eight-representative signed finite Braid
source class printed in Appendix A of the v0.99 integrated preprint.

The machine-readable transcription is:

- `data/canonical_source_class_v099.json`

The transcription is complete for the source-level checks currently exposed
by this repository: basis order, distinguished point, endpoint involution,
sparse crossing permutation, sign rows, marker spectrum, exchange pairs and
right-tail refinement rule.

## Independent reconstruction rule

The verifier reconstructs every `25 x 25` signed crossing matrix from the JSON
input. It does not load private research paths, internal task identifiers,
saved matrices, or precomputed eigensystems. Expected results are frozen in a
separate file and compared only after reconstruction.

## Claim boundary

The eight representatives form eight distinct real typed-gauge orbits under
the declared character test. This repository does not select one of them as
the unique physical sector. That selection remains `OPEN`.

The remaining manuscript claims will be added only when a public runner has a
frozen input, a named decision rule, an expected output and a regression test.
