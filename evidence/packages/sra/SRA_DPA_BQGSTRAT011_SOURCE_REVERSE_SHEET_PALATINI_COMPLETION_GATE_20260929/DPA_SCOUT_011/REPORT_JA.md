# BQGSTRAT-011 監査報告

## 結論

**NO-GO。単純なreverse-face／adjoint完成では二偏極を回復できません。**

ただし、これは有限Braid親全体のNO-GOではありません。閉じたのは、既存の
orientation double coverとreverse-edgeだけを使って、同じscalar Palatini faceを
反転追加する経路です。

## Exact theorem

`BQGSTRAT-009`のoriented plaquetteを`P`とすると、reverse boundary wordは
`P^{-1}`です。共通principal log branch上で

`log(P^{-1})=-log(P)`

がexactに成立します。一方、Palatini作用のoriented face bivectorも、face
orientation reversalで符号を反転します。したがって二つのminusが消え、合法な
reverse-face項は元のforward-face項とexactに同じです。

そのため、forward/reverseをscalar係数で組み合わせた全completionは

`H_completed=lambda H_original`

にしかなりません。`lambda`が非零ならrankは不変、zeroなら作用全体がzeroです。

## Exact consequence

equal-weight orientation pairはHessianを2倍しますが、`BQGSTRAT-010`のrank profile

`60 x1, 64 x12, 65 x12, 66 x600`

を一切変えません。したがって、片方のnull sheetの追加corank 2と、逆側の追加
corank 1という不均衡は残ります。必要だった「24 exceptional sectorすべてrank 64」
にはなりません。

face labelを固定したままedgeだけを逆転すれば符号が反対になり、equal weightでは
zero actionになります。またreverse edgeを独立な新自由度として扱うことは、既存の
groupoid inverse ruleに反します。

## 何が残ったか

単なる向き反転では不足です。`BQGSTRAT-010`と今回の二連続NO-GOにより、次は同じ
mechanismの微調整ではなく、内部表現を変える必要があります。

次の大胆仮説は、source orientation double coverが「同じscalar faceの二重化」では
なく、dagger-conjugateな二つのinternal bivector sheetを選ぶというものです。
自己双対／反自己双対、または同等なoff-diagonal doubled-branch Hessianをsourceから
先に導出し、その後でのみ`Q(zeta_5,i)`上のexact rankを判定します。

これは現時点では**DPA speculation**です。current real GL4 Palatini blockが既に両
chiralityを含むなら、この仮説は即NO-GOになります。

## 境界

- primary evidence status：**Theoretical derivation**
- incident class：`SCIENTIFIC_OUTCOME`
- scalar reverse-sheet completion：NO-GO
- off-diagonal dagger/chiral double-cover completion：OPEN
- generic singular/global continuation、matter coupling、Braid必要性、実測：未主張
