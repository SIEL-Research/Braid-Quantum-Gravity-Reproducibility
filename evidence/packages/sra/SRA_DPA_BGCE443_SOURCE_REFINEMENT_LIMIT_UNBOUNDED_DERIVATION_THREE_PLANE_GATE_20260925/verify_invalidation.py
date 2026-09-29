#!/usr/bin/env python3
import json
from pathlib import Path

here = Path(__file__).resolve().parent
invalidation = json.loads((here / "INVALIDATION.json").read_text())
result = json.loads((here / "RESULT.json").read_text())
assert invalidation["candidate_id"] == "BGCE443-R1"
assert invalidation["primary_incident_class"] == "IMPLEMENTATION_PROVENANCE_FAILURE"
assert invalidation["scientific_decision"] == "NONE"
assert invalidation["invalidated_result_path"].endswith("/RESULT.json")
assert result["candidate_id"] == "BGCE443"
print("BGCE443_R1_INVALIDATION_VERIFIED")
