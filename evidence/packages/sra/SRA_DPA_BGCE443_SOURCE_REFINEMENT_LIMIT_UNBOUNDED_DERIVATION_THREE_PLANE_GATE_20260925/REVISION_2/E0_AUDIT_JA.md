# BGCE443 Revision 2 — 独立 non-DPA E0 監査

## 結論

**FAIL — execution不許可。科学判定なし。**

BGCE443 R2は、R1の誤った`P_chi` tail-pair endpointを明示的に失効させ、
`h_a=i[G1,P_chi_a]`、全marked position、BGCE386 sign、互換性・局所安定化・
implementer growth・rank・bounded-inner exclusion・closabilityを別々の義務として
戻した点では正しい。しかし独立E0に必要なrevision binding、source由来の係数則、
実行可能witness、非構造的control、完全なendpoint定義、raw retention、R1 outcome
隔離がまだ凍結されていない。

本監査はfocal evaluatorを作成・実行・閲覧していない。R1の`evaluate.py`と
`RESULT.json`も閲覧していない。従って本判定は実装・endpoint provenanceの
preflight FAILであり、仮説の`NO_GO`、`PASS`または`INCONCLUSIVE`ではない。

## 監査identity

- repository: `SIEL-Research/SIEL-Research-Agent`
- branch: `codex/dpa-bgce443-source-limit-20260925`
- active audited commit:
  `6ecac190414df484f86de3da375881f1259fce0a`
- declared producer revision in R2 protocol/status:
  `801238084ee43fc58a11fb213cdf9bdb530f103e`
- reviewer: independent non-DPA research auditor
- worktree at entry: clean
- focal evaluator created: false
- focal outcome accessed: false

R2 artifact hashes at the audited commit:

| artifact | SHA-256 |
|---|---|
| `REVISION_2/PROTOCOL.md` | `2cf56f93c902fbb9f8f95836aab41af30c313cae2ff40f1b154c573fe2ce57cf` |
| `REVISION_2/E0_REQUEST.md` | `36007288053ad1b20067d4b1023a1171f7d4b21e2df144769f3a35ab59ae419c` |
| pre-audit `REVISION_2/STATUS.json` | `01db5801e4ba7d63b7011f2dace1e04e4dd644ba041935edb458c3992793809d` |

## 1. Revision binding — FAIL

R2 protocolとstatusはproducer revisionを
`801238084ee43fc58a11fb213cdf9bdb530f103e`と宣言している。しかしそのcommitには
`REVISION_2/PROTOCOL.md`、`E0_REQUEST.md`、`STATUS.json`が存在しない。これら三つは
次のcommit `6ecac190414df484f86de3da375881f1259fce0a`で初めて追加された。

独立確認:

```text
git cat-file -e 801238084...:REVISION_2/PROTOCOL.md  -> exit 128, absent
git cat-file -e 6ecac1904...:REVISION_2/PROTOCOL.md  -> exit 0, present
```

従って、現packetは自身を含まないrevisionへbindされており、revision-matched E0を
発行できない。これは単なる表示上の短縮SHAではなく、実在する異なる親commitへの
bindingである。

## 2. Frozen input identity — PASS（ただしsource law完成を意味しない）

PROTOCOLに列挙された六つの参照artifactはすべて存在し、SHA-256は宣言値と一致した。

| input | verified SHA-256 |
|---|---|
| BGCE443 refinement-outer hypothesis | `ab81d9ab78eb49b1a78c0344787c014473844b7575c67905da2bce9cc0e5f3e0` |
| BGCE442 R2 result | `642dcc4b9de9518dd4b3ca3273ae38f12a16051148891c7b27b68e7d684420ff` |
| OCBFH014 certificate | `717c79fddcf2c94ed89a1c7bef19965627cad9b56e9ccd7bb3fbfa86b45f35f9` |
| OCBFH015 certificate | `adf4ef56c8f58c38703542fa09cfebac15bb976b5d629b1dcca1c59ece1ea7f4` |
| BGCE386 certificate | `4ea139eecf025b5afc66896482f8c6272d5601c22f63c687555562108fce2a9c` |
| BGCE386 result | `16fc79a1db2637eb70bdf3e535b08c93f426a68d807edadc9a650a8ca8db00e3` |

BGCE442のfinite-stage `HH^1=0`、OCBFH014/015のmarked-support transport、
BGCE386の四null-link上のHadamard one-plus-three selectorというsource boundaryは
保持されている。この入力同一性PASSは、次節の欠落した全window係数則を補わない。

## 3. `s_a(x)`のsource fidelity — FAIL

BGCE386が固定するのは四つのnull linkに対する三本の空間sign row:

```text
(+ - - +)
(+ - + -)
(+ + - -)
```

である。OCBFH014/015はmarked finite supportのBraid transportとobserver-frame
coherenceを与えるが、任意orderの各consecutive three-strand window `x`を四つの
null-link orientationのどれへ対応させるか、そのorientationをどう保持・更新するか、
またoverlapping window間でsignをどう共有するかを与えていない。

PROTOCOLの

> stored null-link orientation of each marked window

という対象は、六つの参照artifactのどこにもstored row、manifest、関数または
一意性証明として存在しない。primary hypothesis自身も
`s_a(x)`の全level extensionを一意に構成できないことを第一falsifierとしている。

従って`P_a^(n)=sum_x s_a(x) tau_x(h_a)`は現時点でsource-derivedな一意の演算子列では
ない。ここを実装者が選べば、post-source basis/係数選択になり、source specificityを
監査できない。

