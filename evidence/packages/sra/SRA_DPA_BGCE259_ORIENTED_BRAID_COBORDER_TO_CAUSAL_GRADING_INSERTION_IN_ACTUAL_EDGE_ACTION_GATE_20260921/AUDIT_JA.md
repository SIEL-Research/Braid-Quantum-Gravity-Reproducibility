# BGCE259監査 — Braid orientationだけではLorentz符号を作用へ残せない

## 判定

**FAIL。orientation-only経路は閉じた。** BGCE139のactual event map `R_evt`は25 atoms上のinvolutionである。forward displacementを

\[
\delta(x)=R_{\rm evt}(x)-x
\]

とすると、reverse edgeでは`-delta`になる。全25 atomsのfirst momentはforward/reverseともzero、second momentは双方とも

\[
M_2=
\begin{pmatrix}
28&-20\\
-20&28
\end{pmatrix}
\]

で完全一致した。従ってorientation-odd coborderの二次momentはzero、rank 0である。

## chart parityも符号を残さない

BGCE137の24 chart assignmentsはcanonicalなorientation double coverを持ち、12 even / 12 oddへ分かれる。各chartの3 adjacent crossingsをBGCE256と同じ規則で埋め込むと、

\[
Q_{\rm even}=Q_{\rm odd}=Q_4.
\]

よってparity-signed Haar moment

\[
\frac12(Q_{\rm even}-Q_{\rm odd})
\]

もexact zero、rank 0。even/oddのどちらかだけを採る場合もpositive `Q4`のままで、BGCE258の

\[
K_{\rm evt}=J_{\rm ray}Q_4
\]

にはならない。

## full marked wordの向きとquadratic actionの向きは別

BGCE134はpositive marked wordをaffine cycle `r`、inverse wordを`r^{-1}`へ送るので、full word provenanceはorientationを失っていない。今回失われたのは、その後のevent-map/relative-entropy二次化である。

BGCE254のUmegaki divergenceは有限差では一般に非対称でも、diagonal近傍の二次Hessianはforward/reverseで同じBKM metricになる。Lorentzian principal symbolに必要なのはまさにこの二次項なので、高次のorientation非対称性を時間方向のminusへ読み替えることはできない。

さらにforward/reverse second momentが同じため、任意のscalar係数`alpha,beta`による組合せは`(alpha+beta)Q4`にしかならない。positive definite `Q4`のscalar倍でindefinite `K_evt`を作ることは不可能である。uniform modeだけへ別weightを入れれば作れるが、それはBGCE258の`J_ray`を手動挿入したのと同じであり、導出ではない。

## 依存関係

- BGCE134のfull-word orientation：維持。
- BGCE258のsource-canonical Lorentz carrier：維持。
- forward/reverse coborderによるaction selection：NO-GO。
- A4 parityによるaction selection：NO-GO。
- parent kinetic、off-shell metric variation、Ward、SDPC、無条件`G=(3/5)T`：未達。
- MMR2解除とsource由来`3/5`：維持。今回も`3/5`は設定していない。

## 次の最短候補

実数二次momentへ落とした後ではorientationが消える。従って次はその直前に残る可能性のある構造だけを問う。

1. marked Braidのcomplex/unitary phaseの二次変分。
2. 既存doubled-sourceのbranch pairing。

このどちらかがsourceから`J_ray`と同じtrivial/standard mode splitを持つなら、signed principal symbolを実際の作用から導ける。どちらもbranch spaceの符号をspacetime modeへ送る型付き写像を持たなければ、action-selectionには新原理が必要と確定する。

## DPA分離とclaim ceiling

- Observed Evidence：actual involution、forward/reverse同一second moment、even/odd chart同一`Q4`、orientation-odd rank 0。
- Pattern：word-level orientationはquadratic graph energyで消える。
- Interpretive Leap：coarse graining前のphaseまたはbranch pairingなら符号を保持する可能性がある。
- Alternative Explanation：可逆graph Dirichlet formがorientation-evenなのは標準的であり、Braid固有の異常ではない。
- Novel Hypothesis：source phaseまたはdoubled branchのHessianが`J_ray Q4`を生成する。
- Falsifier：そのHessianがzero、positive、branch-spaceだけに閉じる、または任意intertwinerを要すること。
- Confidence：orientation-only NO-GOには高い。次候補には未判定。
- SIEL-generation classification：`SIEL_GUIDED_STANDARD_COMPATIBLE`。

一次区分は**Theoretical derivation / no-go**。量子重力完成、経験的重力、存在論、主観、意識は示さない。
