# BQG-G3-R02.5 / DPA-SCOUT-BQGEULER-010 — 正規化済み10成分非線形metric-Euler強収束

## 結論

**CLOSED_SCOPED。** BQGEULER-009の空間generatorに欠けていたsource固定`1/25`を補い、exact principal moment、strong local consistency、vanishing subsidiary residual、既存CFL条件を同じ10成分updateで閉じた。

`1/25`は新しい係数ではない。BQGEULER-006の規約

\[
\sum_\delta c_\delta\,\delta_i\delta_j=50A_{ij}
\]

とTaylor二次項の`1/2`から一意に強制される。

## authoritative update

\[
D_\tau^2 g_{AB,h}^n-L_h(g_h^n)g_{AB,h}^n
=N^{\rm src}_{AB,h},\qquad A\le B,
\]

\[
L_h(g)u(x)=\frac1{25h^2}
\sum_{\delta\in C_5^3\setminus\{0\}}
c_\delta(g)\,[u(x+h\delta)-u(x)].
\]

よって

\[
\frac12\frac1{25}\sum_\delta c_\delta\delta_i\delta_j
=A_{ij},
\]

となり、principal spatial tensorはactual inverse spatial metricとexactに一致する。

## strong residual

BGCE446のfive-digit fourth-jetは10 metric成分すべてに同一に作用する。`c_delta=c_-delta`、BGCE302 reverse-edge pairing、source-clock central differenceにより奇数Taylor項は消える。宣言smooth classで

\[
\|E_hI_hU-I_hE(U)\|_{H^{s-1}}
\le C_T(h^2+\tau_h^2).
\]

## subsidiary residual

centered source divergence `B_h:H^(s-1)->H^(s-2)`のnormは`O(h^-1)`。continuum Bianchi＋total Wardでzeroth-order divergenceが消えるため、

\[
\|B_hE_hI_hU\|_{H^{s-2}}
\le C_T\left(h+\frac{\tau_h^2}{h}\right).
\]

`tau_h=O(h)`では`O(h)`でzeroへ行く。finite constraintsはexact zeroではないがasymptotically preservedである。

## trajectory convergence

BQGEULER-006のstrict positivity、positive dual Hessian、stability ratio`3.3912913508957665<4`は十分小さいcompact regular metric neighborhoodで保持される。BQGEULER-003のenergy estimateから

\[
\sup_{0\le t\le T}\|J_hU_h(t)-U(t)\|_{H^{s-1}}
\le C_T\left(\eta_h+h+\frac{\tau_h^2}{h}\right)\to0.
\]

## 境界

閉じたのはlocal regular long-wavelength ten-component generalized-harmonic metric-Euler＋smooth Ward-compatible stress。exact finite HDA/BFV、full coupled matter principal、global/strong-curvature、full finite Lorentzian quantum parent、SI calibration、経験的重力はOPEN。
