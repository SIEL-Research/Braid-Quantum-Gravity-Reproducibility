# BQGADM-013 — source-perfect親作用から10成分metric-Euler軌道への橋

## 結論

**SCOPED PASS + NO-GO + OPEN。**

- **SCOPED PASS:** BQGADM-012 perfect flowとBQGEULER-010 local updateは、
  同じsource metric carrier、同じcontinuum metric-Euler方程式、同じlocal
  regular branchを共有する。positive BKM exact-moment class内ではlocal
  stencilは一意で、`tau=O(h)`のときEuler defectは`O(h^2)`、subsidiary
  constraint defectは`O(h)`へ消え、trajectoryは同じcontinuum branchへ
  strong convergenceする。
- **NO-GO:** 二つは有限meshで同一のflowではない。BQGADM-012はperfect
  history image上でNoether identityとconstraint/refinement closureがexactだが、
  BQGEULER-010はfinite subsidiary residualを許し、zeroへ行くのは極限だけである。
- **OPEN:** 4次元physical phase quotientをBQGEULER-004の2偏極carrierへ送る
  source-derived finite projectorはまだない。dimension 2とprincipal classの一致は
  canonical intertwinerを構成しない。

一次attemptはrepo-root指定の実装ミスで科学判定なしに保存した。source、仮説、
endpoint、thresholdを変更せずrootだけ訂正したattempt 002が上記判定を与えた。

## 大胆仮説の訂正

最初の仮説は、BQGEULER-010がBQGADM-012 perfect actionのgauge-fixed exact
finite flowそのものだというものだった。これはNO-GOである。

成立した仮説は次の限定形である。

> BQGEULER-010は、source `C5^3`方向、positive BKM exponential leaf、actual
> metricの6 exact moments、source固定`1/25` normalizationを同時に課した
> local class内で、BQGADM-012 perfect flowへon shellで漸近可換する一意な
> local shadow representativeである。

ここで`local shadow representative`は「finite actionからexact変分された同一流」
という意味ではない。同じ連続方程式へ、残差とtrajectoryの両方で収束するsource固定
局所代表という意味である。

## 同じ親枝を使う根拠

1. BGCE294のrank-ten `Sym2` solderとBGCE447のexact same-carrier
   intertwinerにより、両構成のmetric carrierは同じである。
2. BGCE099、BGCE295、BGCE300R1により、continuum first variation、Hilbert
   stress/Ward、10成分metric-Euler equationは同じ宣言classに属する。
3. BQGEULER-006/007では、rank-six exact momentsとstrict convex BKM/Bregman
   dualityがpositive exponential leaf上のmemberを一意に選ぶ。
4. BQGEULER-010の`1/25`はfitではなく、source moment conventionとTaylor
   second-order factorから強制される。

新しい作用、manual damping、目標Einstein fit、自由な物理係数は導入していない。

## 漸近可換関係

perfect branchでは

```text
E(S_h^perf) = 0
R_h^dagger E(S_h^perf) = 0                 exact
```

BQGEULER-010 local shadowでは

```text
||E_h I_h U - I_h E(U)|| <= C (h^2 + tau_h^2)
||B_h E_h I_h U||         <= C (h + tau_h^2 / h)
```

`tau_h=lambda h`なら、それぞれ

```text
O((1+lambda^2) h^2)
O((1+lambda^2) h)
```

へ落ちる。さらに

```text
sup_[0,T] ||J_h U_h - U||
  <= C_T (eta_h + h + tau_h^2/h) -> 0
```

なので、finite flow equalityではなく、common smooth interval上のon-shell graph
convergenceとして親作用とtrajectoryを結ぶ。

## counter-intuition scan

最も強い反例は、exact discrete Lagrangianと通常のconsistent stable stencilが同じ
continuum PDEへ収束しても、有限解像度で同じ写像とは限らないことである。本件では
exact constraint preservation対asymptotic preservationの差が、その一般論を具体的に
実現している。

Braid固有なのは、共通10-metric carrier、`1+3` chart、five-adic refinement、
positive BKM leaf、exact metric moments、source clock、normalizationが同じsourceから
固定される点である。収束定理の解析形式自体は通常のperfect-action／consistent-scheme
理論でも説明できる。

## 残る一点

次に行う価値がある最小課題は、source-derived finite physical projectorの構成または
NO-GOである。これが得られれば、BQGADM-012のphysical quotientとBQGEULER-004の
two-polarization carrierのexact intertwiningを判定できる。

それ以外のoff-shell operator equality、raw ultralocal finite parent、global/strong
curvature、full coupled matter、経験的重力は別論文級であり、このSCOPED PASSには
含めない。

## Evidence classificationとclaim ceiling

- Primary evidence status: **Theoretical derivation**
- Scientific layer: mathematical formulation / local finite-to-continuum dynamics
- Claim ceiling: local regular on-shell asymptotic commuting bridge and uniqueness only
  inside the source-typed positive-BKM exact-moment class。exact finite-flow identity、
  explicit physical projector、off-shell variational equivalence、empirical gravity、
  confirmation、RPD adoption、Level 3、Official SIEL adoptionは主張しない。
