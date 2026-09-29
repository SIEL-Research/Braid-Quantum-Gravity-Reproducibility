# BQGSTRAT-009 監査報告

## 結論

**SCOPED PASS**。

`BQGSTRAT-008`が不足物として特定したPalatini二階jetを、既存の
BGCE138 `Pexp` link、BGCE097 face-log、BGCE137 source五進四次元cellから
追加係数なしで構成しました。

actual caustic自体はまだ閉じていません。次は構成済み疎Hessianのrank、
kernel、crossing form、component labelを評価します。

## 二階plaquette jet

oriented faceを

`P=exp(A)exp(B)exp(-C)exp(-D)`

とすると、exactな次数2切断で

`log P=A+B-C-D+(1/2)sum_(i<j)[Z_i,Z_j]+O(3)`、
`Z=(A,B,-C,-D)`

です。

- orientation reversalで符号反転：PASS
- constant connection `C=A,D=B`で`[A,B]`：PASS
- floating-point、係数fit、目標Einstein式：不使用

## source child split

一段のsource refinementは`5^4=625` cellです。exact incidenceは次です。

- vertex：total 1296、interior 256、boundary 1040
- edge：total 4320、interior 1280、boundary 3040
- face：total 5400、interior 2400、boundary 3000

BGCE138のcoframe/GL4 raw coordinateでは、

- interior coordinate：24576
- boundary coordinate：65280
- `K_ii`：24576 × 24576
- `K_ib`：24576 × 65280

です。これはdense matrixを作る指示ではなく、疎incidence operatorとして
評価するためのexact shapeです。

## flat stationary relation

source anchor `e=3I,Gamma=0`では全face logがzeroです。したがってcoframe
gradientはzeroです。さらに全1280 interior edgeでoriented face incidenceが
exactに相殺し、固定boundaryのvacuum blockはinterior stationary pointに
なります。

二次作用は

`delta^2 S=C sum epsilon epsilon [2 ebar f (D a)+ebar ebar Q(a,a)]`

です。このbilinear formをinterior/interiorへ制限したものが`K_ii`、
interior/boundaryへ制限したものが`K_ib`です。

## 残る境界

- raw/reduced Hessian rankは未評価
- rank lossの存在・位置は未評価
- crossing formは未評価
- ordered spectral historyがconnected componentを一意に選ぶかは未評価
- BGCE094の`e_0,U_0` off-shell promotionは条件付き

## 次

`BQGSTRAT-010`でdense matrixを生成せず、cubical Fourier/incidence分解を使って
rankとkernelをexact評価します。rank lossがあればcrossing formとsource
component labelを同時に判定し、無ければactual flat blockでのcaustic不在を
閉じます。
