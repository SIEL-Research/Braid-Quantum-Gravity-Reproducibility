# BGCE495 結果

## 判定

**SCOPED PASS / direct uncorrected NISQ route NO-GO。** BGCE490の最良`G1` full actuatorは有限なexact logical circuitとして維持される。しかしBGCE494で実測したinner native moduleだけを`203`回並べる楽観的subtotalで、既に`3,216,332 CX`、全native operation `14,177,723`に達する。

## Exact composition

- Chebyshev degree: `29`
- exact phase-matched base calls: `7`
- H-block query: `7 * 29 = 203`
- 1 inner module: 11 qubits、depth `35,064`、size `69,841`、`15,844 CX`
- module subtotal depth: `7,117,992`
- module subtotal size: `14,177,723`
- module subtotal CX: `3,216,332`
- known simultaneous register floor: `17` qubits
- unreported workspaceを除くknown-width subtotal: `20` qubits

このsubtotalはHermitianization control、success reflection、30-branch coefficient routing、exact phase matching、measurement、device connectivityをすべて無料とした値であり、full transpiled gate countではない。

## Error boundary

独立なper-CX error `p2`だけを残し、他の全errorを0とする最も楽観的なmodelでも、全CXがerror-freeである確率を50%以上にするには

```text
p2 <= 2.15508568727e-07
```

が必要である。90%以上には`3.27579721037e-08`以下が必要になる。

- `p2=1e-4`: log10 survival `-139.691`
- `p2=1e-5`: log10 survival `-13.968`
- `p2=1e-6`: survival `0.040102`

single-qubit、idle、readout、correlated errorを無視しているため、これは実機に有利な境界である。

## 科学的意味

量子エンジンの有限性は維持されるが、full exact actuatorをそのまま現在の未訂正QPUへ投入する経路は採らない。次は大胆な圧縮仮説として、full unitary全体ではなくBraid固有のsource spectral witnessだけを読む最小回路へ落とす。

## Counter-intuition

この結果はunrestricted global resynthesisに対する普遍的gate-count下限ではない。将来の代数的圧縮、fault-tolerant implementation、analog realizationは排除しない。一方、固定したBGCE490-494 modular constructionについてはwrapperを無料としてなお数百万CXなので、直接NISQ投入を続ける合理性はない。

## 次

`BGCE496_SOURCE_SPECTRAL_MINIMAL_WITNESS_CIRCUIT_COMPRESSION_GATE`。full actuatorを再現する代わりに、標準QM+device noiseとBraid source dynamicsを分ける最小spectral witnessを構成する。新しいwork-package IDは作らず、既存`BQG-G0-R01.2`のimplementation evidenceとして継続する。

## Claim ceiling

This establishes an exact module-preserving native resource subtotal and an optimistic independent-CX error boundary for the best fixed G1 actuator. It does not provide a full controlled-circuit transpilation, device-specific execution, a universal circuit lower bound, fault tolerance, quantum advantage, physical backreaction or quantum-gravity measurement.
