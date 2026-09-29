# BGCE323監査 — strong collision intertwinerと時間metric/Noether方向の不一致

## 結論

**SPLIT PASS。**

BGCE322のcompression balance（collision後をsystemへ戻したときの保存）は、全8 sectorでstrong intertwiner（collision isometryそのものがgeneratorを運ぶ関係）へexactに強化できる。

各source generatorを

\[
X_\alpha=(G_1,H_1,H_2,H_3)
\]

とし、bare output generatorを

\[
Y^{(0)}_\alpha=X_\alpha\otimes I+I\otimes E_\alpha
\]

とする。残差

\[
R_\alpha=VX_\alpha-Y^{(0)}_\alpha V,
\qquad
D_\alpha=V^*R_\alpha
\]

から

\[
\boxed{
J_\alpha=R_\alpha V^*+VR_\alpha^*-VD_\alpha V^*
}
\]

を作ると、`J_alpha`はHermitianであり、

\[
\boxed{
(Y^{(0)}_\alpha+J_\alpha)V=VX_\alpha
}
\]

がexactに成立する。従って任意のreal `t`について

\[
e^{-it(Y^{(0)}_\alpha+J_\alpha)}V
=Ve^{-itX_\alpha}
\]

も成立する。これは一回のfinite collisionに対する強いNoether covariance candidateである。

しかしfull metric Wardへの昇格は止まる。空間3方向はBGCE321のmixed scoreと同じ`G1/P_chi_i` commutatorから生じるが、時間generator`G1`とBGCE321のcentered-charge chemical-potential tangentは独立である。全8 sectorでexact rank 2だった。

したがって、

```text
conserved quartet = G1 + H1 + H2 + H3
metric-response quartet = centered charge + three mixed directions
```

の空間3成分は一致するが、時間1成分はまだ一致しない。

## 1. compression balanceより何が強いのか

BGCE322は

\[
V^*Y_\alpha V=X_\alpha
\]

を閉じた。しかしこの式だけでは、`Y_alpha V-V X_alpha`がStinespring supportと直交する方向へ残り得る。

実際、bare generatorのstrong residual normは全8 sectorで

\[
\|R_\alpha\|_{\rm HS}^2
=\left(12,64,\frac{112}{3},\frac{112}{3}\right)
\]

であり、時間成分も含め全てnonzeroである。

特にBGCE310の時間balanceはcompressionではexactだったが、strong intertwiningとしてはinteraction cross termを必要とする。これは以前の結果の否定ではなく、保存条件を一段強くした結果である。

## 2. minimal strong interaction completion

`V*V=I`、`D=V*R=D*`とする。上の`J`について

\[
J^*=J
\]

かつ

\[
JV=R
\]

が代数的に成立する。

一般のHermitian解は

\[
J=J_{\min}+C,
\qquad C=C^*,\quad CV=0
\]

である。`C`はcollisionが到達しないorthogonal complement内だけに作用する。`Q=I-VV*`として`QJQ=0`を課すreachable-block representativeは一意であり、同時にHilbert--Schmidt norm最小である。

minimal interaction normは

\[
\|J_{\min,\alpha}\|_{\rm HS}^2
=2\|R_\alpha\|_{\rm HS}^2-\|D_\alpha\|_{\rm HS}^2
\]

から

\[
\boxed{
\left(24,104,\frac{182}{3},\frac{182}{3}\right)
}
\]

となる。

新しい係数、fit、sector別選択はない。actual `q=1/4` collisionは使用する。

## 3. unrestricted contactは残る

strong identityは`C V=0`を満たすcomplement-only operatorを見ない。system dimensionは125、collision output dimensionは750なので、Hermitian complement freedomは

\[
(750-125)^2=390625
\]

次元である。CTP doubling後は

\[
(1500-250)^2=1562500.
\]

これはphysical intertwiningを変えないgauge-equivalent extensionだが、full microscopic operatorを一意にしたとは言えない。BGCE321のminimal four-score contact kernel zeroとも別のkernelである。

