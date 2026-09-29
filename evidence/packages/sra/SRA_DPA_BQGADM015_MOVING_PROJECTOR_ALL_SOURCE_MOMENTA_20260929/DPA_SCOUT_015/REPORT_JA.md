# BQGADM-015 — nonlinear moving projectorと全finite source momentum

## 結論

**SCOPED PASS。**

前回の3 source axis限定を、`C5^3`の非零124 momentum方向すべてへexactに拡張した。
同時に、曲がった計量が時間発展するBQGADM-012 local regular perfect-history
branch上で、rank 4のphysical projectorを毎時刻一意に構成するmoving-projector
theoremを閉じた。

## 全124 momentum

BQGADM-006の3本のaxis symbolは、source spatial coframeに対してrotation-equivariantな
次の一つのcompletionを係数まで一意に固定する。

```text
scalar constraint = -4 (|k|^2 tr(q) - k^T q k)
vector constraint =  4 (k_j p_ij - k_i tr(p))
```

これはEinstein/Fierz-Pauli targetを入力した式ではない。scalarではmomentumに二次、
vectorでは一次であるsource-coframe-equivariant mapの全候補を置くと、3 axisの既存
exact rowが全係数を固定する。

`{-2,-1,0,1,2}^3`からzeroを除いた124方向を全検査し、各方向で次が成立した。

- constraint rank 4
- first-class bracket zero
- configuration projector rank 2
- phase projector rank 4
- constraint imageへの包含
- Hamiltonian gauge imageの消去
- physical symplectic rank 4
- constraint surfaceの`gauge 4 + physical 4`分解

選択された一部方向だけの検査ではない。124/124のexact rational判定である。

## nonlinear moving projector

各時刻の状態を`z`とし、既存source objectを

```text
A_z     = 4本のconstraint Jacobian
Omega_z = Palatini symplectic form
G_z     = source spatial coframeが作るpositive phase metric
R_z     = Omega_z^-1 A_z^T
```

と書く。`R_z`はgauge directionである。次を定義する。

```text
H_z = [ A_z ; R_z^T G_z ]
P_z = I - G_z^-1 H_z^T (H_z G_z^-1 H_z^T)^-1 H_z
```

rank-four first-class regular branchでは`H_z`はrank 8で、中央のGram matrixは可逆。
従って`P_z`は滑らかに時間依存しながら、次を保つ。

```text
P_z^2 = P_z
A_z P_z = 0
P_z R_z = 0
rank(P_z) = 4
```

さらにphysical image上のsymplectic formは非退化である。source refinementが
`A_z`、`Omega_z`、`G_z`をintertwineするため、同じ有理式で作る`P_z`もrefinementと
exactに可換する。

5個のexact rational moving-frame witnessでも、rank、constraint、gauge、metric
self-adjointness、symplectic rank、covariant conjugation identityを全て確認した。

## counter-intuition scan

通常の説明は、regular first-class constraint manifold上のYork/TT coisotropic sliceを、
metric-orthogonal projectorとして書いた標準的な幾何である。projector formula自体は
Braidだけの新数学ではない。

Braid固有なのは、finite `C5^3` momentum集合、completionを固定する3 axis symbol、
12次元Palatini carrier、actual symplectic form、`1+3` first-class generator、moving
source coframe metric、five-way refinementが同じsource provenanceから与えられる点である。

最強の境界はregularityである。zero momentum、constraint rank loss、Gram determinant
zero、caustic、singularityではprojectorは定義されない。またposition-spaceでultralocalな
projectorではない。

## Evidence classificationとclaim ceiling

- Primary evidence status: **Theoretical derivation**
- Scientific layer: mathematical formulation / nonlinear constrained dynamics
- Claim ceiling: 全124 nonzero `C5^3` momentumのexact projectorと、BQGADM-012
  local regular noncaustic perfect-history branch上のsmooth refinement-natural nonlinear
  moving projector。zero mode、rank-loss、caustic/singularity、global topology、
  strong curvature、ultralocal position-space formula、empirical gravity、confirmation、
  RPD adoption、Level 3、Official SIEL adoptionは主張しない。
