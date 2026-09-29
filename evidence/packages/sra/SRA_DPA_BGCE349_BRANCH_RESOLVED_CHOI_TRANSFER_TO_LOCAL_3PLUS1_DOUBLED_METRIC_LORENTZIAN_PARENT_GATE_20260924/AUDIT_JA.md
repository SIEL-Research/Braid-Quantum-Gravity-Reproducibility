# BGCE349監査 — raw/Petz記録付きcollisionをlocal 3+1 Lorentzian CTP parentへglueする

## 結論

**SCOPED PASS。`BQG-G1-R02.4`を`CLOSED_SCOPED`とし、`BQG-G1-R01.5`を`ACTIVE`にする。**

BGCE348のraw/Petz branch contrastは、source event cylinderの各cellに局所配置できる。必要なのは二つの`Z2`を混同しないことである。

- CTP contour：forward/backward。二つの物理branch metric `g_forward`, `g_backward`を運ぶ。
- KMS record：raw/Petz。各contour copyの内部に残るsource-fixed classical instrument outcomeである。

各cellでBGCE346の共通two-sided positive normalizationをraw/Petz平均CP mapへ適用すると、raw/Petz記録を保ったlocal instrumentが得られ、priorを足したtotal channelはexactにCPTPになる。一方、conditional effectのlog ratioは

\[
a_c(h;\sigma_c)
=\operatorname{Tr}\sigma_c
\left[\log F_{{\rm raw},c}(h)-\log F_{{\rm Petz},c}(h)\right]
\]

であり、aligned metric方向について

\[
\partial_\alpha a_c(0;\sigma_c)
=\operatorname{Tr}(\sigma_cD_\alpha),
\qquad
D_\alpha=S_\alpha-\Phi(S_\alpha)
\]

をexactに与える。全8 actual Braid sector、4成分すべてでresidualはmachine zeroだった。

source cylinderのaddress algebraをcentral blockとして使い、source causal event permutationの後に各blockのlocal instrumentを作用させる。child-constant address embedding、internal tail identity、`625`-child volume coarsening、`5`-step event-time coarseningは互いに可換である。従って局所gluingとrefinement naturalityが閉じる。

Lorentz符号は手動挿入していない。BGCE258/266のsource event form

\[
K_{\rm evt}
=\frac1{25}
\begin{pmatrix}
36&-16&-16&-16\\
-16&36&-16&-16\\
-16&-16&36&-16\\
-16&-16&-16&36
\end{pmatrix}
\]

の固有値は`(-12/25,52/25,52/25,52/25)`であり、sourceが1 timelike + 3 spacelike splitを固定する。

ここで閉じたparentは、source-typed aligned four-score subbundle、block-local collision、source-null-link routingに限定される。full ten-component nonlinear metric dependence、nontrivial spatial-gradient interaction、local total Ward、direct backreactionはまだ導出していない。

## 0. source・再現性

- fixed revision：`ad2e19be691032d59a362193c6ec72ce9e4da793`
- DPA snapshot：`DPA-SNAPSHOT-ad2e19be6910`
- source inventory SHA-256：`54f5c7f0a1544c6a7d75d3b9fb052c08ca7ba78ff2dea4b9d906c2dde7bab939`
- reservoir SHA-256：`4965d4fab6eeb647b19a84f617e91bce5c7cdfdfd4b6661e1a89f6077431f440`
- BGCE349 result SHA-256：`2385486c5c3f8016d64e831e72859b55371cd542468333b8b928536c2d56de65`
- primary inputs：BGCE138, 139, 258, 266, 321, 324, 326, 333, 336R2, 346, 347, 348
- evidence：`Theoretical derivation`
- Exact-Path Baseline Gate：経験介入ではないため`NOT_APPLICABLE`。全入力をSHA-256照合した。
- E0/E1/E2：経験endpointではないため主張しない。

## 1. local source metricからrecorded instrumentへのmap

宣言metric範囲は、BGCE321のten-component local symmetric metric tangentのうち、BGCE324でcollision conserved quartetにexact alignmentしたfour-score subbundleである。

\[
S(h)=\sum_{\alpha=0}^3h^\alpha S_\alpha,
\qquad
D(h)=(I-\Phi)S(h),
\qquad
T(h)=\frac{D(h)}{4(1+e^{-\pi})}.
\]

BGCE345/346のtwo-sided positive scalingをこの線形source mapへfiberwiseに適用する。operator exponential、positive inverse square root、Petz/KMS adjoint、Reynolds expectationだけを使うためsource conjugation naturalityを保つ。新しい作用、補間、係数fitはない。

raw/Petz conditional branchを別々に保持しつつ、固定prior `1/2`で足したtotal mapはunital CPで、そのdualはCPTPである。raw/Petz recordを捨てると一次のeffect tangentはcancelするが、recordを保持したconditional log-scoreは`D_alpha`を保持する。これはBGCE347のzero total connectionと矛盾しない。

