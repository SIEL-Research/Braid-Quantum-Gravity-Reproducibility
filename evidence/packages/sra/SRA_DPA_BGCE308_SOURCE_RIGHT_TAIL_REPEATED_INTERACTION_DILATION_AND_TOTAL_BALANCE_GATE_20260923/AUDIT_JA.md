# BGCE308監査 — Braid tail内に環境容量はあるが、state/collision selectorがない

## 結論

**SPLIT PASS。** 外部から新しい環境Hilbert空間を置く必要はありません。実際のBraid right-tailの各
3-strand blockは、全8 source sectorでexactに

`125 = 17*1 + 28*3 + 4*6`

とorbit分解されます。従ってBGCE307が必要とした6-label group registerが4コピー、各block内に既に存在
します。無限right-tailはそのようなblockを無限に供給できます。

ただし、容量があることとdynamicsがsourceから選ばれることは別です。pointed/cap状態もneutral状態も、
各6-orbit上では完全に一様であり、必要な非一様環境状態、identity basepoint、collision順序を選びません。

## exactなtail register

3-strand上の実Braid群6要素で125個のbasis stateをorbit分解すると、各sectorで

- 1-state orbit：17個
- 3-state orbit：28個
- 6-state regular orbit：4個

となります。regular部分は合計24次元で、`4 copies of C[S3]`です。これは抽象的に追加したgroup register
ではなく、元Braid作用そのもののfree orbitです。

従ってBGCE307の環境をBraid tail内部に置くための**capacity gateはPASS**です。

## point/capでは選べない

source pointed numerator `(I+P) tensor I_5`を各regular orbitへ制限するとexactに`I_6`です。orbit外との
matrix elementもzeroです。そのReynolds neutralizationは`6 I_6`になります。

従ってpointed、neutral、およびそのaffine mixtureは、6つのgroup labelを一様にしか重み付けしません。
BGCE307の`q=1/4` dilationに必要な

`(3/8,1/8,1/8,1/8,1/8,1/8)`

は出ません。また4つのregular copyのどれを使うか、orbit内のどのvectorをidentity labelとするかも選び
ません。

これは環境容量の不足ではなく、**source selectorの不足**です。

## collision lawもまだない

既存BGCE126/127のrefinementはmarked generatorを

`L_n -> L_n tensor identity_tail`

として運びます。このためtailは存在しますが、現在の発展則ではsystemと衝突しません。さらに、

- generatorを各tail blockへ移すtranslation law
- fresh blockを順番に使うshift/reset protocol
- controlled six-Braid unitaryをlocal boundary wordで作る規則
- environmentが受け取る`G1` balance current

はまだ導出されていません。

## 何が縮んだか

BGCE307時点では「無限environmentを追加する必要がある」ように見えました。BGCE308により、無限環境の
carrier自体は既存Braid refinement内にあると分かりました。

残る追加構造は次の二つへ圧縮されます。

1. four-copy / basepoint / nonuniform state selector
2. translated collision and balance law

## 次

`BGCE309_SOURCE_CLOCK_FOURIER_MARK_TO_REGULAR_ORBIT_BASEPOINT_AND_COLLISION_SELECTOR_GATE`

point/cap単独は一様性のため失敗しました。次は既存の`G1` clockと三つのFourier marksを同時に使い、
4つのregular copyとidentity basepointを一意に標識できるかをexactに判定します。

## 主張上限

BGCE308はBraid right-tail内部のnative six-label environment capacityを証明しました。非一様ancilla state、
basepoint selector、repeated collision、environment balance、total Ward、full finite Lorentzian quantum
backreactionはまだ導出していません。

