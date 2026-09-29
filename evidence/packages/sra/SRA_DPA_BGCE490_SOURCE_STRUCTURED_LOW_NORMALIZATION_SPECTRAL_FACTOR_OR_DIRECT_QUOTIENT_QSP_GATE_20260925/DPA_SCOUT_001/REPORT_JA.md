# BGCE490 結果

## 判定

**CLOSED_SCOPED。** BGCE488のLagrange積LCUをそのまま増幅せず、source-compatibleなChebyshev walkへ基底変換することで、全8 signed sector × 4 controlの32件においてlow-normalization exact actuatorを構成した。BGCE489のexact phase matchingと組み合わせると、成功率1の有限決定論的回路になる。

## 大胆な仮説

`A=H/alpha`、`D=sqrt(I-A^2)`としてBGCE478のcanonical Halmos block encodingを

\[
BE(H)=\begin{pmatrix}A&D\\D&-A\end{pmatrix}
\]

とする。`Z=diag(I,-I)`、`R=Z BE(H)`なら、`A`と`D`は同じfunctional calculusに属して可換なので

\[
\langle0|R^k|0\rangle=T_k(A)
\]

がexactに成り立つ。したがって、BGCE476の有限スペクトルtargetを

\[
P_H(x)=\sum_{k=0}^{m-1}c_kT_k(x),\qquad
P_H(\lambda_j/\alpha)=e^{-i\pi\lambda_j/3}
\]

と一意に変換し、有限power `R^k`をLCUで選べばよい。係数`c_k`はsource spectrumと`pi/3`から一意に定まり、データfitでも手動位相調整でもない。

## 結果

- 全32件PASS
- distinct spectral nodes: `15–32`
- Chebyshev coefficient one-norm `log10(s_C)`: `0.5304–3.2497`
- 増幅前成功確率: 約`10^-1.0609`から`10^-6.4994`
- BGCE488比の改善: `39.40–87.10`桁
- exact phase-matched base calls: `7–2,793`
- 総`H` block-encoding query: `203–39,102`
- 70桁interpolation residual最大: `3.1251574e-69`
- 70桁walk identity residual最大: `1.8111358e-70`

## BGCE489との関係

BGCE489のNO-GOは正しい。旧Lagrange actuatorをblack boxとして増幅する限り、巨大normalization `s`に比例するquery下限がある。BGCE490はそのblack boxを増幅せず、先にsource-compatibleなChebyshev基底へ変換してnormalizationそのものを下げる。したがってNO-GOを取り消すのではなく、その適用範囲の外側へ出た。

## 4確率の役割

4確率のsource-`V4` `1+3`構造は、引き続き`G1,H1,H2,H3`を選ぶouter selectorである。Chebyshev compilerは選択後のbranch内部だけに作用するため、BGCE486で失敗したraw V4 reflectionのsystem-side圧縮を必要としない。

## 境界

この閉鎖はBGCE478のtyped canonical Halmos block encoding、BGCE484のtyped coherent finite-list routing、BGCE487のcontinuous source clockと有限compositionを使う。square-root defectとcontrolled walk powersをbare adjacent-Braid wordsから局所実装すること、hardware error、秒較正、continuum/QFT、実証は未解決。

次は`BGCE491_TYPED_HALMOS_CHEBYSHEV_WALK_TO_SOURCE_WORD_LOCAL_COMPILATION_GATE`でtyped Halmos walkをsource-word local circuitへ下ろせるか判定する。
