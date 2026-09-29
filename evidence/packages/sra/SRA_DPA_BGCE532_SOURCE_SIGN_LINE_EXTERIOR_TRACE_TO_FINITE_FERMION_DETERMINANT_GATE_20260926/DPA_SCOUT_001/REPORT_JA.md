# BGCE532 監査報告

## 判定

**SCOPED PASS。**

BGCE530で条件として残っていた有限odd Gaussian作用は、独立仮定として置く必要がない。既存のsource sign line、BGCE439のdegree-one matter、BGCE321/322/325のordinary CTP trace、BGCE526/530の正の型付きYukawa作用素を合成すると、有限matter marginalはoperator traceとして

\[
Z_m(H)=\operatorname{Tr}_{\Lambda E}\Lambda(A(H))
=\det(I+A(H)),
\qquad
A(H)=M_H^*M_H=|H|^2M^*M
\]

に一意化される。従って

\[
S_{\mathrm{eff}}(H)
=S_H(H)-\log\det(I+|H|^2M^*M)
\]

のdeterminantのプラス符号と、有効作用のマイナス符号が同時に固定される。Grassmann path integralは、このoperator identityのcoherent-state表現として後から書けるが、導出の仮定には使っていない。

証拠区分は **Theoretical derivation**。数値走査、観測質量fit、Higgs radiusの数値解法は行っていない。

## 1. odd交換則の一意性

BGCE439のtotal Boolean degreeをmod 2へ落とすと、matterはdegree 1、Higgsはdegree 0である。`Z2`上のsymmetric bicharacterは

\[
b_\epsilon(p,q)=(-1)^{\epsilon pq},\qquad \epsilon\in\{0,1\}
\]

の二つだけである。GRADEDSEC-196R/BGCE406が既に固定したparticle permutationのsign characterは

\[
b(1,1)=-1
\]

を要求するため、`epsilon=1`だけが残る。従って交換表は

\[
\begin{pmatrix}
1&1\\
1&-1
\end{pmatrix}
\]

に一意化される。degree-one matterへ別のphaseや七つのlocal two-cocycle候補を選んでいない。

これはBGCE518を覆さない。BGCE518はYukawa pathの局所star countだけからKoszul signを導く経路をNO-GOとした。今回は別にsource-derivedだったparticle sign lineを、既に独立導出済みのmatter parityへpull backしている。

## 2. ordinary exterior traceが符号を固定する

有限one-particle作用素`A`のexterior functorは

\[
\Lambda(A)=\bigoplus_{k=0}^{n}\Lambda^k(A)
\]

である。ordinary traceを取ると

\[
\operatorname{Tr}_{\Lambda E}\Lambda(A)
=\sum_{k=0}^n\operatorname{Tr}\Lambda^k(A)
=\det(I+A).
\]

一方、parity insertion `(-1)^F`を入れたsupertraceなら`det(I-A)`になる。BGCE322の有限CTP cumulantは明示的に`log Tr_P exp(...)`であり、supertraceや`(-1)^F` insertionではない。従ってclosed-contour marginalはordinary traceを選び、`det(I+A)`のプラス符号が固定される。

BGCE530の21 modeについてelementary symmetric polynomialをexact算術で再構成し、

\[
\sum_k e_k(A)=\prod_j(1+a_j)
\]

を確認した。全`a_j>0`なのでpartition factorはstrictly positiveである。

## 3. branch pairingと有効作用

forward Yukawa mapを`M_H`、reverse branchを`M_H^*`とすると、branch-neutralな二次作用素は

\[
A(H)=M_H^*M_H=|H|^2M^*M\ge0
\]

である。BGCE439のup/down/lepton cycleは全てcharge-neutralである。反対順序`M_HM_H^*`を使ってもSylvester identityにより

\[
\det(I+M_H^*M_H)=\det(I+M_HM_H^*)
\]

なのでbranch orientationに依存しない。

matterをtrace outすると

\[
e^{-S_{\mathrm{eff}}}=e^{-S_H}Z_m
\]

であり、従って`S_eff=S_H-log Z_m`。マイナス符号も任意ではない。

BGCE530で既に証明したstrict convexityとboundednessを合わせると、非零Higgs半径はこの宣言class内で条件付きではなくなる。

## 4. 保持する境界

- BGCE406の「sign lineだけではinternal chiralityを選ばない」を保持する。chiralityはBGCE439から独立に取得している。
- GRADEDSEC-196Rのsame-163R creation-compatible transfer失敗を保持する。
- BGCE518のlocal star-derived two-cocycle NO-GOを保持する。
- unchanged raw sourceだけの無条件定理とは呼ばない。BGCE439 anomaly-solution groupoidは明示的なsource-derived extensionである。
- 観測Yukawa値、absolute masses、CKM/PMNS、neutrino sector、running、経験的Standard Modelは未導出。

## 次gate

`BGCE534_SOURCE_NORMALIZED_HIGGS_RADIUS_AND_RELATIVE_FERMION_MASS_OUTPUT_GATE`

今度は、導出済みpotentialの一意なdimensionless Higgs radiusと、`5:4:2`世代作用素および`1:315/356:135/178`species metricを合成し、target fitなしでどこまでrelative fermion mass outputを固定できるかを判定する。
