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
assert raw["scoped_nonabelian_face_holonomy_capacity_pass"] is True
assert raw["central_two_form_transgression_pass"] is False
assert raw["minimal_ctp_face_result"]["exact_determinant"] == "1"
assert raw["minimal_ctp_face_result"]["central_U1_flux"] == "0 mod 2*pi"
print("PASS_VERIFY_BQGNEUT_031_X1")
