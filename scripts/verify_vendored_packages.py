#!/usr/bin/env python3
"""Run vendored verifiers and public adapters without the private research Git graph."""

from __future__ import annotations

from decimal import Decimal as D, getcontext
from fractions import Fraction
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[1]
PACKAGES = ROOT / "evidence/packages/calculations"

REPLACED_OR_NONCANONICAL = {
    "BGCE444_TEN_METRIC_SOURCE_TO_THIRTY_FIVE_QUARTIC_SECOND_RESPONSE_GATE_20260925/proof_check.py",
    "BGCE445_AF_QUASILOCAL_CPTP_ALL_SCALE_COMPLETION_GATE_20260925/proof_check.py",
    "BGCE449_PRECONDITIONED_UB612_INTERVAL_RANK35_CERTIFICATE_GATE_20260925/proof_check.py",
    "BGCE499_FISHER_GAIN_AND_OUTER_CUP_TYPED_RECONCILIATION_GATE_20260925/RUN_001/verify.py",
    "BQGSTRAT011_SOURCE_REVERSE_SHEET_PALATINI_COMPLETION_GATE_20260929/RUN_011/verify.py",
}


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def resolve_record(relative: str) -> Path:
    parts = Path(relative).parts
    assert parts and parts[0] == "records", relative
    path = PACKAGES.joinpath(*parts[1:])
    assert path.is_file(), relative
    return path


def checked_json(relative: str, expected_hash: str) -> dict:
    path = resolve_record(relative)
    data = path.read_bytes()
    assert hashlib.sha256(data).hexdigest() == expected_hash, relative
    return json.loads(data)


def adapter_bgce444() -> None:
    path = PACKAGES / "BGCE444_TEN_METRIC_SOURCE_TO_THIRTY_FIVE_QUARTIC_SECOND_RESPONSE_GATE_20260925/proof_check.py"
    module = load_module(path, "public_bgce444")
    docs = {relative: checked_json(relative, digest) for relative, digest in module.INPUTS.items()}
    bgce290 = next(value for key, value in docs.items() if "BGCE290_" in key and key.endswith("RESULT.json"))
    bgce291 = next(value for key, value in docs.items() if "BGCE291_" in key)
    bgce288 = next(value for key, value in docs.items() if "BGCE288_" in key)
    assert bgce290["source_to_causal_Sym2_rank"] == 10
    assert bgce291["algebraic_rank10_Hadamard_Sym2_solder"] == "PASS_CANONICAL_CANDIDATE"
    assert all(record["event_even_plus_theta_odd_combined_rank"] == 10 for record in bgce288["sector_records"])

    U = [[Fraction(x, 2) for x in row] for row in [
        [1, 1, 1, 1], [1, -1, -1, 1], [1, -1, 1, -1], [1, 1, -1, -1]
    ]]
    images = []
    for pair in module.PAIRS:
        matrix = module.basis_matrix(pair)
        images.append(module.quadratic_coefficients(module.mmul(module.mmul(module.transpose(U), matrix), U)))
    solder = [[images[column][row] for column in range(10)] for row in range(10)]
    columns = [module.polynomial_product(images[a], images[b]) for a, b in module.PAIR_PAIRS]
    response = [[columns[column][row] for column in range(55)] for row in range(35)]
    assert module.matrix_rank(solder) == 10
    assert module.matrix_rank(response) == 35


def adapter_bgce445() -> None:
    path = PACKAGES / "BGCE445_AF_QUASILOCAL_CPTP_ALL_SCALE_COMPLETION_GATE_20260925/proof_check.py"
    module = load_module(path, "public_bgce445")
    docs = {relative: checked_json(relative, digest) for relative, digest in module.INPUTS.items()}
    r336 = next(value for key, value in docs.items() if "BGCE336R2" in key)
    r349 = next(value for key, value in docs.items() if "BGCE349_" in key)
    r350 = next(value for key, value in docs.items() if "BGCE350_" in key)
    r444 = next(value for key, value in docs.items() if "BGCE444_" in key)
    assert "Phi_h=exp[h gamma(E-I)]" in r336["decision"]
    assert "converge in operator norm" in r336["decision"]
    assert r349["source_metric_to_instrument_map"]["total_instrument_CPTP"] is True
    assert r349["gluing_and_refinement"]["address_and_collision_refinement_commute"] is True
    assert r350["locality_and_refinement"]["address_and_time_refinement_commute"] is True
    assert r444["gate_decision"]["ten_to_thirty_five_algebraic_capacity"] == "SCOPED_PASS"


