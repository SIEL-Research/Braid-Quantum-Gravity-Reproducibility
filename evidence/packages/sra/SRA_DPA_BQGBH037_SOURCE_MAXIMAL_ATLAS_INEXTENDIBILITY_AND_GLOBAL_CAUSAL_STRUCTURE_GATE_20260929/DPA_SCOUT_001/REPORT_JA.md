# BQGBH-037 報告

## 結論

**CLOSED_SCOPED。**

BQGBH-031/035でsource選択され、BQGBH-036でhorizon-completeになった静的球対称解

\[
R(X)=\sqrt{X^2+\ell_*^2},\qquad
F(X)=1-\frac{r_h}{R(X)},\qquad X\in\mathbb R
\]

について、source event provenanceは周期同一視を選ばず、反復horizon gluingの
**non-quotient universal cover**を標準大域atlasとして選ぶ。このatlasでは全因果
測地線がcompleteで、Cauchy horizonはなく、global hyperbolicityが成立する。

従って、global hyperbolicityとtimelike geodesic completenessから
`C0-inextendibility`を与える標準定理を適用できる。選択された静的球対称連続体解は
`C0`で非延長であり、従ってanalyticにも非延長である。

これは外部の目標Einstein方程式、目標stress、係数fit、周期時間境界条件を使わない。

## 1. 三つの大域因果regime

\(q=r_h/\ell_*\)とする。

| regime | horizon | throat | source-maximal graph |
|---|---:|---|---|
| \(0\le q<1\) | 0 | timelike、two-way | two-ended static wormhole block |
| \(q=1\) | double horizon at \(X=0\) | null、one-way | countable null-bounce chain |
| \(q>1\) | \(X_\pm=\pm\ell_*\sqrt{q^2-1}\) | spacelike bounce | countable two-exterior bounce ladder |

全regimeで\(R\ge\ell_*>0\)であり、BQGBH-036のregular EF/Kruskal atlasが
有限\(X\)のchart endpointを除去する。

## 2. なぜ周期同一視ではなくuniversal coverか

BQGBH-003のsource walkは

\[
U|n,\mathrm{in}\rangle=|n-1,\mathrm{in}\rangle,\qquad
U|n,\mathrm{out}\rangle=|n+1,\mathrm{out}\rangle
\]

と\(n=1\)での一度のreflectionからなるbijectionである。reflection後のoutgoing
screen numberは一段ずつ無限に増加するので、event stepはexactにinjectiveである。

future bounceとpast bounceの周期同一視は、異なるsource eventを同一点に写す追加商で
あり、sourceから供給されない。従って標準completionは周期時間ではなく、異なるevent
を保ったnon-quotient universal coverである。

## 3. 全因果測地線complete

球対称性により、timelikeでは\(\delta=1\)、nullでは\(\delta=0\)として

\[
\dot X^2=E^2-F(X)\left(\delta+\frac{L^2}{R(X)^2}\right).
\]

一方、

\[
R\ge\ell_*,\qquad 1-q\le F\le1
\]

なので右辺のpotentialは全\(X\)で有界である。従って\(|\dot X|\)も有界で、
\(|X|=\infty\)へ有限affine parameterで到達できない。

有限\(X\)では、BQGBH-036のingoing/outgoing EFとKruskal patchによりmetricはsmoothかつ
nondegenerateである。誤った一枚chartの座標発散は別chartで延長され、angular velocity
も\(|L|/R^2\le |L|/\ell_*^2\)で有界である。従って全timelike/null geodesicは未来・過去
の両向きにcompleteである。

## 4. Cauchy block-time

non-quotient coverのblockを\(n\in\mathbb Z\)で番号付けする。各compactified conformal
block内でstrictly temporalな\(\tau\)を選び、gluing上で

\[
T=n+\tau
\]

とする。future-directed crossingは必ず\(n\to n+1\)で、causal cycleも有限終端blockも
ない。inextendible causal curveは、無限個のblockを横切るか二つのconformal infinityの
いずれかへ向かう。どちらも\(T\)の全rangeを通り、各regular levelを一度だけ横切る。

従って\(T=\mathrm{const}\)はCauchy hypersurfaceであり、選択されたnon-quotient spacetime
はglobally hyperbolicである。inner Cauchy horizonは生じない。

## 5. 非延長性

Galloway--Ling--Sbierskiの定理は、smoothでtime-orientedなLorentz manifoldが

1. globally hyperbolic、かつ
2. timelike geodesically complete

なら`C0-inextendible`であることを示す。上の3、4節で両仮定を独立に閉じたため、
本解は`C0-inextendible`である。これはanalytic inextendibilityより強い。

bounded curvatureだけから非延長性を主張していないことが重要である。

## 6. 一次文献との照合

sourceから導出したmetricに

\[
a=\ell_*,\qquad 2m=r_h
\]

を代入するとSimpson--Visser metricと関数的に一致する。一次文献は、同じ三regime、
最大拡張diagram、\(q>1\)でspacelike bounceを通ってad infinitumに続く非特異ladderを
報告しており、本gateのsource-side導出と一致する。

- Alex Simpson and Matt Visser, *Black-bounce to traversable wormhole*,
  https://arxiv.org/abs/1812.07114
- F. S. N. Lobo et al., *Novel black-bounce spacetimes: wormholes, regularity,
  energy conditions, and causal structure*, https://arxiv.org/abs/2009.12057
- L. Sebastiani and S. Zerbini, *Some remarks on non-singular spherically
  symmetric space-times*, https://arxiv.org/abs/2206.03814
- G. J. Galloway, E. Ling and J. Sbierski, *Timelike completeness as an
  obstruction to C0-extensions*, https://arxiv.org/abs/1704.00353

これらはsource action、interaction、metricを選ぶためには使用せず、導出後の因果分類と
一般inextendibility定理の照合にのみ使用した。access dateは2026-09-29。

## 7. 判定

- source-selected non-quotient maximal atlas：**PASS**。
- 三regimeのglobal region graph：**PASS**。
- causal geodesic completeness：**PASS**。
- global hyperbolicity：**PASS**。
- Cauchy horizon：**なし**。
- `C0` / analytic inextendibility：**PASS**。
- target Einstein式・target stress・係数fit：**未使用**。
- static spherical global strong-curvature black-hole closure：**CLOSED_SCOPED**。

## Evidence status / claim ceiling

一次区分は **Theoretical derivation / closed-scoped result**。

閉じたのは、source-selected complete six-face Palatini作用から得た静的球対称連続体
black-bounceの大域・強曲率・最大atlas・非延長性である。dynamical collapse、evaporation、
thermodynamics、rotation、charge、一般nonspherical strong curvature、自然界のblack hole
との同一視、経験的確認、量子重力理論全体の完成は主張しない。
