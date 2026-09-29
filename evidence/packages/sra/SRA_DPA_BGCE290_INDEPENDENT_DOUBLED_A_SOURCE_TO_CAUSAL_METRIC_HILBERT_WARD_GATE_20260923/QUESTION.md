# BGCE290 — independent doubled `a_A` sourceをphysical causal metricへsolderしstress/Wardを閉じる

固定source revisionは`b7499ca5327e1622bf53e77d46d5d06810fa9d64`。結果前に変更しない。

BGCE289はfinite local 7+3 metric familyを得たが、odd座標がmatter thetaと同一なのでfixed-matter Hilbert variationがrank 7に落ちることを証明した。一方、BGCE142/143にはmatter thetaと独立な10個のdoubled metric source `a_A`が存在する。

本gateは次をexactに判定する。

1. 10個の`a_A`は、既存4-operator frame `[G1,{G1,P_i}/2]`の対称二階sourceとして型付けされているか。
2. BGCE150の事前固定operator-frame label mapとBGCE268のsource-normalized Hadamard `U=H4/2`を合成した`Sym^2(U)`は、10次元で可逆か。
3. その写像はsource causal involutionの7 even + 3 odd分解とS4 chart actionをexactにintertwineするか。
4. `a_A`がmatter thetaと独立なので、fixed-matter full rank-10 metric variationを与えるか。
5. 各metric tangentがsource event coframe strainへ一意に持ち上がり、symmetric conservative refinement-compatible Markov principal symbolを保つか。
6. BGCE254/256で選択されBGCE266でLorentz continuationされたBKM parentを、このoff-shell familyで変分するとHilbert stressとon-shell Wardが追加matter actionなしに得られるか。

## 事前判定

- **FULL PASS**：1–6が成立し、宣言した長波長local second-order self-adjoint conservative class内でHilbert stressとon-shell Wardへ到達する。
- **PARTIAL PASS**：独立metric solderは成立するが、active Markov transportまたは同じsource-selected parentへの変分接続が閉じない。
- **FAIL**：`Sym^2(U)`がrank 10でない、7+3/S4を保たない、または`a_A`が独立metric sourceとして型付けできない。

## 境界

BGCE150で失敗した「KMS covariance metricそのものと固定causal metricの同一視」は再主張しない。本gateはsource covector `a_A`をmetric variationへ運ぶsolderを問う。高階微分、異なるprincipal symbol、finite-Braid-onlyを越える既存real affine/Stone completion、MMR2/3/5、Einstein dynamics、経験的重力は別境界として保持する。
