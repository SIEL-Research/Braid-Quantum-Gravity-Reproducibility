#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
cert = json.loads((HERE / "CERTIFICATE.json").read_text())
result = json.loads((HERE / "RESULT.json").read_text())

files = {
    "input_manifest_sha256": "INPUT_MANIFEST.json",
    "evaluator_sha256": "evaluate_scout.py",
    "raw_sha256": "RAW_OUTPUT.json",
    "result_sha256": "RESULT.json",
    "report_sha256": "REPORT_JA.md",
}
for key, name in files.items():
    digest = hashlib.sha256((HERE / name).read_bytes()).hexdigest()
    assert digest == cert[key], (name, digest, cert[key])

assert cert["verified"] is True
assert result["decision"] == cert["decision"]
assert result["all_input_hashes_match"] is True
assert result["bregman_identity_exact_by_coefficients"] is True
assert result["regular_black_bounce_stationary_in_relative_Palatini_class"] is True
assert result["throat_cancellation_exact"] is True
assert result["coefficient_fit"] is False
assert result["target_Einstein_tensor_accessed"] is False
assert result["direct_BGCE348_BGCE349_radial_strong_curvature_action_typed"] is False
assert result["unconditional_source_selection_of_relative_Palatini_prescription"] is False
print("BQGBH032 verification PASS")
