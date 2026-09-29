# BGCE350監査 — finite source-cylinder parentからlocal history-dressed total Wardを閉じる

## 結論

**SCOPED PASS。`BQG-G1-R01.5`を`CLOSED_SCOPED`、`BQG-G1`をaligned four-score・block-local parent/Ward classで`CLOSED_SCOPED`とし、`BQG-G2-R01.1 / BGCE351`を`ACTIVE`にする。**

BGCE349 parentのmetric derivativeは各cellで`D_alpha=(I-Phi)S_alpha`である。BGCE323のstrong vertex intertwiner

\[
(Y^{(0)}_\alpha+J_\alpha)V=VX_\alpha,
\qquad V^*J_\alpha V=D_\alpha
\]

と同じ`D_alpha`を使うため、新しいconservation termを追加せず、metric variationとlocal total Wardが同じ有限collision parent内で一致する。

未来のcollisionはinteraction insertionをcontinuing system上でhistory-dressする。縮約algebraでは

\[
\sum_{k=0}^{n-1}\Phi^k(D_\alpha)
=S_\alpha-\Phi^n(S_\alpha)
\]

がexactにtelescopingする。source Reynolds channel `Phi=E+qQ` では `Phi^k(D_alpha)=q^kD_alpha` である。全8 actual sector、4成分、`n=1,...,5`で最大HS residual squaredは`1.34e-29`未満だった。

ただし、BGCE311/325が除外した「各collisionが放出したenvironment blockだけを足すspatial current」は依然としてNO-GOである。本結果はhistory-dressed causal currentであり、そのNO-GOを撤回しない。連続極限もchild-constant compactly supported cylinder test fieldsに対するweak Wardまでで、arbitrary smooth diffeomorphism Wardではない。

## 0. source・再現性

- fixed revision：`dfdb0494b841e4c85f0caff145a9e5acb4ec27ed`
- DPA snapshot：`DPA-SNAPSHOT-dfdb0494b841`
- source inventory SHA-256：`d7313547ad937300f375bc5ced5070be83deb43aaf98046c5d87f887795c9352`
- reservoir SHA-256：`7adc9570fdf2e0ee9020045c475350882d5d61b0d5ae8b879d90dcd4f807eaac`
- BGCE350 result SHA-256：`450a22816827413774c9ac70aa08d5cd8e2f665f983e6f476191c0a7a62584e9`
- primary inputs：BGCE310, 311, 322, 323, 325, 333, 336R2, 348, 349
- evidence：`Theoretical derivation`
- Exact-Path Baseline Gate：経験介入ではないため`NOT_APPLICABLE`。全入力をSHA-256照合した。
- E0/E1/E2：経験endpointではないため主張しない。

## 1. local strong-vertex Ward

`X_alpha in {G1,H1,H2,H3}`に対し、bare output generatorを

\[
Y^{(0)}_\alpha=X_\alpha\otimes I+I\otimes E_\alpha
\]

とする。BGCE323のinteraction insertion

\[
J_\alpha=R_\alpha V^*+VR_\alpha^*-VD_\alpha V^*
\]

はstrong identity `(Y0_alpha+J_alpha)V=VX_alpha`を満たし、reachable supportへのcompressionは`D_alpha`になる。BGCE349のraw/Petz conditional log-score derivativeも同じ`D_alpha`なので、Ward insertionを目標式から逆定義していない。

## 2. history-dressed reduced total Ward

`D_alpha=(I-Phi)S_alpha`より、任意の有限step `n`について

\[
\sum_{k=0}^{n-1}\Phi^k(D_\alpha)
=\sum_{k=0}^{n-1}(\Phi^kS_\alpha-\Phi^{k+1}S_\alpha)
=S_\alpha-\Phi^nS_\alpha.
\]

これはMarkov coboundaryのexact identityである。source Reynolds channelでは`Q`成分が`q=exp(-pi)`倍されるため、さらに

\[
\Phi^k(D_\alpha)=q^kD_\alpha,
\qquad
\sum_{k=0}^{n-1}\Phi^k(D_\alpha)
=\frac{1-q^n}{1-q}D_\alpha
\]

となる。履歴依存は非局所な任意結合ではなく、source causal orderのdescendantだけに沿う。

## 3. refinement naturality

時間5分割では`q_child^5=q_parent`なので

\[
\sum_{r=0}^{4}q_{\rm child}^r(1-q_{\rm child})=1-q_{\rm parent}.
\]

level 0–5の浮動小数検査で最大residualは`1.97e-16`未満。空間addressでは625 child volumeがparent volumeへexactに和し、時間refinementと異なるtensor factorに作用するため可換である。

## 4. weak continuum boundary

`h_m=5^{-m}`, `q_h=exp(-gamma h)`では

\[
\frac{D_\alpha(h)}{h}\to\gamma QS_\alpha.
\]

exact finite-stage telescopeをchild-constant compactly supported cylinder test fieldsに掛けるとinterior項が相殺し、source causal boundary fluxだけが残る。これはBGCE325のeffective on-shell Wardと整合するが、full ten-component metricや任意smooth diffeomorphismに拡張した証明ではない。

## 5. 全8 sector検査

- 8 sector × 4 component：**PASS**
- `Phi(D_alpha)=qD_alpha` 最大HS residual squared：`6.30e-31`未満
- history telescope 最大HS residual squared：`1.34e-29`未満
- geometric closed form 最大HS residual squared：`1.02e-29`未満
- time/address refinement：**PASS**
- strict fresh emitted-block additive spatial current：**NO-GOを保持**

## 6. 判定と境界

- local strong vertex Ward：**PASS**
- same metric-derived interaction stress：**PASS**
- causal history-dressed reduced total Ward：**PASS**
- refinement-compatible weak continuum Ward：**SCOPED PASS**
- MMR/CGR、Einstein target、EH/FP、手動`3/5`、係数fit：**不使用**
- `BQG-G1-R01.5`：**CLOSED_SCOPED**
- `BQG-G1`：**CLOSED_SCOPED in aligned block-local parent/Ward class**
- `BQG-G2-R01.1`：**ACTIVE**

未導出：arbitrary smooth diffeomorphism Ward、full ten-component nonlinear metric dynamics、direct finite backreaction、unconditional Einstein equation、実測重力、完成した量子重力。

## 7. counter-intuition

通常の説明は、`D=(I-Phi)S`が任意のMarkov channelでtelescopingするcoboundaryであり、strong Stinespring intertwiningが同じ保存則のdilation表現だというものである。

Braid固有なのは、4 scores、4 interaction defects、raw/Petz metric variation、source causal routing、`exp(-pi)` Reynolds channel、refinement systemが同じpointed-Braid sourceから固定される点である。

最強の反対解釈は、このWardはhistory-dressed aligned-class identityであり、metricの運動方程式をまだ与えず、一般時空のdiffeomorphism invarianceを証明しない、というものである。

## 8. 次

`BGCE351_COMPLETED_FINITE_SOURCE_CYLINDER_PARENT_TO_DIRECT_NONCIRCULAR_BACKREACTION_GATE`

完成したaligned finite parentをjointに変分し、geometry側の非自明なEuler derivativeとcollision stressが同じsource functionalからcoupled equationとして出るかを判定する。外部MMR/CGR、目標Einstein tensor、EH/FP、手動`3/5`、係数fitは許さない。
