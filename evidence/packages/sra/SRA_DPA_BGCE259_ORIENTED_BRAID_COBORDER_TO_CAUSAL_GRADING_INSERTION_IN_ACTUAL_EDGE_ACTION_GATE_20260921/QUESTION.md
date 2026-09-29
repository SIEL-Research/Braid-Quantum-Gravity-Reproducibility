# BGCE259 — oriented Braid coborderはactual edge actionへcausal gradingを挿入するか

## 固定質問

BGCE258は`K_evt=J_ray Q4`がsource-canonical Lorentz carrierになることを示したが、BGCE256の実際の
positive Umegaki edge actionが`J_ray`を選ぶ変分則は未導出だった。本gateは、既存のmarked-word
forward/inverse orientationまたはBGCE137のorientation double coverだけから、二次kinetic momentに
`J_ray`が現れるかをexactに判定する。

## 事前固定gate

1. **actual event map**：BGCE139の25-atom deterministic involutionを変更しない。
2. **forward/reverse**：forward displacement `delta=R(x)-x`、reversed edge displacement
   `delta_rev=x-R(x)`のfirst/second momentsをexact計算する。
3. **orientation-odd coborder**：forward minus reverseのfirst/second momentsを検査する。
4. **chart parity**：BGCE137の24 chart assignmentsを12 even/12 oddへ分け、各々のadjacent-crossing
   momentとparity-signed Haar momentをexact計算する。
5. **target**：得られたorientation channelがBGCE258の`K_evt=J_ray Q4`と一致するか、少なくとも
   `(3+,1-)`のnonzero rank-4 principal tensorを与えることを要求する。
6. **edge functional**：BGCE254のUmegaki scalarのBKM二次項はedge reversalで同じであることを保持する。
   高次の非対称性をprincipal kinetic signへ読み替えない。
7. **禁止**：uniform modeだけへ手動minusを置く、chart別weightをfitする、結果後に複素phaseを導入する。

## 判定

- oriented forward/reverseまたはcanonical chart parityが`K_evt`をexact生成すればaction-selection PASS。
- orientation-odd二次momentがzero、またはorientation-even positive `Q4`しか残らなければ、この経路はNO-GO。
- full marked wordがorientationを保持する事実と、quadratic edge actionがそのorientationを保持するかを分離する。
