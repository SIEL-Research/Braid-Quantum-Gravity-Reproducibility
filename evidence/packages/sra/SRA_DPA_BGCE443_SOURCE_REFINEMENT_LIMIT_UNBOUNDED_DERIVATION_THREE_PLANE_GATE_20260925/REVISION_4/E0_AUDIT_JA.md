# BGCE443 Revision 4 — 独立 non-DPA E0 監査

## 結論

**FAIL — execution不許可。科学判定なし。**

Revision 4はR3のflag-fed witnessを明示的toy operatorへ置換し、fresh replayは保存済み
`WITNESS_RESULT.json`とbyte-exactに一致した。固定source hash、revision binding、unit-counting
設計、action-growthを使う方針、retention field、path-contained guardも大きく改善している。

しかしendpoint semantic preflightとしては三つの非補償blockerが残る。

1. 共通rank関数はrank 1をrank 2と誤判定し、single-direction controlだけ別の固定式で迂回する。
2. signed/unsigned comparatorはraw **action**差ではなくimplementer差を判定し、canonical
   unsigned tensor swapも構成しない。
3. bounded-inner negative、closability negativeとpositive closabilityは、計算結果からdecisionを
   導出せず、固定booleanまたは説明文字列をPASS判定へ使う。提示analytic boundからnonzero
   analytic radiusも導けない。

従ってpositive/negative/comparatorが同一endpoint関数を通るというE0_REQUESTの中心条件は
満たされない。本監査はfocal evaluator/source outcome、R1/R2 outcomeを作成・実行・閲覧して
いない。

## Identityと再現

- repository: `SIEL-Research/SIEL-Research-Agent`
- branch: `codex/dpa-bgce443-source-limit-20260925`
- exact freeze/HEAD: `daa6ea468d1f2c3ae6e95af4a20a1a0b1ac488f8`
- entry worktree: clean
- focal evaluator created/executed/viewed: false
- focal/source outcome accessed: false

主要artifact SHA-256:

| artifact | SHA-256 |
|---|---|
| `PROTOCOL.md` | `5fe4388d27f480c915fc9dec69820be6baed0a6eede74bff40770b7bdbe2443e` |
| `exact_witness_constructor.py` | `bfcaf6258256f116055f7edd225eb794cd3f821288996042587911c71bc8da31` |
| `WITNESS_RESULT.json` | `9407efb68a068ee591319b153f5dbbe498491bb7d83e329d075c880030597cec` |
| `CLOSABILITY_THEOREM.md` | `4a5a3cf96e0630d914ff84e2e7c174814b9dc0bffead905563a8d2b8dda0e50a` |
| `RETENTION_SCHEMA.json` | `6e6e600668de9ac706acb387cfd24ba287a37a7a298d548000eed30b883fbda3` |
| `access_guard.py` | `eda790ad8a8a8321557ccc161456ae02fd0c2be4ab0e6171c08cd433f8c30b64` |
| `INPUT_ALLOWLIST.json` | `5444e8670c226960ca284c56463ddd76a868165687bd4c200489a5b31dfb6c05` |

`exact_witness_constructor.py --output <temporary>`をfresh実行し、保存結果と`cmp`一致、同じ
SHA-256を確認した。`verify_packet.py`と登録5 guard testsもPASSし、六つのallowlisted source
hashも宣言値と一致した。

## PASSした範囲

### Revision/source binding

full freeze commitとHEADは一致する。六sourceはpath/hash boundされ、BGCE075/117のordered
`h_a` typing、OCBFH014、BGCE386をwindow coefficientにしないR3訂正、BGCE442 R2の境界は
維持されている。R1/R2とR3 E0 resultはdenylist、defaultはDENYである。

### 明示toy constructionとfresh replay

Pauli matricesからfinite implementer、commutator、normalized trace variance、3x3 minorを
実際に構成しており、R3のendpoint値直入力より本質的に改善した。positive stabilization、
variance、rank 3、action identity、zero/rank-two controlsは保存結果どおり再現する。

### Access guardの実体

absolute、traversal、unlisted、R1、R2は登録testで拒否された。監査者が`/private/tmp`内の
独立fixtureで追加したhash mismatchとsymlink testも、それぞれ`HASH_MISMATCH`、
`SYMLINK_PATH`でreturn前に拒否された。ただしproducerの`test_access_guard.py`自身には
この二testがなく、`ACCESS_GUARD_RESULT.json`の全項目は登録suiteだけからは再生できない。

## Blocking finding 1 — 共通rank endpointをsingle-directionが迂回

`three_row_rank_certificate`は3x3 minorがなければ、非zero rowが一つでもrankを常に2とする。
独立probe:

```text
three_row_rank_certificate([X, ZERO2, ZERO2])
=> {"rank": 2, "nonzero_minor": null}
```

