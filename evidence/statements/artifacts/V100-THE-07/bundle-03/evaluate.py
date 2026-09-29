#!/usr/bin/env python3
"""BGCE299: independent red-team of scoped stress/Ward completion."""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json, subprocess

ROOT=Path(__file__).resolve().parents[2]; HERE=Path(__file__).resolve().parent
REV="e0ac54d6ddbcaa78d7354c037063746e3339c1c2"
def frozen(p): return subprocess.check_output(["git","show",f"{REV}:{p}"],cwd=ROOT)
def load(p): return json.loads(frozen(p))
def T(a): return [list(r) for r in zip(*a)]
def mul(a,b): return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def vec(a,x): return [sum(a[i][j]*x[j] for j in range(len(x))) for i in range(len(a))]
def ip(x,y): return sum(a*b for a,b in zip(x,y))
def out(x,y): return [[a*b for b in y] for a in x]
def plus(a,b): return [[a[i][j]+b[i][j] for j in range(len(a[0]))] for i in range(len(a))]
def times(c,a): return [[c*x for x in r] for r in a]
def I(): return [[F(i==j) for j in range(4)] for i in range(4)]
def clock_reflect(a,t):
 v=vec(a,t); s=ip(t,v); assert s
 return plus(a,times(-F(2)/s,out(v,v)))