def decimal(value: Fraction) -> D:
    return D(value.numerator) / D(value.denominator)


def decimal_inverse(matrix):
    n = len(matrix)
    augmented = [matrix[i][:] + [D(int(i == j)) for j in range(n)] for i in range(n)]
    for column in range(n):
        pivot = max(range(column, n), key=lambda row: abs(augmented[row][column]))
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        value = augmented[column][column]
        assert value
        augmented[column] = [x / value for x in augmented[column]]
        for row in range(n):
            if row != column and augmented[row][column]:
                value = augmented[row][column]
                augmented[row] = [
                    augmented[row][j] - value * augmented[column][j]
                    for j in range(2 * n)
                ]
    return [row[n:] for row in augmented]


def adapter_bgce449() -> None:
    bg448_path = PACKAGES / "BGCE448_ACTUAL_UB612_U4_JETS_TO_SOURCE_CYLINDER_FIFTY_FIVE_COLUMN_HESSIAN_GATE_20260925/proof_check.py"
    bg448 = load_module(bg448_path, "public_bgce448")
    bg448.UB612 = PACKAGES / "UB612_PBM_COVARIANT_SIGMA6_U4_V0_2_PARALLEL4_FOUR_ROOT_GENERATOR_GATE/PBM_COVARIANT_TRANSPORT_JETS_PARTIAL_v1.json"
    bg448.BGCE447 = PACKAGES / "BGCE447_SOURCE_CYLINDER_TO_UB612_PBM_METRIC_SAME_CARRIER_INTERTWINER_GATE_20260925/RESULT.json"

    package = PACKAGES / "BGCE449_PRECONDITIONED_UB612_INTERVAL_RANK35_CERTIFICATE_GATE_20260925"
    certificate = json.loads((package / "PROOF_CERTIFICATE.json").read_text())
    for relative, digest in certificate["source_hashes"].items():
        data = resolve_record(relative).read_bytes()
        assert hashlib.sha256(data).hexdigest() == digest
    carrier = json.loads(bg448.BGCE447.read_text())
    bg448_result = json.loads(
        (PACKAGES / "BGCE448_ACTUAL_UB612_U4_JETS_TO_SOURCE_CYLINDER_FIFTY_FIVE_COLUMN_HESSIAN_GATE_20260925/RESULT.json").read_text()
    )
    assert carrier["gate_decision"]["source_to_actual_UB612_metric_intertwiner"] == "PASS_EXACT_INVERTIBLE"
    assert bg448_result["gate_decision"]["actual_U4_fifty_five_columns"] == "PASS_CONSTRUCTED"
    selected = certificate["selected_columns_zero_based"]
    assert len(selected) == len(set(selected)) == 35

    source = json.loads(bg448.UB612.read_text())
    u4 = source["van_vleck"]["U4_total"]
    midpoint, radius = [], []
    for alpha in bg448.MONS:
        lo, hi = map(Fraction, u4[",".join(map(str, alpha))]["value"])
        midpoint.append((lo + hi) / 2)
        radius.append((hi - lo) / 2)
    midpoint_columns, pairs = bg448.columns(midpoint)
    matrix = [[midpoint_columns[column][row] for column in range(55)] for row in range(35)]

    generators = bg448.source_generators()
    error_columns = []
    for a, left in enumerate(generators):
        for b in range(a, 10):
            right = generators[b]
            operator_columns = []
            for k in range(35):
                unit = [Fraction(int(i == k)) for i in range(35)]
                lr = bg448.rho(left, bg448.rho(right, unit))
                image = lr if a == b else [
                    x + y for x, y in zip(lr, bg448.rho(right, bg448.rho(left, unit)))
                ]
                operator_columns.append(image)
            error_columns.append([
                sum(abs(operator_columns[k][row]) * radius[k] for k in range(35))
                for row in range(35)
            ])
    error = [[error_columns[column][row] for column in range(55)] for row in range(35)]

    center = [[matrix[i][j] for j in selected] for i in range(35)]
    radii = [[error[i][j] for j in selected] for i in range(35)]
    getcontext().prec = 220
    approximate_inverse = decimal_inverse([[decimal(x) for x in row] for row in center])
    preconditioner = [[Fraction(str(x)) for x in row] for row in approximate_inverse]
    comparison = []
    for i in range(35):
        row = []
        for j in range(35):
            residual = Fraction(int(i == j)) - sum(
                preconditioner[i][k] * center[k][j] for k in range(35)
            )
            uncertainty = sum(abs(preconditioner[i][k]) * radii[k][j] for k in range(35))
            row.append(abs(residual) + uncertainty)
        comparison.append(row)
    vector = [D(1) for _ in range(35)]
    for _ in range(500):
        image = [sum(decimal(comparison[i][j]) * vector[j] for j in range(35)) for i in range(35)]
        scale = max(image)
        vector = [value / scale for value in image]
    rational_vector = [Fraction(str(value)) for value in vector]
    exact_upper = max(
        sum(comparison[i][j] * rational_vector[j] for j in range(35)) / rational_vector[i]
        for i in range(35)
    )
    frozen = certificate["exact_Krawczyk_Beeck_Collatz_upper"]
    assert exact_upper == Fraction(int(frozen["numerator"]), int(frozen["denominator"]))
    assert exact_upper < 1
    assert certificate["selected_source_pairs"] == [list(pairs[index]) for index in selected]


