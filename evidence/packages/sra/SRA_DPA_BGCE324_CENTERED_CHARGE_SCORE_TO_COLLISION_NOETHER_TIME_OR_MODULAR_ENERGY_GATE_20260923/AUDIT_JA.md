# BGCE324監査 — centered chargeを外し、保存G1 scoreでfinite 1＋3 metric–Noetherを閉じる

## 結論

**SCOPED FULL PASS。**

BGCE323で見つかった時間方向の型不一致は、centered chargeをNoether timeへ無理に昇格させるのではなく、BGCE321 packetの時間scoreを保存generator`G1`のBKM scoreへ交換することで解消した。

`omega_can`は`G1`とcommuteするため、

\[
\delta_0\omega
=\omega_{\rm can}\left(G_1-\langle G_1\rangle_\omega I\right)
\]

に対応するBKM scoreはexactに

\[
\boxed{
S_0=G_1-\langle G_1\rangle_\omega I
}
\]

である。

これを三つのexisting mixed scoreと合わせると、全8 sectorで

\[
\operatorname{rank}R_{(H_1,H_2,H_3,G_1)}=4,
\]

\[
\operatorname{rank}\widehat{\mathcal A}_{G1}=10.
\]

minimal four-score contact kernelもzeroである。

従ってfinite levelで

```text
metric score quartet     = centered G1 + mixed H1,H2,H3
strong conserved quartet = G1 + H1,H2,H3
```

がidentity shiftを除いてexactに一致した。

## 1. centered charge自体はNoether timeではない

centered-charge tangent`delta_Q rho`について三つの候補を検査した。

### 1.1 unitary Noether orbit

pointed stateはsupport projectorに比例する。unitary commutator tangentなら、support-support blockとkernel-kernel blockはともにzeroでなければならない。

しかし`delta_Q rho`では全8 sectorで

\[
\|P\delta_Q\rho P\|_{\rm HS}^2=\frac{67}{400},
\]

\[
\|Q\delta_Q\rho Q\|_{\rm HS}^2=\frac{217}{6000}
\]

であり、両方nonzeroだった。

従って`delta_Q rho=-i[K,rho]`を満たすsystem Hermitian generatorは存在しない。これはchemical-potential gradientであってunitary orbitではない。

### 1.2 modular energy

もしcharge scoreが`omega_can`のmodular centralizer energyなら、対応tangentは`omega_can`とcommuteする。

実際には

\[
\|[\delta_Q\rho,\omega_{\rm can}]\|_{\rm HS}^2
=\frac{13129}{28476562500}>0.
\]

従ってcentered-charge scoreはmodular Hamiltonianのfunctionまたはcentralizer energyではない。

### 1.3 actual collision conservation

actual `q=1/4` collision channelについて

\[
\|\delta_Q\rho-T_*(\delta_Q\rho)\|_{\rm HS}^2
=\frac{313}{250000}>0.
\]

従ってcharge tangent自体はcollisionで保存されない。

以上により、centered chargeをそのままcollision Noether timeまたはmodular energyと読む経路はexact NO-GOである。

## 2. 保存G1 BKM scoreへの交換

BGCE318の`omega_can`はfaithfulで、`G1`および三つの`H_i`とcommuteする。特にcentered observable

\[
S_0=G_1-\operatorname{Tr}(\omega G_1)I
\]

についてKubo–Mori mapは

\[
\mathcal K_\omega(S_0)=\omega S_0
\]

となる。従って`S_0`は外部で選んだRiesz dualではなく、source-canonical stateと保存energyが直接定めるexact BKM scoreである。

またBGCE319の`Theta`について

\[
\Theta G_1\Theta^{-1}=G_1
\]

が全8 sectorでexactに成立するため、`S_0`はTheta-evenである。

## 3. rank-four responseとrank-ten CTP

10個のsource-typed metric functionalに対する四つのresponse columnを

\[
R_{A\alpha}
=\operatorname{Tr}(\delta_\alpha\rho F_A),
\qquad
\alpha=(1,2,3,0)
\]

とする。ここで`1,2,3`はexisting mixed tangents、`0`は上の`G1` tangentである。

全8 sectorで

\[
\boxed{\operatorname{rank}R=4}
\]

となった。

