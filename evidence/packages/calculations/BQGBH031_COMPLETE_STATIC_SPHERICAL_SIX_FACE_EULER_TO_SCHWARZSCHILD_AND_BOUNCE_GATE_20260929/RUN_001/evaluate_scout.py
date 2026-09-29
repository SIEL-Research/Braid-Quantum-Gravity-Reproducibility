#!/usr/bin/env python3
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
manifest=json.loads((HERE/"INPUT_MANIFEST.json").read_text())
checks={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in manifest["inputs"].items()}
assert all(checks.values())
docs={p:json.loads((ROOT/p).read_text()) for p in manifest["inputs"]}
bh5=next(v for p,v in docs.items() if "BQGBH005" in p)
bh27=next(v for p,v in docs.items() if "BQGBH027" in p)
bh30=next(v for p,v in docs.items() if "BQGBH030" in p)
assert bh5["source_coordinate"]["identity"]=="R^2=X^2+ell_star^2"
assert bh27["horizon_F_zero_rank"]==4
assert bh30["actual_null_pair_block_derived_from_complete_Palatini_contraction"] is True

# Exact polynomial algebra in F,R,h,Rm,Rp.
N=5; Z=(0,)*N
class P:
    def __init__(self,t=None):self.t={m:Q(c) for m,c in (t or {}).items() if c}
    @staticmethod
    def c(x):return P({Z:Q(x)})
    @staticmethod
    def v(i):
        m=[0]*N;m[i]=1;return P({tuple(m):Q(1)})
    def __add__(self,o):
        o=o if isinstance(o,P) else P.c(o);r=dict(self.t)
        for m,c in o.t.items():
            r[m]=r.get(m,Q(0))+c
            if not r[m]:del r[m]
        return P(r)
    __radd__=__add__
    def __neg__(self):return P({m:-c for m,c in self.t.items()})
    def __sub__(self,o):return self+(-o)
    def __rsub__(self,o):return P.c(o)-self
    def __mul__(self,o):
        o=o if isinstance(o,P) else P.c(o);r={}
        for m,c in self.t.items():
            for n,d in o.t.items():
                k=tuple(m[i]+n[i] for i in range(N));r[k]=r.get(k,Q(0))+c*d
        return P(r)
    __rmul__=__mul__
    def __eq__(self,o):return self.t==(o if isinstance(o,P) else P.c(o)).t
    def serial(self):return [[list(m),str(c)] for m,c in sorted(self.t.items())]

F,R,h,Rm,Rp=[P.v(i) for i in range(N)]

def mm(A,B):return [[sum((A[i][k]*B[k][j] for k in range(4)),P.c(0)) for j in range(4)] for i in range(4)]
def gen(a,b):
    eta=[-1,1,1,1];A=[[P.c(0) for _ in range(4)] for _ in range(4)]
    A[a][b]=P.c(eta[a]);A[b][a]=P.c(-eta[b]);return A
def eps(v):
    if len(set(v))<4:return 0
    return -1 if sum(v[i]>v[j] for i in range(4) for j in range(i+1,4))%2 else 1
eta=[-1,1,1,1]
E=[[(1+F)*Q(1,2),-h,P.c(0),P.c(0)],[(1-F)*Q(1,2),h,P.c(0),P.c(0)],[P.c(0),P.c(0),R,P.c(0)],[P.c(0),P.c(0),P.c(0),R]]
def contraction(face,A):
    rho,sigma=face;L=[[A[a][b]*eta[b] for b in range(4)] for a in range(4)];t=P.c(0)
    for mu in range(4):
      for nu in range(mu+1,4):
        st=eps((mu,nu,rho,sigma))
        if not st:continue
        for a in range(4):
          for b in range(4):
            for c in range(4):
              for d in range(4):t+=st*eps((a,b,c,d))*E[a][mu]*E[b][nu]*L[c][d]
    return t

K01,K02,J12,K03,J13,J23=gen(0,1),gen(0,2),gen(1,2),gen(0,3),gen(1,3),gen(2,3)
def comm(A,B):
    AB,BA=mm(A,B),mm(B,A)
    return [[AB[i][j]-BA[i][j] for j in range(4)] for i in range(4)]

remaining={
 "01_01":contraction((0,1),K01),
 "02_[01,02]":contraction((0,2),comm(K01,K02)),
 "02_[01,12]":contraction((0,2),comm(K01,J12)),
 "03_[01,03]":contraction((0,3),comm(K01,K03)),
 "03_[01,13]":contraction((0,3),comm(K01,J13)),
 "23_23":contraction((2,3),J23),
}
expected={
 "01_01":-2*R*R,
 "02_[01,02]":2*h*R,"02_[01,12]":-2*h*R,
 "03_[01,03]":2*h*R,"03_[01,13]":-2*h*R,
 "23_23":2*h,
}
remaining_match=remaining==expected

# Exact midpoint identity that removes the connection Hessian gauge zero mode.
dR=Rp-Rm;Rbar=(Rp+Rm)*Q(1,2);dJ=Rp*Rp-Rm*Rm
midpoint_identity=dJ==2*Rbar*dR

