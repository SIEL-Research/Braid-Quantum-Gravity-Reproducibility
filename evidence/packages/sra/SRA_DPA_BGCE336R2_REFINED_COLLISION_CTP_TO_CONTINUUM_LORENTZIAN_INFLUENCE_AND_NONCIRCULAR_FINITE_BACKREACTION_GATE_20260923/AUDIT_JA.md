# BGCE336R2監査 — refined collision CTPの連続極限と有限backreaction境界

## 結論

**SPLIT PASS。**

任意の`gamma>0`について、同じ有限Braid collision sourceから、連続source-event-time上の正規化されたcausal CTP influence familyと有限な4成分reduced total-balance densityが導出できる。親の数値`q0`を先に一意選択する必要はない。

一方、これはまだfull local `3+1` Lorentzian Schwinger–Keldysh field functionalではない。既存の4 aligned scoreはoperational probeであり、物理計量`g+`,`g-`からcollision generatorへのsource-native mapではない。そのためinteraction termをHilbert metric variationとして導出できず、full finite noncircular quantum backreactionは未達である。

## 1. exact refined semigroup

meshを

\[
h_m=5^{-m},\qquad q_m=e^{-\gamma h_m}
\]

とする。Reynolds expectationを`E`とすると`E^2=E`なので、

\[
\Phi_h=E+e^{-\gamma h}(I-E)
=e^{h\gamma(E-I)}
\]

がexactに成立する。従って

\[
\Phi_{h/5}^{,5}=\Phi_h
\]

であり、`gamma`の具体値を決めなくても各`gamma>0`についてCPTP/unitalな連続semigroupが存在する。

これはabsolute physical rateを一意化したという意味ではない。`gamma`は依然として連続族であり、秒との対応には較正が必要である。

## 2. real-time CTP limit

各cellのsource insertionを積分量として

\[
U_h[J]=e^{-ihJ^\alpha S_\alpha}
\]

とする。doubled one-step mapは

\[
\mathcal M_h^{J_+,J_-}(X)
=\Phi_h\!\left(e^{-ihH[J_+]}Xe^{+ihH[J_-]}\right).
\]

有限次元Lie product theoremにより、bounded piecewise-continuous sourceに対して有限積はoperator normで

\[
Z_\gamma[J_+,J_-]
=\operatorname{Tr}\!\left[
\mathcal T_C
e^{\int(\mathcal L_\gamma+\mathcal K[J_+,J_-])dt}
\rho_0\right]
\]

へ収束する。

有限meshで成立する次の性質は極限でも維持される。

- `Z[J,J]=1`。
- branch Hermiticity。
- largest-time cancellation。
- retarded support。
- noise quadratic formのpositive semidefiniteness。

従ってこれは有限内部代数上のcontinuous event-time Lorentzian/real-time CTP influence functionalである。

## 3. total-balance density

BGCE330のq-symbolic balanceから

\[
D_{G1}(h)
=(1-e^{-\gamma h})[G_1-E(G_1)]
\]

なので、

\[
\lim_{h\to0}\frac{D_{G1}(h)}h
=\gamma[G_1-E(G_1)].
\]

environment chargeも

\[
B_{gh}(h)=\frac{c_{gh}}{36}(1-e^{-\gamma h})
\]

から

\[
\lim_{h\to0}\frac{B_{gh}(h)}h
=\frac{c_{gh}\gamma}{36}
\]

となる。spatial defectも同じ`1-q` scalingを持ち、各有限hで4-generator strong completionが存在するため、reduced/compressed 4成分balance densityは有限である。

ただしfresh-tail dilation spaceはrefinementごとに変わり、off-support completionは非一意である。従って一つの固定Hilbert space上のunique microscopic interaction tensorのstrong limitまでは導出されない。

## 4. finite backreactionがまだ閉じない理由

BGCE325のeffective continuum Hilbert stressとon-shell Ward、およびBGCE300R1の宣言済みクラス内のnoncircular low-energy Einstein backreactionは維持される。fixed-model MMR2もBGCE300R1ではclosedである。

しかし今回のcontinuum CTPがBGCE325のBregman/Hilbert stressのquantum parentであることはまだ証明されていない。必要なのは

\[
(g_+,g_-)
\longmapsto
\mathcal L_\gamma[g_+,g_-]
\]

というsource-derived doubled-metric deformationである。これがなければ

\[
T^{int}_{\mu\nu}
\propto
\frac{\delta\Gamma}{\delta g_a^{\mu\nu}}
\]

を物理的interaction stressとして定義できない。現在のscore insertionをmetric variationと呼ぶだけでは新しい仮定になる。

## 5. 旧revisionの扱い

- `BGCE336`：補助浮動小数点witnessの固定閾値でpre-result停止。科学的結果なし。
- `BGCE336R1`：result dictionaryのPython/JSON literal誤りでpre-result停止。科学的結果なし。
- `BGCE336R2`：科学的gateは変更せず、実行前compileと明示的roundoff boundを適用して完走。

## 6. source・endpoint監査

- source revision：`8afbcfd975bab0455456d0e89f048813cb3ecea3`。
- 全入力はSHA-256でrevision-matched。
- path-derived label、data split、介入データはない。
- 本結果は有限次元operator theoremの`Theoretical derivation`。
- E0/E1/E2は要求も主張もしない。
- 補助数値witnessは`gamma=1`のformula checkだけであり、rate selectionや結論には使用しない。

## 7. 次

次は

`BGCE337_SOURCE_CANONICAL_GNS_DOOB_METRIC_TILT_TO_VARIATIONAL_INTERACTION_STRESS_GATE`

である。canonical modular referenceとaligned BKM scoresから、CPTP性・CTP identities・4成分balanceを同時に保つuniqueなmetric-dependent quantum Doob/GNS tiltが出るかを判定する。

## 8. claim ceiling

BGCE336R2は任意の正`gamma`について、有限source algebra上のcontinuous event-time causal CTP influence familyと有限reduced 4成分balance densityを導出する。full local `3+1` Lorentzian SK field theory、source-native metric deformation、unique microscopic interaction Hilbert stress、physical-temperature FDT、full finite quantum backreaction、自然界の重力、完成量子重力は導出しない。
