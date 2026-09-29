# BGCE443 Revision 1 incident audit

## 結論

**IMPLEMENTATION_PROVENANCE_FAILURE。科学判定なし。**

commit `dd3ac837c`のBGCE443 R1 `SCOPED PASS`は無効である。結果artifactは削除・上書きせず保存し、`INVALIDATION.json`でappend-onlyに失効させる。

## Expected behavior

既存のprimary specification

`outputs/discovery-partner/DPA_BGCE443_REFINEMENT_OUTER_SPACETIME_HYPOTHESIS_20260925_JA.md`

を先に読み、次をprospective packetへ固定してから判定する必要があった。

- local seeds `h_a=i[G1,P_chi_a]`;
- BGCE386 null-tetrad sign transport `s_a(x)`;
- all marked positionsの列挙規則;
- fixed local core上のcompatibility residual;
- norm growthとlocal stabilizationの分離endpoint;
- identity-tail、shuffled-sign、matched non-Braid、single-direction controls;
- PASS後に限るmoment-map / clock-bracket gate。

## Actual behavior and first divergence

R1はprimary specificationを検索・閲覧せず、最初の`QUESTION.md`から別のendpointを定義した。

- seedを`i[G1,P_chi_a]`でなく`P_chi_a`とした;
- all marked positionsでなくdisjoint tail pairsだけを使った;
- null-tetrad signsを使わなかった;
- required controlsを実行しなかった;
- 未固定の`25^r` weightingから直接PASSを記録した。

first divergent artifactは`QUESTION.md`、そのSHA-256は`cd0f939242902312b8c245e46e2153602496c0b087f9ab4ee65bd540211e1af3`。

## Causal chain

`BGCE443` primary specificationを未検索

→ 正式seed・sign・position・control obligationsを認識しない

→ 別のtail-pair projector問題を設計

→ その別問題のexact algebraをBGCE443 endpointとして解釈

→ 無効なSCOPED PASSをcommitしstable台帳へ反映。

## Evidence for and against process causation

プロセス因果を支持する証拠は、DPA source-orderがprimary materialの再読を要求し、既存memoがrequired prospective testを明記していたのに実行されなかったこと。

Research OS ruleの欠落を支持する証拠はない。規則と仕様は明確に存在した。従ってprimary classは`RESEARCH_PROCESS_DEFECT`ではなく`IMPLEMENTATION_PROVENANCE_FAILURE`。

## Scientific impact and containment

- R1 PASS：**INVALID / NON-SCIENTIFIC**
- BGCE442 R2 NO-GO：変更なし
- `BQG-G3-R01.3`：ACTIVE
- BGCE443：Revision 2のprospective packetから再開
- process policy変更：不要

invalid runを消去せず、新しいRevision 2だけが将来の科学判定を持ち得る。
