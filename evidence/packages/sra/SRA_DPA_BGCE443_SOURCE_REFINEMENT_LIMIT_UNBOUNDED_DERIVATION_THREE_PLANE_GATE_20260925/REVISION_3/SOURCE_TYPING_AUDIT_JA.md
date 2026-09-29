# BGCE443 Revision 3 — source typing訂正監査

日付: 2026-09-25

## 結論

**NO-GO（Revision 2の係数型と隣接order互換条件） / OPEN（Revision 3のunit-counting極限derivation）**。

これはBGCE443仮説全体の科学的NO-GOではない。Revision 2を実行不能にした二つの
型エラーをsourceから切り分け、次のprospective packetで許される構成を一つに限定する。
focal evaluatorは作成・実行しておらず、focal outcomeも閲覧していない。

## 固定入力

| artifact | SHA-256 | 使う事実 |
|---|---|---|
| `audits/SRA_DPA_BGCE075_MIXED_BRACKET_TO_TEMPORAL_METRIC_VECTOR_RANK_GATE_20260919/RESULT.json` | `caefe2267222eb37db4027994a96d6302b09ad95f0d032f5eb9be262650a70b0` | ordered `[G1,P_chi_a]`からordered `(g01,g02,g03)`へのexact rank-three map |
| `audits/SRA_DPA_BGCE117_G1_KMS_TO_UB484_DYNAMICAL_KMS_TYPING_GATE_20260919/RESULT.json` | `1f70e356863d4910e4c4d945b328eda7a1c80056df2ff1dcad528cc503ee741f` | `H_a=-i[G1,P_chi_a]`の時間反転odd性と全stage rank-three transport |
| `projects/active/discovery_partner/formal_checks/ocbfh014_source_native_refinement_naturality_certificate_v1.json` | `717c79fddcf2c94ed89a1c7bef19965627cad9b56e9ccd7bb3fbfa86b45f35f9` | `j_n(A)=A tensor I_5`、marked finite supportのword-independent Braid transport |
| `audits/SRA_DPA_BGCE386_SOURCE_NULL_TETRAD_INCIDENCE_THREE_SPATIAL_GENERATOR_GATE_20260924/CERTIFICATE.json` | `4ea139eecf025b5afc66896482f8c6272d5601c22f63c687555562108fce2a9c` | Hadamard rowsは四つのnull linkを一つのtemporalと三つのspatial incidenceへ組み合わせる |

## 1. Revision 2の`s_a(x)`はill-typed

BGCE386のHadamard selector

```text
(+ + + +)
(+ - - +)
(+ - + -)
(+ + - -)
```

の列indexは、各cellの四つのnull linkである。OCBFH014のposition `x`は、pointed
tensor tower上のconsecutive marked three-strand windowである。この二つは異なる型で、
固定sourceには写像

```text
q_n : refinement window x -> local null-link label ell in {0,1,2,3}
```

がない。従ってRevision 2の

```text
s_a(x)=W[a,q_n(x)]
```

は定義されず、実装者が周期、orientationまたはwindow labelを選べばsource外の係数
選択になる。Hadamard rowsをrefinement-window weightsとして使うrouteはNO-GOである。

BGCE386を正しく使うには、各windowに四つのlink-local seed `k_ell(x)`を持たせて
`sum_ell W[a,ell] k_ell(x)`を作る必要がある。しかし現在のsourceは
`h_a=i[G1,P_chi_a]`という三つのseedしか与えず、四つの`k_ell`とのtyped solderを
与えていない。このsolderを次のpacketで暗黙に作ってはならない。

## 2. Revision 2のadjacent-order exact compatibilityは極限derivationの条件ではない

order `n`の全consecutive windowを足す有限volume implementerを`P_a^(n)`とする。
右へ一strand追加すると新しい右境界windowが生じる。そのwindowは、`A`が旧orderの
右端までsupportを持つ場合、`j_n(A)`と一般に可換でない。従って全`A in A_n`について

```text
delta_a^(n+1)(j_n(A)) = j_n(delta_a^(n)(A))
```

を毎隣接orderで要求するのは、全position局所和と両立しない。

quasi-local極限で必要なのはeventual local stabilizationである。supportが最初の`m`
strandに含まれる`A`について、右境界がinteraction rangeだけ離れた後は、新しく加わる
windowが`A`とdisjointになり、

```text
delta_a(A)=eventual_constant_n i[P_a^(n),A]
```

が定義できる。Revision 3はこのall-order theoremをprimary endpointとし、誤った
全`A_n` adjacent intertwiningを撤回する。

## 3. Revision 3で許す一意なsource law

三方向のlocal seedを

```text
h_a=i[G1,P_chi_a],  a=1,2,3
```

とする。方向labelはdimension matchingではなく、BGCE075が固定したordered
`[G1,P_chi_a] -> (g01,g02,g03)` exact rank-three mapと、BGCE117の全stage transportに
bindする。

order `n>=3`のwindow setを`X_n={0,...,n-3}`、OCBFH014のword-independent transportを
`tau_x`とし、pointed window setのcounting measureだけで

```text
P_a^(n)=sum_{x in X_n} tau_x(h_a)
```

と定義する。全windowの係数はexactly oneであり、fit、周期符号、`25^r`、manual `3/5`、
post-outcome normalizationを使わない。

BGCE386はこの和の係数源には使わない。Revision 3が三本のouter derivationを得た場合に
限り、BGCE386の三spatial incidenceとBGCE075の三metric slotsを結ぶtyped solderingを
別endpointとして検査する。三次元というdimensionだけで同一視しない。

## 4. Revision 3がE0前にfreezeすべき義務

1. `X_n`、`tau_x`のcanonical word、local coreのmatrix-unit orderingをexactに固定する。
2. eventual stabilization thresholdをsupport metadataからall-orderで証明する。
3. tracial varianceまたは別のexact certificateで`||P_a^(n)||`のunbounded lower boundを
   fitなしに証明する。
4. stabilized derivation rowsのrank threeを全8 sectorで検査する。
5. local core上のderivation normがunboundedであることからbounded-inner実装を除外する。
6. finite-range interaction theoremを適用するdomainとstrongly continuous automorphism
   groupを明示し、closabilityを証明する。
7. positive、zero、rank-two、bounded-inner、nonclosable、matched non-Braid witnessを同じ
   harnessへ通す。non-Braid comparatorはPASSも許し、その場合はcarrier existenceと
   Braid-transport specificityを分離して後者をNO-GOとする。per-sector/order/window/basis
   raw rowsを保持する。
8. R1/R2 outcome artifactをdenylist化し、focal constructorのinput allowlistをhash固定する。

## Claim ceiling

本監査が確立するのは、Revision 2のHadamard符号の型付けとadjacent-order互換条件が
不成立であること、およびRevision 3で検査可能なunit-counting局所和を一つに限定した
ことだけである。Revision 3のouter derivation、closability、rank three、constraint algebra、
gravity、経験的物理はまだPASSしていない。
