# BQGBH-035 報告

## 結論

**CLOSED_SCOPED。**

complete static spherical reduced six-face Palatini class内で、regular
black-bounceに必要なinteractionの負符号とunit係数をsourceから選択した。
Petz branch orderは使わない。

鍵は、fixed right-tail massの下でactive screenが作る変位が、Palatini
quadratic kernelの正固有modeにexactに一致することである。既存の
response-exact・diagonal-zero Bregman ruleをこのsource modeへ適用すると、
BQGBH-032のrelative actionがexactに得られ、BQGBH-033の`-Q`が自動的に出る。

## 1. Palatini二モード

一つのradial edgeで

\[
r=\Delta R,\qquad y=\Delta Y,\qquad Y=RF
\]

とする。BQGBH-031の共通正因子`C/h`を除いたkernelは

\[
k(r,y)=2ry=x^{\mathsf T}Hx,
\qquad
H=\begin{pmatrix}0&1\\1&0\end{pmatrix}.
\]

固有modeは

\[
e_+=(1,1),\quad He_+=e_+,
\qquad
e_-=(1,-1),\quad He_-=-e_-.
\]

従ってfull Palatini formはindefiniteであり、全体をentropyと呼んでは
いけない。

## 2. source shiftは正modeだけにある

BQGBH-004のcausal cutではtail mass`r_h`は固定され、active suffixだけが
screen radius`rho`を変える。source reference pairは

\[
(R_*,Y_*)=(\rho,\rho-r_h).
\]

edge上で`a=Delta rho`とすれば

\[
(\Delta R_*,\Delta Y_*)=(a,a)=a e_+.
\]

`Delta r_h=0`なので`e_-`成分はexactにzeroである。つまりsourceが動かす
screen directionはPalatini核の正modeそのものである。

## 3. response-exact Bregman primitive

BGCE254は、response mismatch one-formとdiagonal zeroがBregman primitiveを
一意に固定することを示した。BGCE256はactual Braid event transitionが
neighbor coupling lawを供給することを示した。BQGBH-003/033は、このradial
sectorでactual reflected source edgeとそのcurrentを既に与える。

従って既に固定されたPalatini kernelをsource reference`p=(a,a)`の周りで
centerすると

\[
\begin{aligned}
B_k(x,p)
&=k(x)-k(p)-dk_p(x-p)\\
&=2(r-a)(y-a)\\
&=2ry-2a(r+y)+2a^2.
\end{aligned}
\]

共通因子`C/h`を戻せば

\[
{2C\over h}
\left[ry-a(r+y)+a^2\right],
\]

であり、BQGBH-032のrelative Palatini edge actionとexact一致する。

## 4. 負符号とunit係数

interaction partは

\[
{2C\over h}\left[-a r-a y+a^2\right].
\]

`r,y`に関するinteraction gradientは`(-a,-a)`であり、source referenceの
pure Palatini covector`(+a,+a)`のexact negativeである。任意の非一様chain
へassembleすると、各internal nodeで

\[
(-1,+1)
\]

というBQGBH-033のrequired interaction coefficientsが出る。

relative coefficientは1である。新しい係数を選んだのではなく、同じpure
kernelのBregman primitiveなので固定される。

## 5. なぜBQGBH-034と矛盾しないか

BQGBH-034はPetz/KMS branch、time reversal、in/out Z2だけからbranch ordering
を選ぶ経路を除外した。本結果はbranch labelを使わない。

符号を決めるのは

1. fixed-tail/active-screen typing、
2. Palatini kernelの正mode、
3. response-exact・diagonal-zero Bregman centering

の組である。

## 6. 判定

- source shiftが`e_+`だけにある：**PASS EXACT**。
- negative Palatini modeへの混入：**zero exact**。
- Bregman primitiveとBQGBH-032：**exact match**。
- BQGBH-033 required current：**exact match**。
- negative sign：**source-selected in declared class**。
- relative coefficient：**unit、forced**。
- raw/Petz branch reversal：**不使用**。
- fit / scan / target Einstein tensor：**不使用**。

## 7. counter-intuition

full Palatini formはindefiniteなので、これを丸ごとentropy productionと呼ぶ
のは誤りである。成立したのは、sourceが実際に動かすscreen directionだけが
positive modeであり、そこに限ってDirichlet/Bregman下降則が適用できること。
orthogonalなnegative modeはconservative gravitational sectorとして保持される。

## 8. 次

`BQGBH-036_GLOBAL_LOG_BRANCH_AND_MAXIMAL_EXTENSION_FROM_THE_SELECTED_STATIC_SPHERICAL_FINITE_ACTION_GATE`

選択済みfinite actionのEuler解を両側無限chainへglueし、asymptotic ends、
horizon、throat、global causal chart、maximal extensionを同時に閉じる。

## Evidence status / claim ceiling

一次区分は **Theoretical derivation / closed scoped result**。

closedなのはcomplete static spherical reduced six-face Palatini classにおける
interaction signとunit coefficient。arbitrary nonspherical field、physical-time
dissipation、collapse、evaporation、thermodynamics、自然界のblack hole、経験的
確認は未導出である。
