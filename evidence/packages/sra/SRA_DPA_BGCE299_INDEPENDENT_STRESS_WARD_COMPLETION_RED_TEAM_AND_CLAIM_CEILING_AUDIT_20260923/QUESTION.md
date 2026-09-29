# BGCE299 — stress/Ward completion独立red-teamとclaim ceiling監査

## 監査対象

BGCE298は、BGCE297のclock-reflection `K(Q,tau)` とBGCE295のcontinuum parentを合成し、宣言クラス内でBraid-source Hilbert stressとon-shell Wardを完成したと主張する。

## 最強の反証候補

1. rank 10はanchorだけの偶然で、`Q -> K` の真の逆変換が存在しない。
2. `D_tau K=(D_Q K)C` は線形代数上の自明な因子化にすぎず、実際のcontinuum actionに独立 `tau` couplingが残る。
3. metric volume、minimal operatorまたはactive Markov transportが未完で、BGCE295のC2作用鎖を再利用できない。
4. evaluatorが結論をliteral booleanとして置いただけで、上記1–3を証明していない。

## 非補償ゲート

- 固定 `tau` に対し

```text
K = Q - 2(Q tau)(Q tau)^T/(tau^T Q tau)
Q = K - 2(K tau)(K tau)^T/(tau^T K tau)
```

が相互逆であることを一般式と独立exact fixturesで検査する。
- admissible domain `Q>0` では `tau^T K tau<0`、signature `(3+,1-)`、逆写像がregularであることを確認する。
- BGCE295のcontinuum principal actionとBGCE285のmeasure/operatorが `K,g,lambda` のみを物理変数とし、独立 `tau` termを含まないかをsource recordから監査する。
- BGCE293のactive curved Markov transportがBGCE285の条件を実際に解除しているかを確認する。
- BGCE298の硬コード結論に依存せず、逆写像とsource action scopeからstress/Ward可否を再判定する。

## 判定

- **FINAL SCOPED PASS**：全ゲート成立。stress/Wardを宣言クラス内で最終確定する。
- **PARTIAL REVERSAL**：kinematic inverseは成立するが独立clock couplingまたはaction chainが未証明。
- **REVERSAL**：inverse/rank/signatureが破れる。

full finite Lorentzian action、global全domain、Einstein dynamics、経験的重力、完成量子重力へは昇格しない。数値走査は行わない。
