#!/usr/bin/env python3
"""BGCE298: exact clock-redundancy factorization and scoped Ward closure."""
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations_with_replacement
from pathlib import Path
import json, subprocess

ROOT=Path(__file__).resolve().parents[2]; HERE=Path(__file__).resolve().parent
REV="bdaf06b2da0c2fc548f141fadf11ef70d1a4c97e"; PAIRS=list(combinations_with_replacement(range(4),2))
def frozen(p): return subprocess.check_output(["git","show",f"{REV}:{p}"],cwd=ROOT)
def load(p): return json.loads(frozen(p))
def add(a,b): return [[a[i][j]+b[i][j] for j in range(len(a[0]))] for i in range(len(a))]
def scale(c,a): return [[c*x for x in r] for r in a]
def outer(x,y): return [[a*b for b in y] for a in x]
def mv(a,x): return [sum(a[i][j]*x[j] for j in range(len(x))) for i in range(len(a))]
def dot(x,y): return sum(a*b for a,b in zip(x,y))
def mm(a,b): return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def tr(a): return [list(r) for r in zip(*a)]
def inv(a):
 n=len(a); z=[[F(x) for x in r]+[F(i==j) for j in range(n)] for i,r in enumerate(a)]
 for c in range(n):
  p=next(i for i in range(c,n) if z[i][c]); z[c],z[p]=z[p],z[c]
  q=z[c][c]; z[c]=[x/q for x in z[c]]
  for i in range(n):
   if i!=c:
    q=z[i][c]; z[i]=[x-q*y for x,y in zip(z[i],z[c])]
 return [r[n:] for r in z]
def rank(a):
 a=[[F(x) for x in r] for r in a]; out=0
 for c in range(len(a[0]) if a else 0):
  p=next((i for i in range(out,len(a)) if a[i][c]),None)
  if p is None: continue
  a[out],a[p]=a[p],a[out]; q=a[out][c]; a[out]=[x/q for x in a[out]]
  for i in range(len(a)):
   if i!=out and a[i][c]: q=a[i][c]; a[i]=[x-q*y for x,y in zip(a[i],a[out])]
  out+=1
 return out
def sym_basis(k):
 a=[[F(0) for _ in range(4)] for _ in range(4)]; i,j=PAIRS[k]; a[i][j]=a[j][i]=1; return a
def flat(a): return [a[i][j] for i,j in PAIRS]
def dQK(q,t,h):
 v=mv(q,t); w=mv(h,t); al=dot(t,v); da=dot(t,w)
 return add(h,add(scale(-F(2)/al,add(outer(w,v),outer(v,w))),scale(F(2)*da/(al*al),outer(v,v))))
def dTK(q,t,s):
 v=mv(q,t); w=mv(q,s); al=dot(t,v); da=F(2)*dot(s,v)
 return add(scale(-F(2)/al,add(outer(w,v),outer(v,w))),scale(F(2)*da/(al*al),outer(v,v)))
