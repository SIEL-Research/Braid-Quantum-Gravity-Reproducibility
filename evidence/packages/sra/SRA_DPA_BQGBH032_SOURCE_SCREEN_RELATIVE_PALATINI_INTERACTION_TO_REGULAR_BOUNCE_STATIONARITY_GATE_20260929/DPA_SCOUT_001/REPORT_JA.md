# BQGBH-032 報告

## 結論

**SPLIT CONDITIONAL SCOPED PASS / SCOPED NO-GO。**

source signed screenとfixed-tail massを基準点にした、完全六面Palatini作用のexact Bregman remainderは、正則black-bounceを任意の非一様radial chain上で停留解にする。interaction係数は`1`で、throat残差を見て合わせた値ではない。

一方、BGCE348/349のbranch-odd collision actionをこのfull nonlinear radial作用へ直接流用する経路は、現行証拠では型が不足する。従って正則black-bounceの**条件付き作用導出**は成立したが、relative-Palatini prescriptionそのものの無条件Braid-only選択はまだOPENである。

## 1. source基準点

BQGBH-004はfixed emitted prefixとactive screenを同じsource right tail内で分離した。BQGBH-005はactive screenから

\[
\rho^2=X^2+\ell_*^2,
\qquad \rho>0
\]

を導出した。従ってstatic spherical自然変数`R,Y=RF`に対するsource基準pairは

\[
z_*=(\rho,\rho-r_h)
\]

である。`r_h`はfixed prefix chargeなのでedge differenceはzeroである。

## 2. 係数なしrelative Palatini作用

BQGBH-031のcomplete connection-eliminated edge kernelは

\[
S_g=2C\sum_e {\Delta R_e\Delta Y_e\over h_e}
+2C\sum_e\kappa_\Omega h_e
\]

である。この二次作用のsource基準点まわりのBregman remainderを取る。

\[
S_{\rm rel}[z;z_*]
=S_g[z]-S_g[z_*]-dS_g[z_*](z-z_*).
\]

edgeごとにexactに

\[
\boxed{
S_{\rm rel}
=2C\sum_e
{\Delta(R-\rho)_e\,\Delta(Y-\rho+r_h)_e\over h_e}
+2C\sum_e\kappa_\Omega h_e
}
\]

となる。展開したinteraction部分は

\[
S_{\rm int}
=2C\sum_e {-Delta\rho_e\Delta R_e
-\Delta\rho_e\Delta Y_e
+(\Delta\rho_e)^2\over h_e}.
\]

係数列は`(1,-1,-1,1)`であり、Bregman定義から一意に固定される。目標Einstein tensor、必要stress、係数scanは不使用である。

## 3. finite Eulerと大域停留性

内部nodeのEuler方程式は

\[
{\Delta(Y-\rho+r_h)_{k-1/2}\over h_{k-1/2}}
-{\Delta(Y-\rho+r_h)_{k+1/2}\over h_{k+1/2}}=0,
\]

\[
{\Delta(R-\rho)_{k-1/2}\over h_{k-1/2}}
-{\Delta(R-\rho)_{k+1/2}\over h_{k+1/2}}=0.
\]

従って

\[
R=\rho,
\qquad Y=\rho-r_h,
\qquad F=1-{r_h\over\rho}
\]

は、throatだけでなく任意のconnected nonuniform chainの全内部nodeでexactな停留解である。

## 4. throat exact cancellation

BQGBH-031のpure Palatini throat residualは

\[
2-2\sqrt2.
\]

relative interactionの第一変分は

\[
2\sqrt2-2
\]

なので

\[
(2-2\sqrt2)+(2\sqrt2-2)=0
\]

がexactに成立する。事後係数調整はない。

## 5. BGCE348/349直接流用のSCOPED NO-GO

BGCE348はone-collision physical support上の4つのbranch-odd transfer defectを導出する。BGCE349はそれをsource cylinderへ局所配置するが、自己のclaim ceilingで次を未導出としている。

- full ten-component nonlinear metric dependence
- nontrivial spatial-gradient dynamics

強曲率radial作用は`R,Y`の非線形metric dependenceとedge gradientを必要とする。従って現状のBGCE348/349だけから上のrelative interactionを「既に導出済み」と呼ぶことはできない。

BGCE371のunit identity feedbackは係数`1`のsupporting evidenceだが、aligned four-scoreとstrong-curvature radial pairの同一性を証明していないため、無条件選択の証明には使わない。

## 6. counter-intuition

任意の二次作用を選んだ基準点でBregman相対化すれば、その基準点は構成上stationaryになる。従って今回のexact cancellationだけでは、sourceが相対化を選んだ証明にならない。

今回閉じたのは、

1. sourceが基準pairを供給すること、
2. 完全六面Palatini作用がHessianとoverall normalizationを供給すること、
3. relative-action class内ではinteractionと係数が一意であること、
4. その作用が正則black-bounceを全格子点で停留させること

までである。

## 7. 判定と次

- direct BGCE348/349 strong-curvature radial action：**SCOPED NO-GO / typing不足**
- source-relative Palatini Bregman action：**CONDITIONAL SCOPED PASS**
- interaction係数`1`：**declared Bregman class内で一意**
- regular black-bounce finite stationarity：**PASS、任意の非一様chain**
- unconditional Braid-only selection：**OPEN**

次は

`BQGBH-033_BRANCH_ODD_COLLISION_TO_RELATIVE_PALATINI_SELECTION_GATE`

で、actual raw/Petz collision contrastまたはsource Noether lawが、上の一次差引き`dS_g[z_*](z-z_*)`を独立に生成するかを判定する。

## Evidence status / claim ceiling

一次区分は **Theoretical derivation / conditional scoped result**。

本gateは、source-relative Palatini class内の係数なし正則black-bounce stationarityを閉じた。relative prescriptionの無条件source選択、collapse、evaporation、thermodynamics、astrophysical black-hole identification、経験的singularity resolutionは未導出である。
