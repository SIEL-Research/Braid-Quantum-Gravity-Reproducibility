# BGCE458 / DPA-SCOUT-BGCE458-001 結果

## 判定

**SCOPED PASS / `BQG-G0-R01.1 CLOSED_SCOPED`**

実際の25-event pointed-Braid tableだけを三つの履歴へ作用させ、複素行列、量子状態、trace、Born確率、`q`位相、係数fitを入力せずに、非零のcomplex kinematic sectorを構成した。

## exact construction

隣接作用を`R1,R2`、向きを持つ三地点wordを`C=R1 R2`とする。actual event tableはinvolutive Yang-Baxterなので、125 history atoms上で

```text
C^3 = I
```

がexactに成立する。順方向と逆方向の差および非自明sector projectorを

```text
A  = C - C^-1
3P = 2I - C - C^-1
```

と置くと、全125 basis atomで

```text
A^2 = -3P
```

が成立した。従って`im(P)`上の`J=A/sqrt(3)`は`J^2=-I`である。

- actual `C` fixed points：`17`
- actual three-cycles：`36`
- `P` real rank：`72`
- reconstructed complex dimension：`36`
- exact identity failures：`0`
- Yang-Baxter failures：`0 / 125`

基底historyの等号を数えるdelta kernelは正定値で、`R1,R2`はpermutationなので保存する。even word `C`は`J`と可換でcomplex-linear、odd generator `R1,R2`は`J`の符号を反転しcomplex conjugation型に作用する。

## controls

- identity：complex dimension `0`
- ordinary flip：complex dimension `40`
- deterministic involutive Yang-Baxter-broken control：Yang-Baxter failure `18 / 125`、`C^3=I`失敗

ordinary flipも同じ機構で非零sectorを作る。従って今回得たのは「actual Braidからcomplex structureが出る」という存在証明であり、pointed-Braid固有性ではない。

## 失敗履歴

- Attempt 0001：repo-root path誤りでsource読込前に停止
- Attempt 0002：ordinary-flip rankを`120`と誤記したassertionで停止。正しくは40 three-cycles×2実方向=`80`、complex dimension `40`
- Attempt 0003：上記だけを開示訂正しPASS

失敗attemptと全freezeはappend-onlyで保持した。

## 解釈

大胆な仮説の一部は当たった。Braid wordと逆wordの差が、通常は外から入れる虚数単位の役割を、sourceの非自明history sector上で果たす。

しかし量子論全体はまだ出ていない。特に、任意のsuperpositionに対する確率がnormalized squared normへ一意に固定されることは未証明である。次は`BGCE459`でsource counting/gluing lawだけからBorn probabilityを固定できるかを判定する。

## claim ceiling

本結果は固定有限三履歴sectorのcomplex kinematicsに限る。full `M_(5^n)(C)` tower、一意な全sector complex structure、source-selected state、任意observable、tensor composition、interference frequency、Born rule、dynamics、QFT、経験的量子力学、confirmation、Level 3、Official SIEL adoptionは主張しない。ordinary flipもPASSするため、pointed-Braid specificityは未達である。
