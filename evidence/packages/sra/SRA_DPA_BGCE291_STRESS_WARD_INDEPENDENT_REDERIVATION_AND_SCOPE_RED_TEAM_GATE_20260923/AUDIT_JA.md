# BGCE291監査 — BGCE290 stress/Ward昇格の独立red-team

## 結論

**部分撤回。BGCE290のFULL PASSは維持できない。**

独立10 source `a_A`の型と、正規化Hadamardが作るrank-10 `Sym2` mapは再現した。したがってBGCE289のfixed-matter rank-7 lockを避ける**代数的solder候補**は残る。

しかし、次の二段階は導出されていなかった。

1. この候補がoff-shellの物理metric solderとしてsourceから一意に選ばれること。
2. 一次のBKM-horizontal conductance connectionが有限のcurved Markov familyへ可積分であること。

このため、BGCE290で昇格したactive transport、曲率potential排除、Hilbert stress、Wardを条件付きへ戻す。

## 1. source typingとrank 10はPASS

BGCE141の4 operator frameとその10個の対称積、BGCE142の独立source `a_A`との双対結合は一次コードで確認できた。Hadamard `U=H4/2`のcongruence

```text
H_ray = U^T A_char U
```

が`Sym2(R4)`上でrank 10であることもexactに再計算した。ここはBGCE290の実質的な成果として維持する。

## 2. S4共変性は一意性を与えない

`S4`の4次元permutation representationを`Sym2(R4)`へ持ち上げ、そのcommutantをexact有理消去で計算した。

```text
dim End_S4(Sym2(R4)) = 9
```

従って240個のintertwining checkは、Hadamard候補が共変であることを示すが、共変な候補が一つしかないことは示さない。BGCE268自身もHadamardをfinite quantum/causal carrier intertwinerまでに限定し、off-shell spacetime metric deformation naturalityを`OPEN`としている。

つまりHadamard solderは自然で強い候補だが、現時点では物理metric solderの一意なBraid-only選択ではない。

## 3. coframe恒等式はactive dynamicsではない

BGCE290が用いた

```text
S=(1/2)K_evt^{-1}H,
S^T K_evt+K_evt S=H
```

は、任意の対称tangentをcoframe strainで表せるという点ごとの線形代数である。これはevent edge conductanceが有限変形に沿ってどう輸送されるか、閉路を回った結果がpath-independentか、positivity・detailed balance・refinementが有限に保たれるかを証明しない。

実際、BGCE287の凍結結果は

- first-order BKM-horizontal lift：PASS。
- full nonlinear integrability：OPEN。
- full finite physical parent action：OPEN。

と明記している。BGCE290の評価コードはcoframe checkの後でactive transport、curvature exclusion、stress、Wardをliteral `True`に代入しており、欠けた非線形定理を計算していなかった。

## 4. stress/Wardの正しい現在地

仮にminimal BKM sigma-model actionを採れば、Hilbert tensorとNoether identityは正しく得られる。しかしBGCE267の曲率coupling counterexample、BGCE285のconditional minimal-generator theoremは、finite active transportが閉じない限り残る。

したがって現在地は次のとおり。

- 独立metric source：PASS。
- rank-10 algebraic solder candidate：PASS。
- physical solder selection：OPEN。
- first-order active conductance connection：PASS。
- finite nonlinear active Markov transport：OPEN。
- Braid-only Hilbert stress：未導出、条件付き構成は利用可能。
- Braid-only Ward：未導出、条件付きNoether identityは利用可能。

## 最短の次

新しい作用や係数を探さない。BGCE287の既存BKM-horizontal connectionの曲率を計算する。

- curvatureがzeroなら、単連結な局所metric neighborhoodでpath-independentな有限liftが得られる。
- curvatureがnonzeroなら、このconnectionによる一意なfinite parent経路は閉じる。

次は`BGCE292_BKM_HORIZONTAL_CONNECTION_CURVATURE_AND_LOCAL_PATH_INDEPENDENCE_GATE`。

## 主張上限

本監査はHadamard solder候補そのものを反証していない。また、より強いBraid selectorが存在しないことも証明していない。Einstein dynamics、経験的重力、完成量子重力には到達していない。