def adapter_bqgstrat011() -> None:
    package = PACKAGES / "BQGSTRAT011_SOURCE_REVERSE_SHEET_PALATINI_COMPLETION_GATE_20260929/RUN_011"
    module = load_module(package / "evaluate.py", "public_bqgstrat011")
    matrix = json.loads((package / "SOURCE_MATRIX.json").read_text())
    for source in matrix["sources"]:
        data = resolve_record(source["path"]).read_bytes()
        assert hashlib.sha256(data).hexdigest() == source["sha256"]
    forward = module.word_log((("A", 1), ("B", 1), ("C", -1), ("D", -1)))
    reverse = module.word_log((("D", 1), ("C", 1), ("B", -1), ("A", -1)))
    assert reverse == module.scale(forward, Fraction(-1))
    raw = json.loads((package / "RAW_OUTPUT.json").read_text())
    result = json.loads((package / "RESULT.json").read_text())
    assert raw["exact_free_associative_second_jet"]["legal_reverse_action_factor"] == 1
    assert raw["target_gate"]["passed"] is False
    assert result["incident_class"] == "SCIENTIFIC_OUTCOME"


def run_standard_verifiers() -> int:
    ledger = json.loads((ROOT / "theorems/theorem_evidence_v1.json").read_text())
    evidence_roots = {
        ROOT / relative
        for entry in ledger["entries"]
        for relative in entry.get("evidence_paths", [])
        if relative.startswith("evidence/packages/calculations/")
    }
    scripts = sorted(
        {
            path
            for evidence_root in evidence_roots
            if evidence_root.is_dir()
            for path in evidence_root.rglob("*")
            if path.is_file()
            and path.name in {"verify.py", "proof_check.py", "validate_result.py", "evaluate_theorem.py"}
            and path.relative_to(PACKAGES).as_posix() not in REPLACED_OR_NONCANONICAL
        }
    )
    failures = []
    with tempfile.TemporaryDirectory(prefix="bqg-public-verifiers-") as temporary:
        sandbox = Path(temporary) / "repository"
        shutil.copytree(
            ROOT,
            sandbox,
            ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc", ".DS_Store"),
        )
        for script in scripts:
            relative = script.relative_to(ROOT)
            completed = subprocess.run(
                [sys.executable, str(sandbox / relative)],
                cwd=sandbox,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            )
            if completed.returncode:
                failures.append(
                    {
                        "path": relative.as_posix(),
                        "stderr": completed.stderr[-1000:],
                    }
                )
    assert not failures, json.dumps(failures, indent=2)
    return len(scripts)