## 2. 二つのdoublingを分離する理由

raw/PetzをCTP forward/backwardと同一視してはいけない。前者はsource KMS grading、後者は同じphysical processを二重化したcontourである。

本構成では各contour branchが同じrecorded CPTP instrument familyを持つ。従って`g_forward=g_backward`かつgrading bookkeeping source `chi=0`で

\[
Z_m[g,g;0]=1
\]

がexactに成立する。raw/Petz conditional scoreはclassical recordに対するsource-fixed log-likelihood ratioとしてparent内に残る。

## 3. source-cylinder local gluing

stage `m`の局所algebraを

\[
\mathcal A_m=C(C_m)\otimes M_{125}
\]

とする。`C(C_m)`はsource addressのcentral block algebra、`M_125`はfinite collision fiberである。各blockでlocal instrumentを作用させ、block間はBGCE139のsource causal event permutationでsource-null linkに沿ってroutingする。

- cell collision：block-local
- routing：source-derived deterministic causal permutation
- all-to-all coupling：なし
- address refinement：child-constant pullback
- internal refinement：`A -> A tensor I_tail`
- action measure：`625^{-m}`
- time refinement：`q_m=exp[-pi 5^{-m}]`

よって

\[
\mathcal L_{m+1}[j g]\,j=j\,\mathcal L_m[g],
\qquad
625\,625^{-(m+1)}=625^{-m},
\qquad
q_{m+1}^{5}=q_m
\]

が成立する。address refinementとcollision refinementは異なるtensor factorに作用するため可換である。

## 4. CTPの因果・正値性

local recorded branchesはCP、prior-summed channelはCPTPである。central direct sum、spatial tensor product、source permutation unitary、causal compositionはいずれもCP/CPTPを保存する。BGCE326/333/336R2のprocess-tensor論法がそのまま適用できる。

- diagonal normalization：**PASS**
- branch Hermiticity：**PASS**
- largest-time cancellation：**PASS**
- source causal order上のretarded support：**PASS**
- noise quadratic form PSD：**PASS**

noiseはHermitian insertionのcovariance formであり、有限stageでPSD。direct sum、tensor product、causal compositionとfinite-dimensional norm limitでPSD coneを出ない。

## 5. 全8 sector検査

`q=e^{-pi}`、6 actual Braid labels、4 scoresについてBGCE348のoperator identityを各source cellへblock extensionした。

\[
\dot F_{{\rm raw},\alpha}=\frac12D_\alpha,
\qquad
\dot F_{{\rm Petz},\alpha}=-\frac12D_\alpha,
\]

\[
\dot F_{{\rm raw},\alpha}-\dot F_{{\rm Petz},\alpha}=D_\alpha,
\qquad
\frac12(\dot F_{{\rm raw},\alpha}+\dot F_{{\rm Petz},\alpha})=0.
\]

8 sector × 4 componentで、conditional score residualとunconditioned tangent residualはいずれも`<1e-25`だった。defect norm squaredはBGCE348と一致する。

## 6. 判定と境界

- source-derived local recorded instrument：**PASS**
- source-derived 1+3 Lorentz signature：**PASS**
- cellwise four-transfer derivative：**PASS**
- source causal local gluing：**PASS**
- address/time refinement naturality：**PASS**
- CTP causality/positivity：**PASS**
- 全8 sector：**PASS**
- MMR/CGR、Einstein target、EH/FP、手動`3/5`、係数fit：**不使用**
- `BQG-G1-R02.4`：**CLOSED_SCOPED**
- `BQG-G1-R01.5`：**ACTIVE**

未導出：full ten-component nonlinear metric parent、spatial-gradient dynamics、local total Ward、direct backreaction、long-wavelength Einstein structure、実測物理。

## 7. counter-intuition

通常の説明は、classical outcome recordを持つmetric-controlled quantum instrumentをcausal process tensorへ合成したというものである。CP closureとCTP identities自体は一般論であり、Braid固有ではない。

Braid固有なのは、source event cylinder、causal routing、Lorentz event form、raw/Petz KMS grading、`exp(-pi)` collision、4 aligned scores、4 transfer defectsが同じpointed-Braid sourceから固定される点である。

最強の反対解釈は、これはまだaligned four-scoreとblock-local fiberに限定された内部modelであり、full metric field theoryや自然界の時空ではない、というものである。この境界を維持する。

## 8. 次

`BGCE350_FINITE_SOURCE_CYLINDER_PARENT_TO_LOCAL_HISTORY_DRESSED_TOTAL_WARD_IDENTITY_GATE`

BGCE323/325のglobal history-dressed covarianceと今回のlocal parentを組み合わせ、追加のenvironment-only spatial chargeや手挿入conservation termなしに、source causal cellごとのlocal total Ward identityが閉じるかを判定する。
