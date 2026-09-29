# BGCE287 — source event-path BKMはconductance kernelを消して一意なhorizontal liftを選ぶか

固定source revisionは `1768d7f259a8aad654092ee6100d56b77da6fc0b`。結果前に変更しない。

BGCE286では、actual Braid event conductanceのsecond momentからmetric tangentへの写像が全射だが、12変数表示にexact 2次元kernelが残った。
本gateは新しい係数を置かず、BGCE139のactual 8 undirected event edges、BGCE256のevent displacement、BGCE266の全edge共通source rate
`2*pi/3`、BGCE254のresponse-exact Umegaki/KL形式だけを使う。

連続時間event pathの相対エントロピー率の二次形式は、共通正rateの基点では全actual edge-rate tangent上の正定値Fisher/BKM metricになる。
overall positive rate factorはorthogonalityを変えない。4 axesの各unordered pairにactual 8 edgesを置いた48-dimensional microscopic rate tangentから
`Sym2(R4)`へのsecond-moment mapをexactに作り、そのBKM-orthogonal horizontal liftを判定する。

判定項目：

1. 48→10 microscopic moment mapはrank 10か。
2. metric-invisible kernel上でevent-path BKM metricは非退化か。
3. BKM-orthogonal complementからmetric tangentへの制限は同型で、一意なhorizontal liftが得られるか。
4. liftは24個のactual X21R1 tangentsすべてをexactに再現するか。
5. liftは24個のS4 axis permutationsに共変か。
6. 12-variable second-moment quotientに戻したとき、BGCE286の2次元kernelをrank 2で抑えるか。

## 事前判定

- **FULL PASS**：全項目がexactに成立し、追加fitなしで一意なsource-event-BKM horizontal liftが得られる。
- **PARTIAL PASS**：kernelは測れるが、追加係数・非source metric・任意chart選択が必要。
- **FAIL**：BKM restrictionが退化、24 tangentsの一つでも再現不能、またはS4共変性が破れる。

## 境界

これはfirst-order conductance connectionの選択gateである。event-path BKMをfull physical parent actionと同一視しない。
非線形積分可能性、Hilbert stress、Ward、SDPC、無条件Einstein方程式は別gate。E0/E1/E2はDPAから発行しない。