def verify_supporting_dependency_inventory() -> int:
    ledger = json.loads((ROOT / "theorems/theorem_evidence_v1.json").read_text())
    supporting = ledger.get("supporting_evidence_paths", [])
    expected_names = {
        "BGCE137_DISCRETE_S4_CHART_TRANSITION_VERSUS_NEAR_IDENTITY_CARTAN_CONNECTION_FACTORING_GATE_20260919",
        "BGCE138_SOURCE_CYLINDER_DIAGONAL_LOCALIZATION_AND_MINIMAL_SMOOTH_CARTAN_COMPLETION_GATE_20260919",
        "BGCE259_ORIENTED_BRAID_COBORDER_TO_CAUSAL_GRADING_INSERTION_IN_ACTUAL_EDGE_ACTION_GATE_20260921",
        "BGCE288_CAUSAL_EVEN_EVENT_PLUS_X21R1_ODD_THETA_FULL_LORENTZ_TANGENT_GATE_20260923",
        "BGCE290_INDEPENDENT_DOUBLED_A_SOURCE_TO_CAUSAL_METRIC_HILBERT_WARD_GATE_20260923",
        "BGCE291_STRESS_WARD_INDEPENDENT_REDERIVATION_AND_SCOPE_RED_TEAM_GATE_20260923",
        "BGCE350_FINITE_SOURCE_CYLINDER_PARENT_TO_LOCAL_HISTORY_DRESSED_TOTAL_WARD_IDENTITY_GATE_20260924",
        "BGCE447_SOURCE_CYLINDER_TO_UB612_PBM_METRIC_SAME_CARRIER_INTERTWINER_GATE_20260925",
        "BGCE448_ACTUAL_UB612_U4_JETS_TO_SOURCE_CYLINDER_FIFTY_FIVE_COLUMN_HESSIAN_GATE_20260925",
        "BQGSTRAT009_SOURCE_AFFINE_PLAQUETTE_SECOND_JET_AND_CHILD_SPLIT_GATE_20260929",
        "UB612_PBM_COVARIANT_SIGMA6_U4_V0_2_PARALLEL4_FOUR_ROOT_GENERATOR_GATE",
    }
    actual_names = {Path(relative).name for relative in supporting}
    assert actual_names == expected_names
    for relative in supporting:
        path = ROOT / relative
        assert path.is_dir()
        assert any(item.suffix == ".py" for item in path.rglob("*.py"))
        assert any(item.name in {"RESULT.json", "PROOF_CERTIFICATE.json"} for item in path.rglob("*.json"))
    return len(supporting)


def verify_failed_attempt_is_not_endpoint() -> None:
    package = PACKAGES / "BGCE499_FISHER_GAIN_AND_OUTER_CUP_TYPED_RECONCILIATION_GATE_20260925"
    attempt = package / "RUN_001"
    assert not (attempt / "RAW_OUTPUT.json").exists()
    ledger_text = (package / "ATTEMPT_LEDGER.md").read_text()
    assert "FAILED_IMPLEMENTATION" in ledger_text
    canonical = package / "RUN_002"
    assert (canonical / "RAW_OUTPUT.json").is_file()
    assert (canonical / "RESULT.json").is_file()


def main() -> None:
    standard = run_standard_verifiers()
    supporting = verify_supporting_dependency_inventory()
    verify_failed_attempt_is_not_endpoint()
    adapter_bgce444()
    adapter_bgce445()
    adapter_bgce449()
    adapter_bqgstrat011()
    print(
        json.dumps(
            {
                "status": "PASS",
                "standard_verifiers_passed": standard,
                "public_adapters_passed": 4,
                "supporting_dependency_packages_verified": supporting,
                "historical_failed_attempt_retained_and_excluded_from_endpoint": 1,
                "private_root_verifiers_replaced_by_public_adapters": 4,
                "private_git_history_required": False
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
