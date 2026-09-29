# BGCE288 — causal-even event momentとX21R1 odd theta応答はfull Lorentz metric tangentを作るか

固定source revisionは `db378a077ff77b4e4f71ffc210721b6a6e804b63`、X21R1 cross revisionは
`269a832e497c901a2b24bb2167ca97b9e6ce2bd1`。結果前に変更しない。

BGCE287は48 actual edge-rate tangentsから10 symmetric moment componentsへの一意なBKM-horizontal right inverseを得た。
ただしconductance momentは正のcontravariant principal tensorであり、X21R1 ordered-edge Gramはcovariant positive Gramである。
Hilbert stressへ進む前にbasepointとcausal index typeを監査する。

source time reflection `J` は `Sym2` をcanonicalに

```text
J-even  : clock-clock + spatial-spatial = 7 components
J-odd   : clock-spatial                 = 3 components
```

へ分ける。次をexactに判定する。

1. 正actual conductance momentが満たす対角優位条件に、8個のX21R1 Gramまたはそのinverseが直接入るか。
2. uniform event atom weight `1/25`がBGCE256 `Q4`をexactに再現し、`J Q4=K_evt`となるか。
3. actual event momentのJ-even projectionはrank 7か。
4. 各sectorの3 X21R1 theta tangentsのJ-odd projectionはrank 3か。
5. 両者のdirect sumは各sectorでfull rank 10か。
6. この分解はsource S4 atlasでglueするか。

## 事前判定

- **FULL PASS**：direct base anchorと7+3 full tangent completionがともに成立。
- **PARTIAL PASS**：X21R1 Gramのdirect base化は失敗するが、source-fixed `Q4 -> K_evt` base上で7+3 full tangent completionが成立。
- **FAIL**：combined tangent rankが10未満、またはsource base `Q4 -> K_evt`が再現しない。

## 境界

full tangent rankはfirst-order off-shell coverageであり、それだけで有限theta積分可能性、parent action、Hilbert stress、Wardを証明しない。
数値fit・長時間走査を行わず、有理数rankとexact inequalityだけを使う。
