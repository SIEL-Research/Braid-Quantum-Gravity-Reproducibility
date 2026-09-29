# Public provenance

## Scientific object

The initial executable object is the eight-representative signed finite Braid
source class printed in the exact-source appendix of the v1.0 integrated
preprint.

The machine-readable transcription is:

- `data/canonical_source_class_v1.json`

The transcription is complete for the source-level checks currently exposed
by this repository: basis order, distinguished point, endpoint involution,
sparse crossing permutation, sign rows, marker spectrum, exchange pairs and
right-tail refinement rule.

## Independent reconstruction rule

The verifier reconstructs every `25 x 25` signed crossing matrix from the JSON
input. It does not load private research paths, internal task identifiers,
saved matrices, or precomputed eigensystems. Expected results are frozen in a
separate file and compared only after reconstruction.

## Vendored theorem evidence

The directories under `evidence/packages/calculations/` are publication-normalized
exports of the calculation packets from which the v1.0 theorem statements were
drawn. Scientific inputs, executable checks, raw outputs, results and claim
ceilings are retained. Repository-local paths, workflow labels and schemas are
normalized to public identifiers; English public verification notes accompany
the machine artifacts where a narrative endpoint is required. Regenerated
certificates and the integrity manifest bind the resulting public files.

The v1.0 evidence ledger points to this exported content, so no separate
research checkout or mutable project ledger is required.

For each referenced local evidence path, `evidence/evidence_integrity_v1.json`
records either a file SHA-256 or a deterministic directory-tree SHA-256.
`scripts/verify_evidence_integrity.py` recomputes those values.

## Claim boundary

The eight representatives form eight distinct real typed-gauge orbits under
the declared character test. This repository does not select one of them as
the unique physical sector. That selection remains `OPEN`.

Evidence reachability for all 53 v1.0 theorem-like statements is closed. This
does not settle the open physical-sector selection, infinite-depth measure,
singular continuation, absolute numerical scale or prospective empirical
validation.
