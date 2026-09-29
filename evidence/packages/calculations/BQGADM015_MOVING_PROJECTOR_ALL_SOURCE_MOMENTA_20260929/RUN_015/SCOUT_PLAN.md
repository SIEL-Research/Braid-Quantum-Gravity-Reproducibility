# PUBLIC-RUN-BQGADM-015 — moving physical projector and all source momenta

## Parent question

Can BQGADM-014's flat three-axis physical projector be extended in one
source-derived construction to every nonzero finite `C5^3` momentum direction
and to a smoothly time-dependent projector on the curved local regular
BQGADM-012 perfect-history branch, without importing an Einstein/Fierz-Pauli
target, a manual gauge, a fitted coefficient or a new action?

## Pinned source

- Repository: `SIEL-Research/Braid-Quantum-Gravity-Reproducibility`
- Commit: `4d7b0c1a0cb40200c5fe3a64abadc45063ecb9ef`
- public calculation snapshot: `PUBLIC-SNAPSHOT-4d7b0c1a0cb4`
- Reservoir SHA-256:
  `41b861de1475fa977265079e10bccbae3069815a21281a8ca16967f784adaf91`

All scientific inputs are read with `git show` from the pinned commit and
hash-checked before endpoint access.

## Bold hypothesis

The three BQGADM-006 axis symbols are the restrictions of one unique
source-coframe-equivariant symbol: one scalar row quadratic in a nonzero source
momentum and three vector rows linear in it. This exact completion defines a
rank-four first-class symbol on all 124 nonzero `C5^3` directions. Its
transverse-tracefree phase projector is the flat member of a general moving
coisotropic projector.

On the curved regular branch, let `A_z=dC_z` be the four-row constraint
Jacobian, `Omega_z` the Palatini symplectic form, `G_z` the positive spatial
coframe metric on phase variations and `R_z=Omega_z^-1 A_z^T` the Hamiltonian
gauge distribution. Define

```text
H_z = [ A_z ; R_z^T G_z ]
P_z = I - G_z^-1 H_z^T (H_z G_z^-1 H_z^T)^-1 H_z .
```

The hypothesis is that `P_z` is the unique source-metric-orthogonal projector
onto the physical tangent slice. It moves smoothly with the evolving metric,
lands in the constraint tangent space, kills gauge directions, has rank four,
is symplectic on its image and is natural under the exact perfect-history
refinement maps.

No new axiom is introduced. The construction uses only the regular rank-four
coisotropic hypotheses and source objects already asserted by BQGADM-012 plus
the source spatial coframe metric used by BQGADM-014.

## Strongest ordinary alternative

The arbitrary-momentum formula could be an imported continuum TT ansatz whose
cross terms are not fixed by the three source axes. Even if the flat formula
works, a `G`-orthogonal horizontal slice on a curved constraint manifold could
fail to be symplectic, fail refinement naturality, or become singular as the
metric evolves. A coordinate-transformed flat witness is not by itself a
curvature theorem; the moving result must follow from the regular coisotropic
algebra and state its rank-loss boundary explicitly.

## Noncompensating endpoints

### All nonzero finite source momenta

1. the unique rotation-equivariant scalar/vector completion exactly reproduces
   all three pinned BQGADM-006 axis symbols;
2. every one of the 124 nonzero digit directions in `{-2,-1,0,1,2}^3` has
   constraint rank four and zero first-class bracket;
3. the corresponding TT configuration projector is idempotent rank two;
4. its phase lift is idempotent rank four, lands in the constraint surface,
   kills the Hamiltonian gauge image and has symplectic rank four;
5. the constraint surface splits as gauge four plus physical four for all 124
   directions.

### Nonlinear moving projector theorem

6. under `rank(A_z)=4`, nondegenerate `Omega_z`, positive `G_z` and
   `A_z Omega_z^-1 A_z^T=0`, the displayed `H_z` has rank eight and its Gram
   matrix is invertible;
7. `P_z^2=P_z`, `A_z P_z=0`, `P_z R_z=0`, `rank(P_z)=4` and `P_z` is
   `G_z`-self-adjoint;
8. the image of `P_z` is a symplectic complement to gauge inside the constraint
   tangent space;
9. the rational flat members equal the all-momentum TT projectors rather than
   merely having the same rank;
10. exact simultaneous pullback/intertwining of `A`, `Omega` and `G` implies
    exact refinement naturality of `P`;
11. deterministic exact rational moving-frame witnesses preserve every
    identity and reproduce the conjugated projector without tuning.

## Falsifier and stopping rule

Any failed noncompensating endpoint gives `NO-GO` for the unified extension.
Do not repair failure by changing the target, dropping a momentum direction,
adding damping, fitting a phase/coefficient, inserting a new action or calling
dimension equality a projector. Stop at the first rank-loss or Gram
singularity boundary.

## Deterministic evaluator

```text
python3 records/BQGADM015_MOVING_PROJECTOR_ALL_SOURCE_MOMENTA_20260929/RUN_015/evaluate_moving_projector.py
```

Retain every exact direction record, the frozen cross-term completion,
moving-frame witnesses, all endpoint booleans, evaluator hash, environment,
machine-readable result and attempt history.

## Claim ceiling

At most an exact all-124-nonzero-source-momentum flat projector theorem and a
local regular nonlinear moving coisotropic-projector existence/naturality
theorem on the BQGADM-012 perfect-history branch. The zero momentum, rank-loss,
caustic/singular, global-topology and strong-curvature sectors remain outside
scope. No ultralocal position-space projector, global existence, empirical
gravity, confirmation, RPD adoption, Level 3 or Official SIEL statement.
