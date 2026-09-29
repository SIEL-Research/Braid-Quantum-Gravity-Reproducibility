# BQGNEUT-024 audit

## 判定

`SCOPED_PASS_ONE_SOURCE_ORDERED_C3_WEIGHTED_FLOQUET_OPERATOR_IS_EXACTLY_UNITARY_AND_SIMULTANEOUSLY_HAS_DISTINCT_NON_EQUALLY_SPACED_EIGENPHASES_AND_EXACT_NONZERO_CP_ODD_NUMERATOR_WITHOUT_TARGETS_OR_SCAN__PHYSICAL_PMNS_AND_NEUTRINO_MASS_SCALE_REMAIN_OPEN_PENDING_LEPTON_TYPING_AND_ABSOLUTE_SCALE`

## 監査結果

- source commit `7fc09683a6f47ddb11e64f5d41c81b6f0bda26b3`：固定PASS。
- snapshot `DPA-SNAPSHOT-7fc09683a6f4`：生成PASS。
- BQGNEUT-022/023入力hash：PASS。
- fixed operator：`U_F=C_g exp[-i(2*pi/3)L_w]`。
- `Q(zeta_15)` exact unitarity：PASS。
- characteristic quadratic discriminant：exact非零。
- trace：exact非零、equal-third phase spacingを排除。
- fixed circular gaps：三つとも正かつ相異なる。
- CP-odd cycle numerator：exact非零。
- `|J|=0.08557801977513962`。
- direct invariantとeigenframe `J`：一致PASS。
- external neutral carrier：BQGNEUT-023のscoped解除を維持。
- PMNS/NuFIT、mass target、angle/parameter scan、長時間計算：不使用。

## Claim boundary

dimensionless neutral operational propagatorの同時CP/gap閉包まで。physical weak-current
typing、mass-squared interpretation、absolute scale、実測一致は非補償OPENである。
