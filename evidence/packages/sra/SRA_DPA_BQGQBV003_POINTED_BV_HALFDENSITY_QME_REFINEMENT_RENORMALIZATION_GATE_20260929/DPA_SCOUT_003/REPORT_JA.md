# BQGQBV-003監査 — finite QMEとrefinement renormalization

## 結論

**CLOSED_SCOPEDです。**

simply connectedでgap-admissibleなlocal regular source branch、かつ任意の有限
refinement depthにおいて、量子BVの三点は閉じました。

1. BQGQBV-002のsource-derived chiral regulator;
2. finite quantum master equation;
3. QMEを保つassociative Wilsonian refinement pushforward。

## BV half-density

有限source cellのeven fieldsにはcounting/BKM density、odd fieldsにはBGCE532の
source-sign Berezin density、antifieldsにはodd symplectic pairingが誘導するdual
densityを使います。fermion determinant lineのphaseはBQGQBV-002のpointed GW
operatorとsource basepointで固定されます。

残る全体定数はBV Laplacianにもnormalized observableにも影響しません。従って同じ
sourceがmeasureを固定し、classical actionだけからmeasureを推測していません。

## QME

BQGCOUPLED-004は

\[
(S_{\rm BV},S_{\rm BV})=0
\]

を既に与えます。有限measureに対するmodular obstructionは次のように消えます。

- `su(3)+su(2)+u(1)`とLorentz algebraはunimodular;
- source-perfect HDA/groupoid actionは宣言chartでcanonical cotangent actionなので
  induced Liouville/Berezin densityを保存;
- BGCE439は三世代chiral matterのlocal gauge、mixed gravitational--`U(1)` anomalyを
  zero、weak Witten obstructionをevenにする;
- BQGQBV-002のGW regulatorによりこのtraceを有限に定義できる。

よってscope内で

\[
\Delta_{\mu_n}S_{\rm BV,n}=0
\]

であり、

\[
\frac12(S_{\rm BV,n},S_{\rm BV,n})
-i\hbar\Delta_{\mu_n}S_{\rm BV,n}=0
\]

が成立します。order-`hbar` countertermを手で足していません。

## Renormalization

fine BV fiberのLagrangian上で

\[
\rho_n=(\pi_n)_*\rho_{n+1}
\]

と定義します。有限BV Stokesにより

\[
\Delta_n\rho_n=(\pi_n)_*\Delta_{n+1}\rho_{n+1}=0.
\]

また有限Fubiniにより、二段pushforwardと一括pushforwardはexactに一致します。
従って全effective-action space上のWilsonian RG lawは、任意の有限5進refinement列で
associativeです。BQGQBV-001で示したdeterminant項も含むため、classical stationary
recursionより強い量子renormalizationです。

## 残る境界

今回閉じたのは有限理論・有限refinement depthです。次は別gateです。

- infinite-depth continuum quantum measureの存在・tightnessまたはoscillatory control;
- arbitrary strong gauge/metric backgroundやsingular stratumでのuniform gap/locality;
- finite個のrunning couplingだけで閉じること、またはasymptotic safety;
- 実測。

従って「finite quantum BV completion」は成立しましたが、「無条件のcontinuum
nonperturbative quantum gravity completion」までは主張しません。

