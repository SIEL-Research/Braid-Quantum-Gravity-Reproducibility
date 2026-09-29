# BGCE466 / DPA-SCOUT-BGCE466-001 結果

## 結論

**SCOPED PASS。** Braidから有限stochastic quantum engineを構成できた。ただし、これは「元の125次元pulseがそのまま量子carrier内を動く」という主張ではない。元pulseは全8 sectorでcarrierから漏れるため、その直読みに対する判定は **NO-GO** である。

通ったのは、BGCE458-464が選んだ複素carrierとsource counting/cup内積により一意となる直交compressionを、有効Hamiltonianとして先に適用する大胆な仮説である。

```text
O_eff = B* O B
```

ここで`B`はsource cycleから得た正規化`+i`固有基底である。自由係数、pulse探索、係数fitは使っていない。

## 量子エンジン

BGCE362がすでにsourceから選んでいた次の情報を再利用した。

- generator：`G1, H1, H2, H3`
- 内部duration：`pi/3`
- `H1,H2,H3`の全6順序に対する一様law
- resetなしの逐次cycle

compression後の各順序`σ`に対してunitary `U_σ`を作り、engineを次のmixed-unitary channelとした。

```text
E(rho) = (1/6) sum_sigma U_sigma rho U_sigma^*
```

## 検査結果

全8 signed sectorと各sectorの二つの`Z2` block、合計16 blockを検査した。

- 4 generatorは全blockでHermitian
- source `Z2` gradingをexactに保存
- `G1`と各`Hi`は全blockで非可換
- 6順序はglobal phaseを除いても全blockで相異なる
- 一様混合channelは全blockでCPTPかつunital
- Kraus/Choi rankは全blockで6
- 最小commutator norm：`0.4723734930792341`
- 最小projective order separation：`0.8564596811465521`
- 最大unitary residual：`7.52e-15`

従って、これは単なるobservable一覧ではない。source由来の非可換generator、順序law、内部durationを持ち、量子状態を実際に別の量子状態へ送る有限確率engineである。

## 境界

最も強い反例は残る。元の125次元`G1/Hi`は36次元複素carrierを保存しない。従って、compressionを物理的に実装するsource actuator、Zeno制約、またはcarrier-preserving dilationは未導出である。秒単位の較正、deterministic controller、`U(18)xU(18)`万能制御、連続極限/QFT、実験確認も主張しない。

## 次

`BGCE467`で、compressionを仮説として置くのではなく、source-nativeなcarrier-preserving dilationまたはZeno mechanismとして導けるかを判定する。新しい台帳行は作らず、既存`BQG-G0-R01.2`のstrengtheningとして続ける。
