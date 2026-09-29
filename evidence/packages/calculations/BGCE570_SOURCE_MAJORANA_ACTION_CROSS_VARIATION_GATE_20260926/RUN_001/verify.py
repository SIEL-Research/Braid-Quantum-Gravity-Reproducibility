#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
result = json.loads((HERE / "RESULT.json").read_text())
raw = json.loads((HERE / "RAW_OUTPUT.json").read_text())
certificate = json.loads((HERE / "CERTIFICATE.json").read_text())

assert result["pass_rule"] is True
assert result["work_package_status"] == "CLOSED_SCOPED"
assert result["positive_Majorana_rate_scalar"] == "s=1"
assert result["dimensionless_y_nu"] == "+1"
assert result["neutral_mass_mode_count"] == 6
assert all(raw["exact_tests"].values())
assert certificate["decision"] == result["decision"] == raw["decision"]

print(json.dumps({
    "status": "PASS",
    "scout_id": result["scout_id"],
    "result_sha256": hashlib.sha256((HERE / "RESULT.json").read_bytes()).hexdigest(),
    "raw_sha256": hashlib.sha256((HERE / "RAW_OUTPUT.json").read_bytes()).hexdigest(),
    "certificate_sha256": hashlib.sha256((HERE / "CERTIFICATE.json").read_bytes()).hexdigest(),
}, indent=2))
