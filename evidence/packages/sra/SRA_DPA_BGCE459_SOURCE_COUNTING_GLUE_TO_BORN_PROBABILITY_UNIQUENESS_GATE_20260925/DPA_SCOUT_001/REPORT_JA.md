# BGCE459 / DPA-SCOUT-BGCE459-001 結果

## 判定

**SCOPED PASS / `BQG-G0-R01.2 CLOSED_SCOPED`**

BGCE458でBraidから作った36 complex dimensionの有限carrierに、既存sourceのcounting、reversal、cup/cap closureを接続すると、source-typed projectorの確率はnormalized squared normへ一意に固定される。

Born則を入力したのではない。使った順序は次の通りである。

```text
actual pointed-Braid event table
  -> oriented word C and reverse C^-1
  -> J^2=-I on H=im(P)
  -> source reversal as dagger
  -> equality-counting cup/cap closure
  -> p(E|psi)=closure(Epsi,Epsi)/closure(psi,psi)
```

## exact witness

actual `C`が持つ36個のthree-cycleから、canonical history順で最初の二つを選んだ。

```text
cycle 1 = [1,25,5]
cycle 2 = [2,50,10]
```

各cycle上の同じ長さのmean-zero vectorを`x,y`とし、`psi=x+2y`を作る。第一cycleのsource-orbit projectorを`E`とすると、これはself-adjointで`C,A,P,J`と可換である。

```text
closure(Epsi,Epsi) = 2
closure(psi,psi)   = 10
p(E|psi)           = 1/5
```

複素source matrix、density state、入力trace、Gleason noncontextuality、`q` phase、Born確率、frequency fit、係数fitは使っていない。

## なぜ二乗なのか

source capとevaluationは既にdagger adjointとしてexactに固定されている。history atom上のkernelはequality countingである。これをformal superpositionへlinearに延長し、reverse側をdaggerにすると、各係数についてpairingが一意に決まり、自己閉包は二次形式になる。共通loop scaleは分子・分母のnormalizationで消える。

従って二乗則は「確率は二乗」と別に仮定した結果ではなく、固定source/Brauer branchのlinear dagger closureから出る。

## counter-controls

弱い確率条件だけなら別の族が残る。amplitude比`1:2`に対し、normalized power lawは次を与える。

| rule | first outcome |
|---|---:|
| `r=1` | `1/3` |
| `r=2` | `1/5` |
| `r=4` | `1/17` |

`r=1`と`r=4`もpositive、normalized、coordinate-symmetric、phase-blind、product-multiplicativeではある。しかしparallelogram checkはそれぞれ`4 != 8`、`32 != 8`で失敗する。`r=2`だけが`8=8`でsource dagger closureと一致する。

したがって、対称性だけからBorn則が出たとは主張しない。決定的なのはsource由来cup-compatible linear gluingである。

## 何が閉じ、何が残るか

有限source-dagger projective classでは次が閉じた。

- state：`H=im(P)`のnonzero ray;
- complex scalar：外からの`i`ではなく`aI+bJ`;
- observable：`C`-invariant source-cylinder sumsから得るself-adjoint complex-linear projector;
- composition：既に証明済みの全有限Brauer diagram stageのcap/evaluation closure;
- probability：上記projectorに対するnormalized squared norm。

一方、全self-adjoint operatorがpointed Braidだけから生成されること、一般のphysical tensor composition、unitary dynamics、actual tableのordinary flipに対する固有性は未証明である。次の候補は`BGCE460`でobservable connectivityとunitary dynamicsを同じsourceから出せるかの判定である。

## claim ceiling

本結果は固定source/Brauer observation branch上の有限projective probability再構成である。実験的量子力学、QFT、量子重力の経験的確認、Level 3、Official SIEL adoptionは主張しない。数学機構自体は標準dagger-compact/GNS機構であり、ordinary flipも関連controlを共有する。
