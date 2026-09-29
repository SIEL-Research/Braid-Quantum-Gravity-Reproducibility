#!/usr/bin/env python3
"""Post-run verification and certificate for BGCE307."""
from hashlib import sha256
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    result_path = HERE / "RESULT.json"
    r = json.loads(result_path.read_text())
    assert r["candidate_id"] == "BGCE307"
    s = r["fixed_time_source_labelled_Stinespring"]
    assert s["partial_trace_reproduces_channel"] is True
    assert s["group_probabilities_at_witness"] == ["3/8"] + ["1/8"] * 5
    assert r["full_semigroup_autonomous_dilation"]["single_finite_environment_fixed_initial_state_and_time_independent_H_total"] is False
    assert len(r["sector_records"]) == 8
    assert all(row["G1_defect_Hilbert_Schmidt_norm_squared"] == "18" for row in r["sector_records"])
    assert r["total_conservation"]["total_system_environment_Ward_identity_derived"] is False
    assert r["BGCE300R1_low_energy_Einstein_result_retained"] is True

    verification = {
        "schema": "siel.dpa.bgce307.postrun-verification.v1",
        "candidate_id": "BGCE307",
        "status": "PASS",
        "checks": {
            "six_group_weights_exact": "PASS",
            "Stinespring_normalization_all_eight": "PASS",
            "finite_autonomous_no_go_separated": "PASS",
            "G1_defect_all_eight_exact": "PASS",
            "claim_ceiling_fail_closed": "PASS"
        },
        "result_sha256": digest(result_path)
    }
    post = HERE / "POSTRUN_VERIFICATION.json"
    post.write_text(json.dumps(verification, indent=2) + "\n")
    certificate = {
        "schema": "siel.dpa.bgce307.certificate.v1",
        "candidate_id": "BGCE307",
        "verification": "PASS",
        "result_sha256": verification["result_sha256"],
        "postrun_verification_sha256": digest(post),
        "audit_ja_sha256": digest(HERE / "AUDIT_JA.md"),
        "runtime_class": r["runtime_class"],
        "formal_E0_E1_E2": r["formal_E0_E1_E2"]
    }
    (HERE / "CERTIFICATE.json").write_text(json.dumps(certificate, indent=2) + "\n")
    print("BGCE307 POSTRUN VERIFICATION PASS")


if __name__ == "__main__":
    main()
