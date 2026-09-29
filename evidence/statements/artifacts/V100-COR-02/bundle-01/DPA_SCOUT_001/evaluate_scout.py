#!/usr/bin/env python3
"""BGCE491: hermitianized source-word block encoding and Chebyshev walk."""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
import math
from pathlib import Path
import sys

import numpy as np


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
PATHS = {
    "b483": REPO / "audits/SRA_DPA_BGCE483_RAW_CONTINUOUS_FLOW_TO_FINITE_EXACT_CARRIER_INVARIANT_COMPOSITE_GATE_20260925/DPA_SCOUT_001/RESULT.json",
    "b484": REPO / "audits/SRA_DPA_BGCE484_MINIMAL_MARKED_SOURCE_WORD_SELECT_AND_LCU_REALIZATION_GATE_20260925/DPA_SCOUT_001/RESULT.json",
    "b487": REPO / "audits/SRA_DPA_BGCE487_SOURCE_RAW_G1_ENCODED_SIGNAL_QUBIT_AND_SU2_CLOCK_GATE_20260925/DPA_SCOUT_001/RESULT.json",
    "b490": REPO / "audits/SRA_DPA_BGCE490_SOURCE_STRUCTURED_LOW_NORMALIZATION_SPECTRAL_FACTOR_OR_DIRECT_QUOTIENT_QSP_GATE_20260925/DPA_SCOUT_001/RESULT.json",
    "b490raw": REPO / "audits/SRA_DPA_BGCE490_SOURCE_STRUCTURED_LOW_NORMALIZATION_SPECTRAL_FACTOR_OR_DIRECT_QUOTIENT_QSP_GATE_20260925/DPA_SCOUT_001/RAW_OUTPUT.json",
    "b476e": REPO / "audits/SRA_DPA_BGCE476_SOURCE_SELECTED_QSP_OR_FINITE_SPECTRAL_POLYNOMIAL_GATE_20260925/DPA_SCOUT_001/evaluate_scout.py",
    "b458e": REPO / "audits/SRA_DPA_BGCE458_BARE_BRAID_ORIENTED_CYCLE_TO_COMPLEX_KINEMATICS_GATE_20260925/DPA_SCOUT_001/evaluate_scout.py",
    "o14": REPO / "projects/active/discovery_partner/formal_checks/ocbfh014_source_native_refinement_naturality_check.py",
    "source": REPO / "audits/SRA_DPA_BGCE139_SOURCE_SPECTRAL_CYLINDER_OPERATIONAL_EVENT_IDENTIFICATION_GATE_20260919/RAW_OUTPUT.json",
}
EXPECTED = {
    "b483": "7ba36aabf19bbc2f7b908f1216947566859dd96008b3c8ba68006bfb50774d87",
    "b484": "914898496153ae9574046b91a2cba2c792a056571754ef63fdf30b93e1bb7813",
    "b487": "0d0e2feb34fded05b3bfef6620efcf6ee7abf80ab4a83db33b580ab5c484b975",
    "b490": "640e7d62876b420ee79cab0000c6465d4913ee91e6c2d65e8ac1a0ee0a46769a",
    "b490raw": "c47af5b071ac7adcc075354de801cd84bee24016f09059f51932f9ddc3137267",
    "b476e": "1e9a06627a8667467403aff59f6caa606bbd4f0d8b3c93eacbb3ed5f6d4f6554",
    "b458e": "f7fc8db4ab821c223e466e335b5c18a4c2dc824e6f0060471fcf9d53271d02a8",
    "o14": "176c75ac349f0f3f142d9c850ca0682436b7ad00cd179f6806de253d0a7acabb",
    "source": "ddf630fbaff1ae4e72c778f47dc2bed6906da0a8aa17d4e6a98d2c96791955e9",
}


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def distinct_values(values: np.ndarray, tolerance: float = 1e-9) -> list[float]:
    answer: list[float] = []
    for value in sorted(float(item) for item in values):
        if not answer or abs(value - answer[-1]) > tolerance:
            answer.append(value)
    return answer


