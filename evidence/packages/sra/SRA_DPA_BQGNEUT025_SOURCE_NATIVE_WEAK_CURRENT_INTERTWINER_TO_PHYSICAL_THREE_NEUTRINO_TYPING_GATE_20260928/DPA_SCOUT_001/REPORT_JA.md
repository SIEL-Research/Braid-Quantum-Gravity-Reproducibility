# BQGNEUT-025 — physical three-neutrino typing

## 結論

**CLOSED SCOPED。**

BGCE439の明示的derived Standard-Model matter class内で、BQGNEUT-024のinternal
neutral qutritは、source-native weak-current intertwinerによって物理的三世代
neutrino factorとして一意に型付けできる。外部三世代carrierは不要である。

ただし、unchanged raw source単独での物理性、absolute mass scale、実測PMNS一致は未導出。

## 一意なbranch-to-generation写像

source branch orderを

```text
(r1,r2,r121)
```

matter generation軸を

```text
(e3,e2,e1)
```

とすると、source marksとorientationを同時に保つ写像は6候補中一つだけで、

\[
r_1\mapsto e_2,\qquad r_2\mapsto e_1,\qquad r_{121}\mapsto e_3
\]

である。行列は

\[
T=
\begin{pmatrix}
0&0&1\\
1&0&0\\
0&1&0
\end{pmatrix}.
\]

この`T`は三つのminimal projectorsだけでなく、source branch registerのmultiplicationと
comultiplicationをexactに保つdagger-Frobenius isomorphismである。basis phaseを追加すると
copy lawが`d_i=d_i^2`を要求し、unitaryかつnonzeroなら`d_i=1`だけなので、連続phase自由度もない。

## weak-current partial isometry

BGCE439のlepton doublet `(1,2)_{-3}`で、weak basisを `(nu_L,e_L)` とする。
`Q=T3+Y/6`によりchargeはexactに`(0,-1)`となる。

source-derived generation mapとweak ladderを合成して

\[
J_{\rm weak}=T\otimes |e_L\rangle\langle\nu_L|
\]

と置く。すると

\[
J_{\rm weak}^\dagger J_{\rm weak}
=I_3\otimes|\nu_L\rangle\langle\nu_L|,
\]

\[
J_{\rm weak}J_{\rm weak}^\dagger
=I_3\otimes|e_L\rangle\langle e_L|
\]

がexactに成立し、rankは3である。

さらに全9個のgeneration matrix unit `E_ij`について

\[
J_{\rm weak}(E_{ij}\otimes P_\nu)
=
(TE_{ij}T^\dagger\otimes P_e)J_{\rm weak}
\]

が成立する。従って、選んだ三basis stateだけでなく、BGCE544のfull `M3` generation
action全体を保つinteraction typingである。

## BQGNEUT-024との接続

この写像でBQGNEUT-024 Floquet eigenframeをphysical generation orderへtransportしても、
nonzero CPとunequal dimensionless gapsは保持される。`|J|`は

\[
0.08557801977513962
\]

のままである。

従って、declared matter class内では次の鎖が閉じた。

```text
source branches
  -> internal neutral qutrit
  -> source-fixed CP+gap Floquet propagation
  -> unique Frobenius generation map
  -> rank-three weak-current interaction
  -> physical three-generation neutrino factor
```

## 非補償境界

BGCE439は明示的なanomaly-solution-groupoid matter extensionであり、degree-one shellを
physical generationsと読むこと自体がその宣言済みbold scoped hypothesisである。そのため
今回のphysical typingをunchanged raw sourceの無条件定理へ昇格させない。

また次は未達である。

- dimensionless Floquet eigenphaseからdimensionful mass-squared gapへの写像
- absolute neutrino scale
- observed PMNS/oscillation dataとの一致
- empirical confirmation

## 次

`BQGNEUT-026_DIMENSIONLESS_FLOQUET_PHASE_TO_PHYSICAL_MASS_SQUARED_SCALE_GATE`

既存のtime/energy calibrationとFloquet phaseを、係数fitなしでmass-squaredへ型付けできるかを問う。

## Claim ceiling

証拠区分は**Theoretical derivation**。BGCE439 derived matter class内でのphysical
three-neutrino typingと外部generation carrier解除まで。unchanged raw source、absolute
mass、実測PMNS一致、自然界のニュートリノ実証、量子重力完成は未主張。
