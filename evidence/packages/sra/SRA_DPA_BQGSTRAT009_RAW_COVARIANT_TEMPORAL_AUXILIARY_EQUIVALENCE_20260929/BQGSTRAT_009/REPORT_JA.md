# BQGSTRAT-009 — BGCE094 raw covariant temporal auxiliary closure

## 結論

**BGCE094 TEMPORAL PROMOTIONS RECLASSIFIED AS SOURCE-DERIVED AUXILIARY GAUGE COMPLETION CLOSED_SCOPED。**

BGCE094のliteral six-face作用でも、`e_0,U_0`は新しいphysical fieldではなく、
source-derived gauge/constraint構造をoff shellへ完成する補助slotだと確定しました。

## exact split

4次元alternating contractionの24非zero permutationを全列挙すると、exactに

- `e_0 e_i F_jk`型：12項
- `e_i e_j F_0k(U_0)`型：12項

へ分かれます。`e_0`次数は最大1で、actionの`e_0` Hessianはexact zeroです。
従って`e_0`は4本のcoframe constraintを生成するmultiplierであり、独自の
propagating temporal fieldではありません。

`U_0`はmixed faceを作るordered Lorentz linkです。作用のproper-Lorentz invariance、
非可換child linkのordered composition、contractibleな二edge intervalでの
`U_0=I` temporal gaugeを有理数exact algebraで確認しました。`U_0`の値はlocal
physical observableではありません。

## source clock

4 deformation multiplierには任意のsource-clock representativeへ到達するlocal
gauge transformationがあります。したがって`tau`はoff-shell lawを追加するのでは
なく、既存gauge orbitのsliceを選びます。

## 必須の順序

```text
vary e_0,U_0 -> impose Gauss/scalar/vector equations -> gauge fix/quotient
```

変分前の固定・削除は禁止です。解除したのはoff-shell slotそのものではなく、
それらの数値をBraidがphysical fieldとして一意に選ばなければならない、という
BGCE094のpromotion要求です。

## 境界

閉じたのはlocal contractible source cylinder、proper Lorentz component、local
regular variational branchです。noncontractible temporal holonomy、caustic/global
continuation、quantum measure、経験的重力は別課題です。
