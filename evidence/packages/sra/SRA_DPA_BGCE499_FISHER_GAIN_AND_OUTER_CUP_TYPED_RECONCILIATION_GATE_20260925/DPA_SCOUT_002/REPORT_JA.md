# BGCE499監査 — Fisher gain `1`とouter-cup `3/5`の型付き整合

## 結論

**PASS / `BQG-G3-R03.6` CLOSED_SCOPED。**

係数の断絶はありません。`1`と`3/5`は同じscalar couplingの競合値ではなく、
二段階の変分で異なる場所に現れるsource-derived量です。

- `1`：同じrecord actionのscoreとFisher Hessianの間の内部gain。
- `3/5`：full-corner matter actionを、別carrierのgravity actionに対して数える外部weight。

## 決定式

BGCE235のouter cupを

\[
p=\frac35
\]

とする。matter action全体をcupすると、同じactionから取るHessianとscoreは両方
同じ倍率になる。

\[
F_m\mapsto pF_m,\qquad S_m\mapsto pS_m.
\]

したがってFisher/Newton更新は

\[
\delta h=(pF_m)^{-1}(pS_m)=F_m^{-1}S_m
\]

であり、内部gainはexactに`1`のままである。これはBGCE372–373のsame-parent
normalization invarianceそのものであり、`3/5`をscoreだけへ入れる非対称写像は不要である。

一方、gravity actionとmatter actionは別々に型付けされている。full-corner cupはmatter側にだけ
定義されるので、外部のtotal actionは

\[
S_{\rm total}=S_g+pS_m
\]

これはBGCE300R1の表記 \(S_g/p+S_m\) を作用全体へ \(p\) 倍したものと同値であり、
Euler零点を変えない。

となる。共通metricの第一変分では

\[
\delta S_g+p\,\delta S_m=0
\quad\Longrightarrow\quad
G_{\mu\nu}=pT_{\mu\nu}=\frac35T_{\mu\nu}.
\]

つまり、`1`はmatter側の内部最適化でscaleが相殺される値、`3/5`はgravityとmatterの間で
相殺されずに残る相対weightである。

## 既存結果との整合

- BGCE235：full-corner unitのnormalized tail traceから`p=3/5`。
- BGCE371：same-record Fisher actionのstationary updateはunit gain。
- BGCE372：`1`と`3/5`は同一referentでない。
- BGCE373：同じ作用内の共通scaleはunit gainを変えない。
- BGCE300R1：同じfull-corner matter lineageを使う外部第一変分は
  `G=(3/5)T`。

したがってBGCE372–373のNO-GOは維持される。排除されたのは、`3/5`を同じFisher作用の
score legだけへ掛ける経路である。今回採用したのはそれではなく、source cupの定義域を
matter action全体に保つ型付き二段構成である。

## Counter-intuition

最強の反対解釈は、BGCE371 finite updateとBGCE300R1 continuum Euler flowの動力学的な
収束関係がまだ証明されていないことである。これは正しい。今回閉じたのは係数の型整合であり、
有限updateがcontinuum方程式の離散integratorであるという定理ではない。

## 判定

- inner Fisher gain：`1`、PASS。
- outer matter/gravity weight：`3/5`、PASS。
- 同一scalar referent：NO。
- asymmetric score/Hessian map：不使用。
- 手動`3/5`：不使用。
- `BQG-G3-R03.6`：`CLOSED_SCOPED`。

## 証拠区分・主張上限

一次区分は**Theoretical derivation**。固定sourceとBGCE300R1宣言continuum classにおける
typed compatibility theoremである。BGCE371 updateのcontinuum収束、absolute SI scale、
Newton定数の予測、経験的重力、完成量子重力は導出していない。

試行001はrepo-root参照誤りで科学endpoint前に停止し、上書きせず
`FAILED_IMPLEMENTATION`として保存した。試行002はその参照だけを修復し、全7 gateをPASSした。
