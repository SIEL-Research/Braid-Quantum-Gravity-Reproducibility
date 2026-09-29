# BQGNEUT-023 — 内部中性carrierとsource重み付きgap

## 結論

**SPLIT SCOPED PASS。**

1. 中性operational sectorでは、外部の三世代carrierは不要になった。
2. source重みだけで縮退gap `(3,3,3)` は非縮退化した。
3. ただし同じ実LaplacianだけではCPは消え、physical PMNS全体はまだ閉じない。

## 外部carrierの解除

BQGNEUT-022で導出した三つのsource reflectionと一意なsource-induced cycle
`C_g`から生成されるstar algebraをexactに閉じると、

\[
\operatorname{Alg}^*(R_{e_1},R_{e_2},R_{e_3},C_g)=M_3(\mathbb C)
\]

となる。複素次元は9、commutantはscalarだけで次元1である。従ってこの三次元空間は、
中性sector自身の状態・観測量・channel・history transportを全て内部に持つ既約qutrit
carrierである。

これは「三世代を外から置く」必要を、中性operational sectorについて解除する。ただし、
このsectorをStandard Modelのlepton doubletやBGCE524のmatter multiplicityと同一視した
わけではない。

## sourceだけによるgap分裂

三つのsource transpositionに、条件付きbranch確率

\[
(w_{r_1},w_{r_2},w_{r_{121}})=\left(\frac7{15},\frac4{15},\frac4{15}\right)
\]

を置く。新しいfit係数は追加せず、canonical weighted transposition Laplacian

\[
L_w=\sum_a w_a(I-P_a)
\]

を作ると、

\[
L_w=
\begin{pmatrix}
11/15&-7/15&-4/15\\
-7/15&11/15&-4/15\\
-4/15&-4/15&8/15
\end{pmatrix}
\]

であり、characteristic polynomialは

\[
\lambda(\lambda-4/5)(\lambda-6/5)
\]

となる。従ってdimensionless spectrumは

\[
0,\quad \frac45,\quad \frac65,
\]

隣接gapは

\[
\frac45,\quad\frac25,
\]

で、比はexactに2である。BQGNEUT-022のequal chord gaps `(3,3,3)` はsource weightsだけで
非縮退化された。PMNS値、neutrino mass gap、parameter scanは使っていない。

## 非補償境界

`L_w`は実対称なので、その固有frameのJarlskog invariantは0である。従って、
BQGNEUT-022の`F_3` nonzero-CP frameと今回の非縮退gapを、別々の演算子から得たまま
physical propagation observableだと宣言することはできない。

さらに、次は未導出である。

- Standard Model lepton spaceとの物理的同一性
- 一つのsource-selected operatorによるnonzero CPとunequal gapsの同時実現
- mass-squaredとしての型付け
- dimensionful absolute scale
- 実測一致

## Counter-intuition

diagonal qutrit algebraとcyclic shiftが`M_3`を生成し、実weighted graph Laplacianがlevelを
分裂させること自体は一般的である。今回の結果は内部数学的carrierの十分性とsource固定の
dimensionless gap形を示すが、自然界のニュートリノとの同一性までは証明しない。

## 次

`BQGNEUT-024_UNIQUE_SOURCE_ORDERED_C3_WEIGHTED_FLOQUET_TO_SIMULTANEOUS_CP_AND_GAP_GATE`

`C_g`のorientationと`L_w`のweightsを一つのsource-ordered unitary/Floquet operatorに
統合し、fitなしでnonzero CPとunequal gapsを同時に持てるか判定する。

## Claim ceiling

証拠区分は**Theoretical derivation**。外部三世代carrier解除は中性operational sectorに
限定される。source-onlyの非縮退dimensionless gapは導出済み。physical PMNS、絶対scale、
Standard Model埋込み、実測ニュートリノ物理、量子重力完成は未主張。
