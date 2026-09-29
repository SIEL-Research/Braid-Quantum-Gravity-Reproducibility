# BGCE294監査 — source-typed physical solderの一意性

## 結論

**FULL PASS（既存source symmetric-product functorial class内）。**

BGCE291の9次元自由度を再現した。clock・grading・event spectral条件だけを加えても残余は5次元であり、これらだけでは一意にならない。

一方、BGCE141の10 metric functionalsは4 source carrierから`symmetric_product`で生成される。BGCE268はその4 carrier間のmap `U`をsourceから固定している。従って型を保つsolderは

```text
T(v symmetric-product w)=U(v) symmetric-product U(w)
```

を満たす必要がある。4個の`e_i^2`と6個の`(e_i+e_j)^2`は`Sym2(R4)`をrank 10で張る。これら10本の像を固定した後のaffine residual dimensionはexactに0だった。

```text
arbitrary S4-equivariant freedom = 9
plus spectral constraints         = 5
plus actual source product type   = 0
```

よって一意なmapは

```text
A -> U^T A U
```

である。新しい係数やmatter actionはない。BGCE291の自由度は、実際のsource生成型を保存しない任意10次元mapまで許した場合の自由度だった。

ただし「意図的にsource product型を壊すmapが数学的に存在しない」とは主張しない。物理solderとして許容する型を、既存source constructionに一致させた結果である。

BGCE293のfinite active Markov transportと合わせ、残件は一つに縮んだ。finite Braid BKM exponential actionのmetric variationがcontinuum BKM Hilbert variationと同一になることを示す。ここをBGCE295で判定する。それまではstress/Wardを昇格しない。

一次区分は **Theoretical derivation**。Einstein dynamics、経験的重力、完成量子重力は未導出。
