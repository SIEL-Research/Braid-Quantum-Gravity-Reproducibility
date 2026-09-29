# SRA/DPA BGCE137監査 — 離散S4 chartと連続Cartan refinementの分離

## 判定

**conditional exact PASS。** BGCE136で残った二つの直接障害、すなわち`det=-1`の離散chart transitionを
infinitesimal connectionとして扱う誤りと、固定coframeを細分化して発散させる問題は、同じsource
構造の中で分離できた。

四本のBraid由来null rayへ四個の新しいC5 tail factorを対応させると、各親cellは
`5^4=625`個の子addressを持つ。等しい子と親へのexact coarseningを同時に要求すれば、

\[
E_i^{(m+1)}=\frac{1}{5}E_i^{(m)}
\]

が一意である。一段・二段のcoarsening、S4 overlap、向きのparity、UTC1--3は全てexactに通る。
ただしC5 diagonal digitを物理的な局所event addressと読む部分は、まだsourceから強制されていない。

## 1. 「4次元を先に置く」は外れた

旧CE1Dでは、四本のfactorを`clock + 3 spatial`の順に並べる外部選択が残っていた。今回は四という
数を、target-freeなV4 carrier上ですでに導出された四本の独立null rayから取る。四個のtail factorを
四本のrayへ割り当てる方法は24通りあるが、それらは一つのS4 gauge orbitを成す。従って特定の
「時間を一番目に置き、空間を二番目以降に置く」順序は物理ではない。

さらにA4で商を取ると24 assignmentは12個ずつの二つのorbitへ分かれ、S4の符号写像

\[
\operatorname{sign}:S_4\to\mathbb Z_2
\]

がorientationの二重被覆を与える。軸数、軸順序のgauge性、向きの二sheetは、ambient `R^4`を
先に置かずに得られる。したがって数理的な意味での「客観的4次元空間の密輸」はこの段階ではない。

ただし、これだけで四次元の物理時空が経験的に実在すると証明したわけではない。C5 cylinderの
addressをlocal eventとして物理的に読む条件は残る。

## 2. 離散chart transitionと連続connectionを分けた

BGCE136の個々の隣接交換は`det=-1`なので、実matrix exponentialでnear-identity connectionへ
近づけられない。BGCE137ではこれらを定数S4 chart transitionとしてatlas側に置く。overlap上で
transitionは定数なので、その微分項はzeroである。

連続connection側にはS4-uniformなidentity componentだけを置く。このanchorではconnection density
はzeroで、24個のidentity-connection overlap checkと576個のray covariance checkをexactに通過する。
離散parityと連続connectionを混同しないgraded factorizationが成立した。

## 3. 五進細分化が発散を消す

stage `m`でmeshを`h_m=5^{-m}`とし、各ray coframeを`E_i^{(m)}=h_m E_i^{(0)}`とする。
するとnormalized ray densityは全stageで

\[
3e_0,\;3e_1,\;3e_2,\;3e_3
\]

のまま、temporal densityは`(3,3,3,3)`のままである。四次元cell volumeはstageごとに
`1/5^4=1/625`となる。BGCE136の`36*25^m`発散は、同じ固定stepを全stageへ複製したことによる
ものであり、projective child ruleでは起こらない。

四方向それぞれに一個のC5 digitを使うため、一epochのchild数は625である。これは長時間simulation
で見つけた係数ではない。四本のsource-derived rayとC5 factor dimensionから直接決まる。

## 4. UTCで閉じた範囲

- UTC1: identity transportのlog branchはzeroでexact PASS。
- UTC2: normalized anchorの一階・二階差分は全stageでzero。
- UTC3: 一段5-childおよび二段25-grandchildの各ray coarseningはexact。

従って**flatで一定なon-shell Cartan anchor**について、uniform continuum admissibilityは条件付きで
閉じた。条件は、source-labelled C5 diagonal digitを四本のnull rayに沿うchild addressと解釈すること
である。

## 5. 何がまだ重力場ではないか

今回のanchorはflatかつ一定である。BGCE099のPalatini variationが必要とするのは、その一点だけで
なく、openな`C2` metric-affine field domainと、独立でcompact supportを持つ`delta e`、`delta Gamma`
である。tensor tailが増えるだけでは、diagonal digitが物理的位置になることも、任意の非平坦場が
生成されることも従わない。

したがって「UTC anchorを得た」から「Einstein方程式を無条件に変分導出した」への昇格は禁止する。
標準的説明では、これはnull tetradで書いたS4-equivariantな五進cell refinementとorientation local
systemである。SIEL固有の解釈候補は、その四方向とchart labelの交換可能性が、外部座標ではなく
関係的なBraid carrierから来る点にある。

## 6. CGR/MMRへの影響

CGRから次を外せる。

1. 離散S4 transitionと連続identity-component connectionを分離する条項。
2. `E_child=O(h)`かつprojectiveにcoarsenするon-shell UTC anchorの条項。ただしdiagonal-address解釈付き。
3. 物理的に固定された`clock + 3 spatial` factor order。

CGR全体はまだ外れない。残差は一つへ圧縮される。

> `SOURCE_CYLINDER_CARTAN_COMPLETION` law：S4で商を取ったsource-diagonal cylinder addressを
> local eventとして物理的に解釈し、exact anchor familyを、独立なcompactly-supported variationを
> 持つopen `C2` metric-affine field domainへcompletionする。

MMRには変化がない。

## Claim ceiling

BGCE137はambient `R4`や物理的に固定した1+3 factor orderなしに、S4-equivariantな五進細分化と
一定on-shell UTC Cartan anchorを条件付きで導出する。diagonal C5 digitの物理的位置意味、open
off-shell field domain、compactly-supported first variation、CGR全体、MMR、無条件Einstein方程式、
経験的重力、存在論、主観、意識は導出しない。

## 次

`BGCE138_SOURCE_CYLINDER_DIAGONAL_LOCALIZATION_AND_MINIMAL_SMOOTH_CARTAN_COMPLETION_GATE`。

C5 diagonal cylinderをlocal eventとして読むことがsource自身から選ばれるか、またflat anchorの周囲に
必要最小限のsmooth off-shell completionを与えられるかを、二つを混ぜずに最短経路で検査する。
