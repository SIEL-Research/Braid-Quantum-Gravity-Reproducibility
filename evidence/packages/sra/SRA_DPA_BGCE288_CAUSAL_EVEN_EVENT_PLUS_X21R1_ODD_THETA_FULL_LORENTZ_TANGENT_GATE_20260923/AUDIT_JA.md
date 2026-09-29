# BGCE288監査 — physical event base上の7+3 Lorentz tangent completion

## 結論

**PARTIAL PASS。** X21R1の正定値Gramそのもの、またはその逆行列をactual event conductanceのsecond momentと読む案は8 sectorすべてで棄却された。一方、physical baseをsource由来の`Q4 -> K_evt`に戻すと、event側の7成分とX21R1 theta側の3成分が相補的に働き、Lorentz metricの10個の一次変分を全sectorでexactに覆う。

- X21R1 Gramのpositive actual-event moment cone適合：0/8。
- X21R1 inverse Gramの同cone適合：0/8。
- actual eventの一様weight `1/25`：`Q4`をexact再現。
- source time reflection：`Q4`を`K_evt`へexactに写す。
- causal `J`-even event response：rank 7。
- causal `J`-odd theta response：rank 3、8/8 sector。
- direct sum：rank 10、8/8 sector。
- 既存S4 atlasでのgluing：PASS。
- fitted coefficient：なし。

従ってX21R1 Gramはphysical event metricの基底値ではない。使えるのは、その3つのtheta微分がphysical `Q4 -> K_evt` base上で欠けていたclock-space（boost）3方向を与える、という部分である。

## なぜGramそのものは使えないか

positive actual-edge conductance moment

```text
H = sum_e c_e v_e v_e^T,  c_e >= 0
```

には、各対角成分について

```text
H_ii >= sum_(j!=i) |H_ij|
```

という必要条件がある。8個のX21R1 Gramと8個のinverse Gramはすべてこの条件を破る。したがって「正定値だからactual event momentとして読める」は成立しない。

## 何を突破したか

source causal reflection `J`はsymmetric metric tangentをcanonicalに二分する。

```text
J-even = clock-clock + spatial-spatial = 7 components
J-odd  = clock-spatial                  = 3 components
```

actual event moment responseは前者をrank 7で覆い、X21R1の3 theta tangentは後者をrank 3で覆う。両者は`J`固有空間が異なるため交わらず、direct sumはexactにrank 10となる。これは8 sectorすべてで同じで、既存S4 atlasを通じてglueする。

## BGCE287への影響

BGCE287のrank、kernel、BKM horizontal liftという線形代数は保持される。ただしphysical transportとして確定したのは現時点では`J`-even event sectorである。X21R1 thetaの`J`-odd応答が有限変形へ積分できるまでは、10成分全体のnonlinear conductance functionalとは主張しない。

## stress/Wardへ残る一点

一次接空間は10成分そろった。しかしHilbert stressには、3成分のodd responseが単なる接ベクトルではなく、有限近傍のanalytic field familyへ積分でき、そのfamilyを含むsource由来parent actionが必要である。

次のBGCE289は数値走査を行わず、既存Gibbs/X21R1 analytic familyのodd Jacobianについてinverse-function条件と混合微分の可積分性をexactに判定する。通れば、BGCE285のminimal Markov/BKM parentへ接続してHilbert variationとWard identityを同じgateで問う。

## DPA反対直観

- Observed Evidence：direct-base 0/8、`Q4 -> K_evt` exact、even rank 7、odd rank 3、combined rank 10、8/8 sector、S4 glue。
- Pattern：同一pointed-Braid sourceがcausal gradingと相補的なevent/theta responseを供給する。
- Interpretive Leap：odd analytic familyがminimal parent actionへ一意に統合される可能性。未証明。
- Alternative Explanation：任意のLorentz metric tangentもcausal involutionで7+3に分かれるという一般表現論。
- Braid-specific content：`Q4`、actual event set、`K_evt`、8 X21R1 sector、3 theta directions、S4 atlasが同じsource lineageから固定される点。
- Falsifier：odd Jacobian rank低下、混合微分不整合、有限familyのmetric domain離脱、parent variation不一致。
- Confidence in Pattern：高い。
- Confidence in Interpretation：中程度。有限積分と作用は未検証。
- SIEL-generation classification：`SIEL_GUIDED_STANDARD_COMPATIBLE`。

一次証拠区分は **Theoretical derivation with direct-base no-go and full first-order causal tangent completion**。自然界の重力実証、完成した量子重力、存在論・主観・意識の実証ではない。
