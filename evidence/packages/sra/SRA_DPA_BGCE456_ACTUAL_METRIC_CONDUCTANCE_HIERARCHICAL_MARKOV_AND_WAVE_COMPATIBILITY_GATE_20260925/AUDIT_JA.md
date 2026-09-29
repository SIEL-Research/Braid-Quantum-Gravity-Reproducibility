# BGCE456 — actual-metric conductance / hierarchical Markov-wave compatibility

## 結論

**SCOPED PASS。BGCE455のanisotropic UCP障害を、actual metric由来のstrictly positive conductanceで解除した。同じoperatorが全depth UCP heatとpositive waveを生成し、spatial spectral dimension 3を保つ。一般の物理的UV完成はOPEN。**

## 1. source-derived conductance

一つのsource-clock sliceの125 childを`C5^3`とし、`x != y`の群差を一意なcentered residue

`delta(x,y) in {-2,-1,0,1,2}^3`

へ持ち上げる。BGCE455と同じactual inverse spatial metricを`A=gamma^-1`として

`c_A(x,y)=(1/5) (delta^T A delta)/(delta^T delta)`

と置く。`A`はpositive definiteなので全`125*124/2=7750` unordered edgeで`c_A>0`。`1/5`はfitではなく、isotropic limitをBGCE452へ一致させるsource normalizationである。

実際、`A=I`なら全edgeで`c_I=1/5`。従ってgraph Laplacianはoff-diagonal `-1/5`、diagonal `124/5`となり、exactに

`L_I=25(I-E0)`。

## 2. BGCE455の符号障害を解除

BGCE455でraw exterior operatorがpositive off-diagonalを持った同じpair

- `x=(0,1,2)`
- `y=(1,0,2)`

に対して、新しいoperatorは`L_A(x,y)=-c_A(x,y)<0`。全edgeが同じ符号条件を満たすため、`-L_A`はfinite-state continuous-time Markov generatorである。

axis conductanceも`chi1`と`chi2/chi3`でexactに異なり、metric anisotropyは消えていない。

## 3. 全depth refinement、UCP heat、同一operator wave

level `k`の各parent block内へ同じ125-child Laplacianを置き、

`Delta_m^A=sum_(k=1)^m 25^(k-1) L_A^(k)`

とする。新levelのoperatorはchild-constant functionを消すので

`Delta_(m+1)^A j_m=j_m Delta_m^A`

がexact。各項は非負conductance graph Laplacianなので、その和のheatは全有限depthでpositivity preserving、unital、trace preserving。internal `M_125`へのidentity liftはUCPである。

同じ`Delta_m^A`がpositive self-adjointなので、

`partial_s^2 phi + Delta_m^A phi=0`

はspectral cosine/sine waveを持つ。heat用とwave用に別operatorを置いていない。

## 4. spectral dimension 3

exact rational bound

`alpha=1/tr(gamma)`, `beta=tr(A)`

により、全方向で`alpha I <= A <= beta I`。従ってquadratic formとして

`alpha Delta_iso <= Delta_A <= beta Delta_iso`。

min-max comparisonから

`N_iso(Lambda/beta) <= N_A(Lambda) <= N_iso(Lambda/alpha)`。

BGCE452の`N_iso(Lambda)~Lambda^(3/2)`を挟むため、anisotropic carrierのspatial spectral dimensionも3。level eigenvalue bandは25倍、wave frequency bandは5倍で、hierarchical `z=1`を保つ。positive lower boundにより任意の有限次数のheat momentも`t>0`で有限。

## 判定

- actual-metric strictly positive conductance：**PASS**
- exact BGCE452 isotropic limit：**PASS**
- all-depth refinement intertwining：**PASS**
- same-operator UCP heat：**PASS**
- same-operator positive wave：**PASS**
- anisotropic spatial spectral dimension 3：**PASS by exact form comparison**
- conductance mapのsource axiomsからの一意性：**OPEN**
- active PBM metric-volume projectivity：**OPEN**
- smooth principal symbolがexactに`p^T A p`：**OPEN**
- SI traceability / empirical gravity / general physical UV：**OPEN**

MMR/CGR、目標Einstein式、Einstein--Hilbert/Fierz--Pauli作用、手動`3/5`、係数fitは使用していない。

## counter-intuition

通常の説明は、positive definite metricのdirectional Rayleigh quotientは正であり、非負conductance graphはMarkov heatとpositive waveを同時に持つ、というもの。

Braid固有なのは、保存されたactual three-character metric、`C5^3=125` child、BGCE452の`25(I-E0)` normalization、25-per-level scaling、internal collision fiber、全8 sectorを一つのcarrierへ接続した点である。

最強の反対解釈は、このconductance mapが自然であってもsource axiomsから一意と証明されておらず、finite-group Fourier symbolとsmooth inverse-metric principal symbolのexact一致も未証明なこと。従って「anisotropic hierarchical UCP bridge」は閉じたが、「smooth physical anisotropic propagator」はまだ閉じていない。

## 次

予定どおりconstraint laneへ戻り、

`BGCE443_SOURCE_REFINEMENT_LIMIT_UNBOUNDED_DERIVATION_THREE_PLANE_GATE`

を進める。
