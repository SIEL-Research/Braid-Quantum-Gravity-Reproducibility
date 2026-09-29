#!/usr/bin/env python3
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
raw = json.loads((HERE / "RAW_OUTPUT.json").read_text())
result = json.loads((HERE / "RESULT.json").read_text())

assert raw["physical_projector"]["nonzero_momenta_checked"] == 124
assert raw["physical_projector"]["configuration_rank"] == 2
assert raw["physical_symbol_theorem"]["positive_negative_orientation_sheets"] == 24
assert raw["physical_symbol_theorem"]["kernel_dimension_on_every_declared_null_sheet"] == 2
assert raw["raw_block_relation"]["raw_block_repaired"] is False
assert raw["raw_block_relation"]["raw_imbalance_inherited_by_physical_principal_system"] is False
assert raw["source_perfect_schur_scope"]["evaluated_closed_form_full_perfect_Hessian"] is False
assert result["status"].startswith("SCOPED_PASS_SOURCE_PERFECT_PHYSICAL_PRINCIPAL_SYMBOL")
print("BQGSTRAT-013 VERIFY PASS")

