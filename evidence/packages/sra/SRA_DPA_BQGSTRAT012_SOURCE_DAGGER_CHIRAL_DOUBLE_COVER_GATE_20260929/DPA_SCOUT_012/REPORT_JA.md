# BQGSTRAT-012監査 — source dagger/chiral double-cover

## 結論

**NO-GO（宣言経路限定）**。

source-nativeな内部Lorentz Hodge starは実在する。しかし、それを使って
Palatini作用を自己双対・反自己双対へ分解し、daggerで等重みに戻しても、
新しい作用は得られない。等重み和は既存の実Palatini作用をexactに再構成
するため、`BQGSTRAT-010`のHessianとrank profileは変わらない。

## 型監査

二つのHodge構造を区別した。

- `BGCE027/041`の`star_h`：X29/X30 Lorentz carrierの内部bivectorに作用。
- `BQGQBV-002`の`Gamma,S`：source-cylinderのcell cochainに作用し、内部係数
  moduleとはtensor積を取り、両作用は可換。

従って、双方に現れる`80`というrank/dimensionを根拠に同じ作用素とする
ことはできない。これは単なる数の一致で、型付き同一視ではない。

## Exact定理

内部Lorentz Hodge作用素を`J`とすると、

\[
J^2=-I,
\qquad
P_+=\frac{I-iJ}{2},
\qquad
P_-=\frac{I+iJ}{2}.
\]

`P_+`と`P_-`は相補射影で、daggerは両者を交換する。Palatini挿入のchiral
成分は`JP_+`と`JP_-`であり、

\[
JP_+ + JP_- = J
\]

がexactに成立する。したがって係数なしの等重み完成は元のPalatini作用
そのものである。

独立な実partnerは

\[
-i(JP_+-JP_-)=I
\]

で、これはHolst型収縮である。一般のdagger-real係数対は

\[
(a+ib)JP_+ +(a-ib)JP_-=aJ-bI
\]

となる。`b/a`をsourceから決める追加法則がない限り、これは自由な
Holst/Immirzi型相対係数である。rankを見てから選ぶことはfitなので行わない。

## Rankへの帰結

等重み完成は作用レベルで元と同一なので、全625 sectorの再計算は不要である。
rank profileはそのまま

```text
rank 60 x 1
rank 64 x 12
rank 65 x 12
rank 66 x 600
```

であり、二つのnull sheetの追加corank `2対1`は残る。

## 次の最短ゲート

raw ultralocal作用へ別の局所項を足す経路はここで止める。次は
`BQGSTRAT-013`で、既に構成済みのsource-perfect quasi-local BV--BFV親を
source physical projectorで縮約し、補助・constraint・gauge方向をexact
Schur complementした物理symbolが両null sheetでrank 64を持つかを判定する。

これは係数追加ではなく、禁止済みのstrict raw-ultralocal classから、既存の
正の構成であるsource-perfect親へmechanism classを切り替える試験である。

## Claim ceiling

このNO-GOは、既存Palatini作用の係数なし等重みdagger/chiral完成だけを除外
する。source-perfect quasi-local Schur completion、将来のsource-derived phase
law、matter誘起完成、generic singular/global continuation、Braid必要性、経験的
重力は判定していない。

