#!/usr/bin/env python3
"""Independent typed-retention validator for the BGCE443 Revision 5 toy witness."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
SHA256 = re.compile(r"^[0-9a-f]{64}$")


def exact_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def exact_fraction_string(value: object) -> bool:
    if not isinstance(value, str):
        return False
    try:
        Fraction(value)
    except (ValueError, ZeroDivisionError):
        return False
    return True


def check_row(row: dict, fields: dict[str, str]) -> None:
    assert set(row) == set(fields), (set(row), set(fields))
    for key, kind in fields.items():
        value = row[key]
        if kind == "int":
            assert exact_int(value), (key, value)
        elif kind == "exact-rational-string":
            assert exact_fraction_string(value), (key, value)
        elif kind == "sha256-hex":
            assert isinstance(value, str) and SHA256.fullmatch(value), (key, value)
        else:
            raise AssertionError(f"unknown field kind {kind}")


def classify(records: list[dict]) -> dict:
    lower = [int(row["action_norm_lower_bound"]) for row in records]
    upper = [int(row["action_norm_upper_bound"]) for row in records]
    differences = [right - left for left, right in zip(lower, lower[1:])]
    unbounded_linear = len(differences) >= 2 and differences[0] > 0 and all(
        value == differences[0] for value in differences
    )
    uniformly_bounded = len(set(upper)) == 1
    return {
        "lower_bounds": lower,
        "upper_bounds": upper,
        "linear_slope": differences[0] if unbounded_linear else 0,
        "unbounded_linear": unbounded_linear,
        "uniformly_bounded": uniformly_bounded,
        "outer_unbounded_pass": unbounded_linear and not uniformly_bounded,
    }


def validate(result: dict, schema: dict) -> dict:
    assert result["schema"] == schema["result_schema"]
    variants = schema["row_variants"]
    positive = result["positive"]
    negative = result["negative_controls"]
    comparator = result["matched_comparator"]

    assert len(positive["stabilization"]) == schema["endpoint_cardinalities"]["positive_directions"]
    assert len(positive["variance_growth"]) == 3
    assert len(positive["action_growth"]) == 3
    for endpoint in positive["stabilization"]:
        rows = endpoint["records"]
        assert len(rows) == variants["stabilization"]["cardinality_per_direction"]
        for row in rows:
            check_row(row, variants["stabilization"]["fields"])
        reconstructed = all(row["residual_frobenius_square"] == 0 for row in rows)
        assert endpoint["pass"] is reconstructed

    for endpoint in positive["variance_growth"]:
        rows = endpoint["records"]
        assert len(rows) == variants["variance"]["cardinality_per_direction"]
        for row in rows:
            check_row(row, variants["variance"]["fields"])
        reconstructed = all(Fraction(row["variance"]) == Fraction(row["expected"]) and Fraction(row["residual"]) == 0 for row in rows)
        assert endpoint["pass"] is reconstructed

    for endpoint in positive["action_growth"]:
        rows = endpoint["records"]
        assert len(rows) == variants["action_growth"]["cardinality_per_direction"]
        for row in rows:
            check_row(row, variants["action_growth"]["fields"])
        exact = all(
            row["implementer_eigenvector_residual_square"] == 0
            and row["action_vector_residual_square"] == 0
            and row["observable_unitarity_residual_frobenius_square"] == 0
            and Fraction(row["action_ratio_square"]) == int(row["action_norm_lower_bound"]) ** 2
            for row in rows
        )
        classification = classify(rows)
        assert endpoint["exact_norm_certificate"] is exact
        assert endpoint["classification"] == classification
        assert endpoint["bounded_inner_excluded"] is (exact and classification["outer_unbounded_pass"])

    bounded = negative["bounded_telescoping"]
    assert len(bounded["records"]) == variants["bounded_action"]["cardinality"]
    for row in bounded["records"]:
        check_row(row, variants["bounded_action"]["fields"])
        assert row["telescoping_residual_frobenius_square"] == 0
    bounded_classification = classify(bounded["records"])
    assert bounded["classification"] == bounded_classification
    assert bounded["outer_unbounded_pass"] is bounded_classification["outer_unbounded_pass"]

    rank_expectations = {
        "zero_seed_rank": 0,
        "single_direction_rank": 1,
        "rank_two": 2,
    }
    assert len(rank_expectations) == schema["endpoint_cardinalities"]["rank_controls"]
    for key, expected in rank_expectations.items():
        endpoint = negative[key]
        assert endpoint["rank"] == expected
        if expected == 0:
            assert endpoint["nonzero_minor"] is None
        else:
            minor = endpoint["nonzero_minor"]
            assert len(minor["rows"]) == expected
            assert len(minor["columns"]) == expected
            assert minor["determinant"] not in {"0", "0+0i", "0-0i"}
    assert positive["rank"]["rank"] == 3
    assert len(positive["rank"]["nonzero_minor"]["rows"]) == 3
    assert len(positive["rank"]["nonzero_minor"]["columns"]) == 3

    positive_close = positive["closability"]
    assert len(positive_close["self_adjoint_local_terms"]) == schema["endpoint_cardinalities"]["closability_positive_terms"]
    close_reconstructed = (
        all(positive_close["self_adjoint_local_terms"])
        and all(positive_close["local_involutions"])
        and all(positive_close["translated_terms_pairwise_commute"])
        and positive_close["translation_covariance_checked"]
    )
    assert positive_close["explicit_group_constructed"] is close_reconstructed
    assert positive_close["pass"] is close_reconstructed

    bounded_close = negative["bounded_telescoping_closability"]
    bounded_close_reconstructed = (
        all(bounded_close["self_adjoint_local_terms"])
        and all(bounded_close["local_involutions"])
        and all(bounded_close["translated_terms_pairwise_commute"])
        and bounded_close["translation_covariance_checked"]
    )
    assert bounded_close["pass"] is bounded_close_reconstructed

    failed_close = negative["closability_hypothesis_failure"]
    failed_close_reconstructed = (
        all(failed_close["self_adjoint_local_terms"])
        and all(failed_close["local_involutions"])
        and all(failed_close["translated_terms_pairwise_commute"])
        and failed_close["translation_covariance_checked"]
    )
    assert failed_close["pass"] is failed_close_reconstructed
    assert failed_close["star_derivation_defect"]["residual_frobenius_square"] > 0

    assert schema["endpoint_cardinalities"]["comparator_transports"] == 2
    hashes: dict[str, str] = {}
    retained = comparator["raw_action_rows_retained"]
    for transport in ("signed", "unsigned"):
        rows = retained[transport]
        assert len(rows) == variants["raw_action_hash"]["cardinality_per_transport"]
        assert {(row["basis_row"], row["basis_column"]) for row in rows} == {
            (row, column) for row in range(4) for column in range(4)
        }
        for row in rows:
            check_row(row, variants["raw_action_hash"]["fields"])
        payload = [row["action_sha256"] for row in rows]
        hashes[transport] = hashlib.sha256(json.dumps(payload, separators=(",", ":")).encode()).hexdigest()
        assert comparator[f"{transport}_raw_action_sha256"] == hashes[transport]

    difference_count = sum(
        left["action_sha256"] != right["action_sha256"]
        for left, right in zip(retained["signed"], retained["unsigned"])
    )
    assert comparator["differing_raw_action_rows"] == difference_count
    matching = comparator["matching_invariants"]
    signed_carrier = comparator["signed_variance"]["pass"]
    unsigned_carrier = comparator["unsigned_variance"]["pass"]
    comparator_reconstructed = all(matching.values()) and signed_carrier and unsigned_carrier and difference_count > 0
    assert comparator["non_structural"] is comparator_reconstructed

    reconstructed_decision = {
        "positive_all_endpoints": (
            all(item["pass"] for item in positive["stabilization"])
            and all(item["pass"] for item in positive["variance_growth"])
            and positive["rank"]["rank"] == 3
            and all(item["bounded_inner_excluded"] for item in positive["action_growth"])
            and positive_close["pass"]
        ),
        "zero_rejected": negative["zero_seed_rank"]["rank"] == 0,
        "rank_two_rejected": negative["rank_two"]["rank"] == 2,
        "single_direction_reports_rank_one": negative["single_direction_rank"]["rank"] == 1,
        "bounded_inner_rejected": not bounded["outer_unbounded_pass"],
        "bounded_negative_still_closable": bounded_close["pass"],
        "closability_hypothesis_failure_rejected": not failed_close["pass"] and failed_close["star_derivation_defect"] is not None,
        "matched_comparator_non_structural": comparator_reconstructed,
    }
    assert result["decision"] == reconstructed_decision
    assert result["all_expected_separations"] is all(reconstructed_decision.values())
    return {
        "schema": "siel.public-calculation.bgce443.r5.retention-validation-result.v1",
        "status": "PASS",
        "typed_row_count": 9 + 12 + 12 + 5 + 32,
        "decision_reconstructed": True,
        "signed_raw_action_sha256": hashes["signed"],
        "unsigned_raw_action_sha256": hashes["unsigned"],
        "differing_raw_action_rows": difference_count,
    }


if __name__ == "__main__":
    result = json.loads((HERE / "WITNESS_RESULT.json").read_text())
    schema = json.loads((HERE / "RAW_ROW_SCHEMA.json").read_text())
    rendered = json.dumps(validate(result, schema), sort_keys=True, indent=2) + "\n"
    if len(sys.argv) == 3 and sys.argv[1] == "--output":
        Path(sys.argv[2]).write_text(rendered)
    elif len(sys.argv) != 1:
        raise SystemExit("usage: validate_retention.py [--output PATH]")
    print(rendered, end="")
