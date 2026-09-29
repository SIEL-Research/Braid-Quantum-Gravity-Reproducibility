# BQGADM-014 — source-derived finite physical projector

## 結論

**SCOPED PASS。**

3本すべてのsource-selected spatial axisで、BQGADM-006がすでに導出した
flat spatial coframe、12次元Palatini symplectic form、rank-four constraint
symbolだけから、rank 2のconfiguration projectorとrank 4のphase projectorを
exactに構成した。

追加のBKM則、手動polarization basis、Einstein/Fierz-Pauli target、係数fit、
新しい作用は使っていない。

## 何が閉じたか

各source axisで次をexact rational algebraにより確認した。

- configuration projectorはidempotentでrank 2。
- metricとmomentumへ同じprojectorを作用させたphase projectorはrank 4。
- projected phaseは4本すべてのconstraintを満たす。
- actual Palatini symplectic formから計算した4本のHamiltonian gauge vectorを
  projectorがすべてzeroへ送る。
- physical image上のsymplectic rankは4で、退化しない。
- 8次元constraint surfaceは、4次元gauge imageと4次元physical imageの
  direct sumになる。
- projectorはactual symplectic formに関してself-adjointである。
- 6成分symmetric tensor上では、source coframeのFrobenius metricに関する
  transverse-tracefree subspaceへの一意なorthogonal projectorである。
- projectorはinternal tensor factorだけに作用するため、child-constant
  five-way refinementとexactに可換する。

したがってBQGADM-012の4次元physical phase quotientは、BQGEULER-004の
2 configuration polarizationとその2 conjugate momentaへ、flat source-axis
scopeで明示的に接続された。

## 一例

source axisが第1空間方向のとき、configuration projectorは6成分

```text
(q11, q12, q13, q22, q23, q33)
```

から

```text
q_plus  = (q22 - q33) / 2
q_cross = q23
```

だけを残す。残り5成分を手動でzeroにしたのではない。source axisにtransverse、
source coframeにtracefree、Frobenius-orthogonalという3条件からprojector全体が
一意に固定される。他の2 axisでも座標置換された同じ構造がexactに成立した。

## 大胆仮説の修正

事前仮説はconstraint symbolとpositive BKM metricからweighted projectorを作る
というものだった。結果はそれより強く単純だった。BKMは不要であり、既存の
source coframeがFrobenius metricを、source incidenceがlongitudinal directionを、
Palatini formがgauge distributionをすでに固定していた。

従って新しい選択則を追加せず、既存source objectだけでscoped projectorが出た。

## counter-intuition scan

通常の説明は、linearized time-gauge Palatini gravityにおける標準的な
transverse-tracefree coisotropic reductionである。TTという形だけならBraid固有では
ない。

Braid固有なのは、12次元finite carrier、実際に引き戻されたsymplectic form、
3本のsource incidence axis、4本のconstraint symbol、five-way refinementが同じ
source provenanceから与えられ、その組に対してprojectorがexactに通った点である。

最強の境界は、これはflat linearized source-axis theoremであることだ。任意の有限
momentum方向、曲がったmetric上のnonlinear moving projector、BQGEULER-010のfull
nonlinear updateとのoff-shell exact commutationはまだ示していない。

## Evidence classificationとclaim ceiling

- Primary evidence status: **Theoretical derivation**
- Scientific layer: mathematical formulation / finite coisotropic reduction
- Claim ceiling: 3本のsource-selected axisにおけるflat-anchor exact physical
  projector、hierarchical refinement intertwiner、BQGEULER-004 two-copy carrierとの
  同定まで。nonlinear moving projector、arbitrary finite momentum theorem、full
  nonlinear exact commutation、empirical gravity、confirmation、RPD adoption、
  Level 3、Official SIEL adoptionは主張しない。
