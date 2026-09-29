# BGCE491 結果

## 判定

**CLOSED_SCOPED。** BGCE490で使ったcanonical Halmos block encodingの`sqrt(I-A^2)`を直接作る必要はない。既存のsource-word LCU unitaryとそのdaggerを1個のencoded signal qubitでHermitian化し、success reflectionを掛ければ同じChebyshev functional calculusがexactに得られる。

## 構成

BGCE483-484のsource-word LCU unitaryを`U_A`、そのsuccess blockをHermitian contraction `A=H/alpha`とする。

\[
\widetilde U_A=
\begin{pmatrix}0&U_A\\U_A^\dagger&0\end{pmatrix}
\]

はHermitian involutionである。新しいsignal qubitの`|+>`とLCU success stateを埋め込むisometryを`E`とすると

\[
E^\dagger\widetilde U_AE=\frac{A+A^\dagger}{2}=A.
\]

さらに`S=2EE^dagger-I`、`W=S U_tilde`とすれば

\[
E^\dagger W^kE=T_k(A)
\]

がexactに成立する。初期値`B_0=I,B_1=A`とrecurrence

\[
B_{k+1}=2AB_k-B_{k-1}
\]

から直接従う。

## 検査

- 全8 signed sector × 4 control = 32件
- 全spectral node、degree最大31
- source orientation phase `0,+2pi/3,-2pi/3`
- 最大unitary residual: `3.16e-16`
- 最大involution residual: `4.47e-16`
- 最大signal-block residual: `1.12e-16`
- 最大Chebyshev residual: `1.14e-14`
- BGCE490の総query範囲`203–39,102`を維持

## 意味

BGCE490で追加されていたsquare-root defectは物理primitiveではなく、block encodingの一つの表現だった。既に実現済みのsource-word LCU unitaryをHermitian化すれば、そのsquare rootを明示的に実装せず同じChebyshev walkを得られる。

必要な操作はsource-counted PREP、typed source-word SELECT、source reversal/dagger、BGCE487 signal qubit、finite controllerのsuccess-address reflectionである。4確率`1+3`は従来通りouter `G1,H1,H2,H3` selectorであり、branch内部のwalkとは分離される。

## 境界

typed finite-list controllerとsuccess-address markをbare adjacent-Braid relationだけから導出したわけではない。次の`BGCE492`では、このaddress markが最小追加primitiveか、旧bare Braid inventoryでは不可能かを判定する。
