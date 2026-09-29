#!/usr/bin/env python3
"""BGCE495: exact native-module resource composition for the best G1 actuator."""

from __future__ import annotations

from hashlib import sha256
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SOURCE_COMMIT = "b1b3c7fc77082394c09bdd2546c52f8a963f14f9"
INPUTS = {
    "bgce490_result": REPO / "audits/SRA_DPA_BGCE490_SOURCE_STRUCTURED_LOW_NORMALIZATION_SPECTRAL_FACTOR_OR_DIRECT_QUOTIENT_QSP_GATE_20260925/DPA_SCOUT_001/RESULT.json",
    "bgce491_result": REPO / "audits/SRA_DPA_BGCE491_TYPED_HALMOS_CHEBYSHEV_WALK_TO_SOURCE_WORD_LOCAL_COMPILATION_GATE_20260925/DPA_SCOUT_001/RESULT.json",
    "bgce493_raw": REPO / "audits/SRA_DPA_BGCE493_END_TO_END_FINITE_ACTUATOR_RESOURCE_AND_ERROR_BUDGET_GATE_20260925/DPA_SCOUT_001/RAW_OUTPUT.json",
    "bgce494_result": REPO / "audits/SRA_DPA_BGCE494_MINIMAL_G1_SOURCE_WORD_LCU_NATIVE_COMPILER_GATE_20260925/DPA_SCOUT_001/RESULT.json",
    "bgce494_raw": REPO / "audits/SRA_DPA_BGCE494_MINIMAL_G1_SOURCE_WORD_LCU_NATIVE_COMPILER_GATE_20260925/DPA_SCOUT_001/RAW_OUTPUT.json",
}
EXPECTED_HASHES = {
    "bgce490_result": "640e7d62876b420ee79cab0000c6465d4913ee91e6c2d65e8ac1a0ee0a46769a",
    "bgce491_result": "1bb60b005bd075447a42b0a53a57eb9c1f34d74fb0eeb664ef22c37747108ea9",
    "bgce493_raw": "073345f3b1669704af85d428d6d05e4a0ebcc841f5e8411805d4dd244fe0a7fe",
    "bgce494_result": "301a35c9046eae29ba696ec2753b365145eeb23a5bab26704b4bce9ab7615f5b",
    "bgce494_raw": "7ad8fa523a0f124b03623f8e28061d9b81c6783cd4d1dde4f428f089b2055346",
}
TIMESTAMP = "2026-09-25T22:27:21+09:00"


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def load(name: str) -> dict:
    path = INPUTS[name]
    actual = digest(path)
    assert actual == EXPECTED_HASHES[name], (name, actual)
    return json.loads(path.read_text())


def survival(noisy_gates: int, error: float) -> float:
    return math.exp(noisy_gates * math.log1p(-error))


def log10_survival(noisy_gates: int, error: float) -> float:
    return noisy_gates * math.log10(1.0 - error)


def error_for_survival(noisy_gates: int, target: float) -> float:
    return -math.expm1(math.log(target) / noisy_gates)


