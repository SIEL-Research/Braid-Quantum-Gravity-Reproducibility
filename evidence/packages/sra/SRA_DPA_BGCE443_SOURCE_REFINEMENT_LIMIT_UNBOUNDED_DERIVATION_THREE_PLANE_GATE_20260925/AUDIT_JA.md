# BGCE443 — source-refinement-limit unbounded derivation three-plane

## 結論

**SCOPED PASS。固定有限algebraではinnerだった三つのsource spatial derivationが、pointed refinement極限では独立なclosable unbounded generatorになる。三本の相互bracketは共通local core上でexact zero。ただしtyped moment mapとclock-spatial first-class closureはOPENなので、`BQG-G3-R01.3`全体はACTIVE。**

## 1. BGCE442 NO-GOとの関係

BGCE442 R2は全8 sectorで

`dim HH^1(A,A)=0`

を証明した。これは有限段derivationがすべてinnerという意味であり、今回の構成も各有限段ではinnerなので矛盾しない。

違いは極限である。OCBFH014のsource-native pointed refinement

`j_n(a)=a tensor I_5`

を使い、三つのsource Fourier projector `P_chi_i`をrootから順にdisjointなtail pairへ置く。pair depth `r`のsource inverse-length weightは

`5^(2r)=25^r`。

有限段implementerを

`H_i^(m)=sum_(r=1)^m 25^r P_chi_i^(r)`

とし、`delta_i^(m)(a)=i[H_i^(m),a]`とする。

## 2. exact refinementとclosability

新しく追加したtail pairは、それ以前にsupportを持つ全observableと可換する。従って

`delta_i^(m+1) j_m = j_m delta_i^(m)`

がexact。local observableには有限個の項しか作用しないため、極限`delta_i`はdense local algebra上でwell-definedである。

compatible local automorphism

`Ad exp(i t H_i^(m))`

はUHF limit上のstrongly continuous isometric one-parameter groupへ延長する。そのgeneratorはclosedなので、local-core derivationはclosable。

一方、depth `r`のrange/kernel間partial isometryではderivation normが少なくとも`25^r`。従って極限はunboundedであり、一つのbounded limit elementによるinner derivationではない。

## 3. 三方向の独立性

source projector ranksは`[8,4,4]`、三projectorは互いにorthogonal。`M_25`上のcommutator superoperatorのHilbert--Schmidt Gram form

`G_ij=2*25*Tr(P_i P_j)-2*Tr(P_i)Tr(P_j)`

はpositive definiteでrank 3。OCBFH014も全8 sectorで`[G1,P_chi_i] != 0`をexactに保持している。

従って三本は全sectorで非自明かつ独立。

## 4. spatial anomaly

同じpairではorthogonal projector同士が可換し、異なるpairはtensor-localityで可換する。よって共通dense local core上で

`[delta_i,delta_j]=0`。

三つのspatial derivationだけのAbelian algebraにはanomalyがない。

## 判定

- source refinement intertwining：**PASS exact**
- independent spatial derivation rank：**3 / PASS all eight sectors**
- closable unbounded limit：**PASS**
- spatial common-core closure：**PASS / Abelian no anomaly**
- typed cotangent moment maps：**OPEN**
- clock-spatial mixed brackets：**OPEN**
- full finite anomaly-free constraint algebra：**OPEN**
- `BQG-G3-R01.3`：**ACTIVEのまま、spatial derivation three-planeだけCLOSED_SCOPED**

MMR/CGR、目標Einstein式、Einstein--Hilbert/Fierz--Pauli作用、手動`3/5`、係数fitは使用していない。

## counter-intuition

通常の説明は、無限tensor productでは各有限段がinnerでも、急速に重み付けしたlocal Hamiltonian列がunbounded derivation generatorを作れるという標準的機構である。

Braid固有なのは、三projector、そのrankと全sectorでのnonzero clock commutator、pointed `C5` refinement、5倍source scaleが既存sourceから固定されている点。

最強の反対解釈は、これはまだAbelian spatial derivation三本にすぎず、重力のdiffeomorphism constraintだとは証明していないこと。symplectic moment mapとclockとのmixed bracketを閉じなければconstraint完成ではない。

## 次

`BGCE457_TYPED_MOMENT_MAP_AND_CLOCK_SPATIAL_FIRST_CLASS_CLOSURE_GATE`

三derivationをcotangent moment mapへ上げ、既存source clockとのmixed bracketsをexactに判定する。
