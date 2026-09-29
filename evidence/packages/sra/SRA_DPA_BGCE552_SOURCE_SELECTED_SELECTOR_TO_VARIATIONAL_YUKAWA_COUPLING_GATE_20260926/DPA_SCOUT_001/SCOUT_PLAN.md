# DPA-SCOUT-BGCE552-001 plan

- **Parent question:** `BQG-G3-R03.7` — is the BGCE546 selector only an interpretive flavour matrix, or is it the coefficient obtained by varying a source-native finite matter action?
- **North-star claim:** the pointed-right KMS response is the unique coefficient-free first-order variation of the already typed BGCE439 Yukawa trilinear in the declared source-response class, and its CTP adjoint pair reproduces the BGCE532 finite determinant.
- **Closest prior result:** BGCE439 fixes three gauge-neutral Yukawa interaction types; BGCE532 fixes ordinary exterior trace, forward/reverse adjoint pairing and `det(I+M_H^*M_H)`; BGCE546 fixes the pointed-right KMS selector `Y` but leaves its physical-Yukawa identification interpretive.
- **Current missing link:** no retained theorem identifies `Y` as an actual action variation and verifies that the same varied coupling enters the already derived determinant.
- **Directness:** `direct`.
- **Scientific layer:** finite source-derived variational matter action.
- **Evidence class:** `Theoretical derivation` if all exact tests pass.

## Frozen hypothesis and alternatives

Let `C` be the pinned KMS correlation, `0` the pointed vertex, `e_i` its three intrinsic neighbours and `B_ij=L_i^*L_j` the BGCE544 generation basis. Define the coefficient-free diagonal source interpolation

`W(t)=sum_ij [(1-t) C(e_i,0)+t C(e_i,e_j)] B_ij`.

The frozen hypothesis is that

`dW/dt = sum_ij [C(e_i,e_j)-C(e_i,0)] B_ij = Y`,

and that inserting this coefficient into the BGCE439 gauge-neutral odd-odd-even trilinear gives a CTP-real action whose Higgs/fermion mixed variation is `Y`, reverse variation is `Y^T`, and neutral quadratic is `Y^T Y` exactly as required by BGCE532.

- **Interpretive leap tested here:** the BGCE546 response coefficient is the physical relative Yukawa coefficient inside the declared first-order pointed-KMS response action class.
- **Strongest ordinary alternative:** one may choose an uncentered correlation, a symmetric Hessian, a nonlinear source functional or an arbitrary overall dimensionful coupling; then BGCE546 does not uniquely fix a physical Yukawa action.
- **Counter-intuition:** a PASS removes the relative selector-to-action bridge only in the frozen class. It does not derive an SI mass scale, empirical masses, neutrinos, running or unrestricted uniqueness among all possible source functionals.

## Prospective decision rule

`SCOPED_PASS` requires all of the following:

1. all pinned inputs reproduce byte-for-byte from the source commit;
2. the exact finite variation `W(1)-W(0)` equals the retained BGCE546 `Y`;
3. among affine first-order maps `a C(e_i,e_j)+b C(e_i,0)`, baseline annihilation and unit lattice-response normalization have the unique solution `(a,b)=(1,-1)`;
4. the BGCE439 trilinear is parity even and gauge neutral, and the CTP reverse coefficient is exactly `Y^T`;
5. the mixed Higgs variation of `M_H^*M_H` equals the retained `Y^T Y`;
6. `det(I+xY^TY)` has the exact positive coefficient polynomial dictated by the same mass operator;
7. the uncentered and symmetric controls do not silently reproduce the same oriented variational claim.

The hypothesis is falsified if any equality fails or a fitted coefficient is required. Stop after this exact action-variation and determinant-consistency gate. Do not fit observed masses and do not scan alternative nonlinear functionals.

## Claim ceiling

At most this scout can remove the physical-Yukawa identification boundary for the relative generation selector within the BGCE439/BGCE532/BGCE544 declared pointed first-order KMS response-action class. It cannot establish uniqueness among all source functionals, an absolute Yukawa scale, observed-generation matching, neutrino content, RG running, CKM/PMNS, CP violation, empirical Standard-Model confirmation or completed quantum gravity.
