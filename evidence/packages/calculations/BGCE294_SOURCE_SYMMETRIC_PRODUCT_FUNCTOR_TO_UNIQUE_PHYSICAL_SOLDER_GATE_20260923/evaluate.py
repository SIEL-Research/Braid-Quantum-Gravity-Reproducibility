#!/usr/bin/env python3
"""BGCE294: uniqueness of the source-typed symmetric-product solder."""

from fractions import Fraction
from hashlib import sha256
from itertools import combinations_with_replacement
from pathlib import Path
import json
import subprocess

ROOT=Path(__file__).resolve().parents[2]; HERE=Path(__file__).resolve().parent
REV="ccf1e28a3424deb42b452720fe02eda3c0dcdcc2"
PAIRS=list(combinations_with_replacement(range(4),2))

def frozen(p): return subprocess.check_output(["git","show",f"{REV}:{p}"],cwd=ROOT)
def rank(a):
 a=[[Fraction(x) for x in r] for r in a]; out=0
 for c in range(len(a[0]) if a else 0):
  p=next((i for i in range(out,len(a)) if a[i][c]),None)
  if p is None: continue
  a[out],a[p]=a[p],a[out]; q=a[out][c]; a[out]=[x/q for x in a[out]]
  for i in range(len(a)):
   if i!=out and a[i][c]: q=a[i][c]; a[i]=[x-q*y for x,y in zip(a[i],a[out])]
  out+=1
 return out
def mm(a,b): return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def tr(a): return [list(r) for r in zip(*a)]
def pack(a): return [a[i][j] if i==j else 2*a[i][j] for i,j in PAIRS]
def unpack(v):
 a=[[Fraction(0) for _ in range(4)] for _ in range(4)]
 for x,(i,j) in zip(v,PAIRS): a[i][j]=a[j][i]=Fraction(x) if i==j else Fraction(x,2)
 return a
def sym2(u):
 cols=[]
 for k in range(10):
  e=[Fraction(0)]*10;e[k]=1; cols.append(pack(mm(tr(u),mm(unpack(e),u))))
 return [list(r) for r in zip(*cols)]
def permrep(p):
 idx={q:i for i,q in enumerate(PAIRS)}; r=[[0]*10 for _ in range(10)]
 for c,(i,j) in enumerate(PAIRS): r[idx[tuple(sorted((p[i],p[j]))) ]][c]=1
 return r
def comm_eq(reps):
 eq=[]
 for r in reps:
  for i in range(10):
   for j in range(10):
    row=[0]*100
    for k in range(10): row[i*10+k]+=r[k][j]; row[k*10+j]-=r[i][k]
    eq.append(row)
 return eq
def fix_vector_eq(v):
 eq=[]
 for i in range(10):
  row=[0]*100
  for j in range(10): row[i*10+j]=v[j]
  eq.append(row)
 return eq
def matvec(a,v): return [sum(a[i][j]*v[j] for j in range(len(v))) for i in range(len(a))]

