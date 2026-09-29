# BQG-G3-R02.5 / DPA-SCOUT-BQGEULER-004 — 線形2モード有限時間強収束

## 判定

**階層source-cylinder上の2偏極wave trajectory強収束は `CLOSED_SCOPED`。物理ADM/Fierz–Pauli 2モード強収束は `OPEN_SOURCE_IDENTIFICATION_REQUIRED`。課題本体は未完了。**

一次分類は **Theoretical derivation**。

## exact theorem

BGCE452/BGCE456は、有限level空間`H_m`、child-copy isometry `J_m`、positive self-adjoint spatial operator `Delta_m`について

`Delta_(m+1) J_m = J_m Delta_m`

をexactに与える。mean-zero sectorへ制限し、2偏極を`R^2`因子として

`H_m^(2)=H_m tensor R^2`, `Delta_m^(2)=Delta_m tensor I_2`

とする。inductive limit上のenergy spaceを

`E=D(Delta^(1/2)) tensor R^2 direct_sum H tensor R^2`

とし、`qdot=p`, `pdot=-Delta q`のwave groupを`W(t)`とする。functional calculusとexact intertwiningにより、各有限level groupはlimit groupのrestrictionである。

energy projectionを`Q_m`とすると

`sup_(t in R) ||W(t)x - J_m W_m(t)Q_m x||_E = ||(I-Q_m)x||_E -> 0`。

従って要求された有限時間一様強収束より強く、mean-zero energy normでは全実時間一様強収束が成立する。

BGCE456のactual-metric operatorはisotropic operatorに対するexact positive form boundsを持ち、同じrefinement intertwiningを満たすため、同じ結論がactual-metric hierarchical carrierにも移る。

## exact witness

level `k`の各偏極で`q_k=25^-k`, `p_k=5^-k`とした2偏極witnessでは、level `m`以後のisotropic energy誤差二乗はexactに

`(1/6) 25^-m`

となる。good intertwiner residualは`0`。比較用の非refinement operator `Delta_bad=Delta_good+P_coarse`ではunit coarse detail上のresidual norm二乗は`1`であり、endpointは非退化である。

## なぜ「物理ADM強収束」ではないか

BQGADM-011は物理configuration modeが2本であることを確定したが、constraint idealまたはphysical projectorをlevel間で運ぶrefinement pullbackを持たない。BGCE456もhierarchical finite-group symbolとsmooth ADM/Fierz–Pauli principal symbolのexact同一性を未証明としている。

従って`R^2`因子は現在、正しいmode数を持つ二つの受動偏極slotであり、source-derived physical ADM quotientそのものとはまだ言えない。

## counter-intuition

通常の説明は、positive self-adjoint operatorのexact nested restrictionがあればwave groupの強収束はspectral truncationの密度だけで従う、という標準的functional analysisである。Braid固有なのは、`C5^3` hierarchy、`25` scaling、actual metric conductance、exact child-copy intertwiningが保存sourceから供給された点である。

最強の反対解釈は、この定理がsmooth spacetimeへの収束ではなくultrametric/hierarchical carrier内部の収束に過ぎないというもの。この反対解釈は現時点で排除されていない。

## 次

予約済み`DPA-SCOUT-BQGEULER-003`でsource-derived Noether/Koszul–Tate/BFV contractible auxiliary complexを検査し、同時にphysical projector `P_m`について

`P_(m+1)J_m=J_mP_m`, `P_m Delta_m=Delta_m P_m`

をsourceから導出する。その後にsmooth ADM/Fierz–Pauli principal-symbol identityを検査する。

## Claim ceiling

2偏極hierarchical source-cylinder waveのmean-zero energy-norm強収束のみ。physical ADM quotient、smooth Fierz–Pauli generator、nonlinear Euler convergence、finite nonlinear HDA、経験的重力、confirmation、RPD adoption、Level 3、Official SIEL statusは成立していない。