def run() -> dict:
    b490 = load("bgce490_result")
    b491 = load("bgce491_result")
    b493 = load("bgce493_raw")
    b494 = load("bgce494_result")
    b494_raw = load("bgce494_raw")

    best = b493["best_case"]
    assert best["mask"] == 0 and best["control"] == "G1"
    assert best["chebyshev_degree"] == 29
    assert best["phase_matched_base_calls"] == 7
    query_count = best["phase_matched_base_calls"] * best["chebyshev_degree"]
    assert query_count == best["H_block_encoding_queries"] == 203
    assert b490["exact_results"]["total_H_block_encoding_query_range"][0] == query_count
    assert b491["exact_results"]["BGCE490_total_H_query_range_preserved"][0] == query_count

    native = b494["exact_results"]
    raw_native = b494_raw["native_G1_over_5_block"]
    assert native["native_cx"] == raw_native["count_ops"]["cx"]
    assert native["native_depth"] == raw_native["depth"]
    assert native["native_size"] == raw_native["size"]
    assert native["opaque_operations_remaining"] == 0
    assert raw_native["opaque_operations_remaining"] == []

    keys = ["native_depth", "native_size", "native_cx", "native_rz", "native_sx", "native_x"]
    subtotal = {key: int(native[key]) * query_count for key in keys}
    cx = subtotal["native_cx"]
    thresholds = {
        "per_CX_error_for_50pct_error_free_survival": error_for_survival(cx, 0.5),
        "per_CX_error_for_90pct_error_free_survival": error_for_survival(cx, 0.9),
    }
    error_examples = {}
    for p in (1e-4, 1e-5, 1e-6):
        error_examples[f"p2_{p:.0e}"] = {
            "log10_error_free_survival": log10_survival(cx, p),
            "error_free_survival": survival(cx, p),
        }

    known_register_floor = (
        native["system_qubits"]
        + native["LCU_address_qubits"]
        + 1
        + best["coefficient_address_bits"]
    )
    known_width_subtotal = (
        native["system_qubits"]
        + best["controller_address_bit_upper_bound_excluding_system_and_workspace"]
        + 1
    )

    return {
        "schema": "siel.dpa.bgce495.raw.v1",
        "scout_id": "DPA-SCOUT-BGCE495-001",
        "gate_id": "BGCE495",
        "source_commit": SOURCE_COMMIT,
        "primary_evidence_status": "Theoretical derivation",
        "selected_case": {
            "mask": best["mask"],
            "control": best["control"],
            "chebyshev_degree": best["chebyshev_degree"],
            "phase_matched_base_calls": best["phase_matched_base_calls"],
            "H_block_encoding_queries": query_count,
            "chebyshev_LCU_branches": 30,
        },
        "inner_native_module": {
            "qubits": native["block_qubits"],
            "depth": native["native_depth"],
            "size": native["native_size"],
            "cx": native["native_cx"],
            "rz": native["native_rz"],
            "sx": native["native_sx"],
            "x": native["native_x"],
            "opaque_operations_remaining": native["opaque_operations_remaining"],
        },
        "optimistic_native_module_subtotal": subtotal,
        "known_register_floor_qubits": known_register_floor,
        "known_width_subtotal_excluding_unreported_workspace_qubits": known_width_subtotal,
        "error_model": "Independent per-CX error; all single-qubit, idle, readout, correlated, control-wrapper and routing errors are set to zero.",
        "error_thresholds": thresholds,
        "error_examples": error_examples,
        "focal_decision": "SCOPED_PASS_FINITE_LOGICAL_ACTUATOR__DIRECT_UNCORRECTED_NISQ_ROUTE_NO_GO_AT_OPTIMISTIC_MODULE_SUBTOTAL",
        "counter_intuition_scan": "The subtotal is not a full transpilation and not an absolute lower bound under unrestricted global resynthesis. It is deliberately optimistic: it counts only 203 already-compiled inner modules and makes Hermitianization, success reflections, coefficient routing, phase matching, measurement and device connectivity free. Those omissions can only make the fixed modular implementation harder, while future global algebraic compression or fault tolerance remains a separate route.",
        "claim_ceiling": "This establishes an exact module-preserving native resource subtotal and an optimistic independent-CX error boundary for the best fixed G1 actuator. It does not provide a full controlled-circuit transpilation, device-specific execution, a universal circuit lower bound, fault tolerance, quantum advantage, physical backreaction or quantum-gravity measurement.",
    }


