# BGCE444監査 — 10 metric sourceから35 quartic係数への二次応答

## 結論

**SCOPED PASS / OPEN。**

BGCE290/BGCE291のrank-ten source solderを二次化し、total symmetrizationを
合成すると、全8 sectorで

\[
D^2Q_\chi:\operatorname{Sym}^2(A_{10})\longrightarrow
\operatorname{Sym}^4(V_4^*)
\]

はexact rank `35`になる。domainは`55`次元、kernelは`20`次元であり、
`Schur-(2,2)` complementとして削除せず保持される。従って、Braidの10個の
metric sourceは係数fitなしに35個のquartic成分を担える。10→35の**代数的容量橋**は
閉じた。

一方、現在のUB612 packetには実際の`U4` 35係数と`p1,p2,p3,H`の4方向一次微分しか
なく、10 sourceの55組に対する二次応答は保存されていない。従って、実際のPBM
quartic係数をBraid sourceから**予測生成した**とはまだ言えない。既知の`U4`を先に読み、
rank-35 mapの右逆でsource側へ戻すだけならreconstructionであり、生成証明ではない。

## Exact theorem

各sector `chi`で、BGCE288/BGCE290が与える

\[
S_\chi:A_{10}\to\operatorname{Sym}^2(V_4^*)
\]

はrank 10なので同型である。source由来の二次応答を

\[
Q_\chi(a)=\operatorname{Sym}_4(S_\chi(a)\otimes S_\chi(a))
\]

と置く。この定義に外部係数はない。二次微分は

\[
D^2Q_\chi(u,v)=2\operatorname{Sym}_4(S_\chi(u)\otimes S_\chi(v)).
\]

標数0では

\[
\operatorname{Sym}^2(\operatorname{Sym}^2 V_4^*)
\cong \operatorname{Sym}^4V_4^*\oplus\mathbb S_{(2,2)}V_4^*,
\]

次元は`55=35+20`である。total symmetrizationは第一成分へ全射であり、
`Sym2(S_chi)`は可逆なので、合成のrankは全sectorで35、kernelは20である。

## 全8 sector最小検査

- masks：`0, 5, 8, 13, 16, 21, 24, 29`
- BGCE288 combined source rank：各sector `10`
- BGCE290 source-fixed Hadamard solder rank：`10`
- 二次応答rank：各sector `35`
- kernel dimension：各sector `20`

rankはsectorごとの55列総当たりではなく、「rank-ten solderの可逆性」と普遍的な
plethysm分解から決まる。proof checkerは有理数行列で代表sectorを再計算し、8 sectorの
rank-ten前提をcommit-pinned recordから検査した。

## UB612との照合

- actual `U4` coefficient count：`35`
- 保存された微分方向：`p1,p2,p3,H`の`4`
- 必要な10-source pair方向：`55`
- actual ten-source Hessian：**未収録**

したがって現packetから物理bridgeをPASSにすることはできない。これはrank失敗ではなく、
必要な型のresponse packetがまだ存在しないというdata/type gapである。

## Counter-intuition scan

最も強い反論は、rank 35なら既知のquartic targetを必ず逆像へ持ち上げられるため、
surjectivityだけでは予測性がないことである。この反論は正しい。今回PASSしたのは
capacityとnaturalityであり、actual coefficient generationではない。

## 次のgate

`BGCE445_ACTUAL_UB612_TEN_SOURCE_SECOND_VARIATION_AND_REFINEMENT_NATURALITY_GATE`

同じsource-fixed 10 directionsでPBM `U4`の二次変分55列をtarget blindに構成し、
rank 35、20-dimensional kernel、全8 sectorおよびrefinement naturalityを検査する。

## Claim ceiling

本結果は有限次元のsource-fixed algebraic second-response carrierに限る。実際のUB612
`U4`生成、all-scale convergence、renormalization theorem、UV finiteness、完成量子重力、
自然界の重力、RPD採用、Official SIEL採用を導出しない。

MMR/CGR、目標Einstein式、Einstein-Hilbert/Fierz-Pauli作用、手動`3/5`、係数fitは
使用していない。
