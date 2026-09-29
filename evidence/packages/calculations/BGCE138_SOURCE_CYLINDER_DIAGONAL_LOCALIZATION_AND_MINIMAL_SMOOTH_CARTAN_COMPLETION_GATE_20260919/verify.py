#!/usr/bin/env python3
"""Verify BGCE138 retained exact result."""

from pathlib import Path
import importlib.util
import json
import sys


HERE = Path(__file__).resolve().parent


def load_module():
    spec = importlib.util.spec_from_file_location("bgce138_evaluate", HERE / "evaluate.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    evaluator = load_module()
    regenerated = evaluator.run()
    stored = json.loads((HERE / "RAW_OUTPUT.json").read_text())
    assert regenerated == stored
    assert stored["source_marker_MASA_gate"]["actual_signed_sectors"] == 8
    assert all(record["generated_algebra_is_MASA"] for record in stored["source_marker_MASA_gate"]["sector_records"])
    assert stored["spectral_cylinder_gate"]["four_factor_epoch_atoms"] == 625
    assert stored["spectral_cylinder_gate"]["quotient_space"] == "[0,1]^4"
    assert stored["minimal_smooth_completion_gate"]["independent_compactly_supported_delta_e_components"] == 16
    assert stored["minimal_smooth_completion_gate"]["independent_compactly_supported_delta_Gamma_components"] == 64
    assert stored["dependency_effect"]["physical_event_identification_source_derived"] is False
    assert stored["CGR_effect"]["CGR_removed_unconditionally"] is False
    assert stored["MMR_effect"] == "none"
    print("BGCE138 VERIFY PASS")


if __name__ == "__main__":
    main()
