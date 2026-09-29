# BQGSTRAT-010 監査報告

## 結論

**SCOPED SPLIT PASS / 現行single-orientation raw blockの無条件二偏極component選択はNO-GO。**

`BQGSTRAT-009`で構成した80次元Fourier symbolを、
`Q(zeta_5)`上のexact Gaussian eliminationで全625 sectorについて分類しました。
`24576 x 24576` dense matrixは生成していません。

## Exact rank profile

| sector | 個数 | rank | nullity |
|---|---:|---:|---:|
| zero mode | 1 | 60 | 20 |
| generic | 600 | 66 | 14 |
| same-orientation null sheet | 12 | 64 | 16 |
| opposite-orientation null sheet | 12 | 65 | 15 |

same-orientation sheetは、時間digitとただ一つの非零空間digitが等しいsectorです。
opposite sheetは、その空間digitが時間digitの負値mod 5であるsectorです。

これはfloating-point rankではありません。cyclotomic Galois作用と空間3軸の置換で
45 orbitへ圧縮し、各代表を`Q(zeta_5)`上でexact消去した結果です。

## 意味

actual rank lossは存在します。したがって`BQGSTRAT-008`で未同定だった
`K_ii`型のsingular sectorは、少なくともこの条件付きraw blockでは実在します。

さらにsame-orientation sheetではgeneric nullity 14から2方向増えます。これは
二偏極characteristic modeの候補として非常に強い形です。

しかしopposite sheetでは増分が1方向だけです。数値的なtransverse crossing probeも、
same sheetでrank 2、opposite sheetでrank 1でした。crossingのこの部分はまだexact証明では
ありませんが、exact corank差そのものは消せません。

したがって、ordered source digitsは24 exceptional sectorを区別できますが、現行の
single-orientation raw blockだけから「両伝播向きに二偏極を持つ物理component」を選ぶことは
できません。ここを成功扱いすると、有限親と既存二偏極continuum shadowの不整合を隠します。

## 次

`BQGSTRAT-011`で、既存sourceのorientation sheet／reverse-edge dataからreverse-sheetまたは
adjoint face contributionを結果を見る前に固定します。その完成symbolに対し、両null sheetが
ともにrank 64・追加二modeになるかをexact判定します。

係数fit、目標Einstein式、観測値、parameter scanは使いません。

## 境界

- rank profile：exact
- crossing rank：数値support、exact certificateは未完
- physical component selection：現行raw blockではNO-GO
- reverse-sheet completion、matter-coupled caustic、global continuation：OPEN
- Braid必要性・実測：未主張
