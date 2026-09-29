# BQGCAL-010 報告

## 結論

**SPLIT SCOPED PASS。source規格のMisner--Sharp / Schwarzschild質量スペクトルと固定境界での真空保存は導出。加法的total Ward energyとの同一視はSCOPED NO-GO。**

BGCE300R1の導出済みcoupling

\[
G_{\mu\nu}=\kappa_B T_{\mu\nu},
\qquad \kappa_B=\frac35
\]

と、BQGBH-001 / BQGCAL-006のSchwarzschild sector

\[
f(r)=1-\frac{r_h}{r}
\]

を使う。4次元球対称系のgeneralized Misner--Sharp chargeは

\[
\mathcal M_{\rm MS}(r)
=\frac{4\pi}{\kappa_B}r
\left(1-g^{ab}\partial_a r\partial_b r\right)
\]

である。このvacuum metricでは

\[
r(1-f)=r_h
\]

なので、

\[
\boxed{
\mathcal M_{\rm MS}=\frac{20\pi}{3}r_h
}
\]

は半径によらない保存境界電荷になる。

## source area numberへのpullback

BQGCAL-007と009は

\[
r_h=r_K=\ell_*\sqrt K,
\qquad
K=\frac{45}{4}C_{{\rm exc},n}
\]

を与える。合成すると

\[
\boxed{
\mathcal M_K
=\frac{20\pi}{3}\ell_*\sqrt K
}
\]

および

\[
\boxed{
\mathcal M_C
=10\pi\sqrt5\,\ell_*\sqrt{C_{{\rm exc},n}}
}
\]

を得る。従って等間隔なのは質量そのものではなく、

\[
\boxed{
\mathcal M_K^2
=\frac{400\pi^2}{9}\ell_*^2 K
=500\pi^2\ell_*^2 C_{{\rm exc},n}
}
\]

である。係数fit、測定target、parameter scanは使っていない。

## 有限境界での保存

BGCE310のfresh-tail構成では、過去に放出されたtail blockは後続collisionのsupport外にあり、そのchargeは後続collisionと可換する。従って固定されたemitted-tail algebra上の`C_exc,n`も、そのpositive spectral functional calculusである`sqrt(C_exc,n)`も後続collisionで保存される。

これは「固定境界の外側が真空なら準局所質量が保存される」という有限側の対応である。

境界へ新しいnonidentity eventが一つ加わると、質量増分は

\[
\Delta\mathcal M_K
=\frac{20\pi}{3}\ell_*
\frac{1}{\sqrt{K+1}+\sqrt K}
\]

となる。これはexactだが非加法的である。

## なぜtotal Ward energyそのものではないか

`K`と`C_exc`はtail blockについて加法的だが、`sqrt(K)`は加法的でない。実際、

\[
\mathcal M_{1+1}\neq \mathcal M_1+\mathcal M_1.
\]

従って、このboundary massをBGCE310の加法的total Ward chargeと同じ演算子だと呼ぶ経路は閉じた。これは失敗ではなく、局所物質energyと重力のquasi-local boundary chargeを型分離した結果である。

## Counter-intuition scan

通常の説明は、4次元Schwarzschild幾何ではhorizon areaがmassの二乗に比例し、Misner--Sharp chargeがvacuumで一定になるという標準GRである。今回のsquare-root則だけなら、その標準則へ内部integerを代入したものとも読める。

Braid固有なのは、同じpointed sourceが`K`、`C_exc=(4/45)N`、refinement-invariant screen radius、relative coupling `3/5`をfitなしで供給している点である。しかし、finite tetrahedral countと物理的球対称boundary indexの同一性はまだ条件付きである。

## 残る境界

- `K`が物理的geometric screen numberであることの無条件source導出。
- `ell_star`とenergy/stress normalizationのSI traceability。
- physical Newton constant、kg単位のmass。
- entropy、temperature、Hawking radiation、evaporation。
- finite quantum black holeとしての完全なdynamics。

ここでの`\mathcal M`はsource規格のboundary chargeであり、kgではない。またsource tetrahedral screen areaとambient spherical areal radiusの同一視は、BQGCAL-006から引き継ぐconditional typingである。

## 次

`BQGCAL-011_SOURCE_EXCITATION_COUNT_TO_GEOMETRIC_BOUNDARY_INDEX_AND_SINGLE_SI_ANCHOR_GATE`

で、event countとgeometric boundary indexのsource内同一性を先に判定し、その後に残る単位自由度が単一SI anchorへ本当に縮約できるかを問う。

## 主張上限

固定source模型・導出済みIR Schwarzschild sector・既存のconditional screen typing内で、source規格のMisner--Sharp質量スペクトル、`M^2`の整数等間隔、固定tail境界での真空保存を導出した。unconditional physical screen typing、additive total Ward mass、SI絶対較正、black-hole thermodynamics、経験的重力は未導出である。
