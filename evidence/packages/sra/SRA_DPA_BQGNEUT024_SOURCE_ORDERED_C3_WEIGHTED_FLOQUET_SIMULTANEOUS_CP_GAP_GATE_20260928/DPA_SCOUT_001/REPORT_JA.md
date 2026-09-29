# BQGNEUT-024 — source-ordered FloquetでCPとgapを同時閉包

## 結論

**SCOPED PASS。**

一個のsource-fixed演算子

\[
U_F=C_g\exp\!\left[-i\frac{2\pi}{3}L_w\right]
\]

が、exact unitaryであり、同時に以下を持つ。

- 三つの相異なる、等間隔でない固有位相
- exactに非零のCP-odd numerator
- 非零のJarlskog invariant
- 外部三世代carrierなしの中性operational作用

観測PMNS値、neutrino mass gap、角度scan、係数fitは使っていない。

## なぜ一個の演算子なのか

BQGNEUT-022の`C_g`はsource conjugationの正向き三周期を表す。BQGNEUT-023の
`L_w`は同じ三branchのsource weights `(7,4,4)/15`から得た。interaction evolutionの
後に次のsource slotへtransportするhistory orderを、そのまま積の順序にした。

period angle `2 pi/3`は`C_g^3=I`の正向き一stepで固定した。別角度は試していない。

## Exact certificate

全行列要素はcyclotomic field `Q(zeta_15)`にあり、

\[
U_F^\dagger U_F=U_FU_F^\dagger=I
\]

をexact arithmeticで確認した。characteristic polynomialは

\[
(\lambda-1)
\left[
\lambda^2+rac{\zeta_{15}^{-4}+\zeta_{15}^{-6}}2\lambda
+\zeta_{15}^{5}
\right]
\]

である。quadratic discriminantはexactに非零で、`lambda=1`もquadratic factorの根では
ない。またtraceもexactに非零なので、三固有位相は等間隔の三等分ではない。

固定branchでの固有位相は概数

\[
(0,\ 2.1436299182,\ 6.2339504914),
\]

circular gapsは

\[
(2.1436299182,\ 4.0903205733,\ 0.0492348158)
\]

で、三つとも正かつ相異なる。

CPについては`A=U_F-U_F^dagger`として、

\[
2\operatorname{Re}(A_{01}A_{12}A_{20})
\]

の`Q(zeta_15)` power-basis係数が

```text
(1/24, 1/24, 0, 0, -1/24, 0, 1/24, 0)
```

となり、exactに非零である。固有frameから得る値は

\[
|J|=0.0855780197751\ldots
\]

で、direct invariantとの誤差は`2e-16`程度だった。

## 何が閉じたか

BQGNEUT-022ではnonzero CPは出たがgapが縮退していた。BQGNEUT-023ではgapは割れたが、
real Laplacian単独の`J`は0だった。今回は同じ一個の伝播演算子が両方を持つ。

従って「別々の演算子から都合よくCPとgapを読む」という弱点は解除された。

## 非補償境界

これは中性operational qutritのdimensionless Floquet theoremである。次はまだ未導出。

- このqutritと物理的三世代lepton/neutrino spaceのsource-native同一性
- eigenphase gapからmass-squared gapへの物理型付け
- absolute time/mass scale
- 実測PMNS・oscillation dataとの一致

## Counter-intuition

oriented qutrit shiftと非可換weighted unitaryの積がCPとunequal phasesを持つこと自体は
一般に起こり得る。今回強いのは、演算子・順序・角度・weightsが現在のsourceから固定され、
targetを見ずにexact gateを通った点である。自然界のニュートリノとの同一性は別問題である。

## 次

`BQGNEUT-025_SOURCE_NATIVE_WEAK_CURRENT_INTERTWINER_TO_PHYSICAL_THREE_NEUTRINO_TYPING_GATE`

charged-lepton sectorと今回のneutral qutritの間に、source-native weak-current intertwinerが
一意に存在するかを問う。これが通れば「物理的三世代ニュートリノ空間との同一性」を
dimension matchingではなくinteraction typingで閉じられる。

## Claim ceiling

証拠区分は**Theoretical derivation**。一個のsource-ordered dimensionless neutral
Floquet operatorにおけるnonzero CPとunequal eigenphase gapsまで。physical PMNS、
dimensionful neutrino masses、実測一致、量子重力完成は未主張。
