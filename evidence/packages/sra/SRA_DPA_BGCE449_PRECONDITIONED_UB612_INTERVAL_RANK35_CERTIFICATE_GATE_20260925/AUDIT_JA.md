# BGCE449 preconditioned UB612 interval rank-35 audit

## 結論

**PASS。** correlated backend replayは不要になった。BGCE448の55列からsource-fixedな35列を選び、
exact rational Krawczyk/Beeck型regularity certificateを構成した。actual UB612が保存した
componentwise interval box全体で、35×35 minorは非特異である。

## Certificate

220桁decimal inverseは候補preconditionerを作るためだけに使った。その全entryを有理数へ戻し、
`I-RA`のresidualと`|R|E`のinterval perturbationをFractionでexactに計算した。
さらに正の対角scalingを有理数として凍結し、exact Collatz row upperを評価した。

得られた上界は約

`0.012750158721617564`

で、exactに1未満である。従って選択minorは保存boxの全点で非特異であり、元の35×55 responseは
全boxでrow rank 35を持つ。

BGCE448の最初のminorが失敗したのは物理modeの欠落ではなく、列選択とconditioningの問題だった。

## 意味

BGCE444の抽象10→35 capacity、BGCE447のactual same-carrier theorem、BGCE448のactual 55列構成が、
actual UB612 interval rank 35として結合した。これはtargetを読む係数fitではなく、十個の
source-fixed symmetric generatorsから作った55 unordered pairsの部分minorである。

## Counter-intuition scan

rank 35はfull metric Frechet Hessianや物理的UV completionを自動的に意味しない。本証明対象は
actual U4 quartic tensorのsame-carrier frame二次osculating responseである。full sigma6、parallel
operator、非多項式625-child sampling、smooth continuum stress renormalizationは別境界として残る。

一方、「correlated replay待ち」は撤回する。相関を使わない、より大きい独立interval boxですでにPASSした。
