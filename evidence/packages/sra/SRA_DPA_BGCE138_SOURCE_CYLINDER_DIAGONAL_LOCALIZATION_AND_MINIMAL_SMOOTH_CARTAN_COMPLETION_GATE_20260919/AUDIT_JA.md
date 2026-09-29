# SRA/DPA BGCE138監査 — source spectral cylinder局在とminimal smooth Cartan completion

## 判定

**exact PASS。ただし物理event同定だけを明示的に残す。**

BGCE137で残った`SOURCE_CYLINDER_CARTAN_COMPLETION`のうち、次の二つは閉じた。

1. C5上のどのMASAを位置addressに使うか。
2. flat anchorの周囲にopen `C2` metric-affine field domainと独立compact-support変分が存在するか。

一方、得られたGelfand点を自然界の局所eventそのものと同定することは、数学だけからは従わない。
従ってCGRを無条件に「除去済み」とはしない。残余は`SPECTRAL_EVENT_IDENTIFICATION`一項である。

## 1. 任意のdiagonal MASAではなくなった

CE1Dは`M5`のsource-labelled diagonal MASAを使ったが、BIGTだけではその選択は一意でないと明記して
いた。BGCE138は後続のUB443で既に得られていたsource-native marker

\[
L=\operatorname{Tr}_2[(J\otimes I)F(J\otimes I)HR]
\]

を使う。actual 8 signed sectorすべてで、`L`はreal symmetricかつsimple spectrum

\[
-7,-5,-4,-1,7
\]

を持つ。各固有値のprojectorは

\[
P_\lambda=\prod_{\nu\ne\lambda}\frac{L-\nu I}{\lambda-\nu}
\]

でbasis choiceなしに定まり、rank one、相互直交、和がidentityである。

さらにcommutator map `X -> LX-XL`を有理数消去すると、全8 sectorでrank 20、従ってcommutantの
dimensionは5である。五個の`P_lambda`が既に五次元可換代数を張るため、

\[
C^*(L)=\operatorname{span}\{P_{-7},P_{-5},P_{-4},P_{-1},P_7\}
\]

は自分自身のcommutantに等しいMASAである。

typed basisを`S`で変えると`L -> SLS^T`、`P_lambda -> SP_lambda S^T`となる。固有値labelは不変で
ある。従ってこれはcomputational basisの対角代数を外から選んだものではない。

## 2. digit順序もmarkerが与える

五固有値の大小順に

```text
-7 -> 0, -5 -> 1, -4 -> 2, -1 -> 3, 7 -> 4
```

と置ける。この順序はbasis順序ではなく、source markerのsimple eigenvalue順序である。従ってCE1Dで
暗黙に使った`0,1,2,3,4`は、ここでは外部labelではない。

四本のBGCE136 null rayへ四個のspectral digitを対応させると、一epochのatom数は

\[
5^4=625
\]

である。親addressから新しい四digitを落とす写像がcoarseningであり、代数側では
`f -> f tensor 1_(5^4)`である。stage `m`のcylinder数は`625^m=5^(4m)`、meshは`5^-m`。

四方向を並べる24通りは全てS4で移り合う。625 cellに対する全24 permutation、計15,000件で集合
covarianceをexact確認した。固定されたclock-first factor orderは使っていない。

## 3. 連続四次元base

固有値のrankをdigitとして、各null ray `a`へ

\[
x^a(\omega)=\sum_{j\ge1}\operatorname{rank}(\lambda_{j,a})5^{-j}
\]

を定義する。同じ四つの実数極限を持つaddressだけを同一視する。非単射性は有限5進展開と末尾4の
反復が表す同じ境界点だけなので、商空間は

\[
[0,1]^4
\]

となる。四という数は外部`R4`からでなく四本のsource null rayから、五進digitはsource markerから
来る。ここまでがbasis-freeな**数学的局在**である。

## 4. open off-shell domainを明示構成した

内部cube `Q=(0,1)^4`上で、BGCE137のnormalized anchorを

\[
e_*=3I_4,\qquad \Gamma_*=0
\]

