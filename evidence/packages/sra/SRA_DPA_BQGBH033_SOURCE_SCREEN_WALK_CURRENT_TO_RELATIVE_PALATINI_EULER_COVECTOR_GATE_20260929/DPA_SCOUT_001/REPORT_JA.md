# BQGBH-033 報告

## 結論

**SPLIT SCOPED PASS / SCOPED NO-GO。**

actual reflected active-screen walkから、BQGBH-032のinteractionに必要な有限Euler currentの**形と大きさ**をexactに導出した。これはtarget Einstein tensorや必要stressからの逆算ではない。

一方、既存raw/Petz記録は、必要な負符号`Petz-minus-raw`を数学的には含むが、それをphysical radial backreactionとして一意に選んでいない。prior-summed instrumentの一次変分はzeroである。従って残る未導出は符号選択lawである。

## 1. source screen current

sourceは

\[
\rho=\ell_*\sqrt J,
\qquad
X=\ell_*\Sigma\sqrt{J-I}
\]

を持つ。signed chainの各oriented edgeに

\[
j_e={\Delta\rho_e\over\Delta X_e}
\]

を置く。これはBQGBH-003のin/out unitary walkに沿うscreen-radius coboundaryを、source edge lengthで規格化したものである。

internal nodeでのdivergenceは

\[
Q_k=j_{k-1/2}-j_{k+1/2}.
\]

## 2. Palatini Eulerとのexact一致

BQGBH-031のpure radial Euler covectorを`R=rho`で評価すると

\[
{\Delta\rho_{k-1/2}\over h_{k-1/2}}
-{\Delta\rho_{k+1/2}\over h_{k+1/2}}
\]

である。これは上の`Q_k`そのものである。left/right slopeに対する係数は両方ともexactに

\[
(+1,-1)
\]

で、mesh uniformityを仮定しない。

従ってinteractionが必要とするcovectorは

\[
-Q_k
\]

であり、その係数は`(-1,+1)`とsource currentから固定される。

## 3. throat witness

throat tripletでは

\[
j_-=1-\sqrt2,
\qquad
j_+=\sqrt2-1.
\]

従って

\[
Q_0=2-2\sqrt2,
\qquad
-Q_0=2\sqrt2-2.
\]

これはBQGBH-032のinteraction variationとexact一致し、total residualはzeroになる。

## 4. raw/Petz sign audit

BGCE348のsource-fixed branch tangentは

\[
\dot F_{\rm raw}=+{D\over2},
\qquad
\dot F_{\rm Petz}=-{D\over2}.
\]

従って利用可能な組合せは次である。

- raw：`+D/2`
- Petz：`-D/2`
- raw-minus-Petz：`+D`
- Petz-minus-raw：`-D`
- prior平均：`0`

必要なunit negative currentは`Petz-minus-raw`としてexactに存在する。しかしBGCE348が物理metric contrastとして固定した順序はraw-minus-Petzであり、既存記録は逆順をphysical radial reactionとして選んでいない。

「必要な符号が候補の中にある」ことと「sourceがその符号を選んだ」ことは別であるため、ここで無条件導出には昇格しない。

## 5. 判定

- source walkからedge current：**PASS**
- 任意非一様chainでPalatini Euler shapeと一致：**PASS EXACT**
- throat magnitude：**PASS EXACT**
- target stress / Einstein tensor / coefficient fit：**不使用**
- unconditioned raw/Petz stress：**NO-GO、zero**
- negative unit contrastの存在：**PASS、Petz-minus-raw**
- negative contrastのphysical selection：**OPEN**

次は

`BQGBH-034_PETZ_RECOVERY_ORIENTATION_TO_NEGATIVE_SCREEN_CURRENT_COUPLING_GATE`

で、Petz recoveryの向き、source time reversal、in/out reflectionが、negative contrastをbackreaction branchとして一意に選ぶかを判定する。

## Evidence status / claim ceiling

一次区分は **Theoretical derivation / split scoped result**。

source-derived interaction-currentの形と大きさは閉じた。physical sign、unconditional relative action、collapse、evaporation、thermodynamics、自然界のblack hole、経験的確認は未導出である。