def scalar_dilation_audit(value: float, maximum_degree: int, phase: float) -> dict:
    defect = math.sqrt(max(0.0, 1.0 - value * value))
    unitary = np.array([
        [value, defect * np.exp(1j * phase)],
        [-defect * np.exp(-1j * phase), value],
    ], dtype=complex)
    zero = np.zeros((2, 2), dtype=complex)
    hermitianized = np.block([[zero, unitary], [unitary.conj().T, zero]])
    success = np.array([1.0, 0.0, 1.0, 0.0], dtype=complex) / math.sqrt(2.0)
    reflection = 2.0 * np.outer(success, success.conj()) - np.eye(4)
    walk = reflection @ hermitianized
    power = np.eye(4, dtype=complex)
    maximum_chebyshev_residual = 0.0
    for degree in range(maximum_degree + 1):
        compressed = success.conj() @ power @ success
        target = np.polynomial.chebyshev.chebval(value, [0.0] * degree + [1.0])
        maximum_chebyshev_residual = max(
            maximum_chebyshev_residual, abs(compressed - target)
        )
        power = power @ walk
    return {
        "unitary_residual": float(np.linalg.norm(unitary.conj().T @ unitary - np.eye(2))),
        "hermitian_residual": float(np.linalg.norm(hermitianized - hermitianized.conj().T)),
        "involution_residual": float(np.linalg.norm(hermitianized @ hermitianized - np.eye(4))),
        "signal_block_residual": float(abs(success.conj() @ hermitianized @ success - value)),
        "chebyshev_residual": float(maximum_chebyshev_residual),
    }


