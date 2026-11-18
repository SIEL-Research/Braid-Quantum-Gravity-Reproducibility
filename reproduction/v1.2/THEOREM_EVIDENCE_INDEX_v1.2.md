# BQG v1.2 theorem and evidence index

This index covers the additional statements of version 1.2. The printed formula tags and the stable evidence IDs identify the same results in the paper and in this directory.

| Evidence ID | Paper statement and equations | Supporting material |
| --- | --- | --- |
| V120-THE-01 | Theorem 11A.1, §11A, folios 11a–11b. Common action and reduction (S1)–(S3), generators (S4), DD and DH (S5), HH (S6), field-dependent response (S7). | Analytic derivation in §11A. [Exact rational (S7) example](verify_hda_example.py), [expected values](expected_hda_example.json), and [Teitelboim's primary reference](https://doi.org/10.1016/0003-4916(73)90096-1). |
| V120-THE-02 | Theorem 11A.2, §11A, folio 11c. Same classical action (S1)–(S2), metric BV/CME (S8), Ward correction (S9), formal local QME (S10). | [Analytic proof route and primary references](QME_PROOF_ROUTE.md). |
| V120-LEM-01 | Lemma A.1, folio 21a. Eight crossings (55), recovered projector (P1), interpretation relative to Definition 2.1. | [Exact integer replay](verify_pointing.py), [crossing input](crossings.json), [expected results](expected_pointing.json), and [Conti–Lechner, Theorem 5.8](https://doi.org/10.1112/jlms.12387) for the general background on partial traces. |

The HDA theorem uses smooth, nondegenerate, interior-supported pure gravity on the domain in §11A. The QME uses the same classical reduction followed by the reduced metric perturbative EFT construction. The finite lemma gives the reference line in the specified tensor representation. It leaves selection among the signed sectors open.
