#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PACKET = HERE / "PBM_COVARIANT_TRANSPORT_JETS_PARTIAL_v1.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    p = json.loads(PACKET.read_text())
    result = {
        "schema": "ub612.pbm-covariant-sigma6-u4-v0-2-parallel4-four-root-generator-gate.v1",
        "date": "2026-09-13",
        "status": p["status"],
        "primary_evidence_status": "Actual interval transport-jet computation; partial pass with an exact regression first-fail",
        "scientific_layer": "mathematical formulation and computational QFT certification",
        "executed": {
            "actual_sigma_through_degree_6_in_frozen_gamma0_spatial_frame": False,
            "actual_U_through_degree_4_center_and_four_roots": True,
            "actual_v0_through_degree_2_center_and_four_roots": True,
            "parallel_horizontal_operator_through_degree_4": False,
            "complete_UB611_callback": False,
            "stress_or_face_target_read": False,
        },
        "actual_output": {
            "packet": PACKET.name,
            "sha256": sha(PACKET),
            "coefficient_counts": p["coefficient_counts"],
            "v0_recurrence_interval_residual_contains_zero": p["v0"]["recurrence_interval_residual_contains_zero_all_coefficients_and_roots"],
            "root_direction_order": p["root_direction_order"],
        },
        "route_reduction": {
            "spacetime_midpoint_identity": "For endpoints Exp_m^g(+-y/2), sigma=g_m(y,y)/2 exactly.",
            "why_it_does_not_close_actual_sigma6": "The frozen state frame uses the gamma0 spatial exponential midpoint at equal Cauchy time. With nonzero extrinsic curvature this is not generally the four-dimensional spacetime exponential midpoint.",
            "U4_and_v0_2": "closed from the saved actual Riemann, Ricci, nabla Ricci and nabla2 Ricci interval tensors, including p1,p2,p3,H derivatives",
        },
        "first_fail": {
            "id": "PBM_SPACETIME_TO_FROZEN_SPATIAL_MIDPOINT_ADAPTER_v1",
            "missing": p["sigma6_parallel4_first_fail"]["missing_object"],
            "why_not_zero": p["sigma6_parallel4_first_fail"]["why_curvature_values_alone_do_not_close_it"],
            "exact_regression": p["sigma6_parallel4_first_fail"]["fixture_detects_omission"],
            "consequence": "Setting the connection/parallel term to zero would fail the saved UB516 quartic regression by trace(S)/192.",
        },
        "next_gate": "UB613_PBM_SPACETIME_TO_FROZEN_SPATIAL_MIDPOINT_ADAPTER_GATE_v1",
        "claim_ceiling": p["claim_ceiling"],
        "input_hashes": p["input_hashes"],
    }
    (HERE / "RESULT.json").write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
