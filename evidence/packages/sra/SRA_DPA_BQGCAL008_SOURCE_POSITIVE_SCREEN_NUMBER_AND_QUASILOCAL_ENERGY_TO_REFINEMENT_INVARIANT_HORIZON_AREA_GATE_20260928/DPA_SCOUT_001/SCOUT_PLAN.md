# DPA-SCOUT-BQGCAL-008-X1 plan

## Parent question

Can the pointed six-label source supply the positive additive screen number `K` required by BQGCAL-007 and relate it directly to the conserved linear total Ward energy?

## Pinned source

- Commit: `8dd3bc9a5ce11a2ecc43d471e0f8a501139ac792`
- Snapshot: `DPA-SNAPSHOT-8dd3bc9a5ce1`
- Hash-bound inputs: `INPUT_MANIFEST.json`

## Hypothesis and ordinary alternative

Use `N_1=I-|e><e|` and `N_n=sum_k N_1^(k)` as a source-pointed positive integer count. The ordinary alternative is that this is only a stochastic record count with no conserved-energy or area meaning.

## Exact endpoints

1. Prove positivity, projection property, integer spectrum and additivity of `N_n`.
2. Compute its exact mean and variance under the fixed source ancilla probabilities.
3. Compute the exact commutator with `H_E`.
4. Test the unconditional and identity/nonidentity-conditional first moments of `H_E`.
5. Accept direct `K=N_n` only if the count is energy compatible without a fitted coefficient.

Stop after the direct linear-energy test. No target data, scan or long computation.

## Command

`python3 -B evaluate_scout.py`

## Claim ceiling

Positive source count construction and direct linear-energy compatibility only.
