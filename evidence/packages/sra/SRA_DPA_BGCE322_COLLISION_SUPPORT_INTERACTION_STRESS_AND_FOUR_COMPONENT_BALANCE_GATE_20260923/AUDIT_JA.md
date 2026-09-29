# BGCE322監査 — collision support上のinteraction balanceと4成分total balance

## 結論

**SPLIT PASS。**

一回のactual six-state Braid collisionについて、時間1成分と空間3成分を合わせたexactなtotal operator balanceが全8 sectorで成立する。

BGCE311でpure environment chargeには運べなかった空間欠損

\[
\|D_i\|_{\rm HS}^2=(24,14,14)
\]

は消失ではない。actual Stinespring isometry `V`のphysical output support `P=VV*`上で

\[
\boxed{\mathcal I_i=V D_iV^*}
\]

という一意なsystem–environment interaction balance operatorへ持ち上がる。これにBGCE310の時間environment chargeを合わせると、

\[
\boxed{
V^*\bigl(X_\alpha\otimes I+I\otimes E_\alpha+\mathcal I_\alpha\bigr)V
=X_\alpha,
\qquad \alpha=0,1,2,3
}
\]

がexactに成立する。

ただし、これはまだphysical variational interaction stressではない。sourceはmetric-dependent collision deformation `V(F)`をまだ与えていない。従ってstandard dynamical influence action、repeated local Ward、continuum total Wardは未導出である。

## 1. なぜpure environment経路は失敗し、interaction経路は閉じるのか

BGCE311で、空間generator

\[
H_i=-i[G_1,P_{\chi_i}]
\]

のone-collision defect

\[
D_i=H_i-V^*(H_i\otimes I)V
\]

は、任意のsix-state environment-only observableがsystem側へ作れるrange

\[
\mathcal R_E=\operatorname{span}\{U_g^*U_h\}
\]

とexactに直交していた。このため`I tensor K_i`だけでは欠損を回収できない。

しかしinteraction observableはfull joint output algebraに属する。`V*V=I`と`P=VV*`から、support algebra

\[
P\mathcal B(\mathcal H_S\otimes\mathcal H_E)P
\]

のcompression

\[
C_P(J)=V^*JV
\]

は`B(H_S)`へのisomorphismである。従って任意のsystem defect `D`はsupport上にただ一つ

\[
J=VDV^*
\]

を持つ。

これは候補を片端から探索した結果ではなく、isometryのexact lemmaである。

## 2. 1＋3 total balance

`X_0=G1`とし、`E_0=H_E`をBGCE310のenvironment chargeとする。BGCE310が

\[
V^*(G_1\otimes I+I\otimes H_E)V=G_1
\]

を既に証明したため、support上の時間interaction remainderはzeroである。

空間成分では`X_i=H_i`, `E_i=0`とし、

\[
\mathcal I_i=V\left(H_i-V^*(H_i\otimes I)V\right)V^*
\]

と置く。すると

\[
V^*(H_i\otimes I+\mathcal I_i)V=H_i
\]

が直ちにexactに成立する。

従って一回のcollisionでは、

- temporal：system＋pure environment。
- spatial：system＋interaction。

という型で4成分が閉じる。新しい係数、fit、sector別符号はない。空間interactionはnonzeroで、そのcompressed defect normは全8 sectorで`24,14,14`である。

copyまたはbasepointをenvironment unitary `Q`で変更すると、`V`と`I_i`はともに`I tensor Q`で共役されるため、このbalanceはtorsor-gauge covariantである。

## 3. BGCE321 rank-ten operatorのcollision support transport

BGCE321のdoubled operatorを

\[
\widehat{\mathcal A}(F)
\]

とし、doubled isometryを

\[
\widehat V=I_2\otimes V
\]

とする。collision support上のoperatorを

\[
\boxed{
\widehat{\mathcal J}(F)=
\widehat V\widehat{\mathcal A}(F)\widehat V^*
}
\]

と定義する。

BGCE321の三つのmixed scoreとBGCE311の三つの`H_i`は、どちらも同じ`G1/P_chi_i` commutator方向から生成される。従って空間interaction balanceとmetric-response packetの三方向ラベルは外部対応表で貼ったものではない。

