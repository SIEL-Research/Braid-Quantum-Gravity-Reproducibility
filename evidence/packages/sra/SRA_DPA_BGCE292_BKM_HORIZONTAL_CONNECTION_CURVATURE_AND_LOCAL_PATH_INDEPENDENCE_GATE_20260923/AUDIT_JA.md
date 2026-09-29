# BGCE292監査 — BKM-horizontal connection曲率

## 結論

**PASS。source anchorで接続曲率はexact zero。**

BGCE287の48 microscopic edge-rateから10 metric momentへの写像`M`を用い、positive rate空間のevent-path BKM metric

```text
g_r(v,w)=sum_e v_e w_e/r_e
```

に対するhorizontal right inverse

```text
H(r)=D(r)M^T[M D(r)M^T]^-1
```

をexactに微分した。10 metric方向が作る45個の二平面すべてでEhresmann curvatureはzeroだった。

```text
tested two-planes = 45
nonzero curvature = 0
curvature rank    = 0
```

これはBGCE287の一次liftが、source anchor近傍で直ちにpath dependenceを生むという懸念を外す。

さらにhorizontal条件は

```text
delta log r in image(M^T)
```

と書けるため、候補となる有限leafは

```text
r(theta)=r0 elementwise exp(M^T theta)
```

である。全rateは自動的に正である。次のBGCE293で、この指数族のmoment map Jacobianが正定値で局所一意、かつsource refinementと整合することを解析的に閉じる。

本gateだけではfinite parent action、Hilbert stress、Ward、Einstein dynamicsをまだ昇格しない。
