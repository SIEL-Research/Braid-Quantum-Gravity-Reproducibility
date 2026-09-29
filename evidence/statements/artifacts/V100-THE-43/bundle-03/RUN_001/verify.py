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
    "report_sha256": "REPORT.md",
}
for key, name in files.items():
    digest = hashlib.sha256((HERE / name).read_bytes()).hexdigest()
    assert digest == cert[key], (name, digest, cert[key])
assert cert["verified"] is True
assert result["decision"] == cert["decision"]
assert result["current_shape_matches_pure_Palatini_Euler_on_every_nonuniform_internal_node"] is True
assert result["throat_exact_cancellation"] is True
assert result["negative_unit_Petz_minus_raw_contrast_available"] is True
assert result["unconditioned_branch_average_supplies_nonzero_interaction"] is False
assert result["negative_radial_backreaction_coupling_uniquely_selected_by_existing_source_record"] is False
assert result["coefficient_fit"] is False
assert result["target_Einstein_tensor_accessed"] is False
print("BQGBH033 verification PASS")
