# BQGCAL-008 報告

## 結論

**SPLIT RESULT：source-pointed positive countはSCOPED PASS。既存linear Ward energyとの直接同一視はSCOPED NO-GO。**

six-label sourceのpointed identity `e`から

\[
N_1=I-|e\rangle\langle e|
=\operatorname{diag}(0,1,1,1,1,1)
\]

を作ると、これはpositive projectionであり、tail上の

\[
N_n=\sum_{k=1}^nN_1^{(k)}
\]

は加法的でspectrum`{0,1,...,n}`を持つ。したがってpointed sourceからpositive integer event countは係数なしに導出できる。

固定ancilla確率`(3/8,1/8,...,1/8)`の下では

\[
\mathbb E[N_1]=\frac58,
\qquad
\operatorname{Var}(N_1)=\frac{15}{64}.
\]

## linear energyとの直接結合が失敗する理由

BGCE310のenvironment charge `H_E`に対して

\[
\boxed{\|[N_1,H_E]\|_{\rm HS}^2=\frac19}
\]

であり、countとenergyは可換でない。

さらに

\[
\langle H_E\rangle=0
\]

だけでなく、identity sectorとnonidentity sectorへ条件付けても、それぞれのlinear energy平均はexactにzeroである。従ってnonidentity event一個あたりの非零energyをlinear chargeから得られない。

このため

\[
K=N_n
\]

をBQGCAL-007のgeometric screen numberへ直接昇格させることはできない。

## Counter-intuition scan

pointed finite alphabetからnonidentity countを作れること自体は一般的であり、Braid固有のblack-hole physicsではない。今回重要なのは、実際のsix Braid labelsでこのcountを固定したうえで、実際のconserved chargeとの関係をexactに棄却できた点である。

linear chargeがsignedかつcoherent off-diagonalであるため、positive energyは一次平均ではなく二次量にある可能性が残る。これは成功を救うための係数調整ではなく、linear first momentが対称性でzeroになることから導かれるmechanism changeである。

## 次

`BQGCAL-009_SOURCE_QUADRATIC_CHARGE_CASIMIR_AND_DIRICHLET_ENERGY_TO_SCREEN_NUMBER_AREA_LAW_GATE`

で、`H_E^2`またはsource Dirichlet formが

1. positiveか。
2. tailで加法的なenergy densityを持つか。
3. identity/nonidentity countと係数なしに結び付くか。
4. refinement-invariant `K A_0`へquasi-local energy lawを与えるか。

を判定する。

## 主張上限

pointed sourceからpositive additive integer event countを導出した。これをphysical screen number、quasi-local energy、black-hole areaへ同一視するdirect linear routeは排除した。quadratic energy、absolute radius/mass、Newton定数、entropy、Hawking physics、finite quantum black holeは未導出である。