def write_outputs(raw: dict) -> None:
    hashes = {name: digest(path) for name, path in INPUTS.items()}
    manifest = {
        "schema": "siel.dpa.bgce495.input-manifest.v1",
        "source_commit": SOURCE_COMMIT,
        "inputs": [
            {"name": name, "path": str(path.relative_to(REPO)), "sha256": hashes[name]}
            for name, path in INPUTS.items()
        ],
        "no_randomness": True,
        "no_coefficient_fit": True,
        "no_manual_phase_tuning": True,
    }
    baseline = {
        "schema": "siel.dpa.bgce495.baseline-gate.v1",
        "status": "PASS",
        "checks": {
            "all_input_hashes_match": hashes == EXPECTED_HASHES,
            "best_case_is_mask0_G1": raw["selected_case"]["mask"] == 0 and raw["selected_case"]["control"] == "G1",
            "seven_times_degree29_is_203": 7 * 29 == raw["selected_case"]["H_block_encoding_queries"],
            "inner_native_module_has_no_opaque_operations": raw["inner_native_module"]["opaque_operations_remaining"] == 0,
        },
    }
    result = {
        "schema": "siel.dpa.bgce495.result.v1",
        "scout_id": raw["scout_id"],
        "gate_id": raw["gate_id"],
        "work_package": "BQG-G0-R01.2",
        "status": "SPLIT_SCOPED_PASS_AND_DIRECT_UNCORRECTED_NISQ_ROUTE_NO_GO",
        "primary_evidence_status": raw["primary_evidence_status"],
        "source_commit": SOURCE_COMMIT,
        "decision": "The best fixed G1 actuator remains a finite exact logical construction, but its module-preserving native implementation is already outside a credible direct uncorrected NISQ route before any wrapper cost: 203 inner modules contribute 3,216,332 CX gates and 14,177,723 native operations. In an optimistic independent-CX-only model, 50% error-free survival requires per-CX error at most 2.16e-7.",
        "exact_results": {
            "chebyshev_degree": raw["selected_case"]["chebyshev_degree"],
            "exact_phase_matched_base_calls": raw["selected_case"]["phase_matched_base_calls"],
            "H_block_encoding_queries": raw["selected_case"]["H_block_encoding_queries"],
            "optimistic_native_module_subtotal": raw["optimistic_native_module_subtotal"],
            "known_register_floor_qubits": raw["known_register_floor_qubits"],
            "known_width_subtotal_excluding_unreported_workspace_qubits": raw["known_width_subtotal_excluding_unreported_workspace_qubits"],
            **raw["error_thresholds"],
            "coefficient_fit": False,
            "manual_phase_tuning": False,
        },
        "programme_effect": {
            "BQG-G0-R01.2": "UNCHANGED_CLOSED_SCOPED_FULL_LOGICAL_ACTUATOR_NATIVE_BOUNDARY_STRENGTHENED",
            "finite_exact_logical_actuator": "RETAINED_SCOPED_PASS",
            "direct_uncorrected_current_NISQ_route": "NO_GO_AT_OPTIMISTIC_MODULE_SUBTOTAL",
            "fault_tolerant_or_new_compression_route": "OPEN",
        },
        "counter_intuition": raw["counter_intuition_scan"],
        "next_gate": "BGCE496_SOURCE_SPECTRAL_MINIMAL_WITNESS_CIRCUIT_COMPRESSION_GATE",
        "claim_ceiling": raw["claim_ceiling"],
    }
    status = {
        "schema": "siel.dpa.bgce495.status.v1",
        "scout_id": raw["scout_id"],
        "status": "COMPLETE",
        "decision": result["status"],
        "timestamp": TIMESTAMP,
    }
    execution = {
        "schema": "siel.dpa.bgce495.execution-log.v1",
        "command": "python3 evaluate_scout.py --write",
        "timestamp": TIMESTAMP,
        "exit_status": 0,
        "random_seed": None,
        "notes": "Exact integer composition and analytic independent-error inversion only; no giant circuit materialization or external QPU call.",
    }
    report = f"""# BGCE495 結果

## 判定

**SCOPED PASS / direct uncorrected NISQ route NO-GO。** BGCE490の最良`G1` full actuatorは有限なexact logical circuitとして維持される。しかしBGCE494で実測したinner native moduleだけを`203`回並べる楽観的subtotalで、既に`3,216,332 CX`、全native operation `14,177,723`に達する。

## Exact composition

- Chebyshev degree: `29`
- exact phase-matched base calls: `7`
- H-block query: `7 * 29 = 203`
- 1 inner module: 11 qubits、depth `35,064`、size `69,841`、`15,844 CX`
- module subtotal depth: `{raw['optimistic_native_module_subtotal']['native_depth']:,}`
- module subtotal size: `{raw['optimistic_native_module_subtotal']['native_size']:,}`
- module subtotal CX: `{raw['optimistic_native_module_subtotal']['native_cx']:,}`
- known simultaneous register floor: `{raw['known_register_floor_qubits']}` qubits
- unreported workspaceを除くknown-width subtotal: `{raw['known_width_subtotal_excluding_unreported_workspace_qubits']}` qubits

このsubtotalはHermitianization control、success reflection、30-branch coefficient routing、exact phase matching、measurement、device connectivityをすべて無料とした値であり、full transpiled gate countではない。

## Error boundary

独立なper-CX error `p2`だけを残し、他の全errorを0とする最も楽観的なmodelでも、全CXがerror-freeである確率を50%以上にするには

```text
p2 <= {raw['error_thresholds']['per_CX_error_for_50pct_error_free_survival']:.12g}
```

が必要である。90%以上には`{raw['error_thresholds']['per_CX_error_for_90pct_error_free_survival']:.12g}`以下が必要になる。

- `p2=1e-4`: log10 survival `{raw['error_examples']['p2_1e-04']['log10_error_free_survival']:.3f}`
- `p2=1e-5`: log10 survival `{raw['error_examples']['p2_1e-05']['log10_error_free_survival']:.3f}`
- `p2=1e-6`: survival `{raw['error_examples']['p2_1e-06']['error_free_survival']:.6f}`

single-qubit、idle、readout、correlated errorを無視しているため、これは実機に有利な境界である。

## 科学的意味

量子エンジンの有限性は維持されるが、full exact actuatorをそのまま現在の未訂正QPUへ投入する経路は採らない。次は大胆な圧縮仮説として、full unitary全体ではなくBraid固有のsource spectral witnessだけを読む最小回路へ落とす。

## Counter-intuition

この結果はunrestricted global resynthesisに対する普遍的gate-count下限ではない。将来の代数的圧縮、fault-tolerant implementation、analog realizationは排除しない。一方、固定したBGCE490-494 modular constructionについてはwrapperを無料としてなお数百万CXなので、直接NISQ投入を続ける合理性はない。

## 次

`BGCE496_SOURCE_SPECTRAL_MINIMAL_WITNESS_CIRCUIT_COMPRESSION_GATE`。full actuatorを再現する代わりに、標準QM+device noiseとBraid source dynamicsを分ける最小spectral witnessを構成する。新しいwork-package IDは作らず、既存`BQG-G0-R01.2`のimplementation evidenceとして継続する。

## Claim ceiling

{raw['claim_ceiling']}
"""
    ledger = """# BGCE495 iteration ledger

| Iteration | Input | Action | Result | Decision |
|---|---|---|---|---|
| `DPA_SCOUT_001` | Pinned BGCE490/491/493/494 artifacts | Exact best-case query/native-module composition; analytic error inversion | `203` queries, `3,216,332 CX` optimistic subtotal; 50% survival requires `p2 <= 2.16e-7` | `SCOPED_PASS / DIRECT_UNCORRECTED_NISQ_ROUTE_NO_GO` |
"""

    outputs = {
        "RAW_OUTPUT.json": raw,
        "RESULT.json": result,
        "INPUT_MANIFEST.json": manifest,
        "BASELINE_GATE.json": baseline,
        "STATUS.json": status,
        "EXECUTION_LOG.json": execution,
    }
    for name, payload in outputs.items():
        (HERE / name).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    (HERE / "REPORT_JA.md").write_text(report)
    (HERE / "ITERATION_LEDGER.md").write_text(ledger)


if __name__ == "__main__":
    raw = run()
    import sys
    if "--write" in sys.argv:
        write_outputs(raw)
    print(json.dumps(raw, indent=2, sort_keys=True))
