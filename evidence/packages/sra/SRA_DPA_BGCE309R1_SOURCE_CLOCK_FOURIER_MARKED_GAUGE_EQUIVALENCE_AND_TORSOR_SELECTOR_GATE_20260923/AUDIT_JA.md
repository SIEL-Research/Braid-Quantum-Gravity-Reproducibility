# BGCE309R1監査 — copy/basepoint selectorはreduced channelではgaugeとして除去

## 結論

**SPLIT PASS。** `G1`と3つのFourier marksは、4つのregular copyまたは一つのidentity basepointを物理的に
一意選択しません。しかし、この未選択性はreduced GKSL channelについては新しい物理仮定ではありません。
copy/basepointの変更はenvironment-only unitaryであり、partial trace後のchannelをexactに不変にします。

従ってBGCE308で残ったselectorのうち、**reduced channel用のcopy/basepoint selectorは解除**できます。
未解決なのはenvironment stressとtotal Wardを同じgaugeに共変化できるかです。

## 32 blockのmarked gauge equivalence

全8 sector × 4 regular copyの32 blockを検査しました。`G1`の符号配置はliteralには同じでない場合があります。
しかし全blockについて、対角成分が`±1`のunitary `D`がexactに存在し、

`D G1_block D = G1_standard`

となります。各`P_chi`は対角なので、同時に

`D P_chi D = P_chi`

です。各blockには`D`と`-D`の2解があり、同じconjugationを表します。従って全32 blockは
Fourier marksを保ったまま一つの標準marked representationへ移ります。

## 6本のclock/Fourier ray

各`P_chi`はregular orbit内でrank 2です。圧縮clock

`P_chi G1 P_chi`

のnumeratorは符号gaugeを除けば

`[[15,-7],[-7,15]]`

で、固有値は`8`と`22`、すなわち`G1`固有値は`4/3`と`11/3`です。3つの`chi`それぞれに2 rayが
あるため、6本のorthogonal rank-1 rayがsource marksから得られます。

ただしfull Braid generatorはこの6 rayをregular group basisとしてpermuteせず、一部をsuperpositionへ
送ります。従って、このspectral frameをそのまま6つのgroup-element labelと同一視することはできません。

## なぜbasepointは不要か

regular orbitは`S3` torsorです。basepoint `b`を選ぶと各stateを`|g b>`と書けます。別のbasepoint
`b'=h b`へ変えると、二つのStinespring isometryはenvironment unitary `Q_h`により

`V_b' = (I tensor Q_h) V_b`

で結ばれます。regular copyの変更も同様にenvironment isometryです。partial traceはenvironment unitaryに
不変なので、どのcopy/basepointを使ってもreduced channelは同一です。

したがってcopy/basepoint選択はdilation座標のgaugeであり、reduced quantum dynamicsのMMR型物理仮定では
ありません。

## 残る境界

environment Hamiltonianまたはstress observableを入れると、それも`Q_h`で共変変換されなければなりません。
現在はそのobservable自体が未導出なので、total balanceやWardについてchoice independenceはまだ言えません。

## 次

`BGCE310_TORSOR_GAUGE_COVARIANT_ENVIRONMENT_CHARGE_AND_TOTAL_G1_BALANCE_GATE`

BGCE307で測ったsystem側の`G1`欠損を、BGCE309R1のtorsor-gaugeに共変なenvironment chargeでexactに
相殺できるかを、one-collision operator identityとして解きます。

## 主張上限

BGCE309R1はcopy/basepoint selectorをreduced GKSL channelの物理仮定から除去しました。environment stress、
total Ward identity、full finite Lorentzian quantum backreactionはまだ導出していません。

