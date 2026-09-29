# BGCE307監査 — fixed-time unitary dilationは導出、total stress/Wardは未閉鎖

## 結論

**SPLIT PASS。** BGCE125のReynolds semigroupは、実際の6つのBraid unitaryを環境ラベルに使うことで、
各時刻ごとにexactなsource-labelled Stinespring dilationを持ちます。これは任意の無関係なbathを持ち込む
構成ではありません。

一方、同じ有限環境・固定初期状態・time-independent Hamiltonianで全時刻の指数緩和を再現することは
不可能です。またsystemのsource clock observable `G1`は保存されず、環境stressとtotal Ward balanceは
まだ導出されていません。従ってfull finite Einstein backreactionは未閉鎖です。

## exactなunitary化

Reynolds channelを`E`、`q=exp(-gamma t)`とすると、

`T_t = q Id + (1-q)E`

です。6要素の実Braid群のidentity成分へ二つの重みをまとめると、A55 crossing `q=1/4`では

`p_e=3/8`,  `p_g=1/8  (g != e)`

となります。環境を6つの実Braid作用で標識したgroup register `C[S3]`とし、

`W = sum_g U_g tensor |g><g|`

および

`|psi_t> = sum_g sqrt(p_t(g)) |g>`

を使えば、`W`はunitaryで、環境をpartial traceした結果はexactに`T_t`です。全8 source sectorで成立し、
fit係数はありません。

## なぜこれだけではfull semigroupにならないか

有限次元のtime-independent total Hamiltonianから得られるreduced dynamicsの各matrix elementは、有限個の
phase `exp(-i omega t)`の和です。このような関数が`t -> infinity`で極限を持つなら、非ゼロ周波数成分は
消え、関数は定数でなければなりません。

しかし`T_t=E+exp(-gamma t)(I-E)`は非定数でありながら`E`へ収束します。従って、固定された一つの有限
environmentで全時刻をautonomousに再現することはできません。exact Markov semigroupには、infinite ancilla
chain、Fock environment、または毎回freshなancillaが必要です。

## 保存則のexactな欠損

Reynolds adjoint generatorについて全8 sectorを直接計算すると、

`E^*(G1)-G1 != 0`

で、そのHilbert–Schmidt norm squaredは全sectorでexactに

`18`

です。従ってtrivialな環境Hamiltonianではbalanceできません。これは失敗だけではなく、環境側が受け取る
べきsource energy/stressの欠損が具体的に固定されたことを意味します。

## 次の最短経路

`BGCE308_SOURCE_RIGHT_TAIL_REPEATED_INTERACTION_DILATION_AND_TOTAL_BALANCE_GATE`

既存のsource-native refinement `A -> A tensor I_5`で追加されるright-tail C5 strandsをfresh ancilla chainとして
使えるかを調べます。これが通れば外部bathを仮定せず、Braid自身の無限refinementからGKSL環境とbalance
currentを得られる可能性があります。

## 主張上限

BGCE307は各finite-time Reynolds channelのsource-labelled unitary dilationと、system `G1`保存欠損を導出
しました。autonomous full-semigroup environment、environment stress、total Ward identity、full finite Lorentzian
quantum backreactionはまだ導出していません。

