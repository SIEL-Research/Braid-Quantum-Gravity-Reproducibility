# BQGCAL-009 報告

## 結論

**SCOPED PASS。positive quadratic excitation Casimirがinteger event numberとexactに一致した。**

BGCE310のsource environment charge `H_E`をexactに二乗し、pointed partition

\[
P_e=|e\rangle\langle e|,
\qquad
P_{\rm non}=I-P_e
\]

へのtrace-preserving conditional expectationを取る。

\[
\mathbb E_{\rm point}(X)
=\operatorname{Tr}(P_eX)P_e
+\frac{\operatorname{Tr}(P_{\rm non}X)}5P_{\rm non}.
\]

exact計算は

\[
\operatorname{Tr}(P_eH_E^2)=\frac1{18},
\qquad
\frac{\operatorname{Tr}(P_{\rm non}H_E^2)}5=\frac{13}{90}
\]

を与えた。

pointed identity sectorが固定するvacuum baseline `1/18`を全体から引くと、

\[
C_{\rm exc}
=\mathbb E_{\rm point}(H_E^2)-\frac1{18}I
=\left(\frac{13}{90}-\frac1{18}\right)P_{\rm non}
\]

なので、

\[
\boxed{C_{\rm exc}=\frac4{45}N_1}
\]

が演算子identityとして成立する。係数`4/45`はfitではなくsource chargeのexact quadratic valueから出た。

## tailと面積則

各tail blockへ加法的に持ち上げると、

\[
C_{{\rm exc},n}=\frac4{45}N_n,
\qquad
N_n=\frac{45}{4}C_{{\rm exc},n}.
\]

BQGCAL-007のcomplete-screen lawと合成すると、

\[
\boxed{
A_{\rm total}=\frac{45}{4}A_0C_{{\rm exc},n}
}
\]

および

\[
\boxed{
r=\sqrt{\frac{45}{4}C_{{\rm exc},n}}\,\ell_*
}
\]

を得る。これはrefinement level `m`に依存しない。

## 重要な境界

ここで得たのはsource quadratic activityとarea-numberのexact関係である。まだ次は証明していない。

- `N_n`がgeometric screen数そのものであること。
- `C_exc`がcollisionで保存されるphysical quasi-local massであること。
- Schwarzschild/Misner--Sharp massとの同一性。
- absolute SI radius、mass、Newton定数。

特にblack-hole areaが`K`に比例するなら、Schwarzschild massは通常`√K`に比例する。従って`C_exc`をそのままmassと呼ばず、area-number carrierに止める。

## Counter-intuition scan

pointed finite Hamiltonianを二つのsectorへ平均すれば、quadratic contrastがnumber projectionに比例する場合は一般にもあり得る。従って`4/45` identityだけで重力を証明したとは言えない。

Braid固有なのは、実際のsix-label charge、pointing、positive count、25-adic screen lawが同じsource内で係数なしに接続した点である。次のmass conservation testに失敗すれば、内部代数的一致に留まる。

## 次

`BQGCAL-010_SOURCE_EXCITATION_AREA_NUMBER_TO_CONSERVED_MISNER_SHARP_MASS_AND_SCHWARZSCHILD_SPECTRUM_GATE`

で、

1. `sqrt((45/4)C_exc)`がfinite conserved massとして型付けできるか。
2. continuum Misner--Sharp massと同じnormalizationを持つか。
3. `r_K=ell_star sqrt(K)`とSchwarzschild marginal conditionが同一関係になるか。

を判定する。

## 主張上限

source-canonical positive quadratic excitation Casimirとinteger event countのexact operator identity、およびrefinement-invariant area-number compositionを導出した。physical screen typing、conserved mass、absolute calibration、entropy、Hawking physics、finite quantum black holeは未導出である。