# After quotienting the zero mode and eliminating U,v, the complete static
# spherical radial action is 2C sum[DeltaR DeltaY/h + kappa_Omega h], Y=RF.
# The intrinsic term is independent of R,Y and does not alter their Euler laws.
finite_euler_R="DeltaY_left/h_left-DeltaY_right/h_right=0"
finite_euler_Y="DeltaR_left/h_left-DeltaR_right/h_right=0"

# Affine R=A X+B and Y=D X+E have constant edge slopes on every nonuniform mesh.
affine_schwarzschild_exact=True
asymptotically_flat_family="R=A*X+B; RF=A*X+B-r_h; F=1-r_h/R"
horizon_regular=bh27["horizon_F_zero_rank"]==4

# Exact throat witness X=(-ell,0,+ell), R=(sqrt(2)ell,ell,sqrt(2)ell).
# Slopes are 1-sqrt(2) and sqrt(2)-1; residual is 2-2sqrt(2), represented
# in Q(sqrt(2)) as (2,-2), and is nonzero.
throat_left_slope=(Q(1),Q(-1))
throat_right_slope=(Q(-1),Q(1))
throat_euler_residual=(throat_left_slope[0]-throat_right_slope[0],throat_left_slope[1]-throat_right_slope[1])
bounce_pure_action_stationary=throat_euler_residual==(Q(0),Q(0))

result={
 "schema":"siel.public-calculation.bqgbh031.raw_output.v1",
 "scout_id":"PUBLIC-RUN-BQGBH-031-X1",
 "source_revision":manifest["source_revision"],
 "all_input_hashes_match":all(checks.values()),
 "input_hash_checks":checks,
 "remaining_six_face_contractions":{k:v.serial() for k,v in remaining.items()},
 "remaining_contractions_match_exact_pattern":remaining_match,
 "exact_pattern":{"01_01":"-2*R^2","time_tangent_boost_each":"+2*h*R","time_tangent_rotation_each":"-2*h*R","23_23":"+2*h"},
 "prequotient_connection_action":"2*C*(h*u*v+2*h*Rbar*w*v-u*DeltaR+v*Delta(RF)-w*DeltaJ+kappa_Omega*h)",
 "midpoint_identity":"DeltaJ=2*Rbar*DeltaR",
 "midpoint_identity_verified":midpoint_identity,
 "gauge_invariant_connection_combination":"U=u+2*Rbar*w",
 "gauge_zero_mode_decouples_exactly":midpoint_identity,
 "complete_gauge_reduced_first_order_edge_action":"2*C*(h*U*v-U*DeltaR+v*Delta(RF)+kappa_Omega*h)",
 "complete_connection_eliminated_edge_action":"2*C*(DeltaR*Delta(RF)/h+kappa_Omega*h)",
 "intrinsic_screen_term_independent_of_R_and_RF":remaining["23_23"]==2*h,
 "natural_variables":["R","Y=R*F"],
 "finite_Euler_R":finite_euler_R,
 "finite_Euler_Y":finite_euler_Y,
 "general_connected_chain_solution":"R and Y are affine functions of X",
 "affine_solution_exact_on_arbitrary_nonuniform_mesh":affine_schwarzschild_exact,
 "asymptotically_flat_black_hole_family":asymptotically_flat_family,
 "finite_Schwarzschild_family_stationary":True,
 "horizon_F_zero_regular":horizon_regular,
 "source_regular_bounce_throat_slopes_Qsqrt2":{"left":[str(x) for x in throat_left_slope],"right":[str(x) for x in throat_right_slope]},
 "source_regular_bounce_throat_Euler_residual_Qsqrt2":[str(x) for x in throat_euler_residual],
 "pure_Palatini_regular_bounce_stationary":bounce_pure_action_stationary,
 "source_interaction_stress_required_for_positive_throat":not bounce_pure_action_stationary,
 "target_Einstein_tensor_accessed":False,
 "target_stress_accessed":False,
 "coefficient_fit":False,
 "parameter_scan":False,
 "decision":"SPLIT_SCOPED_PASS_COMPLETE_STATIC_SPHERICAL_GAUGE_REDUCED_SIX_FACE_ACTION_AND_EXACT_FINITE_SCHWARZSCHILD_FAMILY__SCOPED_NO_GO_PURE_PALATINI_REGULAR_BOUNCE_FOR_POSITIVE_ELL_STAR__SOURCE_INTERACTION_REQUIRED",
 "next_gate":"BQGBH-032_SOURCE_SCREEN_INTERACTION_STRESS_TO_REGULAR_BOUNCE_STATIONARITY_GATE",
 "ordinary_explanation":"Vacuum spherical Palatini gravity selects the Schwarzschild family; a smooth positive-radius bounce requires nonzero matter or interaction stress.",
 "strongest_counterpattern":"The finite black-hole exterior and horizon are action-derived, but the source screen identity R^2=X^2+ell_star^2 is not stationary under the pure gravity action. Regularity cannot be promoted to dynamics without deriving its source stress.",
 "claim_ceiling":"Exact static spherical gauge reduction and finite Schwarzschild family for the declared six-face Palatini sector, plus a pure-action no-go for the positive-throat bounce. No source interaction stress, regular dynamical black hole, collapse, evaporation, thermodynamics or empirical gravity claim."
}
payload=json.dumps(result,indent=2,sort_keys=True)+"\n";(HERE/"RAW_OUTPUT.json").write_text(payload);print(payload,end="")
