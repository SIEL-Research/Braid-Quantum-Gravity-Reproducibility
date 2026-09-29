# BGCE300R1監査 — A49 非循環backreactionと低エネルギーspin-2 / Einstein出力

## 結論

**FULL SCOPED PASS。A49は宣言class内で閉じた。**

固定source模型と、長波長・局所・二階・形式的自己共役・保存的continuum class内で、既存の
source-native finite first-order gravity actionとfull-corner BKM/Umegaki matter actionは、BGCE138の
同じsource-event base上の同じlocal-GL4 metric `g`を変分する。BGCE238のMMR2、BGCE235/239の手動でない
相対`3/5`、BGCE299のHilbert stress / on-shell Wardを合成すると、共通停留条件は

\[
G_{\mu\nu}(g)=\frac35T_{\mu\nu}(g,\lambda)
\]

となる。Einstein tensorをmatter stressの定義へ使わず、新しいEinstein--Hilbert作用、mixed interaction、
係数fit、手動`3/5`を追加していない。

## 1. BGCE300の扱い

最初のBGCE300 evaluatorは、BGCE295 RAWに存在しない`final_decision`キーを参照し、科学判定と
`RAW_OUTPUT.json`生成前に停止した。これは`IMPLEMENTATION_PROVENANCE_FAILURE`であり科学的FAILではない。
凍結artifactは上書きせず、同じ仮説・source hash・判定条件を持つBGCE300R1として再実行した。

## 2. なぜ二つの`g`は同じか

単に記号が一致したのではない。

1. BGCE138はsource spectral cylinderから`Q=(0,1)^4`とnative metric-affine GL4 domainを構成した。
2. BGCE139はそのevent base上でformal vacuum first-variation chainを閉じた。
3. BGCE283はX21R1 metric/tangentを同じsource-event atlas上でtensorとしてglueした。
4. BGCE284はそれをBGCE138のopen local GL4 domainへ拡張し、同じbase上のmetric fieldとした。
5. BGCE294はsource symmetric-product型からphysical solder `A -> U^T A U`を一意化した。
6. BGCE295のmatter parentは明示的に

```text
(1/2) integral sqrt|g| G_AB(lambda)
g^mn partial_m lambda^A partial_n lambda^B d4x
```

を使い、この`g`のHilbert変分を取る。

従ってgravityとmatterは別々の四次元空間または別のmetricを後から同一視したものではない。

## 3. matter lineageは切れていない

BGCE235のfull-corner Gibbs actionはBKM Hessian rank 10を持つ。BGCE238は固定source packetを変えない
matter algebraとしてfull cornerを一意選択し、固定模型内MMR2を閉じた。BGCE252--256は同じfaithful
Gibbs/BKM responseから、actual Braid event coboundaryに沿うlog-Z Bregman/Umegaki neighbor actionと
off-source label dynamicsを導いた。BGCE294/295はこのactionを同じmetric `g`へsolderしてHilbert変分へ運ぶ。

したがってBGCE299のstressは、MMR2と`3/5`を持つmatter theoryとは別に作られたstressではない。

## 4. backreactionの第一変分

既存gravity sectorの変分を

\[
\delta S_g=\frac{1}{2\kappa_B}\int\sqrt{|g|}\,
G_{\mu\nu}\,\delta g^{\mu\nu},
\]

同じ`g`に対するmatter Hilbert変分を

\[
\delta S_m=-\frac12\int\sqrt{|g|}\,
T_{\mu\nu}\,\delta g^{\mu\nu}
\]

と書く。BGCE235/238/239のsource routingは相対規格化を
`kappa_B=3/5`へ固定するため、`delta(S_g+S_m)=0`は上式を与える。

この加法は新しいcurvature-matter operatorの挿入ではない。既に同じsource model内で閉じた二つの
variational sectorと、その相対routingの依存伝播である。Bianchi identityとBGCE299のon-shell Wardは
同じ`g`上で両辺のdivergenceを一致させる。

## 5. 低エネルギーspin-2

BGCE138のflat source anchorは`e=3 I_4, Gamma=0`。定数scaleを吸収して`g=eta+h`と置くと、Palatini
connection equationはsymmetric Ricciに見えないprojective modeを除きLevi-Civitaへ落ちる。二次metric
sectorは標準Fierz--Pauli gauge classである。

matter shellではflat limitのWardが`partial^mu T_mu_nu=0`を与えるため、線形化されたgauge symmetryと
source couplingは整合する。四次元ではgauge reduction後の伝播helicityは2。mass termまたはcosmological
termを追加して得た結論ではない。

## 6. 何が初めて閉じたか

- 以前：真空gravity first variationとmatter stress/Wardは別々に成立。
- 今回：同じsource base・同じmetric・同じmatter lineage・同じrelative routingであることを照合。
- 結果：matterがmetricを変え、そのmetricがPalatini gravity equationで応答するbackreactionが閉じた。

したがって「Einstein形へ到達した」だけでなく、固定source模型・宣言class内では**作用の共通第一変分から
物質付きEinstein方程式を導出した**と表現できる。

## counter-intuition

標準的説明は、同じmetricを共有するPalatini gravityとdiffeomorphism-covariant matterを足せば通常の
backreactionとmassless spin-2極限が出る、というもの。SIEL/Braid固有なのは、そのgravity action、event
base、metric solder、full-corner matter action、MMR2 routing、相対`3/5`が一つのpointed-Braid source
provenanceで接続した点である。

## 主張上限

これはfixed source modelと宣言continuum class内の**理論導出**である。次はまだ示していない。

- full finite Lorentzian quantum backreaction;
- higher-curvature、higher-derivative、nonlocal、独立clock項の不在;
- source単位からSI単位への変換と物理Newton定数の数値;
- 自然時空・天体・実験との経験的同定;
- 完成量子重力、存在論、主観、意識の実証。

ここでの`3/5`はsource-normalized相対couplingであり、SI単位のNewton定数そのものではない。

## 次

`BGCE301_A50_FINITE_QUANTUM_BACKREACTION_AND_HIGHER_DERIVATIVE_RESIDUAL_BOUNDARY_GATE`。

低エネルギーEinstein出力を作り直さず、finite Braid actionのmetric変分がcontinuum backreactionへ直接
収束する範囲と、高階・非局所補正が最初に現れ得る境界を特定する。

実行時間は0.4秒。数値走査なし。DPAによるformal E0/E1/E2発行なし。
