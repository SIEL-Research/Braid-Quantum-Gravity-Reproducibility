#!/usr/bin/env python3
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
raw = json.loads((HERE / "RAW_OUTPUT.json").read_text())
result = json.loads((HERE / "RESULT.json").read_text())

assert raw["id"] == "BQGCTRL-013"
assert all(raw["gates"].values())
assert raw["source_presentations"]["P_free"]["words_equal"] is False
assert raw["source_presentations"]["B_min"]["words_equal"] is True
assert raw["full_chain"]["complete_product_cone_match"] is True
assert len(raw["full_chain"]["branch_ids"]) == 6
assert raw["countermodels"][0]["faithful_on_crossing_subcategory"] is False
assert raw["countermodels"][1]["decision"] == "NO_GO_BY_HOM_SET_INJECTIVITY"
assert result["decision"] == "CLOSED_SCOPED__UNIVERSAL_SOURCE_ONTOLOGY_NO_GO__MINIMAL_FAITHFUL_BRAID_QUOTIENT_PASS"
assert result["full_chain_actual"] == "PASS_RETAINED_FROM_BQGCTRL012"
print("BQGCTRL-013 validation PASS")