## 4. finite Noether covariance

strong identityは指数化できるため、input stateのsource unitary curve

\[
\rho_\alpha(t)=e^{-itX_\alpha}\rho e^{itX_\alpha}
\]

はoutputで

\[
V\rho_\alpha(t)V^*
=e^{-itY_\alpha}(V\rho V^*)e^{itY_\alpha}
\]

となる。

空間`X_i=H_i`では、この微分はBGCE141/320/321の三つのactual mixed tangentsを生成する。従って空間interaction generatorとmetric-response directionの対応は外付けではない。

これはphysical finite Noether/Ward candidateとしてBGCE322より強い。ただし10成分すべてのmetric variationでも、scalar influence actionのHilbert variationでもまだない。

## 5. 時間方向のexact obstruction

BGCE321の第4 scoreは`G1` tangentではなく、centered source chargeのchemical-potential tangent

\[
\delta_Q\rho
\]

である。

もしそのBKM scoreがcentered `G1` scoreと同じ方向なら、faithful `K_omega`が可逆なので、対応する二つのstate tangentも比例するはずである。

`omega_can`は`G1`とcommuteするため、`G1` scoreのtangentは

\[
\delta_{G1}\omega
=\omega G_1-\operatorname{Tr}(\omega G_1)\omega
\]

である。`delta_Q rho`とのexact Gramは全8 sectorで

\[
\begin{pmatrix}
4/375 & 3217/3796875\\
3217/3796875 & 598699/34171875
\end{pmatrix}
\]

となり、rankは2である。

従って

\[
\boxed{S_Q\not\propto S_{G1}}
\]

である。これは小さな数値ずれではなくexactな独立性である。

このため`G1+H_i`のstrong conserved quartetを、そのままBGCE321の`charge+mixed` metric quartetと同一視できない。

## 6. repeated collisionで成立する範囲

全`n`-step isometryを`W_n`とすれば、global support上のgenerator transport

\[
Y^{(n)}_\alpha W_n=W_nX_\alpha
\]

はisometry compositionで成立する。

しかし空間`J_i`はcontinuing systemとemitted blockの両方に作用する。従って過去のinteraction termは後続collisionでdressされ、BGCE310のpure environment chargeのような単純なlocal additive sumにはならない。

よって

- global repeated support covariance：PASS。
- local additive Ward telescoping：未導出。

である。

## Counter-intuition scan

通常の説明：generatorを一つ選べば、任意のfinite isometryにHermitian strong completionを作れる。従ってcompletion formula自体はBraid固有ではない。

Braid固有の部分：actual sourceが`V,G1,H_i`、全sector共通のexact residual norms、charge-plus-mixed BKM responseを同時に固定し、時間だけが独立方向として残る点である。

最強のcounterpattern：strong intertwinerは一般isometry geometryであり、時間metric scoreが`G1`ではない以上、これをfull physical stress/Wardと呼べない。

このcounterpatternを採用し、主張をfinite strong Noether candidateまでに制限する。

## 次の最短路

`BGCE324_CENTERED_CHARGE_SCORE_TO_COLLISION_NOETHER_TIME_OR_MODULAR_ENERGY_GATE`。

centered charge scoreが

1. collisionの独立なconserved Noether timeを生成するか、
2. `omega_can`のmodular energyとして`G1`を置き換えられるか、または
3. chargeと`G1`を結ぶsource-derived two-component temporal sectorが必要か

をexactに判定する。

## Claim ceiling

BGCE323はactual finite Braid collisionについてexactなstrong one-collision four-generator intertwinerと指数化Noether covarianceを導出し、同時にconserved `G1`方向とBGCE321 centered-charge metric scoreのexactな独立性を証明する。full four-component physical variational stress、full ten-component metric collision deformation、standard causal influence action、local repeated Ward、continuum Hilbert stressとの同一性、collision parentからのcontinuum Einstein backreaction、経験的重力、完成量子重力は未導出である。
