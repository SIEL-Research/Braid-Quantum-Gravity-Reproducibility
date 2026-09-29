#!/usr/bin/env python3
"""Freeze the canonical eight-sector BGCE443 matrix source without evaluating BGCE443 endpoints."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE_CHECK = ROOT / "public-inputs/formal_checks/ocbfh014_source_native_refinement_naturality_check.py"
SOURCE_CERTIFICATE = ROOT / "public-inputs/formal_checks/ocbfh014_source_native_refinement_naturality_certificate_v1.json"
EXPECTED = {
    str(SOURCE_CHECK.relative_to(ROOT)): "176c75ac349f0f3f142d9c850ca0682436b7ad00cd179f6806de253d0a7acabb",
    str(SOURCE_CERTIFICATE.relative_to(ROOT)): "717c79fddcf2c94ed89a1c7bef19965627cad9b56e9ccd7bb3fbfa86b45f35f9",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def sparse_integer(matrix: np.ndarray) -> dict:
    assert np.issubdtype(matrix.dtype, np.integer)
    rows, columns = matrix.shape
    nonzero = np.argwhere(matrix != 0)
    return {
        "rows": int(rows),
        "columns": int(columns),
        "entries": [
            {"row": int(row), "column": int(column), "value": int(matrix[row, column])}
            for row, column in nonzero
        ],
    }


def run() -> dict:
    for relative, expected in EXPECTED.items():
        assert digest(ROOT / relative) == expected, relative
    source = load_module("bgce443_r7_canonical_source", SOURCE_CHECK)
    survivors, projectors, characters, source_record = source.reconstruct_actual_source()
    identity5 = np.eye(5, dtype=np.int64)
    projector_records = []
    p3_numerators = []
    for character, (numerator, denominator) in zip(characters, projectors):
        p3 = np.kron(numerator, identity5)
        projector_records.append({
            "character": list(character),
            "rank": int(np.trace(numerator) // denominator),
            "denominator": int(denominator),
            "two_site_numerator": sparse_integer(numerator.astype(np.int64)),
            "three_site_numerator": sparse_integer(p3.astype(np.int64)),
        })
        p3_numerators.append(p3)
    sectors = []
    for survivor in survivors:
        relation = survivor["R"].astype(np.int64)
        gnum, gden, _, _ = source.source_g1(relation)
        directions = []
        for index, pnum in enumerate(p3_numerators, start=1):
            commutator_numerator = gnum @ pnum - pnum @ gnum
            assert np.array_equal(commutator_numerator.T, -commutator_numerator)
            directions.append({
                "direction": index,
                "hermitian_generator_representation": "h=i*commutator_numerator/24",
                "commutator_numerator": sparse_integer(commutator_numerator.astype(np.int64)),
            })
        sectors.append({
            "mask": int(survivor["mask"]),
            "signed_relation": sparse_integer(relation),
            "G1_denominator": int(gden),
            "G1_numerator": sparse_integer(gnum.astype(np.int64)),
            "directions": directions,
        })
    return {
        "schema": "siel.public-calculation.bgce443.r7.actual-source-snapshot.v1",
        "scientific_outcome_computed": False,
        "source_revision": source_record["cross_source_commit"],
        "source_hashes": EXPECTED,
        "source_reconstruction": source_record,
        "local_dimension": 5,
        "base_order": 3,
        "sector_masks": [row["mask"] for row in sectors],
        "spatial_projectors": projector_records,
        "sectors": sectors,
    }


if __name__ == "__main__":
    rendered = json.dumps(run(), sort_keys=True, indent=2) + "\n"
    if len(sys.argv) == 3 and sys.argv[1] == "--output":
        Path(sys.argv[2]).write_text(rendered)
    elif len(sys.argv) != 1:
        raise SystemExit("usage: build_actual_source_snapshot.py [--output PATH]")
    print(rendered, end="")