## 4. Endpoint discriminating capacity — FAIL

R2 directoryにはE0に必要な実行可能positive、negative、matched comparator witness、
共通harness、raw witness rowが存在しない。PROTOCOLは将来の「endpoint witness」を
参照するだけで、そのartifact path、hash、constructor、expected response、retained raw
schemaを凍結していない。

以下も未定義である。

1. `all tested adjacent orders`のexact order listまたはall-order proof route;
2. `complete frozen local-core basis`のbasis、ordering、support metadata、hash;
3. `||P_a^(n)||`のnorm種別と、有限samplingでなくunboundedを証明するexact certificate;
4. bounded-inner exclusionで量化するcompatible implementer family、uniform bound、
   同値許容範囲;
5. closabilityのdense domain、graph norm、closure witness、またはstrongly continuous
   automorphism groupのconstructor;
6. eight sectorsにおける三本のderivation rowの共通carrierとexact rank matrix;
7. compatibility residual、local stabilization、growth、rank、exclusion、closabilityを
   同一入力から非補償的に出力するschema。

六endpointを列挙しただけでは、zero、rank-deficient、bounded-inner、nonclosableと
compatible rank-three unbounded actionを実行可能に識別できない。degeneracy classは
`UNRESOLVED_SEMANTIC_CAPACITY`である。

## 5. Controls and noncompensation — FAIL

- shuffled-sign controlはexact permutationが未固定である。「witnessで選ぶ」は、
  witnessが存在しない現packetではfreezeにならない。単なる位置relabelingなら
  rank/stabilizationを保持し得るため、失敗は定義からも保証されず、source specificityを
  示すmatched rivalにもまだなっていない。
- matched non-Braid coordinate-swap rivalはmatrix/action、word set、position map、
  dimension/rank/norm matching manifestが未固定である。
- identity-tailはrefinement inclusionのvalidity controlにはなるが、Braid specificityの
  non-structural comparatorではない。
- single-direction controlは一方向だけ残せばrank oneになる構造的controlであり、
  三平面specificityを単独では証明できない。

さらに、どのcontrolもfocal endpointと同じconstructor・row schema・decision codeを
通ることを確認できるharnessがない。六primary endpointを別々にPASSさせる以外の
rescueを禁止するnoncompensation ruleは文章としてあるが、machine-enforced decision
recordがない。

## 6. Raw retention and Exact-Path Baseline Gate — FAIL / not authorized

E0_REQUESTはper-sector、per-order、per-position、per-local-basis raw rowsの保持を要求する。
しかしR2にはrow schema、manifest、path、ordering、hash、atomic preservation ruleがない。
filename/orderからsector/order/position/basisを復元する規則も未固定である。

focal evaluatorは存在せず、実行していないため、同一harnessによるpositive/negative/
comparator baselineを再現できない。Exact-Path Baseline Gateは科学結果に対してFAILを
出したのではなく、**pre-outcomeで未充足のためscience outcome access不許可**である。

```text
source_identity                  FAIL (packet revision mismatch)
path_manifest                    MISSING
split/task-order manifest        MISSING
baseline intermediate            NOT RUN
baseline primary                 NOT RUN
intervention invariants          UNRESOLVED
science_outcome_authorized       false
```

## 7. R1 leakage and tuning containment — FAIL

R1 invalidationはappend-onlyで正しく、SHA-256
`e88b6ad4a0185ee46069c3c1ef35790393817e629c134bb3733fee0ea6fe72cd`
の記録はR1を`IMPLEMENTATION_PROVENANCE_FAILURE`、科学判定なしとする。R2 protocolも
R1 resultを再利用しないと宣言している。

しかしR1 `evaluate.py`と`RESULT.json`は同じ親directoryで物理的にアクセス可能であり、
R2にはfocal constructorのallowlist、R1 denylist、isolated input root、pre-access audit log
がない。focal evaluatorが未作成なので、R1 outcomeへ到達しないことをcode上で検査する
こともできない。宣言だけではitem 7のinaccessibilityを満たさない。

本独立監査者は指定どおりR1 evaluator/resultを閲覧していない。

## Claim ceiling

本E0 FAILから科学的な正負判定は出ない。BGCE442 R2のfinite-stage NO-GOはそのまま、
BGCE443 R2は未実行、`BQG-G3-R01.3`は本監査によって完了しない。

将来R2系統がPASSしても、最大claimは宣言carrier上の三本のsource-selected、compatible、
closable、unbounded derivationに限られる。cotangent moment map、clock-spatial
first-class closure、diffeomorphism gravity、empirical gravity、RPD adoption、Official
SIEL adoptionは別gateである。

## Executionを再検討するための最小修正

新しいappend-only revisionで少なくとも次をfreezeする必要がある。

1. packet自身を含むfull source commitへのrevision binding;
2. 各order/windowのnull-link orientationと`s_a(x)`を一意に出すsource-derived mapと
   exact manifest;
3. order setまたはall-order proof、local-core basis、norm、bounded-inner exclusion、
   closability domain/certificateの完全定義;
4. exact shuffled permutationとexact coordinate-swap rival;
5. focalと同じ非結果harnessを通るpositive、zero/rank-deficient/bounded/nonclosable、
   shuffled、matched non-Braid、single-direction witnessesとraw rows;
6. 六endpointを非補償的に判定するmachine-readable decision rule;
7. per-sector/order/position/basis retention manifestとR1 artifactの実行時隔離。

これらがrevision-matched independent E0でPASSするまで、focal evaluatorの作成・実行・
閲覧は不許可である。