isometryなのでrank 10は全8 sectorで保存される。BGCE319のtime reversalもsupportへ共役輸送できるため、`Jhat(F)`はoutput support上でoddである。

branch-system state

\[
\Omega_{\rm in}=\frac{I_2}{2}\otimes\omega_{\rm can}
\]

を

\[
\Omega_{\rm out}=\widehat V\Omega_{\rm in}\widehat V^*
\]

へ送る。`Omega_out`はfull output algebraではrank deficientだが、`P_hat` support上ではfaithfulである。従ってsupport上で

\[
\Phi_{\rm out}(F)=
\log\operatorname{Tr}_{\widehat P}
\exp\left(\log\Omega_{\rm out}+\widehat{\mathcal J}(F)\right)
\]

が定義でき、isometric invarianceにより`Phi_out=Phi_in`である。

`Phi(0)=0`、一次微分はbranch Pauli tracelessnessによりzero、Hessianはfaithful BKM covarianceでrank 10となる。従って一回のcollision supportには、係数なしのlocal doubled cumulantとfull metric susceptibilityが存在する。

## 4. contact ambiguityの正確な範囲

support内ではcompressionがisomorphismなので、`I_i=VD_iV*`は一意である。

しかしfull output algebraでは

\[
V^*CV=0
\]

を満たすoff-support operatorを自由に加えられる。Hermitian real dimensionで、そのkernelは

\[
(125\times6)^2-125^2=546875
\]

である。CTP doubling後は

\[
(2\times125\times6)^2-(2\times125)^2=2187500.
\]

BGCE321がzeroにしたのはsource-generated four-score span内のmetric contact kernelであり、このoff-support collision contact kernelではない。二つを混同してはいけない。

## 5. なぜまだphysical stress / Ward完成ではないのか

今回の`I_i`は、source-derived defectの一意なsupport liftである。さらにBGCE321によりmetric-response typingを持つ。しかしphysical variational stressと呼ぶには、collision dynamics自身のmetric deformation

\[
F\longmapsto V(F)
\]

またはunitary dilation `U(F)`がsourceから固定され、その微分が`I_i`を返す必要がある。現在はその矢印がない。

またinteraction operatorはsystemにも作用するので、fresh environment chargeのように各blockへそのまま加算してtelescopingできない。後続collisionによるdressingを含むlocal continuity equationが必要である。

BGCE299の

\[
\nabla^\mu T_{\mu\nu}=0
\]

はdeclared long-wavelength, local, second-order, formally self-adjoint, conservative class内で独立に維持される。しかし今回のfinite collision interactionがそのcontinuum tensorへ収束する同一性は未証明である。

## Counter-intuition scan

通常の説明：任意のisometryは入力observableをそのrangeへ一意に輸送できる。従ってsupport balanceだけならBraid固有の現象ではない。

Braid固有の部分：actual sourceが同時に、six-state collision `V`、時間environment charge、nonzero空間defect`24,14,14`、1＋3 source directions、rank-ten BKM/CTP metric typingを与えている点である。

最強の反論：`VD_iV*`をmetric-dependent collision variationなしに「物理stress」と呼べば、一般isometry lemmaの改名になる。

この反論を採用し、今回の昇格は`exact finite interaction-balance candidate with metric typing`までに止める。

## 次の最短路

`BGCE323_SOURCE_SELECTED_COLLISION_METRIC_DEFORMATION_TO_DYNAMICAL_INFLUENCE_AND_REPEATED_TOTAL_WARD_GATE`。

問うのは一つだけである。BGCE319 time reversalとBGCE321 BKM scoreが、係数なしに`V(F)`または`U(F)`の微分を固定し、そのvariationが`I_i`を返してrepeated collision上でlocalにtelescopingするか。

## Claim ceiling

BGCE322はactual finite Braid collisionのphysical support上で、時間environment chargeと空間interaction-balance representativesからexactな一回collisionの4成分total operator balanceを導出し、rank-ten BKM/CTP operatorをcollision support上のlocal doubled cumulantへ輸送する。physical variational interaction stress、metric-dependent collision dynamics、standard causal influence action、repeated local Ward、BGCE299 continuum tensorとの同一性、collision parentからのcontinuum total Ward、full finite Lorentzian Einstein backreaction、経験的重力、完成量子重力は未導出である。