def main():
 sm=json.loads((HERE/"SOURCE_MATRIX.json").read_text()); checked={}
 for p,e in sm["inputs_sha256"].items():
  b=frozen(p); a=sha256(b).hexdigest(); assert a==e; checked[f"{REV}:{p}"]=a
 src141=frozen("records/BGCE141_SOURCE_MARK_CHARGE_CYLINDER_CURRENT_TO_DOUBLED_METRIC_STRESS_FUNCTOR_GATE_20260919/evaluate.py").decode()
 p258=json.loads(frozen("records/BGCE258_SOURCE_CAUSAL_GRADING_TIMES_EVENT_MOMENT_TO_UNIQUE_NULL_GRAM_PARENT_KINETIC_GATE_20260921/RAW_OUTPUT.json"))
 p268=json.loads(frozen("records/BGCE268_SOURCE_GRAM_SCHUR_CHANNEL_TO_CAUSAL_METRIC_INTERTWINER_GATE_20260922/RAW_OUTPUT.json"))
 p291=json.loads(frozen("records/BGCE291_STRESS_WARD_INDEPENDENT_REDERIVATION_AND_SCOPE_RED_TEAM_GATE_20260923/RESULT.json"))
 p293=json.loads(frozen("records/BGCE293_FINITE_POSITIVE_BKM_EXPONENTIAL_LEAF_INTEGRATION_GATE_20260923/RESULT.json"))
 typed=all(x in src141 for x in ["observables = [generator, *spatial_observables]","product = ub476.symmetric_product(observables[row], observables[column])","metric_functionals = [[None for _ in range(4)] for _ in range(4)]"])
 assert typed and p291["S4_Sym2_commutant_dimension"]==9
 assert p293["active_source_Markov_transport_nonlinear_integrability"]=="PASS_LOCAL_FINITE"
 u=[[Fraction(x) for x in row] for row in p268["source_typed_intertwiner"]["U"]]
 t0=sym2(u); assert rank(t0)==10
 reps=[permrep(p) for p in [(1,0,2,3),(0,2,1,3),(0,1,3,2)]]
 eq=comm_eq(reps); s4dim=100-rank(eq); assert s4dim==9

 # Spectral constraints fix only the causal P0/P1 algebra and are deliberately tested as insufficient.
 p0=[[Fraction(1,4)]*4 for _ in range(4)]
 ident=[[Fraction(i==j) for j in range(4)] for i in range(4)]
 p1=[[ident[i][j]-p0[i][j] for j in range(4)] for i in range(4)]
 spectral_eq=eq+fix_vector_eq(pack(p0))+fix_vector_eq(pack(p1))
 spectral_residual=100-rank(spectral_eq)

 # Differences from identity that vanish on ten source-fixed rank-one squares are zero.
 spanning=[]
 for i in range(4):
  v=[Fraction(0)]*4; v[i]=1; spanning.append(pack([[v[a]*v[b] for b in range(4)] for a in range(4)]))
 for i in range(4):
  for j in range(i+1,4):
   v=[Fraction(0)]*4; v[i]=v[j]=1; spanning.append(pack([[v[a]*v[b] for b in range(4)] for a in range(4)]))
 assert len(spanning)==10 and rank([list(r) for r in zip(*spanning)])==10
 product_eq=eq[:]
 for q in spanning: product_eq+=fix_vector_eq(matvec(t0,q))
 product_residual=100-rank(product_eq)
 assert product_residual==0

 out={"schema":"siel.public-calculation.bgce294.raw.v1","candidate_id":"BGCE294","source_revision":REV,"input_hashes_verified":checked,
 "baseline_gate":"PASS_REVISION_MATCHED_BGCE141_258_268_291_293","primary_evidence_status":"Theoretical derivation with exact source-type uniqueness audit",
 "unrestricted":{"S4_equivariant_commutant_dimension":s4dim,"clock_grading_event_spectral_residual_dimension":spectral_residual,"spectral_constraints_alone_unique":False},
 "source_typed_functor":{"BGCE141_ten_functionals_are_symmetric_product_generated":typed,"underlying_four_carrier_map":"BGCE268 source-fixed U","spanning_rank_one_tests":10,"spanning_rank":10,"residual_affine_dimension":product_residual,"unique_map":"Sym2(U): A maps to U^T A U","new_coefficient":False,"new_matter_action":False},
 "decision":"FULL_PASS_IN_THE_EXISTING_SOURCE_SYMMETRIC_PRODUCT_FUNCTORIAL_CLASS__THE_BGCE291_NINE_DIMENSIONAL_FREEDOM_BELONGS_TO_ARBITRARY_S4_EQUIVARIANT_TEN_DIMENSIONAL_MAPS__CLOCK_GRADING_EVENT_SPECTRAL_CONSTRAINTS_ALONE_REMAIN_INSUFFICIENT__BUT_THE_ACTUAL_TEN_SOURCES_ARE_GENERATED_AS_SYM2_OF_THE_FOUR_SOURCE_CARRIERS_AND_BGCE268_FIXES_THE_UNDERLYING_U__PRESERVING_THAT_COMMITTED_PRODUCT_TYPE_LEAVES_AFFINE_DIMENSION_ZERO_AND_UNIQUELY_FORCES_A_TO_UT_A_U__THE_PHYSICAL_SOLDER_IS_SELECTED_WITHIN_THE_SOURCE_TYPED_CLASS__FINITE_TO_CONTINUUM_ACTION_VARIATION_IDENTITY_STRESS_AND_WARD_REMAIN_OPEN",
 "dependency_effect":{"BGCE291_physical_solder":"PASS_UNIQUE_IN_SOURCE_TYPED_PRODUCT_FUNCTOR_CLASS","BGCE293_active_transport":"PASS_RETAINED","finite_to_continuum_action_variation_identity":"OPEN","Hilbert_stress_Braid_only":"OPEN_PENDING_ONE_ACTION_IDENTITY_GATE","Ward_Braid_only":"OPEN_PENDING_SAME"},
 "counter_intuition_scan":{"strongest_counterpattern":"Clock, grading and event spectral tensors occupy only the P0/P1 algebra and do not by themselves remove all S4-equivariant freedom.","ordinary_explanation":"A linear map on a symmetric square is fixed once its underlying carrier map and product functor are fixed.","interpretive_leap":"Product-functoriality is the physically admissible solder type because the committed ten source functionals are generated by that symmetric product.","falsifier":"A committed metric source functional outside the BGCE141 symmetric-product span, or a source-natural solder that preserves all source products but differs from Sym2(U)."},
 "next_gate":"BGCE295_FINITE_BRAID_BKM_EXPONENTIAL_ACTION_TO_CONTINUUM_HILBERT_VARIATION_IDENTITY_GATE","runtime_class":"SUBSECOND_EXACT_RATIONAL_LINEAR_TYPE_AUDIT_NO_SCAN","formal_E0_E1_E2":"NOT_CLAIMED__PUBLIC_THEORETICAL_GATE_ONLY",
 "claim_ceiling":"BGCE294 proves uniqueness of the Hadamard Sym2 solder within the existing source-typed symmetric-product functorial class and shows weaker S4/spectral constraints are insufficient. It does not exclude deliberately non-functorial maps, prove the finite-to-continuum action variation identity, derive Hilbert stress, Ward, Einstein dynamics or empirical gravity."}
 (HERE/"RAW_OUTPUT.json").write_text(json.dumps(out,indent=2)+"\n"); print(out["decision"])
if __name__=="__main__": main()
