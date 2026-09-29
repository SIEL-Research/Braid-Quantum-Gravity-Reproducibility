# BQGNEUT-031 finite neutral CTP to causal-face transgression gate

## 結論

**SPLIT RESULT：非可換face holonomyはSCOPED PASS、中央`U(1)` transgressionはSCOPED NO-GO。**

既存のsource transport `C_g`、weighted neutral interaction

```text
E = exp[-i(2*pi/3)L_w]
```

およびCTP dagger reversalを一つの最小causal plaquette境界として読むと、face holonomyは

```text
W_face = C_g E C_g^dagger E^dagger
```

で固定される。新しい係数、観測値、branch scanは使用していない。

## 成立した内容

`C_g`と`E`は非可換であり、

```text
||C_g E - E C_g||_F^2 = 0.9926081809234254
```

である。`W_face`はunitaryかつ非identityで、

```text
||W_face-I||_F = 0.9962972352282352
```

となる。従って既存finite sourceから非自明な**非可換causal-face holonomy**を作るcapacityは成立した。

## 決定的NO-GO

任意の可逆な`A,B`について

```text
det(A B A^-1 B^-1)=1
```

である。従って今回のordinary CTP group commutatorもexactに

```text
det(W_face)=1
```

であり、determinant lineが読む中央`U(1)` fluxは`0 mod 2*pi`である。BQGNEUT-027のliftは非零なので、BQGNEUT-030のcentral two-form transgressionをこのminimal plaquetteから得ることはできない。

さらにcircular eigenphase gap multisetは、

```text
BQGNEUT-027/Floquet:
(0.0492348157621, 2.1436299181553, 4.0903205732622)

minimal CTP plaquette:
(0.7199359597338, 0.7199359597338, 4.8433133877120)
```

で一致しない。plaquette側には二重gapが復活するため、非可換eigenphaseを旧liftと読み替えることもできない。

## 意味

BQGNEUT-030で得た「25分割される因果面」は維持される。今回分かったのは、その面を運ぶ線束の型である。

- ordinary CTP group commutator：非可換`SU(3)` face holonomyは出る
- 必要なneutral central phase：出ない

よって次は、ordinary unitary determinantではなく、既存Nambu pairingが持つPfaffian/determinant lineのBerry curvatureを検査する。これは中央`U(1)`位相を自然に担える別の機構classである。

## 境界

排除したのはminimal rectangular dagger-CTP commutator classだけである。Pfaffian line、open Wilson surface、別のsource-derived transgressionは未排除。実測PMNS、SI traceability、量子重力完成は主張しない。

## 次gate

`BQGNEUT-032_PFAFFIAN_DETERMINANT_LINE_BERRY_CURVATURE_TO_CAUSAL_FACE_TRANSGRESSION_GATE`
