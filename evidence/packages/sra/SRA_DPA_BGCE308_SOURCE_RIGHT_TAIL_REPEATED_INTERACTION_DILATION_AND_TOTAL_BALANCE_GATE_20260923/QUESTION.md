# BGCE308 preregistered question

## Decision question

Does the already source-native right-tail refinement supply, without an
external bath, the fresh six-label ancilla chain, state preparation, collision
interaction and balance law required by the BGCE307 dilation?

## Frozen tests

1. Decompose the actual three-strand tail representation under the six Braid
   group elements in all eight source sectors and count regular six-state
   orbits.
2. Restrict the source pointed/cap state and its Reynolds neutralization to
   every regular orbit; test whether they select the identity group label and
   the nonuniform `q=1/4` weights `(3/8,1/8,...,1/8)`.
3. Check whether the existing right-tail extension actually couples the marked
   system to successive fresh blocks or only tensors the generator with the
   identity.
4. Keep Hilbert-space capacity, state selection, interaction selection and
   total stress balance as separate requirements.

## Decision rule

- **Full pass:** the frozen source selects the register, preparation,
  sequential interaction and conserved total balance.
- **Split pass:** the tail contains sufficient native register capacity, but
  one or more dynamical selections remain absent.
- **Fail:** the tail contains no native six-state Braid register at all.

## Runtime

Short exact orbit and integer block calculations; no parameter scan.

