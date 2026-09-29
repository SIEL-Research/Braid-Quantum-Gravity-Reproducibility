# DPA-SCOUT-BGCE495-001 scouting plan

## North-star

- **North-star claim:** BGCE490の最良`G1` actuatorを、BGCE494で実測したnative `G1/5` module countへexactに合成し、full logical actuatorのdirect uncorrected NISQ境界を最短で判定する。
- **Closest prior result:** BGCE490はdegree `29`、exact phase-matched base call `7`、合計`203` H-block queryの最良caseを与え、BGCE494は1 query内部の11-qubit `rz/sx/x/cx` native moduleを実測した。
- **Current missing link:** full actuatorを数千万gateの巨大回路として実体展開せず、query countとnative module countのexact product、必要logical width、error-free survival thresholdを閉じる。
- **Directness:** `direct exact resource composition`。

## Scope and evidence class

- Parent item: existing `BQG-G0-R01.2`; no new work-package ID。
- Gate: `BGCE495_MINIMAL_G1_CHEBYSHEV_POWER_SELECTOR_AND_FULL_ACTUATOR_NATIVE_RESOURCE_GATE`。
- Scientific layer: hardware-resource boundary for a fixed source-derived logical circuit。
- Evidence class: `Theoretical derivation` plus retained exploratory native compilation measurement。
- Zero-cost local arithmetic only。巨大full circuit、外部QPU、paid service、hardware submissionは実行しない。

## Fixed construction

- BGCE493のbest caseを変更せず使う: mask `0`, control `G1`, Chebyshev degree `29`, exact phase-matched base calls `7`, total H-block queries `203`。
- 1 H-block queryのinner native moduleはBGCE494のexact transpiled resultを使う: 11 qubits、depth `35,064`、size `69,841`、`15,844 cx`。
- native module subtotalは各native countと`203`のexact productとする。これはHermitianization control、success reflection、coefficient-address routing、phase matching、measurement、device routingを全て無料と仮定する**optimistic subtotal**であり、full compiled countとは呼ばない。
- simultaneous known-register floorは9 system + 2 source-word address + 1 encoded signal + 5 Chebyshev coefficient address = 17 qubits。BGCE493のcontroller-address subtotalを合わせたknown-width subtotalも別記する。
- independent-CX error modelで、`N_cx`回すべてがerror-freeである確率を `(1-p2)^N_cx` とする。50%および90% survivalに必要な`p2`をexact inversionで求める。single-qubit error、idle、readout、correlationを無視するため楽観的である。

## Noncompensating gates

- **A — pinned lineage:** BGCE490、491、493、494の指定artifact hashとsource commitを一致させる。
- **B — exact composition:** `7 * 29 = 203`とBGCE493のquery countを一致させ、BGCE494 native countsとのinteger productsを記録する。
- **C — fail-closed interpretation:** subtotalをfull native countや最適下限と呼ばない。巨大回路をtranspileしたと偽らない。
- **D — NISQ boundary:** 50% error-free survivalに必要なper-CX errorと、`10^-4`、`10^-5`、`10^-6`でのoptimistic survivalを報告する。

## Decision rule

- `SCOPED PASS / DIRECT UNCORRECTED NISQ NO-GO`: exact finite logical actuatorは維持されるが、wrapperを無料としたnative subtotalだけで数百万CXとなり、50% survivalにsub-micro error thresholdが必要。
- `OPEN`: source/query identityが不足しresource compositionを固定できない。
- `NO-GO`: prior exact identitiesが不整合、またはinteger compositionが再現しない。

## Claim ceiling

このscoutは、固定された最良`G1` full actuatorのmodule-preserving optimistic native subtotalとdirect uncorrected NISQ error boundaryを与える。full controlled/Hermitianized circuitの実体transpile、device-specific routing、fault tolerance、quantum advantage、現実の重力backreaction、量子重力実測を確立しない。
