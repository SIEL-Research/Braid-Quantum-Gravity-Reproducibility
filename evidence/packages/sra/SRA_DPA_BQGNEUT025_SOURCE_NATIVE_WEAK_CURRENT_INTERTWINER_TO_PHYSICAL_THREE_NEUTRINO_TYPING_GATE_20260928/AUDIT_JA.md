# BQGNEUT-025 audit

## 判定

`CLOSED_SCOPED_UNIQUE_SOURCE_POINTED_ORIENTED_DAGGER_FROBENIUS_FUNCTOR_COMPOSED_WITH_THE_DERIVED_LEPTON_SU2_LADDER_GIVES_A_RANK_THREE_WEAK_CURRENT_PARTIAL_ISOMETRY_INTERTWINING_FULL_M3_AND_TYPES_THE_INTERNAL_NEUTRAL_QUTRIT_AS_THE_PHYSICAL_THREE_GENERATION_NEUTRINO_FACTOR_WITHOUT_AN_EXTERNAL_GENERATION_CARRIER_IN_THE_BGCE439_DERIVED_MATTER_CLASS__UNCHANGED_RAW_SOURCE_ABSOLUTE_MASS_SCALE_AND_EMPIRICAL_PMNS_REMAIN_OPEN`

## 監査結果

- source commit `dc26af7d378897962c72b28283eaa2b16a2eb1a1`：固定PASS。
- snapshot `DPA-SNAPSHOT-dc26af7d3788`：生成PASS。
- BQGNEUT-024、BQGFM-011、BQGFLAV-036、BGCE439、BGCE544入力hash：PASS。
- branch-to-generation候補：6。
- pointed候補：2。
- pointed-oriented候補：1。
- multiplication/comultiplication/minimal-projector intertwining：exact PASS。
- residual continuous basis phase dimension：0。
- weak-current partial isometry：exact PASS、rank 3。
- full `M3` matrix units：9/9 intertwining PASS。
- lepton doublet charges：`Q(nu_L)=0`、`Q(e_L)=-1`。
- BQGNEUT-024 nonzero CP/unequal gaps：transport後も保持。
- external generation carrier：declared matter class内で不要。
- target data、parameter scan、長時間計算：不使用。

## Claim boundary

physical typingはBGCE439 explicit derived matter class内に限定する。unchanged raw source、
absolute mass scale、empirical PMNS matchはFAIL/OPENのまま保持する。
