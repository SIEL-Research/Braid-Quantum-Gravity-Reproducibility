# UB612 — PBM covariant transport jet generator gate

## 実行結果

固定済みUB597A PBM中心について、保存済みのactual `Riemann`、`Ricci`、`nabla Ricci`、`nabla2 Ricci` 区間tensorを同じ `p1,p2,p3,H` dual方向で縮約した。target stress、face符号、root位置は入力していない。

`U=1+U2+U3+U4+O(|y|^5)` の10個の二次係数、20個の三次係数、35個の四次係数を生成した。四次は `nabla2 Ricci/80`、`tr(K0^2)/360`、`tr(K0)^2/288` の三sectorを別々に保存した。さらに `v00`、4個の `v01`、10個の `v02` を生成し、UB530のtransport recurrenceを全係数・四root区間で零包含確認した。

## sigma6 の座標監査

4次元時空計量 `g` のexponential-midpointを使い、endpointを `Exp_m^g(-y/2)` と `Exp_m^g(+y/2)` に取れば、world functionは `sigma=g_m(y,y)/2` でexactになる。しかしUB594Fで固定されたstate側frameは、初期3次元計量 `gamma0` の**空間**exponential-midpointとequal-time Cauchy kernelである。

現在のPBM中心はextrinsic curvatureが非零なので、equal-timeの `gamma0` 空間geodesicを4次元時空geodesicと同一視できない。従って4D midpoint identityを使ってactual `sigma3..6` を零とする短縮は棄却した。

## 最初の失敗点

残ったのは4D Hps germを固定 `gamma0` spatial-midpoint Cauchy frameへ移す一つの有限adapterである。このadapterが `sigma6`、time-normal derivatives、parallel/horizontal curvature termsを同時に生成する。radial parallel frameではparallel propagatorの成分を恒等にできるが、そのframeを横方向へ動かす微分は曲率を生むので零とは置けない。

UB516 quartic fixtureをdependency-free有理数で再生すると、raw `U` contributionは `tr(S)/192`、必要なparallel/horizontal contributionは `-tr(S)/192` である。後者を捨てればexact regressionが失敗する。従ってUB612は `U4,v0_2` のactual center＋四rootを通したが、actual `sigma6,parallel4` はここでfail-closedとする。

## 次

UB613は、4D spacetime Fermi/normal jetから固定 `gamma0` spatial-midpoint Cauchy frameへの有限変換をdegree 6/4まで導出し、UB516の相殺とcoincidence identitiesを先に通す。これが通れば本artifactの `U4,v0_2` に作用させ、UB611 callbackのHadamard側を閉じる。

20 stress値、8 face、無条件root、Ward時間発展、Braid固有性、自然実証、完全統一は未完である。
