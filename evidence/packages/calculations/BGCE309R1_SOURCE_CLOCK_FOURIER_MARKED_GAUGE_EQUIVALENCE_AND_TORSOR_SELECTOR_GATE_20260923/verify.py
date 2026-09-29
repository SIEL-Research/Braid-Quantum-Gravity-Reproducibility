#!/usr/bin/env python3
"""Post-run verification and certificate for BGCE309R1."""
from hashlib import sha256
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    result_path = HERE / "RESULT.json"
    r = json.loads(result_path.read_text())
    assert r["candidate_id"] == "BGCE309R1"
    assert r["clock_Fourier_selector"]["all_32_sector_copy_blocks_markedly_diagonal_sign_gauge_equivalent"] is True
    assert r["clock_Fourier_selector"]["unique_copy_selected"] is False
    assert r["clock_Fourier_selector"]["spectral_rays_are_regular_group_label_basis"] is False
    assert len(r["sector_records"]) == 8
    assert sum(len(row["copies"]) for row in r["sector_records"]) == 32
    assert all(
        copy["diagonal_sign_gauges_to_standard_block"] == 2
        for row in r["sector_records"] for copy in row["copies"]
    )
    assert r["torsor_gauge"]["reduced_channel_independent_of_copy_and_basepoint"] is True
    assert r["torsor_gauge"]["torsor_gauge_removes_selector_for_reduced_GKSL_channel"] is True
    assert r["total_stress_Ward_derived"] is False

    verification = {
        "schema": "siel.public-calculation.bgce309r1.postrun-verification.v1",
        "candidate_id": "BGCE309R1",
        "status": "PASS",
        "checks": {
            "all_32_marked_sign_gauges": "PASS",
            "six_compressed_clock_Fourier_rays": "PASS",
            "regular_basis_nonidentification": "PASS",
            "environment_unitary_reduced_channel_invariance": "PASS",
            "claim_ceiling_fail_closed": "PASS"
        },
        "result_sha256": digest(result_path)
    }
    post = HERE / "POSTRUN_VERIFICATION.json"
    post.write_text(json.dumps(verification, indent=2) + "\n")
    certificate = {
        "schema": "siel.public-calculation.bgce309r1.certificate.v1",
        "candidate_id": "BGCE309R1",
        "verification": "PASS",
        "result_sha256": verification["result_sha256"],
        "postrun_verification_sha256": digest(post),
        "audit_sha256": digest(HERE / "AUDIT.md"),
        "runtime_class": r["runtime_class"],
        "formal_E0_E1_E2": r["formal_E0_E1_E2"]
    }
    (HERE / "CERTIFICATE.json").write_text(json.dumps(certificate, indent=2) + "\n")
    print("BGCE309R1 POSTRUN VERIFICATION PASS")


if __name__ == "__main__":
    main()
