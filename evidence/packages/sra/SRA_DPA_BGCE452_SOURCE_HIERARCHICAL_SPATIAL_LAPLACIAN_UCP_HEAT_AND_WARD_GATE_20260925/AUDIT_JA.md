# BGCE452 — hierarchical spatial Laplacian UV theorem

## 結論

**SCOPED PASS。fundamental source-cylinder UV completionを閉じた。**

BGCE451のnearest-neighbor Laplacianは既存child-constant embeddingと可換しなかった。そこでembeddingを変更せず、既存のuniform child conditional expectationそのものからhierarchical generatorを構成した。

source clockで一時刻を固定すると空間child数は`5^3=125`。level `k`までのcylinder functionsへのconditional expectationを`E_k`、detail projectorを

`D_k=E_k-E_(k-1)`

とする。すると

`Delta_m=sum_(k=1)^m 25^k D_k`

は正で、`25^k=(5^-k)^-2`はsource cell spacingのinverse-squareである。

## exact refinementとUCP

新detailはcoarse child-constant functionを消すので

`Delta_(m+1) j_m = j_m Delta_m`

がexactに成立する。heat mapも全`m,t`でintertwineする。

`a_k=exp(-t25^k)`とすると

`H_(m,t)=a_m I+(1-a_1)E_0+sum_(k=1)^(m-1)(a_k-a_(k+1))E_k`

である。係数は非負で総和1、各`E_k`はUCP conditional expectationなので、`H_(m,t)`は全depthでUCP・trace preserving・cb norm 1である。

## spectral dimension 3とUV有限性

level `k`の固有値とmultiplicityはexactに

`lambda_k=25^k`,

`mu_k=124*125^(k-1)`

である。累積mode数は

`N(lambda_k)=125^k=(25^k)^(3/2)=lambda_k^(3/2)`

となり、spatial spectral dimensionは**exact 3**。

任意の` t>0`と有限次数`r`について

`sum_k mu_k (1+lambda_k)^r exp(-t lambda_k)`

は収束する。従って有限次数の全polynomial composite momentは、同じ一つのsource heat carrierでUV有限になる。momentごとのcounterterm fitやmomentum cutoffは不要である。

## Ward

generatorは

`Delta_m=25(I-E_0)+sum_(k=1)^(m-1)(25^(k+1)-25^k)(I-E_k)`

とも書ける。各項は同じparent block内の平均化currentで、block totalはexact zero。内部collision mapとも可換するため、BGCE350のsystem＋environment Ward telescopeはuniform source measure上で保持される。

## 残る物理境界

これはsmooth nearest-neighbor空間でなくhierarchical/ultrametricなfundamental source spaceである。未完なのは次である。

- dimensionful physical heat rate
- actual metric volumeでweightしたconditional expectation
- 同じLorentzian parent作用からのHilbert stress
- metric-weighted local Ward
- smooth-spacetime propagatorと経験的重力

従って「一般のsmooth-spacetime物理UV完成」はまだOPENだが、**Braid source-cylinder自身をfundamental carrierとする非摂動UV completion**は宣言範囲で閉じた。

次は`BGCE453_ACTUAL_METRIC_WEIGHTED_HIERARCHICAL_HEAT_HILBERT_STRESS_AND_LORENTZIAN_WARD_GATE`。

MMR/CGR、目標Einstein式、Einstein–Hilbert/Fierz–Pauli作用、手動`3/5`、係数fitは使用していない。DPA理論監査なのでE0/E1/E2は発行しない。
