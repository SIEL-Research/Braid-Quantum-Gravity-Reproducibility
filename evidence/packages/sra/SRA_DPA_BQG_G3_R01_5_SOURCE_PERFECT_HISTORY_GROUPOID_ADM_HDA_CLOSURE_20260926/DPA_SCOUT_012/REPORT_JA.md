# BQG-G3-R01.5 / DPA-SCOUT-BQGADM-012 — source-perfect history groupoidによるADM/HDA閉包

## 結論

**CLOSED_SCOPED。** 固定格子上の有限Lie代数を閉じる経路を捨て、source Palatini towerの定常refinement limitをperfect history-groupoid作用として取ることで、同じ構成からexact Noether identity、4方向kernel、metric-dependent HDA、BFV nilpotency、refinement intertwining、4次元physical phase quotientを得る。

閉じた範囲はlocal regular noncaustic source-perfect history sectorである。raw finite-cell actionそのものがultralocalなexact HDAを持つとは主張しない。

## 大胆な仮説

BQGADM-008が過剰拘束になった理由は、4つのprimitive moveから生成された全`gl(5)`線形spanを独立constraintとして数えたことにある。

正しい有限対象はLie algebraではなくhistory groupoidである。

- 独立generatorはsourceが選ぶ`1 clock + 3 spatial`の4種類だけ。
- その合成は新しいconstraintではなくhistory arrow。
- 異なる合成順序の一致はhigher coherence cell。
- HDAはこのgroupoidのLie algebroidとして現れる。

これによりexact closureと正しい自由度数を両立できる。

## perfect action

有限段`m`のsource Palatini slab actionを`S_m`とする。coarse boundary dataを固定した局所regular・noncaustic branchで

\[
S_n^{\rm perf}(z_-,z_+)
=
\lim_{m\to\infty}
\operatorname{stat}_{R_{m,n}z_m^{\partial}=(z_-,z_+)}S_m[z_m]
\]

と定義する。

BGCE097/BGCE099が作用とfirst variationのsource-limitを与え、BQGEULER-010が同じregular区間でtrajectory強収束を与えるため、このstationary limitは宣言scope内で存在する。

ここでのanalytic domainは、共通smooth区間、gauge固定後に一意なnoncaustic stationary branch、4 gauge方向を除いたtransverse Hessianの非退化、boundary traceを許す十分高いSobolev regularity、BQGADM-006のrank-four minorが非零のopen neighborhoodである。これはglobal existenceの仮定ではなく、局所perfect-action定理の適用範囲である。

exact discrete Lagrangianのstationary compositionから

\[
S_{02}^{\rm perf}
=\operatorname{stat}_{z_1}
\left(S_{01}^{\rm perf}+S_{12}^{\rm perf}\right)
\]

が成立する。nested source refinementでは

\[
J_{n+1,n}^{*}S_{n+1}^{\rm perf}=S_n^{\rm perf}.
\]

## Noetherと4方向kernel

同じhistoryのgroupoid refactorizationはperfect actionを変えない。4つのprimitive deformationを`R_n`とすれば

\[
\boxed{R_n^\dagger\mathcal E(S_n^{\rm perf})=0}
\]

がoff shellでexactに成立する。

BQGADM-005のLorentz/torsion reduction後は12次元symplectic carrier、BQGADM-006のscalar 1本＋vector 3本はrank 4である。したがって、そのminorが非零のopen regular neighborhoodでは4 generatorは独立で、constraint surfaceはcoisotropic、kernelはexactに4方向となる。

## HDA・BFV・自由度

perfect history groupoidのLie algebroidは、BQGADM-011で確定したmetric-dependent HDAのfinite-boundary pullbackである。

\[
\{D[N],D[M]\}=D[[N,M]],
\]

\[
\{D[N],H[M]\}=H[\mathcal L_NM],
\]

\[
\{H[N],H[M]\}
=D[\gamma^{ij}(N\partial_jM-M\partial_jN)].
\]

composite arrowを独立constraintへ昇格させないため、BQGADM-008の25-generator overgaugeは起きない。Lie-algebroidのhomological vector fieldとしてlocal BFV differential `s_n`が存在し、`s_n^2=0`。groupoid associativityがhigher coherenceを与える。

12次元reduced phaseに4本のregular first-class constraintsなので

\[
12-2\times4=4
\]

となり、物理configuration modeは2つである。

## 境界

これはsource refinement towerから得たperfect actionの存在定理である。次は不要になった固定格子Lie代数の係数探索ではない。

なお以下は未導出である。

- perfect actionの有限depthでの明示的ultralocal closed form
- caustic、singularity、strong curvatureを含むglobal theorem
- refinement limitに依存しないraw finite-cell action自身のexact HDA
- full quantum matter BFV、SI calibration、経験的検証
