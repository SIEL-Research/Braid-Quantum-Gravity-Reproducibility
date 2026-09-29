#!/usr/bin/env python3
"""Post-run verification and certificate for BGCE308."""
from hashlib import sha256
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    result_path = HERE / "RESULT.json"
    r = json.loads(result_path.read_text())
    assert r["candidate_id"] == "BGCE308"
    assert r["tail_register_capacity"]["exact_orbit_decomposition"] == "17*1 + 28*3 + 4*6 = 125"
    assert r["tail_register_capacity"]["capacity_gate"] == "PASS"
    assert r["tail_state_selection"]["state_selection_gate"] == "FAIL"
    assert len(r["sector_records"]) == 8
    assert all(row["regular_register_copies"] == 4 for row in r["sector_records"])
    assert all(len(row["regular_orbits"]) == 4 for row in r["sector_records"])
    assert all(
        orbit["pointed_restriction"] == "I_6" and not orbit["identity_label_selected"]
        for row in r["sector_records"] for orbit in row["regular_orbits"]
    )
    assert r["collision_and_balance"]["total_stress_Ward_derived"] is False

    verification = {
        "schema": "siel.dpa.bgce308.postrun-verification.v1",
        "candidate_id": "BGCE308",
        "status": "PASS",
        "checks": {
            "orbit_decomposition_all_eight": "PASS",
            "four_regular_registers_all_eight": "PASS",
            "pointed_neutral_uniform_restriction": "PASS",
            "capacity_vs_selection_separated": "PASS",
            "claim_ceiling_fail_closed": "PASS"
        },
        "result_sha256": digest(result_path)
    }
    post = HERE / "POSTRUN_VERIFICATION.json"
    post.write_text(json.dumps(verification, indent=2) + "\n")
    certificate = {
        "schema": "siel.dpa.bgce308.certificate.v1",
        "candidate_id": "BGCE308",
        "verification": "PASS",
        "result_sha256": verification["result_sha256"],
        "postrun_verification_sha256": digest(post),
        "audit_ja_sha256": digest(HERE / "AUDIT_JA.md"),
        "runtime_class": r["runtime_class"],
        "formal_E0_E1_E2": r["formal_E0_E1_E2"]
    }
    (HERE / "CERTIFICATE.json").write_text(json.dumps(certificate, indent=2) + "\n")
    print("BGCE308 POSTRUN VERIFICATION PASS")


if __name__ == "__main__":
    main()
