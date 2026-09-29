# BGCE298監査 — clock redundancyからstress/Ward completionへ

## 結論

**FULL PASS（宣言した長波長・局所・二階・形式的自己共役・保存的クラス内）。**

BGCE297のco-moving gradingは、BGCE296が発見したfixed-`J` rank-7障害を単に回避するだけでなく、clock `tau` をphysical continuum actionの独立background couplingとして残さない。BGCE295のfinite-to-continuum Hilbert変分とon-shell Wardは、この宣言クラス内で再昇格できる。

独立red-team `BGCE299` までは最終確定としない。

## exactな判定

actual source anchorで

```text
A = D_Q K : Sym2(R4) -> Sym2(R4)
B = D_tau K : R4 -> Sym2(R4)
```

を計算した。

```text
rank(A) = 10
rank(B) = 3
B tau = 0
B = A C
```

がexact有理線形代数で成立した。`B tau=0` はclockの尺度変更が `K` を変えないことを表す。残る3つのclock-line変化も全て `Q` 変化を通じて再現される。

cotangent側では任意のHilbert variation covector `H=dS/dK` に対して

```text
E_Q   = A^T H
E_tau = B^T H = C^T E_Q
```

である。従って独立なclock Euler方程式を付け足す必要はない。`tau` は局所的に同じphysical `K` を表すsource parametrizationの冗長性である。

## stress/Wardへの効果

BGCE295は既に、宣言クラス内で

- finite log-Z Bregman/Umegaki edge actionのBKM Hessian
- C2 Riemann limit
- continuum minimal parent
- off-shell Noether identity

を与えていた。BGCE296が止めた唯一の決定的欠陥は、fixed `J` がmetric variationをrank 7に落とすことだった。

BGCE297–298によりmetric variationはfull rank 10となり、clockは独立couplingでないことが証明された。よって

```text
T_mn = G_AB[partial_m lambda^A partial_n lambda^B
       -(1/2) g_mn g^rs partial_r lambda^A partial_s lambda^B]

nabla^m T_mn = -E_A partial_n lambda^A
```

が同じsource-derived continuum actionから成立し、matter shell `E_A=0` で

```text
nabla^m T_mn = 0
```

となる。

## 何を追加していないか

- 新しいclock field/action
- 新しいmatter action
- 手動 `3/5`
- Einstein targetからの逆算
- 係数fit
- 数値走査

## 反直観・残る反証可能性

この結論は局所C2クラスに限る。full finite Lorentzian actionに `tau` が `K` 以外の形で再出現する、`Q -> K` が大変形で特異になる、または高階項が残る場合、global/full-finite Ward completionにはならない。

## 次

`BGCE299_INDEPENDENT_STRESS_WARD_COMPLETION_RED_TEAM_AND_CLAIM_CEILING_AUDIT`。

今回の因子化、BGCE295の作用極限、`tau` 非独立性を別実装で攻撃し、stress/Wardの最終昇格可否を決める。

## 主張上限

一次区分は **Theoretical derivation**。Einstein dynamics、full finite Lorentzian Umegaki action、global invertibility、経験的重力、完成量子重力は未導出。
