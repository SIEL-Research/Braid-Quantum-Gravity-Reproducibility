# BQGCAL-042 監査報告

## 結論

**SPLIT CLOSED_SCOPED_EXACT / SOURCE-ONLY NO-GO**。

宣言済みの型付き連続体量子unit-restoration classでは、独立なdimensionful external anchorの最小本数は厳密に

\[
N_{\rm anchor}=1
\]

である。

- `0本`：不可能。dimensionless source packetを不変に保つ非自明な正のglobal rescaling軌道が残る。
- `1本`：十分。正のtime anchor `tau`を一つ与えれば、固定された変換定数`c`, `hbar`と、必要なら温度用の`k_B`により、検査した全dimensionful quantityが一意なmonomialとして復元される。

従ってBGCE374のscale rank `2`は、物理stress/action typingが未接続だった段階の上限である。BQGCAL-035の4次元event-cell measure、BGCE325のeffective Hilbert stress、BQGCAL-025の量子作用単位、BGCE499-002の型付き`3/5`を合成した宣言済みクラスでは、残る自由scaleは`1`本へ減る。

## 必要性：なぜゼロ本では閉じないか

任意の`lambda>0`に対する

\[
\tau\mapsto\lambda\tau
\]

は、すべてのdimensionless source記録、確率、相対係数、正規化作用を不変に保つ。一方で物理量は

\[
 t,x,E,V_4,T_{\mu\nu},\kappa,G,m,\Theta
 \mapsto
 \lambda^{1,1,-1,4,-4,2,2,-1,-1}
 (t,x,E,V_4,T_{\mu\nu},\kappa,G,m,\Theta)
\]

と変化する。作用`S`だけは`hbar`を単位として指数`0`である。

従ってsource-only mapはこの軌道上でinjectiveではない。dimensionful source invariantが新たに導出されない限り、ゼロアンカー絶対スケールは数学的に不可能である。

## 十分性：一つのanchorで何が決まるか

一つの正のtime anchor`tau`を与えると、次が一意に決まる。

\[
\begin{aligned}
t_{\rm phys}&=\tau\hat t,&
x_{\rm phys}&=c\tau\hat x,\\
\omega_{\rm phys}&=\tau^{-1}\hat\omega,&
E_{\rm phys}&=\hbar\tau^{-1}\hat E,\\
S_{\rm phys}&=\hbar\hat S,&
V_{4,{\rm phys}}&=c^3\tau^4\hat V_4,\\
T_{\rm phys}&={\hbar\over c^3\tau^4}\hat T,&
\kappa_{\rm phys}&={3\over5}{c\tau^2\over\hbar},\\
G_{\rm phys}&={3\over5}{c^5\tau^2\over8\pi\hbar},&
m_{\rm phys}&={\hbar\over c^2\tau}\hat m,\\
\Theta_{\rm phys}&={\hbar\over k_B\tau}\hat\theta.&
\end{aligned}
\]

log calibration mapは一列で、timeの指数が`1`なのでrankは厳密に`1`である。このクラス内に第二の独立scaleは残らない。

ここで`c`, `hbar`, `k_B`はfitする経験anchorではなく、物理単位を結ぶ固定変換定数として数えている。この数え方を変えれば用語上のanchor数も変わるが、独立な未同定scale parameterが一つであるというrank定理は変わらない。

## 既存device clockとの区別

BQGCAL-001は、既存PMNS/AWS device clockを同じcellの普遍anchorとして直接使うと、予測`G`がCODATA値の約`1.65 x 10^65`倍になることを示した。

これは今回の構造定理と矛盾しない。

- 今回：普遍anchorが何本必要かを証明した。
- BQGCAL-001：既存device clockがその普遍anchorではないことを示した。

従って既存device clockを普遍化してはいけない。

## BQG台帳への判定

- `BQG-G3-R03.2`：`EXTERNAL_PENDING`を維持するが、欠落内容を「二つの独立anchor」から「厳密に一つの普遍anchorの値とmetrological traceability」へ縮小する。
- absolute scale rank：`2 -> 1`。
- source-only zero-anchor closure：`NO-GO`。
- minimal one-anchor theorem：`CLOSED_SCOPED_EXACT`。
- `BQG-G3-R03.5`：absolute observablesは同じ一anchorの値に依存する。

## 主張上限

本gateは、宣言済みの長波長・局所・二階・形式的自己共役・保存的な連続体classにおけるunit restorationの独立anchor本数を閉じた。

普遍anchorの数値、SI traceability、finite all-scale action、観測Newton定数の予測、black-hole観測、完成量子重力を導出したものではない。またphysical-action typingを無条件finite Braid source theoremへ昇格したものでもない。

## 次gate

`BQGCAL-043_SOURCE_QUANTUM_PHASE_ACTION_AND_EVENT_CELL_TYPE_COMPOSITION_TO_UNCONDITIONAL_ONE_ANCHOR_GATE`

目的は、今回の一anchor十分性に残る`declared typed continuum class`という条件を、source quantum phaseとevent-cellの合成からさらに狭めることである。
