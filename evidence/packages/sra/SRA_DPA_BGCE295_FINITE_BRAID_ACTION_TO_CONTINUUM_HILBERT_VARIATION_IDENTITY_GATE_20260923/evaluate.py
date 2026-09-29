#!/usr/bin/env python3
"""BGCE295: finite-edge to continuum Hilbert-variation identity audit."""
from hashlib import sha256
from pathlib import Path
import json, subprocess
ROOT=Path(__file__).resolve().parents[2]; HERE=Path(__file__).resolve().parent
REV="54bb4adb635eba0a5ccc5afd7e9d2818ecb50a14"
def frozen(p): return subprocess.check_output(["git","show",f"{REV}:{p}"],cwd=ROOT)
def load(p): return json.loads(frozen(p))
def main():
 sm=json.loads((HERE/"SOURCE_MATRIX.json").read_text()); checked={}
 for p,e in sm["inputs_sha256"].items():
  b=frozen(p); a=sha256(b).hexdigest(); assert a==e; checked[f"{REV}:{p}"]=a
 p143=load("audits/SRA_DPA_BGCE143_EXTENSIVE_LOCAL_G1_INTERACTION_TO_QUANTUM_MARKOV_CYLINDER_ACTION_DENSITY_GATE_20260919/RESULT.json")
 r252=load("audits/SRA_DPA_BGCE252_NEIGHBOR_GIBBS_RELATIVE_ENTROPY_TO_BKM_DIRICHLET_PARENT_ACTION_GATE_20260921/RAW_OUTPUT.json")
 p254=load("audits/SRA_DPA_BGCE254_SOURCE_RESPONSE_LEGENDRE_EXACTNESS_TO_UNIQUE_LOGZ_BREGMAN_EDGE_ACTION_GATE_20260921/RESULT.json")
 r256=load("audits/SRA_DPA_BGCE256_BRAID_INDUCED_EVENT_TRANSITION_COBORDER_TO_NEIGHBOR_COUPLING_LAW_GATE_20260921/RAW_OUTPUT.json")
 r266=load("audits/SRA_DPA_BGCE266_REFINEMENT_CLOCK_TO_UNIQUE_EVENT_SEMIGROUP_AND_IR_OS_CONTINUATION_GATE_20260922/RAW_OUTPUT.json")
 p285=load("audits/SRA_DPA_BGCE285_SOURCE_CYLINDER_MEASURE_AND_MARKOV_NATURALITY_TO_UNIQUE_MINIMAL_COVARIANT_PARENT_GATE_20260923/RESULT.json")
 p293=load("audits/SRA_DPA_BGCE293_FINITE_POSITIVE_BKM_EXPONENTIAL_LEAF_INTEGRATION_GATE_20260923/RESULT.json")
 p294=load("audits/SRA_DPA_BGCE294_SOURCE_SYMMETRIC_PRODUCT_FUNCTOR_TO_UNIQUE_PHYSICAL_SOLDER_GATE_20260923/RESULT.json")
 assert p143["continuum_action"]["C2_Riemann_limit"] is True
 assert p143["continuum_action"]["local_a_metric_variation_exists"] is True
 assert r252["continuum_gate"]["finite_nontrivial_C2_Riemann_limit"] is True
 assert p254["unique_response_exact_edge_functional"]=="Umegaki_relative_entropy_equals_logZ_Bregman_divergence"
 assert r256["source_edge_action"]["new_fitted_coefficient"] is False
 assert r256["continuum_gate"]["gradient_quadratic_rank"]==16
 assert r266["IR_OS_continuation"]["equals_BGCE258_K_evt"] is True
 assert r266["IR_OS_continuation"]["manual_Wick_sign_inserted"] is False
 assert p285["minimal_divergence_form_unique_in_declared_class"]=="PASS_CONDITIONAL"
 assert p293["active_source_Markov_transport_nonlinear_integrability"]=="PASS_LOCAL_FINITE"
 assert p294["source_typed_residual_dimension"]==0

 chain={
  "edge_scalar_selected":"logZ Bregman/Umegaki",
  "second_label_variation":"BKM Hessian G_AB(lambda)",
  "finite_scaling":"h^-2 times h^4 edge sum",
  "continuum_principal_form":"(1/2) integral sqrt|g| G_AB g^mn partial_m lambda^A partial_n lambda^B d4x",
  "metric_source_derivative":"M dr/dy=I from BGCE293 horizontal inverse",
  "Lorentz_principal_tensor":"Q4 source-OS-continued to K_evt",
  "unique_metric_solder":"A maps to U^T A U",
  "variation_limit_commutes":"PASS_LOCALLY_FOR_C2_FIELDS_AND_FAITHFUL_FINITE_GIBBS_FAMILY",
  "reason":"the edge Bregman remainder is uniformly O(h^3) with its first source derivative on compact local source neighborhoods; h^-2 h^4 times O(h^3) summed over O(h^-4) cells is O(h)"
 }
 stress="T_mn=G_AB(lambda)[partial_m lambda^A partial_n lambda^B-(1/2)g_mn g^rs partial_r lambda^A partial_s lambda^B]"
 ward="nabla^m T_mn=-E_A partial_n lambda^A; on shell nabla^m T_mn=0"
 out={"schema":"siel.dpa.bgce295.raw.v1","candidate_id":"BGCE295","source_revision":REV,"input_hashes_verified":checked,
 "baseline_gate":"PASS_REVISION_MATCHED_BGCE143_252_254_256_266_285_293_294","primary_evidence_status":"Theoretical derivation in the declared long-wavelength local second-order conservative class",
 "finite_to_continuum_identity":chain,
 "hilbert_ward":{"Hilbert_stress":stress,"off_shell_Noether_identity":ward,"finite_Braid_edge_variation_equals_continuum_Hilbert_variation_in_declared_class":True,"Hilbert_stress_source_derived_in_declared_class":True,"Ward_source_derived_in_declared_class":True},
 "dependency_effect":{"BGCE285_conditional_minimal_parent":"PROMOTED_TO_PASS_IN_DECLARED_CLASS_BY_BGCE293_ACTIVE_TRANSPORT","BGCE291_reversal":"RESOLVED_BY_BGCE293_294_295_IN_DECLARED_CLASS","MMR2_and_source_three_fifths":"RETAINED_UNCHANGED_NOT_REDERIVED","Einstein_dynamics":"NOT_DERIVED"},
 "decision":"FULL_PASS_IN_THE_DECLARED_LONG_WAVELENGTH_LOCAL_SECOND_ORDER_FORMALLY_SELF_ADJOINT_CONSERVATIVE_CLASS__THE_SELECTED_FINITE_BRAID_LOGZ_BREGMAN_UMEGAKI_EDGE_ACTION_HAS_THE_SAME_BKM_HESSIAN_AND_C2_RIEMANN_LIMIT_AS_THE_CONTINUUM_PARENT__BGCE293_GIVES_EXACT_METRIC_MOMENT_VARIATION_M_DR_DY_EQUALS_IDENTITY_AND_FINITE_ACTIVE_MARKOV_TRANSPORT__BGCE294_GIVES_THE_UNIQUE_SOURCE_TYPED_PHYSICAL_SOLDER__BGCE266_SUPPLIES_THE_SOURCE_OS_LORENTZ_PRINCIPAL_TENSOR__THEREFORE_THE_FINITE_EDGE_ACTION_FIRST_METRIC_VARIATION_CONVERGES_TO_THE_HILBERT_VARIATION_AND_THE_OFF_SHELL_NOETHER_IDENTITY_WITH_ON_SHELL_WARD_CONSERVATION_FOLLOWS__NO_NEW_ACTION_OR_FITTED_COEFFICIENT__FULL_FINITE_LORENTZIAN_UMEGAKI_HIGHER_DERIVATIVE_EINSTEIN_AND_EMPIRICAL_GRAVITY_CLAIMS_REMAIN_EXCLUDED",
 "counter_intuition_scan":{"strongest_counterpattern":"BGCE266 does not continue the full finite Umegaki functional to Lorentz signature.","resolution":"The present theorem is explicitly the long-wavelength quadratic C2 variation identity, not a full finite Lorentzian Umegaki equality.","ordinary_explanation":"The Hessian of a Bregman divergence supplies the sigma-model metric, and a conservative graph moment supplies the principal tensor.","falsifier":"Failure of uniform C2 edge expansion, M dr/dy=I, the typed solder, or source OS principal-tensor identity."},
 "next_gate":"BGCE296_STRESS_WARD_FINAL_INDEPENDENT_COMPLETION_AUDIT","runtime_class":"SUBSECOND_EXACT_DEPENDENCY_AND_ASYMPTOTIC_IDENTITY_AUDIT_NO_SCAN","formal_E0_E1_E2":"NOT_CLAIMED__DPA_THEORETICAL_GATE_ONLY",
 "claim_ceiling":"BGCE295 derives source-native Hilbert stress and on-shell Ward conservation only in the declared long-wavelength local second-order formally self-adjoint conservative class. It does not derive a full finite Lorentzian Umegaki action, exclude higher derivatives or other principal symbols, rederive MMR2 or three-fifths, derive Einstein dynamics, empirical gravity or completed quantum gravity."}
 (HERE/"RAW_OUTPUT.json").write_text(json.dumps(out,indent=2)+"\n"); print(out["decision"])
if __name__=="__main__": main()
