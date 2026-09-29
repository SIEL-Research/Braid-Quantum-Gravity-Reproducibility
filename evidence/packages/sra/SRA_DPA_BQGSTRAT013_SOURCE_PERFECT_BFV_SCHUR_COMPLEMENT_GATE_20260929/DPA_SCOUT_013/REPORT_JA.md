# BQGSTRAT-013監査 — source-perfect physical Schur reduction

## 結論

**SCOPED PASS。**

raw 80成分Palatini blockで見つかった正負orientation sheetの追加corank
`2対1`は、物理2偏極principal systemには継承されない。

正規化済み10成分metric-Euler principal operatorはsymmetric-tensor成分に
対して同じscalar `q_h(omega,k)`として作用する。source-derived TT projectorは
tensor因子だけに作用し、全124非零`C5^3` momentumでconfiguration rank 2、
phase rank 4である。従って両者はexactに可換し、物理principal symbolは

\[
\sigma_{\rm phys}(\omega,k)=q_h(\omega,k)I_2
\]

となる。

## 両null sheetのexact判定

flat source-axis stencilでは、5次cyclotomic変数を使って

\[
q_h=(z_0+z_0^{-1}-2)-(z_i+z_i^{-1}-2)
\]

と書ける。空間digitが時間digitの`+1`倍または`-1`倍なら、cosine型symbolは
同じなので`q_h=0`である。

- 時間digit：4通り
- 空間axis：3通り
- orientation：正負2通り
- 合計：24 sector
- 各sectorのphysical kernel dimension：exactに2

非characteristic controlではphysical rankは2である。新しい係数、Holst位相、
Einstein target、rank fitは使っていない。

## raw blockとの関係

`BQGSTRAT-010`のrank profile

```text
60 x 1, 64 x 12, 65 x 12, 66 x 600
```

は撤回も修正もしない。これはsingle-orientation raw ultralocal
coframe/connection blockの正しいnegative route evidenceである。

ただし、そのraw blockはconstraint・gauge・auxiliary方向を含むため、物理parent
そのものではない。source-perfect親のTT quotientでは二つのpolarizationへ同じ
principal scalarが作用し、正負sheetはexactに均衡する。

## source-perfect Schur complementの範囲

`BQGULTRA-002`はregular transverse branch上で

\[
K_{\rm eff}=K_{bb}-K_{bi}K_{ii}^{-1}K_{ib}
\]

というexact Schur complementを証明している。`BQGADM-013`はこのperfect親と
metric-Euler trajectoryのon-shell asymptotic bridgeを閉じるが、有限meshでの
literal exact map同一性はNO-GOである。

従って今回のPASSは、物理principal symbolとregular Schur theoremについてで
ある。characteristic点を含むfull perfect Hessianの全係数とlower-order crossing
formはまだ評価していない。

## 次

`BQGSTRAT-014`で、有限depth source Palatini stationary solveを実装してactual
perfect Hessianとlower-order crossingを評価する。ただし、量子重力の2偏極
principal構造を成立させるための必須条件は今回すでに閉じた。

