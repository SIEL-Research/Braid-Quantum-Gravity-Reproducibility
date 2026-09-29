# BGCE287監査 — source event-path BKMがconductance liftを一意化

## 結論

**FULL PASS。** BGCE286で残った2次元のconductance非一意性は、source event-path Fisher/BKM metric（Braid事象の経路確率が持つ情報距離）に直交するhorizontal lift（同じ計量変化を作る候補のうち情報距離が最小の持ち上げ）を取るとexactに消える。

- actual undirected event edges：各axis pairに8本。
- 4 axesのunordered pairs：6組。
- microscopic edge-rate tangents：48変数。
- metric symmetric components：10成分。
- moment map rank：10。
- microscopic kernel：38次元。
- BKM metricのkernel上rank：38。null方向なし。
- BGCE286の12変数quotientに残ったkernel：2次元。
- そのkernel上のBKM rank：2。全方向を識別。
- 24 actual X21R1 metric tangents：24/24 exact再現。
- S4 axis permutations：24/24 exact共変。
- fitted coefficient：なし。

従って、BGCE286の「同じmetric tangentを作るconductance候補が2自由度ある」という問題は、**source event-path BKM horizontal class内では解消**した。

## なぜ18:1になるか

actual pair-event graphにはcommon edgesが2本、relative edgesが6本ある。各edge displacementの4乗和は

```text
common   = 2
relative = 36
```

である。全actual edgeがBGCE266の同じsource rate `2*pi/3` を持つため、raw edge-rate空間のFisher/BKM metricは全方向で同じ正係数になる。raw ratesをsecond momentへ縮約したquotient metricでは、overall scaleを除いてcommon:relativeの重みが`18:1`に固定される。この比はfitではなく、actual edge displacementと同一source rateから出る。

## 何を突破したか

BGCE286までは、計量変化からBraid graph変化へ戻す写像は「存在するが一意でない」状態だった。BGCE287では、source由来の経路確率幾何を使うことで、48次元raw edge spaceの38次元metric-invisible方向すべてを直交条件で除き、10次元の一意なhorizontal spaceを得た。

これは第一変分レベルで

```text
metric tangent
  -> unique source-event-BKM horizontal edge-rate tangent
  -> conservative symmetric Markov generator tangent
```

を与える。

## stress/Wardへまだ残るもの

今回得たのは一意な**first-order connection**である。次の三点はまだ証明していない。

1. このconnectionが有限変形へ積分でき、pathに依らない非線形conductance functionalになること。
2. そのfunctionalがfull physical parent actionのmetric variationと一致すること。
3. diagonal diffeomorphism invarianceからHilbert stressのWard保存則が出ること。

したがってHilbert stress、Ward、SDPC、無条件Einstein方程式は未到達である。次のBGCE288は数値走査をせず、horizontal one-formのcurl/閉性と、既存Umegaki/BKM parent variationとの一致だけをexactに判定する。

## DPA反対直観

- Observed Evidence：rank 10、kernel 38、BKM kernel rank 38、24 tangent再現、S4 24/24。
- Pattern：source probability geometryがmetric moment mapのcanonical horizontal connectionを選ぶ。
- Interpretive Leap：このconnectionがそのままfull physical matter actionの変分である可能性。未証明。
- Alternative Explanation：正定値内積を持つ全射には最小norm右逆が常に存在するという一般線形代数。
- Braid-specific content：actual edge set、共通rate、displacement、4-axis S4構成、24 target tangentsがすべて同じpointed-Braid source由来。
- Falsifier：kernel上BKM退化、actual tangent再現失敗、S4非共変のいずれか。
- Confidence in Pattern：高い。
- Confidence in Interpretation：中程度。非線形積分と作用変分が未検証。
- SIEL-generation classification：`SIEL_GUIDED_STANDARD_COMPATIBLE`。

一次証拠区分は **Theoretical derivation**。自然界の重力実証、完成した量子重力、存在論・主観・意識の実証ではない。
