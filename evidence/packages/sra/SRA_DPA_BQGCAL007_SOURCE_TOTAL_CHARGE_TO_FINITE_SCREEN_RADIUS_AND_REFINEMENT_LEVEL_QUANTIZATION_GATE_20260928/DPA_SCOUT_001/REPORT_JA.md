# BQGCAL-007 報告

## 結論

**SPLIT RESULT：既存total chargeから唯一のrefinement levelを選ぶ経路はSCOPED NO-GO。refinement-invariant composite screenはSCOPED PASS。**

BGCE310の保存total chargeは、全refinement stageで

\[
Q_m=Q_{\rm source}\otimes I_{\rm tail}
\]

として運ばれる。従ってchargeだけに依存する判定は全ての`m`で同じ値を持ち、ちょうど一つの`m`を識別できない。

一方、BQGCAL-004の単一cell面積とBQGCAL-005の25-child conservationを同時に使うと、物理screenの正しい合成則がexactに出る。

\[
A_m=A_0 25^{-m},
\qquad
N_m=K25^m,
\]

なので、完全なdescendant screenの総面積は

\[
\boxed{A_{\rm total}(K,m)=N_mA_m=K A_0}
\]

となり、`m`に依存しない。BQGCAL-006のscreen law

\[
A_B(r)=\frac{24\sqrt3}{25}r^2
\]

と比較すると、shape係数も消えて

\[
\boxed{r_K=\sqrt K\,\ell_*}
\]

を得る。

## 何が修正されたか

`m`はblack-hole stateを表す物理量ではなく、同じscreenをどこまで細かく記述するかというresolution coordinate（解像度の番号）である。単一cellの半径`ell_star 5^{-m}`を、そのままblack-hole半径と読むのが誤りだった。

物理半径を担う候補は、complete screenに含まれる加法的sector数`K`である。従って必要なのはunique `m`ではなく、sourceからpositive integer screen-number operatorを導出することである。

## 既存total chargeをそのままKにできない理由

BGCE310のenvironment chargeはHermitianかつnonzeroだが、非零entryは全てoff-diagonalでtraceはzeroである。従って正・負の固有値を持つindefinite operatorであり、positive integer countではない。

さらにfull environment extensionは一意でなく、source-fixedなのはStinespring compression classである。このchargeを説明なしにcell数`K`へ読み替えることはできない。

## Counter-intuition scan

通常の説明は単純である。mesh refinementは固定された面を細分化するだけなので、総面積と総energyは変わらない。今回の`25^m`と`25^{-m}`の相殺自体はこの標準的なregulator invarianceで説明できる。

Braid固有なのは、25-child law、正四面体screen係数、total chargeのidentity-tail transportが同じsourceからexactに与えられる点である。しかし`K`がまだsource observableではない以上、量子black-hole面積スペクトルとは呼ばない。

## 次

`BQGCAL-008_SOURCE_POSITIVE_SCREEN_NUMBER_AND_QUASILOCAL_ENERGY_TO_REFINEMENT_INVARIANT_HORIZON_AREA_GATE`

で、次を一度に問う。

1. source-centralなpositive integer number operator `N_screen`を導出できるか。
2. `N_screen`が25-adic refinementと可換で、`K`を保存するか。
3. finite total Ward energyとの係数なし関係から、marginal screen面積を選べるか。

## 主張上限

既存total charge単独によるunique refinement-level selectionを排除し、complete descendant screenのrefinement-invariant area/radius lawを導出した。`K`のsource observable化、quasi-local energyとの結合、absolute SI radius、mass、Newton定数、entropy、Hawking physics、finite quantum black holeは未導出である。