真のrankは1である。保存single-direction controlはこの関数を使わず、
`1 if any(derivation_row(X)) else 0`で1を直接返す。zero/rank-two/rank-threeとsingle-directionが
同じrank endpointを通らず、要求された共通関数・rank-one separationを満たさない。
これは`GATE_COLLAPSE_OR_DUPLICATION`であり、保存`all_expected_separations:true`をE0 PASSに
使えない。

## Blocking finding 2 — comparatorはraw action差を計算していない

`signed_unsigned_comparator`はsigned/unsigned implementerを作るが、差として計算するのは
`||P_signed-P_unsigned||_F^2`だけである。その値を
`PASS_TOY_RAW_ACTION_DIFFERENCE`と命名しており、commutator action差を一度も構成しない。
implementerはscalar差を持っても同じinner actionを与え得るため、implementer差はaction差の
代用にならない。

独立probeではこのtoyにaction差を持つobservableが実際に存在したが、それは凍結harnessが
発見・保持・decisionに使用した証拠ではない。またtoyの「unsigned」はseedをそのままembed
するidentity transportで、protocolが指定するcanonical unsigned tensor-factor swapや同じ
adjacent wordを構成していない。よってgeneric carrierとBraid-transport specificityの二層
decisionを検証するmatched non-structural comparatorには未到達である。

## Blocking finding 3 — negative controlsとclosability/action bridge

bounded telescoping codeはtelescoping residualを計算する一方、`unbounded_action:false`と
`pass_as_outer_unbounded:false`を固定値として返し、decisionは後者を否定するだけである。
star-defect codeもdefectは計算するが`closability_endpoint_pass:false`を固定する。従って
negative interventionsはpositiveと同一のaction-growth/closability endpointを通らない。

positive action-growthはcommutator identity residualを計算するが、`action_norm=2(n-2)`と
observable normは文字列として代入され、operator norm、spectral lower bound、
`||delta_B||<=2||B||`との矛盾は実行可能certificateになっていない。toy Pauli familyではこの
等式を別途証明可能だが、現在のPASS predicateはidentity residualだけで
`bounded_inner_excluded`をtrueにする。

closability PASSもself-adjointnessとinvolutionだけで決まり、translation covariance、overlap
count、finite-volume group convergence、graph closureは説明文字列である。
`||delta^k(A)|| <= (2(m+2k))^k k! ||A||`という記載boundをpower seriesの`k!`で割ると
`(2|t|(m+2k))^k`が残るため、このbound自体から任意のnonzero analytic radiusは従わない。
標準finite-range dynamics theoremまたはexplicit commuting toy groupを使う方向は妥当だが、
現在のconstructorはそのgroup law/strong limitを構成せず、theorem hypothesisをdecisionへ
bindしていない。

## RetentionとExact-Path baseline

R4 retention key listはR3の欠落を広く埋め、source/seed、window completeness、variance両辺、
action lower bound、bounded-inner、closability、transport hash、二層decisionを要求している。
ただしこれは`required_raw_keys`の文字列listで、row schema、型、cardinality、uniqueness、
cross-field validationを持たない。focal evaluatorが未実装なので、conformance validatorと
atomic raw artifactもまだ存在しない。設計改善としてはPASS、E2再構成可能性の実証としては
UNRESOLVEDである。

non-focal constructorのpath/byte baselineはPASSしたが、intervention invariantsとprimary
endpointは上記の共通関数違反でFAILする。

```text
source_identity              PASS
path_manifest               PASS
split_manifest              NOT_APPLICABLE
baseline_intermediate       PASS (non-focal replay only)
baseline_primary            FAIL (rank/action/closability semantics)
intervention_invariants     FAIL (controls bypass common endpoints)
focal science authorized    false
```

## Evidence statusとclaim ceiling

一次statusは **Inconclusive result — implementation/provenance failure before focal execution**。
これはBGCE443科学仮説のnegative resultではない。R1 invalid、R2/R3 E0 FAIL、BGCE442有限段
NO-GOは変更しない。

将来E0 PASSでも許される最大claimは、固定sourceと宣言unit-counting familyに対する
prospective endpoint discriminating capacityである。unsigned comparatorがcarrier PASSなら
generic carrierはSCOPED PASSでも、raw actionが一致する限りBraid specificityはNO-GOである。
BGCE386 soldering、moment map、gravity、empirical calibration、RPD/Official SIEL adoptionは
導かれない。

## 最小修正

append-only Revision 5で少なくとも次を行う。

1. exact rank routineを0/1/2/3すべて同じ関数で計算し、single-directionをそこへ通す。
2. canonical unsigned tensor swapと同じwordを明示構成し、matched invariantsを検査する。
3. implementer差ではなく、固定raw observable basis上のcommutator-action hash/差を保持し、
   generic carrierとtransport specificityを別々に決定する。
4. bounded telescoping/star-defectを固定booleanでなくpositiveと同じendpoint関数へ通す。
5. action norm lower boundとbounded-inner inequality、closability theorem hypothesesまたは
   explicit group/graphを実行可能certificateにする。
6. retentionを型付きraw-row schemaとvalidatorへ変え、全negative guard testを登録suiteへ入れる。
