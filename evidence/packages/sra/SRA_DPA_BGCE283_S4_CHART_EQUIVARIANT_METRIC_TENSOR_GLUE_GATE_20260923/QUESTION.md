# BGCE283 — source event atlas上でmetric responseはtensorとしてglueするか

固定source revisionは `d7ea49bec4557b820e0a72d906a6b6c4af31fa34`、固定X21R1 revisionは `269a832e497c901a2b24bb2167ca97b9e6ce2bd1`。結果前に変更しない。

BGCE282は、source-derived operational event cylinderの4 base方向と3 theta方向を結ぶfirst-order metric chain-rule symbolが全8 sectorでrank 12であることを示した。残る問題は、それが一つの固定chart上のmatrix fieldに過ぎないのか、BGCE137の24個のS4 chartをまたいで同じtensor fieldとして貼り合わさるのかである。

BGCE268のsource-fixed Hadamard intertwiner `U` を使い、ray chart permutation `P_pi` をcharacter/carrier basisへ

\[
C_\pi=U P_\pi U^T
\]

で移す。各 `C_pi` はclock characterを固定するsigned monomialであること、projector/label側の作用 `S_pi=(C_pi)^{\circ2}` がclockを固定し3 spatial labelを並べ替えることをexactに判定する。

metricとtheta tangentのoverlap lawは

\[
G_m^{(\pi)}=C_\pi^T G_m C_\pi,
\qquad
D_{m,j}^{(\pi)}=C_\pi^T\left(\sum_iD_{m,i}(S_\pi)_{ij}\right)C_\pi.
\]

ray basisでは同じ式が `g_m^(pi)=P_pi^T g_m P_pi` になる必要がある。BGCE280の `A=0` とchart transitionの定数性から、overlap上でも `A^(pi)=0`、従って `N^(pi)=D^(pi)` でなければならない。

**FULL PASS条件**：

1. 24/24の `C_pi` がexact signed monomial、clock-fixed、orthogonal。
2. carrier imageが6個、kernelが4個で、24 chartsのlabel actionがsource spatial S3へ閉じる。
3. `C` と `S` が全576 chart pairでcocycle/homomorphismを満たす。
4. 8 sector × 24 charts = 192 metric packetsでcharacter/ray covarianceがexact。
5. 8 × 24 × 3 = 576 tangent/nonmetricity packetsがexact symmetric rank 2で、ray covarianceと二重overlap compositionがexact。

**PARTIAL条件**：metricはglueするがtheta tangent/nonmetricity subbundleが閉じない、または一部sectorだけ閉じる。

**FAIL条件**：Hadamard transportがS4 chart actionをcarrier representationへ移さない、cocycleが破れる、またはmetric/tangent overlap lawが破れる。

**停止条件**：保存済みexact matricesに対する有限群演算だけを一回行う。係数、basis、chart、sectorを探索しない。長時間計算を使わない。

**境界**：FULL PASSでも、証明されるのはsource-derived operational event atlas上のS4-equivariant continuous first-order tensor gluingである。arbitrary smooth diffeomorphism covariance、自然時空との経験的同定/calibration、mu方向のX21R1 metric tangent、Hilbert stress、Ward、Einstein dynamicsは導出しない。
