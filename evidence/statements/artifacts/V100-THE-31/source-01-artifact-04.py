#!/usr/bin/env python3
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
c = json.loads((HERE / "CERTIFICATE.json").read_text())
r = json.loads((HERE / "RESULT.json").read_text())
assert c["candidate_id"] == r["candidate_id"] == "BGCE439"
assert c["derived_extension"]["is_existing_source_operation"] is False
assert c["derived_extension"]["BGCE438_existing_operation_rank_retained"] == 0
assert c["crossed_product"]["exact_matrix_span_rank"] == 64
assert c["crossed_product"]["faithful_regular_representation"] is True
assert c["solution_degree_resolution"]["generation_linear_response_degree_one_rank"] == 3
assert c["matter_content"]["generation_count"] == 3
assert all(value == 0 for value in c["matter_content"]["three_generation_anomalies"].values())
assert c["matter_content"]["global_kernel"] == "Z6"
assert c["Higgs_real_pair"]["orientation_projector_rank"] == 1
assert c["Higgs_real_pair"]["independent_complex_weak_doublets"] == 1
assert c["Yukawa_content"]["all_three_cycles_present"] is True
assert c["Yukawa_content"]["groupoid_average_generation_diagonal_rank"] == 3
assert len(c["all_eight_sector_checks"]) == 8
assert all(item["pass"] for item in c["all_eight_sector_checks"])
assert all(c["decision_tests"].values()) is False  # E10 deliberately preserves the current-source NO-GO.
assert all(value for key, value in c["decision_tests"].items() if key != "E10_UNCHANGED_CURRENT_SOURCE_ALONE_COMPLETE")
assert r["gate_decision"]["BQG_G3_R03_4"].startswith("CLOSED_SCOPED")
assert r["next_gate"] is None
print("BGCE439_VERIFY_DERIVED_GROUPOID_SM_MATTER_SCOPED_PASS")
