# BQG v1.2 reproduction supplement

This self-contained directory accompanies *Subjectivity-Intersection Braid Quantum Gravity*, version 1.2. It is located at `reproduction/v1.2/` in the paper's public reproduction repository. The original repository inventory is pinned to [6d68794](https://github.com/SIEL-Research/Braid-Quantum-Gravity-Reproducibility/tree/6d68794cbc075d24415d0a02f8a9974803f91616) and documents the v1.0 executable release.

Open [the theorem and equation index](THEOREM_EVIDENCE_INDEX_v1.2.md) for the three new statements. For the exact computations, run from this directory with Python 3 and its standard library.

```sh
python3 verify_pointing.py
python3 verify_hda_example.py
```

The two outputs can be compared with [expected_pointing.json](expected_pointing.json) and [expected_hda_example.json](expected_hda_example.json). The HDA script evaluates the nonzero shift example following (S7). For the general smooth HDA identities, use the derivation in §11A. For the local perturbative QME, follow [the analytic proof route](QME_PROOF_ROUTE.md).

The signed permutation and row signs in [crossings.json](crossings.json) agree with Eq. (55) and were taken from the [canonical source input at the pinned public revision](https://github.com/SIEL-Research/Braid-Quantum-Gravity-Reproducibility/blob/6d68794cbc075d24415d0a02f8a9974803f91616/data/canonical_source_class_v1.json). The replay recovers the point without taking a point as input.

The original finite-to-smooth correspondence, finite HDA, and finite BV QME for the Braid-selected measure are open. The supplement covers the three new statements in v1.2. Numerically unspecified quantum counterterms and phenomenological interpretations belong to separate questions.