とする。各coframe成分の摂動をentrywiseで`|delta e|<1/2`に取ると、各行について

\[
3-\frac12=\frac52>\frac32=3\times\frac12
\]

なのでstrict diagonal dominanceによりcoframeは非退化のままである。従ってanchorはopenな
nondegenerate `C2` field domainの内部点である。

compact supportを持つ明示的な`C2` bumpとして、

\[
b(t)=
\begin{cases}
(t-\tfrac14)^3(\tfrac34-t)^3,&\tfrac14\le t\le\tfrac34,\\
0,&\text{otherwise},
\end{cases}
\qquad
\beta(x)=\prod_{a=0}^3b(x^a)
\]

を使える。境界で値・一階・二階微分がzeroなのでzero extensionは`C2`である。`beta`を各basis
componentへ掛けることで、coframeの16成分と`GL4` connection one-formの64成分を独立に変分できる。

この非一意性は欠陥ではない。off-shell domainは独立変分を含まなければならず、どのfieldがon-shell
になるかは作用とEuler方程式が選ぶ。

## 5. UTCへの接続

continuum fieldから五進edge dataを

\[
E_{edge}=\int_{edge}e,
\qquad
U_{edge}=\mathcal P\exp\int_{edge}\Gamma
\]

で定義する。

- coframe parentは五child積分の和にexact一致。
- connection parentは五child holonomyのordered productにexact一致。
- bounded `C2` connectionは十分細かいstageで共通near-identity log branchを持つ。
- `C2` boundが一階・二階five-adic differenceを一様に抑える。

従ってUTC1--3を満たすminimal smooth discretizationが存在する。新しいtarget係数や連続fitはない。
ただしこれはsourceが一つの非平坦fieldを力学的に選んだという主張ではなく、BGCE099の変分に必要な
configuration spaceを明示したものである。

## 6. Einstein導出への効果

source spectral cylinderをlocal event baseとして受け入れるなら、BGCE099の真空Palatini first
variationに必要な数学的条件は揃う。

```text
source marker MASA
  -> S4-equivariant spectral [0,1]^4
  -> open C2 metric-affine fields
  -> compactly supported independent variations
  -> BGCE099 conditional vacuum Einstein equation
```

従って旧CGRの**formal mathematical completion**は、`SPECTRAL_EVENT_IDENTIFICATION`だけに条件付けて
閉じる。しかし「marker outcomeが内部modeではなく物理的spacetime eventである」という同定はまだ
導出されていない。UB469は同じmarker distributionにoperational Fisher distanceを与えるが、独立な
natural spacetime responseは未測定だと明記している。

## 7. CGR/MMR

CGRを無条件には除去しない。残る一項は次である。

> `SPECTRAL_EVENT_IDENTIFICATION`：source-marker cylinder/Gelfand点と、そのcausal affine transitionを、
> 内部の識別可能modeだけでなく物理的local eventとして同定する。

MMRには変化がない。従って物質付き`G=(3/5)T`のBraid-only導出はまだ成立しない。

## Counter-intuition / claim ceiling

simple-spectrum operatorがMASAを生成すること、base-five inverse limit、open `C2` field spaceは標準数学
でも説明できる。Braid固有部分は、marker、五label、四null ray、S4 transportが同一source provenance
から出る点に限られる。

BGCE138はsource-selected C5 MASA、S4-equivariantな四次元spectral cylinder quotient、独立compact
variationを持つopen `C2` metric-affine configuration spaceを導出する。自然界のevent同定、MMR、
無条件Braid-only Einstein方程式、経験的重力、存在論、主観、意識は導出しない。

## 次

`BGCE139_SOURCE_SPECTRAL_CYLINDER_OPERATIONAL_EVENT_IDENTIFICATION_GATE`。

UB469のmarker outcome readout、BGCE135のcausal transition、OCBFH014のrefinementを同じcylinder上で
結び、eventを「再現可能に読み出せ、隣接介入で変化し、単なるbasis relabelingではない局所記録」として
operationalizeできるかを最優先で検査する。
