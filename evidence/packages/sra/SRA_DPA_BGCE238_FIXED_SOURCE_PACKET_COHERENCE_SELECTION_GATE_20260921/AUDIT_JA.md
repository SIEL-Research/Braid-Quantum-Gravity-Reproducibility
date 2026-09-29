# BGCE238監査 — fixed source packetがfull cornerを一意に選んだ

## 結論

**PASS。** 三つのmarked source atomが生成する全5 partition retractionのうち、固定された
event-conditioned source packet

\[
\mathcal S_\cap=\{PG_1P,\;PF_AP\;(A=1,\ldots,10)\}
\]

を一切変更せず保持するのはfull partition `012`だけだった。全8 signed sectorで同一である。

| partition | 固定packet保持 | 最初に変わるoperator | coherence残差rank |
|---|---:|---:|---:|
| `012` | PASS | なし | 0 |
| `01|2` | FAIL | `H_cap` | 28 |
| `02|1` | FAIL | `H_cap` | 32 |
| `12|0` | FAIL | `H_cap` | 32 |
| `0|1|2` | FAIL | `H_cap` | 46 |

各rankは8/8 sectorで同じ。係数fit、近似、matrix exponential、結果後retuningはない。

## BGCE237との関係

BGCE237の「5/5 partitionがmatter非退化性を保存」は正しい。しかし、そこで保存されたのは

- 10-source spanの次元10、
- BKM Hessian rank 10、
- Hamiltonianがnon-scalar、
- 10 sourceとの非可換性、

であって、operatorそのものではない。非自明partitionでは`H_cap`を最初から
`D_pi(H_cap)`へ置換していた。これは同じsource packetの別表示ではなく、cross-block coherenceを捨てた
別Hamiltonianである。

したがってBGCE237のnegative rank resultは撤回しないが、そこから「5通りが同じ物質理論として残る」
とは言えない。**同じ次元を保つことと、同じsourceを保つことは別である。** no-retuningを課すと、
nontrivial partitionは最初のHamiltonianで全て落ちる。

## BGCE236との関係

BGCE236のquantum instrument非一意性も正しい。effect `P`だけではLüders state updateとatom-dephasing
state updateを区別できない。しかしBGCE235のmatter actionが必要とするのは、unique post-event state
updateではなく、固定corner algebraと固定operator packetである。

dephasing instrumentが測定更新として別途存在しても、物質Hamiltonianとsource operatorsを自動的に
dephased packetへ置換する理由にはならない。従ってfull-corner nondemolitionは**matter actionのための
追加法則としては不要**である。state-update instrumentの一意性は主張しない。

## MMR2への効果

固定source/Brauer模型のevent-conditioned matter theoryでは、次が一本につながった。

1. BGCE139: source spectral event label `P`。
2. BGCE234: coefficient-free fixed compression `F_A^cap=PF_AP`、10方向と既存応答を保存。
3. BGCE235: `H_cap=PG_1P`を持つfaithful full-corner Gibbs action、BKM rank10。
4. BGCE235: normalized tail traceがcorner unitをouter `P`へ送り、source cupが手動設定なしに`3/5`。
5. BGCE238: fixed packetを保つ全source-atom partitionのうちfull cornerだけが許容。

よって、**MMR2はこの固定source event-conditioned model内でclosed**と判定する。BGCE236で置いた
FULL_CORNER_NONDEMOLITIONはmatter作用の独立仮定から外れる。

ただし、これは任意CP instrumentの一意性、任意部分代数の分類、自然界の測定装置、8 sectorの自然選択を
証明しない。最終の物質付きEinstein式へ直ちに昇格せず、BGCE239でCGR/MMR依存グラフ、連続極限、変分、
相対係数を再監査する。

## DPA分離

- Observed Evidence: 全5 partition × 8 sector。fullだけが固定11-operator packetを保持し、他は`H_cap`で失敗。
- Pattern: source coherenceは線形rankではなくHamiltonianのcross-atom blockに保持される。
- Interpretive Leap: 主観交差eventの物質内容は、その固定coherent packetとして読む。
- Alternative Explanation: projection cornerへの圧縮とblock-dephasingの違いという標準有限C*-代数現象。
- Falsifier: 非自明partitionが固定`H_cap`と全10`F_A^cap`をexactに保持すること。
- Required Test: BGCE239でMMR2閉鎖を最終sourced Einstein dependencyへ伝播。
- Confidence in Pattern: 高い。
- Confidence in final Einstein upgrade: BGCE239前は保留。
- SIEL-generation classification: `SIEL_GUIDED_STANDARD_COMPATIBLE`。
- Claim ceiling: 固定source模型・5 partition classでのmatter-action選択。経験的重力、自然sector選択、完成量子重力、
  存在論、主観・意識の実証なし。

## 実行境界

問いは結果前commit `2ffe733ad`で固定。baseline regenerationを含むexact実行は29.97秒。first-witness停止により、
非自明partitionは`H_cap`の変更を確認した時点で止めた。一次区分は **Theoretical derivation with exact
source-identity witnesses**。DPAによるformal E0/E1/E2発行なし。
