#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from build_actual_source_snapshot import run


HERE = Path(__file__).resolve().parent
frozen_path = HERE / "ACTUAL_SOURCE_SNAPSHOT.json"
frozen = json.loads(frozen_path.read_text())
fresh = run()
assert fresh == frozen
assert frozen["scientific_outcome_computed"] is False
assert frozen["sector_masks"] == [0, 5, 8, 13, 16, 21, 24, 29]
assert [row["rank"] for row in frozen["spatial_projectors"]] == [8, 4, 4]
assert len(frozen["sectors"]) == 8
assert sum(len(row["directions"]) for row in frozen["sectors"]) == 24
print(json.dumps({
    "status": "PASS",
    "snapshot_sha256": hashlib.sha256(frozen_path.read_bytes()).hexdigest(),
    "producer_sha256": hashlib.sha256((HERE / "build_actual_source_snapshot.py").read_bytes()).hexdigest(),
    "sector_count": len(frozen["sectors"]),
    "direction_count": sum(len(row["directions"]) for row in frozen["sectors"]),
    "scientific_outcome_computed": frozen["scientific_outcome_computed"],
}, sort_keys=True, indent=2))
