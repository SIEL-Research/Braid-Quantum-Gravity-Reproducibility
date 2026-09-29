# BQGBH-031 報告

## 結論

**SPLIT SCOPED PASS / SCOPED NO-GO。**

actual complete six-face Palatini actionのstatic spherical sectorを、全connection成分とLorentz gauge zero modeを含めてexactに縮約した。その有限Euler方程式は任意の非一様source mesh上でSchwarzschild familyをstationary outputとして選ぶ。

\[
\boxed{
R=A X+B,qquad RF=A X+B-r_h,qquad
F=1-{r_h\over R}
}
\]

地平線 \(F=0\) ではBQGBH-027のcoframeはrank 4で正則である。これによりblack-hole exteriorとhorizonは、条件付きmetric ansatzではなくfinite Palatini variationの出力になった。

一方、source identity \(R^2=X^2+\ell_*^2\) が与えるpositive-throat regular bounceはpure Palatini作用のstationary pointではない。regular interiorには同じsourceから導かれるinteraction stressが必要である。

## 1. 残る三種類のsix-face contraction

BQGBH-030のradial--tangent sectorに加え、actual Palatini contractionはexactに

\[
K(01;01)=-2R^2,
\]

各time--tangent faceで

\[
K_{\rm boost}=+2hR,qquad
K_{\rm rotation}=-2hR,
\]

intrinsic screen faceで

\[
K(23;23)=+2h
\]

を与えた。全式は \(F\) に依存せず、target tensorやblack-hole equationを参照していない。

## 2. Lorentz gauge zero modeのexact消去

time--radial connectionを \(w\)、BQGBH-030のnull pairを \(u,v\) とすると、edge actionは

\[
S_e=2C\left[
h_eu_ev_e+2h_e\bar R_e w_ev_e
-u_e\Delta R_e+v_e\Delta(RF)_e
-w_e\Delta J_e+\kappa_\Omega h_e
\right].
\]

endpoint midpoint \(\bar R_e=(R_{e+}+R_{e-})/2\) に対して

\[
\Delta J_e
=R_{e+}^2-R_{e-}^2
=2\bar R_e\Delta R_e
\]

がexactに成立する。従って

\[
U_e=u_e+2\bar R_e w_e
\]

だけが作用に残り、直交するconnection方向はlocal Lorentz gauge zero modeとして完全にdecoupleする。

## 3. complete reduced action

gauge quotient後のfirst-order edge actionは

\[
S_e=2C\left[
h_eU_ev_e-U_e\Delta R_e
+v_e\Delta(RF)_e+\kappa_\Omega h_e
\right].

\]

\(U_e,v_e\) を消去すると

\[
\boxed{
S_{\rm sph}^{\rm red}
=2C\sum_e\left[
{\Delta R_e\Delta Y_e\over h_e}
+\kappa_\Omega h_e
\right],qquad Y=RF
}
\]

となる。intrinsic screen termは \(R,Y\) に依存しないため、radial Euler方程式を変更しない。

## 4. finite Euler equations

内部node \(k\) でのvariationは

\[
{\Delta R_{k-1/2}\over h_{k-1/2}}
-{\Delta R_{k+1/2}\over h_{k+1/2}}=0,
\]

\[
{\Delta Y_{k-1/2}\over h_{k-1/2}}
-{\Delta Y_{k+1/2}\over h_{k+1/2}}=0.
\]

従ってconnected radial chain上で \(R\) と \(Y=RF\) はともに \(X\) のaffine functionである。この結論はmeshがuniformであることを要求しない。

asymptotic flatnessで両方のslopeを一致させると

\[
R=A X+B,qquad Y=R-r_h,qquad F=1-{r_h\over R}
\]

を得る。これは有限格子上でexactなSchwarzschild familyであり、\(r_h\)はboundary chargeとして残る。

## 5. horizon

\(F=0\) は \(R=r_h>0\) にある。BQGBH-027で

\[
\det E=J h\Delta v(\Delta\alpha)^2
\]

がexactに示されているので、\(J=R^2>0\)ならhorizonでもcoframe rankは4である。従ってEF chart上の地平線は作用由来familyの正則面である。

## 6. regular bounceのpure-action NO-GO

BQGBH-005のsource throat tripletは

\[
X=(-\ell_*,0,+\ell_*),qquad
R=(\sqrt2\ell_*,\ell_*,\sqrt2\ell_*).
\]

左右のfinite slopeは

\[
s_-=1-\sqrt2,qquad s_+=\sqrt2-1.
\]

Euler residualは

\[
s_--s_+=2-2\sqrt2\neq0.
\]

従って \(\ell_*>0\) のpositive-throat bounceはpure Palatini vacuumではstationaryでない。これはregular geometry自体のNO-GOではなく、「真空作用だけで選ばれる」という経路のNO-GOである。

## 7. 反直観監査

vacuum spherical PalatiniがSchwarzschildを選び、smooth bounceにnonzero stressを要求することは通常重力と整合する。Braid固有の次の問いは、source screen/collisionがこのstressを外部matter ansatzなしに供給するかである。

## 8. 次

`BQGBH-032_SOURCE_SCREEN_INTERACTION_STRESS_TO_REGULAR_BOUNCE_STATIONARITY_GATE`

既存source screen number、signed incidence、Casimir/Dirichlet currentおよびcollision stressから、上のexact throat residualを相殺するinteraction variationが事前係数なしで出るかを判定する。

## Evidence status / claim ceiling

一次区分は **Theoretical derivation / scoped split result**。

complete static spherical finite Palatini action、Euler方程式、Schwarzschild family、regular EF horizonは導出済み。source interaction stress、regular dynamical black hole、singularity resolution、collapse、evaporation、thermodynamics、自然界のblack hole、経験的重力は未導出である。
