# BGCE238 — fixed source packetはfull-corner coherenceを選ぶか

固定source revision: `cacd2cec998ef95e5abf3fb48bdeb57f2a76e54a`。

BGCE237は三つのmarked source atomの全partition retractionが、10-source span rank、BKM Hessian rank、
Hamiltonian non-scalarityを保存すると示した。しかしその試験は各partitionごとに元の固定operator
`P F_A P`と`P G_1 P`をさらに`D_pi`で置換しており、**同じsource packetを保存したのではなく、同じ
次元を持つ別packetへ変更することを許していた。**

MMR2の目的は元の全matter sourceをmarked cornerへroutingすることであって、post-event quantum
instrumentを一意化することではない。本gateではno-retuning/source-identityを判定基準に戻す。

固定packetを

\[
\mathcal S_\cap=\{P G_1P,\;P F_A P\ (A=1,\ldots,10)\}
\]

とする。三atomの各partition `pi`について

\[
D_\pi(X)=\sum_{B\in\pi}P_BXP_B
\]

を作用させ、`D_pi(X)=X`が11 operatorすべて、全8 signed sectorで成立するかをexactに検査する。

成功条件は次の通り。

1. full partition `012`は固定packetを全てexactに固定する。
2. `01|2`, `02|1`, `12|0`, `0|1|2`は、それぞれ全sectorで少なくとも一つの固定operatorを変更する。
3. 変更はnonzero cross-block coherence residualとして保存し、係数fitやrankだけの比較を使わない。

成功すれば、BGCE236のinstrument非一意性はmatter-action選択には不要だったと訂正する。source-atom
partition class内では、元packetを変更せずに保持する物質代数はfull cornerだけであり、BGCE235の
`W_cap`、outer `P`、source cup `3/5`をそのまま採用できる。任意CP instrumentの一意性や自然界での
物理測定は主張しない。

失敗すればcross-atom coherence/recoverability則がなお必要である。5要素partition latticeの完全判定、
first-witness停止を使い、長時間走査を行わない。DPAはformal E0/E1/E2を発行しない。
