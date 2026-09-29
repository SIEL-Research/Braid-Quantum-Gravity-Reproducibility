#!/usr/bin/env python3
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
r = json.loads((HERE / "RESULT.json").read_text())
raw = json.loads((HERE / "RAW_OUTPUT.json").read_text())
assert r["decision"].startswith("CLOSED_SCOPED_FINITE_QUANTUM_BV_QME")
assert all(r["checks"].values())
assert raw["renormalization"]["exact_5x5_witness"]["direct"] == raw["renormalization"]["exact_5x5_witness"]["nested"]
assert raw["berezinian_witnesses"] == ["1", "1"]
print("BQGQBV-003 verification PASS")

