# Braid Quantum Gravity — Public Reproduction Repository

This repository contains public data and code for independently reconstructing
and testing computational claims made in the Subjectivity-Intersection Braid
Quantum Gravity preprint series. This release is aligned with v1.0.

The paper and the reproduction package have different roles:

- the paper states definitions, principal equations, scoped theorem claims and
  interpretation boundaries;
- this repository stores machine-readable inputs, executable checks, expected
  outputs and tests.

The archival manuscript of record will be linked here by its Zenodo DOI when
the v1 deposit is published. The development repository is not the citation
target for the paper.

## Evidence reachability

All 53 theorem-like statements in v1.0 are indexed in
[`THEOREM_EVIDENCE_INDEX_v1.0.md`](THEOREM_EVIDENCE_INDEX_v1.0.md). Each entry
terminates in one of three public evidence classes:

- repository-local executable code and frozen result artifacts;
- a repository-local analytic proof;
- a checked reduction to a named external theorem, with the model hypotheses
  stated explicitly.

The former private-path dependency has been removed. Relevant calculation
packages are vendored under `evidence/packages/sra/`; the public index, rather
than an internal work-package number, is the navigation layer.

This is an evidence-reachability closure. It is not a claim that all 53 results
have received independent third-party replication.

The gate definition, counts and reproduction boundary are recorded in
[`EVIDENCE_REACHABILITY_AUDIT_v1.0.md`](EVIDENCE_REACHABILITY_AUDIT_v1.0.md).

## Canonical-source executable scope

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
.venv/bin/python scripts/verify_theorem_coverage_v1.py
.venv/bin/python scripts/verify_version_cleanliness.py
.venv/bin/python scripts/verify_evidence_integrity.py
.venv/bin/python scripts/verify_vendored_packages.py
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
evidence/   vendored calculation packages and integrity manifest
expected/   frozen expected verification output
src/        reusable reconstruction and exact-check code
scripts/    command-line entry points
tests/      independent public regression tests
theorems/   v1.0 inventory, evidence ledger and analytic proofs
```

The same commands run in GitHub Actions for every push and pull request.

See `CLAIM_TEST_MAP.md` for the evidence classes and scientific boundary of
each group of claims.

## Provenance policy

This package is self-contained for evidence navigation and canonical-source
reconstruction. The vendored packages preserve their historical identifiers as
provenance labels, but no reader must access a private path or mutable internal
ledger to reach the evidence. File history documents development; it is not a
premise of the mathematics.

## Citation

Cite the v1.0 preprint through its Zenodo DOI of record and cite this repository
for the executable evidence package. The manuscript DOI will be inserted here
as soon as the v1 Zenodo deposit is published.

## Scientific status

This repository is an evidence and reproduction instrument, not an additional
theoretical claim. A gate marked `PASS` establishes that its evidence is
present, addressable and structurally complete under the declared rule. It
does not promote an open bridge, establish physical-sector selection, validate
the full quantum-gravity interpretation, or substitute for independent review.
