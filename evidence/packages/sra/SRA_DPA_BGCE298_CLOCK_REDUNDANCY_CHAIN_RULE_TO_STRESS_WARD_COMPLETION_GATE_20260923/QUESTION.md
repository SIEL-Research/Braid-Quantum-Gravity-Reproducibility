# BGCE298 — clock redundancyとchain ruleでstress/Wardを閉じられるか

## 問い

BGCE297のclock-reflection `K(Q,tau)` は `Q` 変分に関してrank 10を持つ。では `tau` は独立なbackground couplingではなく、同じphysical Lorentz tensor `K` の冗長なsource parametrizationとして消去できるか。

## 非補償ゲート

actual source anchorで

1. `A=D_Q K : Sym2 -> Sym2` がrank 10で局所可逆。
2. `B=D_tau K : R4 -> Sym2` がrank 3で、clock scale方向 `B tau=0`。
3. exactに `B=A C` となる `C` が存在し、全clock変化が既存 `Q` 変化へ因子化する。
4. cotangent側で `E_tau=C^T E_Q`。従って独立clock Euler式を追加しない。
5. continuum作用は `K` とmatter fieldだけのBGCE295 parentとして書かれ、`tau` を独立couplingとして残さない。
6. BGCE295のC2 finite-to-continuum variation identity、BGCE297のfull-rank continuation、標準off-shell Noether identityを同じ宣言クラス内で合成する。

## 判定

- **FULL PASS**：1–6が成立し、BGCE296の反転原因を除去して、宣言した長波長・局所・二階・形式的自己共役・保存的クラス内でHilbert stressとon-shell Wardを再昇格する。
- **PARTIAL/FAIL**：clockが独立方向を持つ、因子化しない、または作用に独立 `tau` couplingが残る。

Einstein dynamics、full finite Lorentzian action、経験的重力、完成量子重力は結論に含めない。exact有理線形代数だけを使い、数値走査は行わない。