BGCE320のTheta-odd operator packetはrank 7、三つのmixed responseを加えるとrank 9、`G1` responseを加えると

\[
\boxed{7\longrightarrow9\longrightarrow10}
\]

となる。

BGCE321と同じBKM Riesz＋Pauli CTP constructionで

\[
\widehat{\mathcal A}_{G1}(F)
=\tau_z\otimes P_-F
+\tau_x\otimes S_-[R_{G1}(F)]
+\tau_y\otimes S_+[R_{G1}(F)]
\]

を作ると、Hermitian、`Theta_hat`-odd、rank 10を全8 sectorで満たす。

四score responseがrank 4なので、declared minimal span内のcontact candidate`C=sum c_alpha S_alpha`が全metric functionalから見えないなら`Rc=0`、従って`c=0`である。

## 4. BGCE323 strong Noetherとの完全なfinite alignment

BGCE323は

\[
(Y^{(0)}_\alpha+J_\alpha)V=VX_\alpha,
\qquad
X_\alpha=(G_1,H_1,H_2,H_3)
\]

を導出した。

今回のmetric score quartetは

\[
(G_1-\langle G_1\rangle I,S_{H_1},S_{H_2},S_{H_3})
\]

である。identity shiftはcommutator、normalized BKM tangent、Ward generatorに物理的効果を持たない。

従ってfinite source上で初めて、

\[
\boxed{
\text{full metric response}
\longleftrightarrow
\text{strong conserved }1+3\text{ generators}
}
\]

が係数なしに閉じた。

## 5. 3/5とMMRへの影響

従来のcentered chargeは

\[
Q=\sum_i(P_{{\rm src},i}-3I/5)
\]

を使っていた。今回その列を完全に`G1`列へ交換したため、このfinite metric–Ward packetはcentered chargeも`3/5`も使わない。

これは手動`3/5`だけでなく、source charge由来`3/5`もfinite Ward completionには不要だったことを意味する。

ただしMMR2はmatter作用全体をgravity作用へどうrouteするかという別問題である。今回の結果だけではrelative Einstein action coupling`3/5`を導出も否定もしない。

## 6. まだ残るもの

今回閉じたのはfixed finite sourceのmetric–Noether identificationである。

未導出：

- interaction termをfresh right-tail上のlocal additive currentとしてtelescopingすること。
- standard causal Feynman–Vernon / Schwinger–Keldysh influence action。
- finite interaction generatorとBGCE299 continuum Hilbert stressの同一性。
- collision parentからのcontinuum covariant total Ward。
- full finite Lorentzian Einstein backreaction。

## Counter-intuition scan

通常の説明：faithful stationary stateと可換な保存observableがあれば、そのcentered observableは自身のBKM scoreになる。nonconserved chemical-potential方向を保存energy方向へ交換するのは標準的information geometryである。

Braid固有の部分：actual sourceが`omega_can,G1,H_i,Theta`、10 metric functionals、strong collision intertwinerを同時に固定し、交換後も全8 sectorでrank 10を失わない点である。

最強のcounterpattern：finite rankとfinite Noether covarianceが閉じても、continuum locality、causality、Hilbert variationとの一致は自動ではない。

このcounterpatternを採用し、continuum Ward完成はまだ主張しない。

## 次の最短路

`BGCE325_G1_ALIGNED_STRONG_CTP_GENERATOR_TO_REPEATED_LOCAL_WARD_AND_CONTINUUM_STRESS_IDENTIFICATION_GATE`。

aligned quartetをright-tail repeated interactionへ入れ、interaction generatorがhistory-nonlocal dressingではなくlocal discrete divergenceとしてtelescopingするかを判定する。同時に、そのrefinement limitがBGCE299 Hilbert stressと同じtensor variationを返すかをfirst-failで検査する。

## Claim ceiling

BGCE324はfixed finite Braid sourceで、centered chargeを保存centered-G1 BKM scoreへ係数なしに交換し、four-response rank 4、single CTP rank 10、minimal contact kernel zero、BGCE323 strong conserved quartetとのexact alignmentを全8 sectorで導出する。local repeated Ward、standard causal influence action、continuum Hilbert stressとの同一性、collision由来continuum Einstein backreaction、MMR2除去、経験的重力、完成量子重力は未導出である。
