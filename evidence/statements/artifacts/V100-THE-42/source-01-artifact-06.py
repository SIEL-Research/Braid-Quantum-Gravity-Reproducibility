#!/usr/bin/env python3
"""Verify retained BQGCAL-010 artifacts."""

from hashlib import sha256
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


cert = json.loads((HERE / "CERTIFICATE.json").read_text())
raw = json.loads((HERE / "RAW_OUTPUT.json").read_text())
result = json.loads((HERE / "RESULT.json").read_text())
status = json.loads((HERE / "STATUS.json").read_text())

assert digest(HERE / "evaluate_scout.py") == cert["evaluator_sha256"]
assert digest(HERE / "RAW_OUTPUT.json") == cert["raw_output_sha256"]
assert digest(HERE / "RESULT.json") == cert["result_sha256"]
assert all(cert["tests"].values())
assert result["misner_sharp_derivation"]["vacuum_charge"] == "M_MS=(20*pi/3)*r_h"
assert result["source_mass_spectrum"]["mass_from_casimir"] == "M_C=10*pi*sqrt(5)*ell_star*sqrt(C_exc,n)"
assert result["source_mass_spectrum"]["equally_spaced_quantity"] == "M_K^2"
assert result["finite_boundary_conservation"]["fixed_emitted_tail_boundary"] is True
assert result["finite_boundary_conservation"]["additive_total_Ward_charge"] is False
assert result["unconditional_physical_screen_typing_pass"] is False
assert result["absolute_si_calibration_pass"] is False
assert status["status"] == "COMPLETE"
assert raw["decision"] == result["decision"] == cert["decision"] == status["decision"]
print("PASS_VERIFY_BQGCAL_010_X1")
