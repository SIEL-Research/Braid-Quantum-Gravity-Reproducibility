# BQGBH-036 報告

## 結論

**SPLIT CLOSED_SCOPED。**

BQGBH-031/035で選択されたstatic spherical finite six-face Palatini作用は、

\[
R(X)=\sqrt{X^2+\ell_*^2},\qquad
Y=R-r_h,\qquad
F=1-\frac{r_h}{R}
\]

を全source line`X in R`上のexact stationary solutionとして持つ。この解は
二つの漸近平坦端、正の最小areal radius、有限curvature、regular throat、
source-maximalなhorizon-complete analytic atlasを持つ。

また、選択済み作用はconnection-firstであり、有限holonomyからconnectionを
matrix logarithmで逆算しない。従って旧来のglobal matrix-log branchは物理的
completion conditionではなくなった。

ただしBQGBH-005の「一枚のingoing EF chartだけで全causal geodesic complete」
という証明は不十分だった。outgoing radial null familyはsimple horizonへ有限
affine parameterで到達しながら`v`が発散する。outgoing EFとKruskal patchを
加えればsmoothに延長されるため、これはphysical singularityではなくchart
endpointである。

## 1. action-selected global solution

BQGBH-031のcomplete reduced actionとBQGBH-035のsource-selected interactionを
合わせると、任意非一様edge上で

\[
\Delta(R-\rho)=0,\qquad
\Delta(Y-\rho+r_h)=0
\]

がstationary conditionになる。asymptotic normalizationにより上のsolutionが
全connected chainでexactに固定される。

BQGBH-003のreflected source walkはsigned lineを両向きに無限延長し、

\[
R^2=X^2+\ell_*^2
\]

なので`R>=ell_star>0`である。

## 2. 二つの漸近平坦端

`X -> +/- infinity`で

\[
R=|X|+O(|X|^{-1}),\qquad
F=1-\frac{r_h}{|X|}+O(|X|^{-3}).
\]

右端はingoing EF、左端は向きを反転したoutgoing EF型のflat endへ漸近する。
throat`X=0`は`R=ell_star`を持つ内部面で、境界ではない。

## 3. horizon classification

`F=0`は`R=r_h`である。

- `r_h<ell_star`：horizonなし、two-way traversable throat。
- `r_h=ell_star`：`X=0`のdouble horizon。局所的に
  \[
  F(X)=\frac{X^2}{2\ell_*^2}+O(X^4).
  \]
- `r_h>ell_star`：
  \[
  X_\pm=\pm\sqrt{r_h^2-\ell_*^2}
  \]
  の二つのsimple horizon。

simple horizonでは

\[
F'(X_s)=\frac{X_s}{r_h^2},\qquad
\kappa_s=\frac{F'(X_s)}2=\frac{X_s}{2r_h^2}\ne0.
\]

## 4. BQGBH-005 single-chart claimの訂正

ingoing EF metric

\[
ds^2=-Fdv^2+2dvdX+R^2d\Omega^2
\]

でradial null geodesicは`dot X=+/- E`を満たす。しかし`dot X=+E`のfamilyでは

\[
\frac{dv}{dX}=\frac2F.
\]

simple horizon近傍で`F=2kappa_s(X-X_s)+...`だから

\[
v=\frac1{\kappa_s}\log|X-X_s|+O(1).
\]

一方`lambda=(X-X_0)/E`は有限である。従って一枚のingoing EF chartだけでは
このfamilyのaffine endpointを含まない。

これは旧BQGBH-005の`X` velocity boundだけでは検出できなかった。凍結artifact
は改変せず、本gateをappend-only correctionとする。

## 5. horizon-complete atlas

outgoing chartを

\[
u=v-2r_*,\qquad \frac{dr_*}{dX}=\frac1F
\]

で定義すると

\[
ds^2=-Fdu^2-2dudX+R^2d\Omega^2
\]

で、上のoutgoing null familyをregularに通す。

各simple horizonではsigned`kappa_s`を使い

\[
U_s=-e^{-\kappa_s u},\qquad
V_s=e^{\kappa_s v}
\]

を置く。すると

\[
U_sV_s=-(X-X_s)e^{\text{analytic}}
\]

であり、2次元metric係数

\[
-\frac{F}{\kappa_s^2}e^{-2\kappa_s r_*}
\]

はhorizonで有限かつnonzeroになる。Kruskal patchはbifurcation sphereも含む。

degenerate caseはsimple-horizon exponential patchではなく、ingoing/outgoing EF
pairを使う。metric determinantは`-R^4 sin^2 theta`で全域nonzeroである。

このatlasをhorizon crossingごとに反復glueすれば、有限affine endpointで
残るmetric boundaryはない。absolute analytic inextendibilityは次gateへ残す。

## 6. curvature regularity

\[
R'=\frac XR,\quad
R''=\frac{\ell_*^2}{R^3},\quad
F'=\frac{r_hX}{R^3},\quad
F''=\frac{r_h(\ell_*^2-2X^2)}{R^5}.
\]

`R>=ell_star`なので、これらと`1/R`から作るcurvature building blocksは全域
有限である。horizon patchの追加はisometric coordinate extensionなので、この
結論を変えない。

## 7. global matrix-log branchは不要

BQGBH-031のfirst-order Euler equationは各edgeで

\[
v_e=\frac{\Delta R_e}{h_e},\qquad
U_e=-\frac{\Delta Y_e}{h_e}
\]

を直接与える。selected solutionでは`DeltaY=DeltaR=Delta rho`であり、
`rho(X)=sqrt(X^2+ell_star^2)`は1-Lipschitzだから

\[
|v_e|\le1,\qquad |U_e|\le1.
\]

connectionからedge holonomyをordered exponentialで作る。reverse edgeでは
integrated connectionが符号反転するためholonomyはinverseになり、refinementは
ordered productで定義される。どの段階でもmatrix logarithmを取らない。

sphereのangular connectionは標準chart transitionとintrinsic screen curvature
termで扱う。topological sector全体へsingle-valued logarithmを要求しない。

## 8. 判定

- action-selected all-chain solution：**PASS exact**。
- two asymptotically flat ends：**PASS**。
- positive throat / finite curvature：**PASS**。
- horizon-complete analytic atlas：**CLOSED_SCOPED**。
- ingoing EF chart単独のcompleteness：**FAIL、訂正**。
- connection-first global finite holonomy：**PASS**。
- global matrix-log obligation：**removed**。
- absolute analytic inextendibility / unique maximal extension：**OPEN**。
- collapse / evaporation / thermodynamics：**OPEN**。

## 9. 次

`BQGBH-037_SOURCE_MAXIMAL_ATLAS_INEXTENDIBILITY_AND_GLOBAL_CAUSAL_STRUCTURE_GATE`

反復Kruskal gluingのregion graph、Cauchy horizonの有無、global hyperbolicity、
analytic inextendibilityを判定し、source-maximal atlasと通常の最大解析拡張の
差を閉じる。

## Evidence status / claim ceiling

一次区分は **Theoretical derivation / split closed-scoped result and
append-only correction**。

静的球対称sectorのhorizon-complete two-ended analytic developmentは閉じた。
absolute `C^k` maximality、dynamical formation、evaporation、thermodynamics、
rotation、charge、自然界のblack hole、経験的確認は未導出である。
