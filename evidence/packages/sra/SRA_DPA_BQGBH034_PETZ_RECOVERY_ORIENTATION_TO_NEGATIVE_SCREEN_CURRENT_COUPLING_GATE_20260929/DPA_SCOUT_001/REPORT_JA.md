# BQGBH-034 報告

## 結論

**SCOPED NO-GO。**

現行のPetz/KMS随伴、source-canonical time reversal、reflected in/out
orientationのどれも、BGCE348のbranch pairから

\[
\dot F_{\rm Petz}-\dot F_{\rm raw}=-D
\]

をphysical radial backreactionとして一意に選ばない。prior付きinstrument
の一次変分はzeroのままである。

これはregular black-bounceそのもののNO-GOではない。BQGBH-033で導出した
source currentの形と大きさ、BQGBH-032のconditional stationary solutionは
維持される。閉じなかったのは、可逆なbranch pairだけから負のreaction
arrowを選ぶ経路である。

## 1. 完全符号表

BGCE348の固定結果は

\[
\dot F_{\rm raw}=+\frac12D,
\qquad
\dot F_{\rm Petz}=-\frac12D.
\]

従って

| readout | coefficient |
|---|---:|
| raw | `+1/2` |
| Petz | `-1/2` |
| raw minus Petz | `+1` |
| Petz minus raw | `-1` |
| prior average | `0` |

必要な`-1`は候補として存在する。しかし存在と選択は別である。

## 2. Petz/KMS随伴は負のreaction arrowではない

BGCE341のPetz mapはfaithful stateに対するKMS adjoint

\[
\Phi_\rho^\sharp(A)
=\rho^{-1/2}\Phi_*(\rho^{1/2}A\rho^{1/2})\rho^{-1/2}
\]

として固定される。これはraw mapのcanonical partnerを与えるが、
`Phi_sharp-Phi`をradial reactionにするという作用lawは与えない。

さらにbaseから離れると、このraw Petz familyは追加normalizationなしには
unital CPTP/GKSL familyではない。従ってPetz branchだけをphysical evolution
として採用して負符号を得ることも、現行結果からはできない。

## 3. source時間反転はrecordを向き付けない

BGCE319の

\[
\Theta=VK
\]

はsource Reynolds channelとcanonical stateを保存し、modular parameterを
反転する。しかし`Theta`-odd carrierからphysical difference metricへのtyped
mapはない。従って`Theta`はraw/Petz ordered differenceのphysical signを
選ばない。

## 4. in/out反射とraw/Petzは別のZ2

BGCE349は次の二つを明示的に分離している。

- CTP/in-out contour：physical processのforward/backward doubling。
- raw/Petz：各contour copy内部のKMS instrument record。

従ってBQGBH-003のreflected walk orientationを、そのままraw/Petz orderingへ
移すのはtype errorである。

## 5. prior平均とfeedback

base pointではraw/Petz priorは`(1/2,1/2)`、branch effectsはともにidentity、
conditional state mapsも一致する。よってprior付き一次応答は

\[
\frac12\left(+\frac12D\right)
+\frac12\left(-\frac12D\right)=0.
\]

BGCE357/361も、このrecordだけではunique feedback lawを選べないことを既に
示している。

## 6. 判定

- `Petz-minus-raw=-D`の代数的存在：**PASS**。
- Petz/KMS随伴によるphysical ordering：**NO-GO current grammar**。
- `Theta`によるordering：**NO-GO current grammar**。
- in/out反射によるordering：**NO-GO、別Z2**。
- prior付きnegative response：**NO-GO、exact zero**。
- coefficient fit / parameter scan / target Einstein equation：**不使用**。

## 7. counter-intuition

“recovery”という名前は時間的な復元方向を連想させる。しかし現行の有限式が
与えるのはstate-relative adjointである。adjoint pairは両符号を含むが、
どちらがgeometryへ反作用するかを決めない。

## 8. 次

`BQGBH-035_SOURCE_RELATIVE_ENTROPY_PRODUCTION_TO_NEGATIVE_PALATINI_GRADIENT_GATE`

可逆なbranch labelを反転するのではなく、source由来のrelative entropy、
Dirichlet formまたはLyapunov functionalがscreen currentを負勾配
`-Q`として強制するかを判定する。

## Evidence status / claim ceiling

一次区分は **Theoretical derivation / route-specific scoped NO-GO**。

除外したのはexisting Petz/KMS・time reversal・in/out構造だけからsignを選ぶ
経路である。unconditional interaction action、collapse、evaporation、
thermodynamics、自然界のblack hole、経験的確認は未導出である。
