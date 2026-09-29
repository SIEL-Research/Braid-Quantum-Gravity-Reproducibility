# BGCE290監査 — 独立source solderからHilbert stress / Wardへ

## 結論

**FULL PASS（宣言した長波長・局所・二階・形式的自己共役・保存的クラス内）。**

BGCE289で残った問題は、metricのodd 3方向がmatterのthetaと同じ変数だったため、matter固定のHilbert変分がrank 7に落ちることだった。BGCE290は、新しい変数を足さず、BGCE142/143から既に存在するmatter-independentな10個のdoubled source `a_A`を用いてこのlockを解除した。

- source frame：`[G1,{G1,P1}/2,{G1,P2}/2,{G1,P3}/2]`。
- metric sources：その対称二乗に属する10個の`a_A`。
- causal frame map：BGCE268の正規化Hadamard `U=H4/2`。
- induced solder：`H_ray=U^T A_char U`。
- exact rank：10。
- causal parity split：even 7、odd 3。
- `S4` intertwining：240/240 exact。
- fixed-matter metric variation：rank 10。
- fitted coefficient：なし。

したがってBGCE289のrank-7 obstructionは、この宣言クラス内では解除された。

## stressとWard

任意の対称metric tangent `H`には、既存のevent causal metric `K_evt`に対して

```text
S=(1/2) K_evt^{-1} H,
S^T K_evt + K_evt S = H
```

というexactなcoframe strain liftがある。10 basisすべてで成立した。source-selected Umegaki/logZ-Bregman edge scalar、Braid event transition coboundary、BKM target metric、source-OS continuationを保つ最小IR作用は

```text
S_BKM=(1/2) integral sqrt|g| G_AB(lambda)
      g^mn partial_m lambda^A partial_n lambda^B d4x
```

である。これをmatter field `lambda`を固定してmetric変分すると

```text
T_mn=G_AB(lambda)[partial_m lambda^A partial_n lambda^B
     -(1/2)g_mn g^rs partial_r lambda^A partial_s lambda^B]
```

を得る。diffeomorphism Noether identityは

```text
nabla^m T_mn = -E_A partial_n lambda^A
```

であり、matter方程式 `E_A=0` 上で

```text
nabla^m T_mn = 0
```

となる。

## 何が突破されたか

これは「stressの式を外から置いた」のではない。既存Braid lineage内の独立source、operator frame、causal Hadamard map、event transition、BKM応答、OS continuationを同じ型で結び、metricとmatterを独立に変分できるようにした。新しいmatter actionも手動係数も追加していない。

## 保留境界

本結果はまだ次を意味しない。

- 高階微分または異なるprincipal symbolを持つ全作用の排除。
- full finite-Braid Lorentz parentの導出。
- retained real affine/Stone completionの除去。
- MMR2またはsource `3/5` の再導出。
- Einstein方程式、自然界の重力、完成量子重力の証明。

さらに、本gateは同じDPA lineage内の導出である。`a_A`の物理metric source typing、Hadamard solderの一意性、active Markov transport、曲率potential排除、Noether対象の同一性をBGCE291で一次コードから独立に再導出し、過剰昇格がないかを判定する。それまでは「宣言クラス内FULL PASS、独立scope red-team待ち」とする。

## DPA反対直観

- Observed Evidence：rank-10 Sym2 map、7+3 split、240 exact intertwining checks、10 exact strain lifts。
- Interpretive Leap：このsource-frame mapが物理的metric solderであり、source actionのactive transportを固定する。
- Alternative Explanation：Hadamardはquantum carrierの同型にすぎず、metric sourceの物理同定には追加の自然性仮定または`GL(10)`自由度が残る。
- Falsifier：source typingの不一致、同じ固定構造を保つ非同値solder、transport後のon-site killing term、またはBKM作用と変分対象metricの不一致。
- 判定：BGCE290内ではPASS。最終昇格はBGCE291に留保。
