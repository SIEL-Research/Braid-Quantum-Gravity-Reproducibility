#!/usr/bin/env python3
"""Lightweight stored-result verification for BGCE238."""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
raw = json.loads((HERE / "RAW_OUTPUT.json").read_text())
result = json.loads((HERE / "RESULT.json").read_text())

expected = ["012", "01|2", "02|1", "12|0", "0|1|2"]
assert len(raw["sector_records"]) == 8
assert raw["admissible_partitions_preserving_exact_packet_all_eight"] == ["012"]
assert raw["full_corner_uniquely_selected"] is True
for sector in raw["sector_records"]:
    assert [item["partition"] for item in sector["partitions"]] == expected
    assert sector["partitions"][0]["fixes_entire_fixed_packet"] is True
    for item in sector["partitions"][1:]:
        assert item["fixes_entire_fixed_packet"] is False
        assert item["first_changed_operator"]["operator"] == "H_cap"
        assert item["first_changed_operator"]["cross_block_residual_nonzero"] is True
assert result["MMR2_braid_only_removed_within_declared_fixed_model"] is True
assert result["remaining_full_corner_nondemolition_law_for_matter_action"] is False
print("BGCE238 STORED VERIFY PASS")
