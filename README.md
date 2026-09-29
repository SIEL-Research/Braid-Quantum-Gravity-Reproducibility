# Braid Quantum Gravity — Public Reproduction Repository

This repository contains public data and code for independently reconstructing
and testing computational claims made in the Subjectivity-Intersection Braid
Quantum Gravity preprint series. The initial release is aligned with v0.99.

The paper and the reproduction package have different roles:

- the paper states definitions, principal equations, scoped theorem claims and
  interpretation boundaries;
- this repository stores machine-readable inputs, executable checks, expected
  outputs and tests.

The manuscript itself remains in the separate
[Subjectivity-Intersection Mathematics repository](https://github.com/SIEL-Research/Subjectivity-Intersection-Mathematics/tree/main/docs/preprint/subjectivity-intersection-braid-quantum-gravity-v0.99).

## Current executable scope

The package reconstructs all eight signed `25 x 25` Braid representatives from
the printed sparse definition and verifies, in exact integer/rational
arithmetic:

- involution and Yang--Baxter relations;
- the common distinguished point;
- endpoint involution and cup/cap relation;
- the exact source Hamiltonian polynomial;
- the Brauer projectors;
- the marker characteristic polynomial;
- the eight distinct three-character sector labels.

The result is deliberately bounded: the eight representatives are inequivalent
real typed-gauge orbits, and selection of one physical sector remains open.

## Quick start

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/verify_manifest.py
.venv/bin/python scripts/verify_source.py
.venv/bin/python -m unittest discover -s tests -v
```

Expected top-level result:

```json
{
  "status": "PASS",
  "representatives": 8,
  "real_typed_orbits": 8,
  "physical_sector_selection": "OPEN"
}
```

## Layout

```text
data/       frozen machine-readable source inputs
expected/   frozen expected verification output
src/        reusable reconstruction and exact-check code
scripts/    command-line entry points
tests/      independent public regression tests
```

The same commands run in GitHub Actions for every push and pull request.

See `CLAIM_TEST_MAP.md` for the exact boundary between currently executable
claims and claims that still require curated public runners.

## Provenance policy

This package is self-contained for the source reconstruction. It does not
depend on private paths, internal task numbers, mutable ledgers or Git commit
identifiers. File history may document development, but it is not a premise of
the mathematics.

## Citation

Cite the v0.99 preprint and this repository. A versioned archival DOI should be
added when the first public release is archived.

## Scientific status

This repository is a reproduction instrument, not an additional theoretical
claim. A test marked `PASS` establishes only the exact finite statement named
in `CLAIM_TEST_MAP.md`. It does not promote an open bridge, establish physical
sector selection, or validate the full quantum-gravity interpretation.
