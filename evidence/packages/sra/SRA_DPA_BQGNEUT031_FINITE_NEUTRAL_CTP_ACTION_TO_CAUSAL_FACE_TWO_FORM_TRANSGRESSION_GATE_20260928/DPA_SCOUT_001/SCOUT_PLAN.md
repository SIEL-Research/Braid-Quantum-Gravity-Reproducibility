# BQGNEUT-031-X1 scout plan

## Parent question

Does the existing finite neutral CTP action itself select the BQGNEUT-030
central causal-face two-holonomy?

## Pinned source

- SRA commit: `e9b56f10b1daad49e7e4910236cd1372a148a71c`
- DPA snapshot: `DPA-SNAPSHOT-e9b56f10b1da`
- Hash-bound inputs: BGCE532, BGCE570 and BQGNEUT-024, 027, 030.

## Bold hypothesis

Read one source transport slot and one weighted neutral interaction slot as the
two oriented edges of a minimal causal CTP plaquette. Dagger reversal fixes the
opposite edges, so its face holonomy is the group commutator

`W_face = C_g E C_g^dagger E^dagger`,

where `E=exp[-i(2*pi/3)L_w]`.

## Minimum decisive test

- Verify the same source operators are noncommuting and produce a nonidentity
  unitary face holonomy.
- Apply the exact determinant identity for a group commutator.
- Decide whether the resulting central `U(1)` flux can equal the lifted neutral
  phase of BQGNEUT-027/030.
- Compare the plaquette eigenphase-gap multiset with the source Floquet gap
  multiset without parameter or branch scans.
- Keep any non-Abelian face-holonomy capacity separate from central-phase
  transgression.

## Claim ceiling

At most a theorem about the minimal rectangular CTP commutator class. Failure
does not exclude a Pfaffian/determinant-line Berry curvature, an open Wilson
surface, or another independently derived transgression mechanism.