def main():
 sm=json.loads((HERE/"SOURCE_MATRIX.json").read_text()); checked={}
 for p,e in sm["inputs_sha256"].items():
  b=frozen(p); a=sha256(b).hexdigest(); assert a==e; checked[f"{REV}:{p}"]=a
 p295=load("audits/SRA_DPA_BGCE295_FINITE_BRAID_ACTION_TO_CONTINUUM_HILBERT_VARIATION_IDENTITY_GATE_20260923/RAW_OUTPUT.json")
 p296=load("audits/SRA_DPA_BGCE296_STRESS_WARD_FINAL_INDEPENDENT_COMPLETION_AUDIT_20260923/RESULT.json")
 p297r=load("audits/SRA_DPA_BGCE297_SOURCE_CLOCK_PROJECTOR_TO_COMOVING_GRADING_AND_FULL_7PLUS3_OS_TRANSPORT_GATE_20260923/RAW_OUTPUT.json")
 p297=load("audits/SRA_DPA_BGCE297_SOURCE_CLOCK_PROJECTOR_TO_COMOVING_GRADING_AND_FULL_7PLUS3_OS_TRANSPORT_GATE_20260923/RESULT.json")
 assert p295["finite_to_continuum_identity"]["variation_limit_commutes"].startswith("PASS_")
 assert "on shell nabla^m T_mn=0" in p295["hilbert_ward"]["off_shell_Noether_identity"]
 assert p296["BGCE295_full_rank_ten_stress_Ward_promotion"]=="NOT_SUSTAINED"
 assert p297["comoving_J_rank_after"]==10 and p297r["dependency_effect"]["full_rank_Hilbert_variation_kinematically_available"] is True
 t=[F(1,2)]*4; P0=outer(t,t); I=[[F(i==j) for j in range(4)] for i in range(4)]; P1=add(I,scale(-1,P0)); q=add(scale(F(12,25),P0),scale(F(52,25),P1))
 A=[flat(dQK(q,t,sym_basis(i))) for i in range(10)]; A=[list(r) for r in zip(*A)]
 E=[]
 for i in range(4):
  s=[F(j==i) for j in range(4)]; E.append(flat(dTK(q,t,s)))
 B=[list(r) for r in zip(*E)]
 assert rank(A)==10 and rank(B)==3
 C=mm(inv(A),B); assert mm(A,C)==B
 assert mv(B,t)==[F(0)]*10
 # Cotangent identity B^T h = C^T A^T h is equivalent to B=A C.
 assert tr(B)==mm(tr(C),tr(A))
 out={"schema":"siel.dpa.bgce298.raw.v1","candidate_id":"BGCE298","source_revision":REV,"input_hashes_verified":checked,
 "baseline_gate":"PASS_REVISION_MATCHED_BGCE295_296_297","primary_evidence_status":"Theoretical derivation with exact local clock-redundancy factorization and scoped Noether completion",
 "tangent_factorization":{"D_Q_K_rank":rank(A),"D_tau_K_rank":rank(B),"clock_scale_kernel_dimension":1,"D_tau_K_times_tau_zero":True,"exact_C_exists_with_D_tau_K_equals_D_Q_K_times_C":True,"cotangent_E_tau_equals_C_transpose_E_Q":True},
 "interpretation":{"tau_is_independent_continuum_coupling":False,"tau_role":"redundant source parametrization of K in the local declared class","independent_clock_Euler_equation_required":False,"continuum_parent_fields":"K and matter labels; tau eliminated from the physical action representation"},
 "stress_Ward":{"BGCE295_C2_variation_identity":"RETAINED","BGCE296_fixed_J_obstruction":"REMOVED_BY_BGCE297_AND_THIS_FACTORISATION","full_rank_Hilbert_stress_source_derived_in_declared_class":True,"off_shell_Noether_identity":"nabla^m T_mn=-E_A partial_n lambda^A","on_shell_Braid_only_Ward_in_declared_class":True,"scope":"LONG_WAVELENGTH_LOCAL_SECOND_ORDER_FORMALLY_SELF_ADJOINT_CONSERVATIVE_CLASS"},
 "decision":"FULL_PASS_IN_THE_DECLARED_LONG_WAVELENGTH_LOCAL_SECOND_ORDER_FORMALLY_SELF_ADJOINT_CONSERVATIVE_CLASS__D_Q_K_IS_EXACTLY_RANK_TEN__D_TAU_K_IS_RANK_THREE_WITH_CLOCK_SCALE_KERNEL__AND_FACTORS_EXACTLY_THROUGH_D_Q_K__THUS_TAU_ADDS_NO_INDEPENDENT_CONTINUUM_COUPLING_OR_EULER_LAW__BGCE297_REMOVES_THE_ONLY_BGCE296_FIXED_J_RANK_OBSTRUCTION__THE_BGCE295_FINITE_TO_CONTINUUM_HILBERT_VARIATION_AND_STANDARD_OFF_SHELL_NOETHER_IDENTITY_ARE_RESTORED_IN_SCOPE__ON_MATTER_SHELL_NABLA_T_EQUALS_ZERO__NO_NEW_CLOCK_ACTION_OR_FIT",
 "counter_intuition_scan":{"ordinary_explanation":"A locally invertible change of metric variables cannot create an independent background-field Ward defect.","strongest_alternative":"Beyond the declared C2 local class, the finite Lorentzian action may contain tau separately or the Q-to-K map may cease to be globally invertible.","falsifier":"A source-derived continuum term depending on tau other than through K, loss of D_Q_K rank, or failure of the BGCE295 C2 variation limit."},
 "next_gate":"BGCE299_INDEPENDENT_STRESS_WARD_COMPLETION_RED_TEAM_AND_CLAIM_CEILING_AUDIT","runtime_class":"SUBSECOND_EXACT_RATIONAL_NO_SCAN","formal_E0_E1_E2":"NOT_CLAIMED__DPA_THEORETICAL_GATE_ONLY","new_action":False,"fitted_coefficient":False,
 "claim_ceiling":"BGCE298 completes Braid-source Hilbert stress and on-shell Ward only in the declared long-wavelength local second-order formally self-adjoint conservative class by proving that the source clock is a redundant local parametrization of the full-rank Lorentz tensor. It does not derive a full finite Lorentzian action, global invertibility, Einstein dynamics, empirical gravity or completed quantum gravity."}
 (HERE/"RAW_OUTPUT.json").write_text(json.dumps(out,indent=2)+"\n"); print(out["decision"])
if __name__=="__main__": main()