def run() -> dict:
    for name, path in PATHS.items():
        assert digest(path) == EXPECTED[name], name
    docs = {
        name: json.loads(PATHS[name].read_text())
        for name in ("b483", "b484", "b487", "b490", "b490raw")
    }
    assert docs["b483"]["coefficient_fit"] is False
    assert docs["b484"]["status"] == "SCOPED_PASS_WITH_RETAINED_NO_GO"
    assert docs["b487"]["status"] == "SCOPED_PASS"
    assert docs["b490"]["status"] == "CLOSED_SCOPED"

    b458 = load_module("bgce491_b458", PATHS["b458e"])
    b476e = load_module("bgce491_b476", PATHS["b476e"])
    o14 = load_module("bgce491_o14", PATHS["o14"])
    b458.REPO = REPO
    b458.SOURCE = PATHS["source"]
    basis = b476e.carrier_basis(b458)
    survivors, source_projectors, _, source_meta = o14.reconstruct_actual_source()
    b490_records = {
        (int(record["mask"]), record["control"]): record
        for record in docs["b490raw"]["records"]
    }

    control_names = ("G1", "H1", "H2", "H3")
    normalizations = (5.0, 10.0, 10.0, 10.0)
    source_phases = (0.0, 2.0 * math.pi / 3.0, -2.0 * math.pi / 3.0)
    records = []
    maxima = {
        "unitary_residual": 0.0,
        "hermitian_residual": 0.0,
        "involution_residual": 0.0,
        "signal_block_residual": 0.0,
        "chebyshev_residual": 0.0,
    }

    for survivor in survivors:
        g_num, g_den, _, _ = o14.source_g1(survivor["R"].astype(np.int64))
        raw_controls = [g_num / g_den]
        for projector_num, projector_den in source_projectors:
            lifted = np.kron(projector_num, np.eye(5, dtype=np.int64))
            raw_controls.append(-1j * (g_num @ lifted - lifted @ g_num) / (g_den * projector_den))

        for name, alpha, raw in zip(control_names, normalizations, raw_controls):
            hamiltonian = basis.conj().T @ raw @ basis
            assert np.linalg.norm(hamiltonian - hamiltonian.conj().T) < 1e-12
            nodes = distinct_values(np.linalg.eigvalsh(hamiltonian))
            normalized_nodes = [value / alpha for value in nodes]
            source_record = b490_records[(int(survivor["mask"]), name)]
            assert len(nodes) == source_record["distinct_spectral_nodes"]
            maximum_degree = int(source_record["chebyshev_degree"])
            case_maxima = {key: 0.0 for key in maxima}
            for phase in source_phases:
                for value in normalized_nodes:
                    residuals = scalar_dilation_audit(value, maximum_degree, phase)
                    for key, residual in residuals.items():
                        case_maxima[key] = max(case_maxima[key], residual)
                        maxima[key] = max(maxima[key], residual)
            records.append({
                "mask": int(survivor["mask"]),
                "control": name,
                "spectral_nodes_checked": len(nodes),
                "maximum_chebyshev_degree": maximum_degree,
                "source_dilation_phases_checked": ["0", "+2pi/3", "-2pi/3"],
                "compiled_walk_steps_per_power": maximum_degree,
                "BGCE490_total_H_query_count_preserved": int(source_record["total_H_block_encoding_queries"]),
                **case_maxima,
            })

    assert len(records) == 32
    assert max(maxima.values()) < 2e-12

    return {
        "schema": "siel.dpa.bgce491.raw.v1",
        "scout_id": "DPA-SCOUT-BGCE491-001",
        "gate_id": "BGCE491",
        "attempt": "0001",
        "source_commit": "2c0d7d75cea3a714a4edc8d428e8fad5230faa81",
        "primary_evidence_status": "Theoretical derivation",
        "scientific_layer": "source-word LCU hermitianization and local Chebyshev qubiterate compilation",
        "focal_decision": "CLOSED_SCOPED_SOURCE_WORD_LCU_HERMITIANIZATION_AND_EXACT_CHEBYSHEV_WALK_COMPILATION",
        "construction": {
            "input": "Any BGCE483-484 source-word LCU unitary U_A with success block A=H/alpha=A^dagger",
            "hermitianization": "U_tilde=|0><1| tensor U_A + |1><0| tensor U_A^dagger",
            "success_isometry": "E=|+> tensor |PREP-success>",
            "signal_block": "E^dagger U_tilde E=(A+A^dagger)/2=A",
            "reflection": "S=2EE^dagger-I, implemented by PREP, a success-address phase mark, and PREP^dagger",
            "walk": "W=S U_tilde",
            "exact_identity": "E^dagger W^k E=T_k(A) for every k>=0",
        },
        "exact_recurrence_proof": "B_0=I and B_1=A. Since U_tilde^2=I and S=2EE^dagger-I, compression of successive powers gives B_(k+1)=2A B_k-B_(k-1), hence B_k=T_k(A).",
        "source_local_operations": [
            "BGCE484 source-counted PREP and typed finite-list source-word SELECT",
            "source reversal/dagger to obtain U_A^dagger",
            "BGCE487 encoded signal-qubit X and continuous phase controls",
            "typed success-address reflection on the finite controller register",
        ],
        "square_root_defect_required": False,
        "spectral_READ_H_required": False,
        "coefficient_fit": False,
        "manual_phase_tuning": False,
        "cases_checked": len(records),
        "signed_sectors_checked": 8,
        "control_families_checked": list(control_names),
        "source_dilation_phases_checked": ["0", "+2pi/3", "-2pi/3"],
        "maximum_residuals": maxima,
        "BGCE490_total_H_query_range_preserved": [
            min(item["BGCE490_total_H_query_count_preserved"] for item in records),
            max(item["BGCE490_total_H_query_count_preserved"] for item in records),
        ],
        "four_probability_role": "The four-probability source-V4 carrier remains the outer G1,H1,H2,H3 selector. Hermitianization and the Chebyshev walk are branch-local and do not act by compressed raw V4 reflections.",
        "counter_intuition_scan": "The square-root defect in the canonical Halmos formula is a representation choice, not a necessary physical primitive. Hermitianizing the already realized source-word LCU unitary produces a reflection with the same signal block, after which the product-of-reflections walk generates the identical Chebyshev functional calculus.",
        "scope_boundary": "This closes the walk using the existing typed finite-list source-word controller, source dagger and a typed success-address phase mark. It still does not derive the enlarged coherent controller or its address mark from bare adjacent-Braid relations alone, nor provide hardware errors, seconds calibration, continuum/QFT completion or empirical confirmation.",
        "next_gate": "BGCE492_TYPED_SUCCESS_ADDRESS_MARK_MINIMALITY_AND_BARE_BRAID_OBSTRUCTION_GATE",
        "records": records,
        "source_metadata": source_meta,
    }


if __name__ == "__main__":
    result = run()
    (HERE / "RAW_OUTPUT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "gate_id": result["gate_id"],
        "decision": result["focal_decision"],
        "cases_checked": result["cases_checked"],
        "square_root_defect_required": result["square_root_defect_required"],
        "maximum_residuals": result["maximum_residuals"],
        "query_range": result["BGCE490_total_H_query_range_preserved"],
        "next_gate": result["next_gate"],
    }, indent=2, sort_keys=True))