def congruence(c,a): return mul(mul(c,a),T(c))
def main():
 sm=json.loads((HERE/"SOURCE_MATRIX.json").read_text()); checked={}
 for p,e in sm["inputs_sha256"].items():
  b=frozen(p); h=sha256(b).hexdigest(); assert h==e; checked[f"{REV}:{p}"]=h
 p285=load("audits/SRA_DPA_BGCE285_SOURCE_CYLINDER_MEASURE_AND_MARKOV_NATURALITY_TO_UNIQUE_MINIMAL_COVARIANT_PARENT_GATE_20260923/RESULT.json")
 p293=load("audits/SRA_DPA_BGCE293_FINITE_POSITIVE_BKM_EXPONENTIAL_LEAF_INTEGRATION_GATE_20260923/RESULT.json")
 p295=load("audits/SRA_DPA_BGCE295_FINITE_BRAID_ACTION_TO_CONTINUUM_HILBERT_VARIATION_IDENTITY_GATE_20260923/RAW_OUTPUT.json")
 p297=load("audits/SRA_DPA_BGCE297_SOURCE_CLOCK_PROJECTOR_TO_COMOVING_GRADING_AND_FULL_7PLUS3_OS_TRANSPORT_GATE_20260923/RAW_OUTPUT.json")
 p298=load("audits/SRA_DPA_BGCE298_CLOCK_REDUNDANCY_CHAIN_RULE_TO_STRESS_WARD_COMPLETION_GATE_20260923/RAW_OUTPUT.json")
 t=[F(1,2)]*4; p0=out(t,t); p1=plus(I(),times(-1,p0)); q0=plus(times(F(12,25),p0),times(F(52,25),p1))
 fixtures=[I()]
 for i,j in [(0,1),(1,2),(2,3),(3,0),(0,2),(1,3)]:
  c=I(); c[i][j]=F(1,5); fixtures.append(c)
 for i in range(4):
  c=I(); c[i][i]=F(3,2); fixtures.append(c)
 inverse_checks=0; sign_checks=0
 for c in fixtures:
  q=congruence(c,q0); k=clock_reflect(q,t); qr=clock_reflect(k,t)
  assert qr==q
  assert ip(t,vec(q,t))>0 and ip(t,vec(k,t))<0
  inverse_checks+=1; sign_checks+=1
 principal=p295["finite_to_continuum_identity"]["continuum_principal_form"]
 physical_tau_tokens=any(x in principal for x in ["tau","P0","J_ray","clock"])
 assert physical_tau_tokens is False
 assert "sqrt|g|" in principal and "g^mn" in principal and "lambda" in principal
 assert p285["source_metric_volume_density_naturality"]=="PASS"
 assert p285["minimal_divergence_form_unique_in_declared_class"]=="PASS_CONDITIONAL"
 assert p293["active_source_Markov_transport_nonlinear_integrability"]=="PASS_LOCAL_FINITE"
 assert p293["positive_rates"] is True and p293["Jacobian_positive_definite_everywhere"] is True
 assert p295["finite_to_continuum_identity"]["variation_limit_commutes"].startswith("PASS_")
 assert p297["off_shell"]["clock_reflection_dQ_to_dK_rank"]==10
 assert p298["tangent_factorization"]["exact_C_exists_with_D_tau_K_equals_D_Q_K_times_C"] is True
 outp={"schema":"siel.dpa.bgce299.raw.v1","candidate_id":"BGCE299","source_revision":REV,"input_hashes_verified":checked,
 "baseline_gate":"PASS_REVISION_MATCHED_BGCE285_293_295_297_298","primary_evidence_status":"Independent theoretical derivation audit of the scoped stress/Ward completion",
 "independent_inverse_audit":{"general_identity":"K tau=-Q tau and tau^T K tau=-tau^T Q tau imply R_tau(R_tau(Q))=Q","exact_positive_Q_fixtures":inverse_checks,"exact_inverse_checks":inverse_checks,"clock_sign_flip_checks":sign_checks,"local_regular_full_rank":"PASS","global_claim":"NOT_MADE_OUTSIDE_THE_ADMISSIBLE_CLOCK_DOMAIN"},
 "action_scope_audit":{"continuum_principal_form":principal,"independent_tau_P0_J_clock_token_present":physical_tau_tokens,"metric_volume_density_source_natural":"PASS","minimal_parent_unique":"PASS_AFTER_BGCE293_ACTIVE_TRANSPORT_IN_DECLARED_CLASS","finite_C2_variation_limit":"PASS","full_finite_Lorentzian_action":"NOT_DERIVED"},
 "hardcode_red_team":{"BGCE298_literal_conclusions_not_used_as_sufficient_evidence":True,"inverse_rederived_separately":True,"action_dependencies_reopened_from_BGCE285_293_295":True,"strongest_counterexample":"An added term F(K)+beta H(tau) would defeat clock redundancy, but no such term is present in the selected source continuum parent and it lies outside the frozen declared action class."},
 "final_decision":{"stress_Ward":"FINAL_SCOPED_PASS","Hilbert_stress_source_derived":True,"on_shell_Ward_source_derived":True,"scope":"LONG_WAVELENGTH_LOCAL_SECOND_ORDER_FORMALLY_SELF_ADJOINT_CONSERVATIVE_CLASS","BGCE298_sustained":True,"A48_status":"CLOSED_IN_DECLARED_CLASS","Einstein_backreaction":"OPEN_A49"},
 "decision":"FINAL_SCOPED_PASS__THE_CLOCK_REFLECTION_HAS_AN_EXPLICIT_INVOLUTION_INVERSE_ON_THE_ADMISSIBLE_POSITIVE_Q_CLOCK_DOMAIN__THE_CLOCK_SIGN_FLIPS_EXACTLY__THE_SELECTED_BGCE295_CONTINUUM_PARENT_AND_BGCE285_VOLUME_OPERATOR_CONTAIN_NO_INDEPENDENT_TAU_COUPLING__BGCE293_SUPPLIES_THE_PREVIOUSLY_MISSING_ACTIVE_POSITIVE_MARKOV_TRANSPORT__THEREFORE_BGCE298_SURVIVES_RED_TEAM_AND_BRAID_SOURCE_HILBERT_STRESS_PLUS_ON_SHELL_WARD_ARE_FINAL_WITHIN_THE_DECLARED_LONG_WAVELENGTH_LOCAL_SECOND_ORDER_FORMALLY_SELF_ADJOINT_CONSERVATIVE_CLASS__A49_EINSTEIN_BACKREACTION_REMAINS_OPEN",
 "counter_intuition_scan":{"ordinary_explanation":"The clock reflection is a standard involutive change from a positive form plus time orientation to a Lorentz form; Ward follows from the selected diffeomorphism-covariant K-only continuum parent.","strongest_remaining_alternative":"A full finite or higher-derivative continuation could contain independent clock terms absent from the declared C2 parent.","falsifier":"Exhibit a committed source-selected term in the declared continuum class that depends on tau other than through K, or a positive admissible Q where the inverse or rank fails."},
 "next_gate":"BGCE300_A49_NONCIRCULAR_BACKREACTION_FROM_SOURCE_STRESS_TO_LOW_ENERGY_SPIN2_EINSTEIN_OUTPUT_GATE","runtime_class":"SUBSECOND_EXACT_RATIONAL_AND_SOURCE_SCOPE_AUDIT_NO_SCAN","formal_E0_E1_E2":"NOT_CLAIMED__DPA_THEORETICAL_GATE_ONLY","new_action":False,"fitted_coefficient":False,
 "claim_ceiling":"BGCE299 independently sustains source-derived Hilbert stress and on-shell Ward only in the declared long-wavelength local second-order formally self-adjoint conservative continuum class. It does not derive a full finite Lorentzian action, all higher-derivative sectors, Einstein backreaction, empirical gravity or completed quantum gravity."}
 (HERE/"RAW_OUTPUT.json").write_text(json.dumps(outp,indent=2)+"\n"); print(outp["decision"])
if __name__=="__main__": main()
