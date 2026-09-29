# BGCE447 source-cylinder / actual UB612 same-carrier audit

## 結論

**PASS。** actual UB612 PBM metric は、BGCE290/BGCE446のsource-cylinder metricと
同じ ordered four-carrier へ、係数fitなしで可逆に戻せる。

鍵は「どちらも4次元だから」ではない。BGCE290のsource frameは

`G1, {G1,P_chi1}/2, {G1,P_chi2}/2, {G1,P_chi3}/2`

であり、actual PBM lineageのUB476は同じ順序で

`X_chi=(G1 P_chi+P_chi G1)/2`

を採用する。この二つの空間方向は同じ演算子である。三characterの順序も
`H4/2`の三つの非自明rowと一致する。

## 可逆変換

UB476が行うclock直交化は `Y_i=X_i-c_i G1` である。変換行列は対角がすべて1の
三角行列なのでdeterminantはexactに1。保存metricはclock-space混合がexactに0、
clock成分が負、spatial LDL pivotがすべて正である。

creation scaleも保存interval全体で正である。したがって、Hadamard frame、clock直交化、
正のscale、PBM coordinate transportを合成した4-carrier mapは可逆で、そのSym2誘導写像も
rank 10のまま可逆である。これは自由な`GL(4)`合わせではなく、既存source recipesで固定された写像である。

## Actual lineage

`UB476 -> UB496 -> UB596E -> UB597A -> UB598J/UB598O -> UB612`

をdigestと保存box IDで照合した。UB612のmetric loaderはUB596Eのterminal chartを再利用し、
actual Ricci、nabla Ricci、nabla2 Ricci、Riemann packetは同じUB597A boxと
`p1,p2,p3,H` root orderを持つ。従ってBGCE447のintertwinerは、抽象PBMではなく
actual UB612が読んだmetric lineageへ接続する。

変換はsource座標に依存しない定数線形写像なので、metricの微分および有限jetと可換する。

## Counter-intuition scan

A57S-X49は、character screenと別の `H,L,L^2,L^3` marker-moment screenが同じ部分空間ではないと示した。
このnegative resultは保持する。しかしactual UB612 lineageはその旧screenではなく、UB476の
`G1,X_chi1,X_chi2,X_chi3` screenからPBMへ入る。従ってX49の残差をcurrent PBM carrierへ
移植するのは型違いである。

## 境界

同じcarrierと可逆intertwinerは閉じたが、これだけでactual PBM metricが625 child sampleから
生成されたとは言えない。非多項式metricの一様補間誤差、actual 55-column U4 source Hessian、
full sigma6/parallel operator、物理的UV completionは次ゲートに残る。
