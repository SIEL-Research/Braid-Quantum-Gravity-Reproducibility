# Verification scope for release v0.99

## Executable now

The source verifier checks all eight declared sectors and requires, without
floating-point tolerances:

1. orthogonality and involution of each crossing operator;
2. the Yang--Baxter identity on the full `5^3` basis;
3. preservation of the distinguished point;
4. the endpoint involution and cup/cap relation;
5. the source-Hamiltonian minimal polynomial;
6. the exact Brauer-projector identities;
7. the marker characteristic polynomial;
8. all eight distinct three-character labels.

The command exits nonzero if any equality fails or if the reconstructed result
differs from `expected/source_verification_v099.json`.

## Not executable yet

The current release does not yet provide public runners for the full chain from
the four-direction carrier through continuum gravity, ADM/HDA--BFV closure,
finite quantum BV, strong-curvature black-bounce results, calibration, or the
separate registered CKM confirmation. Their presence in the manuscript does
not make them reproduced by this repository.

Each future addition must declare its finite or analytic domain, input
identity, decision rule, expected output, test command and claim ceiling.
