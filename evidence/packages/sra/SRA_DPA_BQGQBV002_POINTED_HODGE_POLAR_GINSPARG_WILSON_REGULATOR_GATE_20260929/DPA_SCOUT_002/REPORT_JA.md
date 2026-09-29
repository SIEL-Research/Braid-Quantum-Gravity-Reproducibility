# BQGQBV-002監査 — pointed Hodge-polar chiral regulator

## 結論

**CLOSED_SCOPEDです。chiral regulatorはflatおよびgap-admissibleなlocal regular
source branchで導出されました。**

BGCE399のactual 4次元source-cylinder complexは、one cubeでeven/odd次元
`41/40`、Hodge-incidence rank `40`、index `1`です。全Hodge--Dirac

\[
B_n=d_n+d_n^\dagger
\]

のkernelはexactに1次元で、algebra unitであるconstant 0-cochainだけです。sourceの
pointingとunitalityがこのlineの符号を`+1`に固定します。

`B_n`のnonzero support上のpolar signを使い、harmonic unit上だけ`+1`で完成した
self-adjoint involutionを`S_n`と置きます。すると

\[
V_n=\Gamma_nS_n,\qquad D_{\rm GW,n}=1-V_n
\]

は外部Wilson係数、mass threshold、観測fermion dataなしで定まります。

exactに

\[
V_n^\dagger V_n=1,
\qquad
\Gamma_nV_n\Gamma_n=V_n^\dagger,
\]

したがって

\[
\Gamma_nD_{\rm GW,n}+D_{\rm GW,n}\Gamma_n
=D_{\rm GW,n}\Gamma_nD_{\rm GW,n}
\]

です。modified chiralityは`S_n`そのもので、indexは

\[
\frac12\operatorname{Tr}(\Gamma_n+S_n)=1
\]

となります。

## 全refinement gap

一辺`n=5^m`のcubical complexで、`h^{-1}=n`によりrescaleしたnonzero gapは

\[
\delta_n=2n\sin\!\frac{\pi}{2(n+1)}.
\]

`sin x >= 2x/pi`から

\[
\delta_n\ge \frac{2n}{n+1}\ge1
\]

です。従ってfree source regulatorのgapはrefinementで閉じません。gauge/metricを
covariant edge transportとして入れても、このgapを閉じないlocal regular admissible
branchではpolar functional calculus、index、GW identityが維持されます。

## 境界

- BGCE439 coefficient moduleとのtensorはflat backgroundでcompact-gauge equivariant。
- local gauge transformationはcovariant incidenceを共役するためpolar signも共役する。
- arbitrary strong gauge/metric backgroundでgapが閉じないこと、exponential locality、
  singular branch横断は未証明。
- anomaly cancellationは既知だが、BV half-densityとregulated BV divergenceはまだ未構成。

したがってchiral regulatorは限定scopeで閉じましたが、QMEとrenormalizationはまだ
閉じていません。

## 次

`BQGQBV-003`でsource-induced BV half-densityを構成し、regulated modular anomalyを
計算し、finite QMEとrefinement BV pushforwardのassociativityを同時に判定します。

