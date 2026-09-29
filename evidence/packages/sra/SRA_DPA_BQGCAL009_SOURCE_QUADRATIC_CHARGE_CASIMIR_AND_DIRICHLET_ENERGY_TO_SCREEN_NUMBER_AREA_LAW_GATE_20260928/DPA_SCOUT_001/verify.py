#!/usr/bin/env python3
from hashlib import sha256
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
cert = json.loads((HERE / "CERTIFICATE.json").read_text())
raw = json.loads((HERE / "RAW_OUTPUT.json").read_text())
result = json.loads((HERE / "RESULT.json").read_text())
status = json.loads((HERE / "STATUS.json").read_text())

assert cert["evaluator_sha256"] == sha256((HERE / "evaluate_scout.py").read_bytes()).hexdigest()
assert cert["raw_output_sha256"] == sha256((HERE / "RAW_OUTPUT.json").read_bytes()).hexdigest()
assert cert["result_sha256"] == sha256((HERE / "RESULT.json").read_bytes()).hexdigest()
assert all(cert["tests"].values())
assert raw["decision"] == result["decision"] == status["decision"]
assert raw["positive_quadratic_count_relation_pass"] is True
assert raw["excitation_casimir"]["exact_operator_identity"] == "C_exc=(4/45)N_1"
assert raw["conserved_quasilocal_mass_pass"] is False
print("PASS_VERIFY_BQGCAL_009_X1")
