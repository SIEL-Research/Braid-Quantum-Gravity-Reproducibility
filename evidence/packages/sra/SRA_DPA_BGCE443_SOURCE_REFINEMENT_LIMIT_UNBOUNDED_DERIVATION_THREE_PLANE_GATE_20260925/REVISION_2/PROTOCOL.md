# BGCE443 Revision 2 prospective protocol

Status: `AWAITING_INDEPENDENT_E0_REVIEW`

Revision 1 is preserved as an `IMPLEMENTATION_PROVENANCE_FAILURE` with no scientific decision. Revision 2 does not reuse its substituted `P_chi` tail-pair endpoint or its outcome.

## Fixed source revision and inputs

Producer revision: `801238084ee43fc58a11fb213cdf9bdb530f103e`

| Input | SHA-256 |
|---|---|
| `outputs/discovery-partner/DPA_BGCE443_REFINEMENT_OUTER_SPACETIME_HYPOTHESIS_20260925_JA.md` | `ab81d9ab78eb49b1a78c0344787c014473844b7575c67905da2bce9cc0e5f3e0` |
| `audits/SRA_DPA_BGCE442_SOURCE_DERIVATION_HH1_OUTER_THREE_PLANE_MOMENT_MAP_GATE_20260924/REVISION_2/RESULT.json` | `642dcc4b9de9518dd4b3ca3273ae38f12a16051148891c7b27b68e7d684420ff` |
| `projects/active/discovery_partner/formal_checks/ocbfh014_source_native_refinement_naturality_certificate_v1.json` | `717c79fddcf2c94ed89a1c7bef19965627cad9b56e9ccd7bb3fbfa86b45f35f9` |
| `projects/active/discovery_partner/formal_checks/ocbfh015_typed_refinement_observation_dinaturality_certificate_v1.json` | `adf4ef56c8f58c38703542fa09cfebac15bb976b5d629b1dcca1c59ece1ea7f4` |
| `audits/SRA_DPA_BGCE386_SOURCE_NULL_TETRAD_INCIDENCE_THREE_SPATIAL_GENERATOR_GATE_20260924/CERTIFICATE.json` | `4ea139eecf025b5afc66896482f8c6272d5601c22f63c687555562108fce2a9c` |
| `audits/SRA_DPA_BGCE386_SOURCE_NULL_TETRAD_INCIDENCE_THREE_SPATIAL_GENERATOR_GATE_20260924/RESULT.json` | `16fc79a1db2637eb70bdf3e535b08c93f426a68d807edadc9a650a8ca8db00e3` |

## Frozen construction

At every actual source sector use the source operators

`h_0=G1`, `h_a=i[G1,P_chi_a]`, `a=1,2,3`.

For every finite order `n>=3`, enumerate every consecutive marked three-strand window in pointed left-to-right order. Transport each seed to window `x` by the OCBFH014/015 word-independent Braid transport `tau_x`. Do not select a subset of positions after outcome access.

Use the three spatial rows of the exact BGCE386 Hadamard selector to assign `s_a(x)` through the stored null-link orientation of each marked window. Coefficients are exactly the stored signs and unit position weights. No `25^r`, fitted scale or post-outcome normalization is permitted.

Define

`P_0^(n)=sum_x tau_x(h_0)`

and

`P_a^(n)=sum_x s_a(x) tau_x(h_a)`.

On the algebraic local core define `delta_mu^(n)(A)=i[P_mu^(n),A]`.

## Frozen primary endpoints

1. **Compatibility:** exact residual `delta_mu^(n+1)j_n(A)-j_n delta_mu^(n)(A)` on the complete frozen local-core basis. PASS requires zero for all four `mu`, all tested adjacent orders and all eight sectors.
2. **Local stabilization:** for every frozen local basis element, the commutator row must become exactly constant once the refinement boundary is outside its support.
3. **Implementer growth:** `||P_a^(n)||` must be proved unbounded independently of endpoint 2. A fitted extrapolation is prohibited.
4. **Spatial rank:** the three stabilized derivation rows must have exact rank three in every actual sector.
5. **Bounded-inner exclusion:** no uniformly bounded compatible implementer family may reproduce all three stabilized rows.
6. **Closability:** prove the stabilized `*-derivations` are restrictions of generators of strongly continuous automorphism groups or supply an equivalent graph-closure proof.

All six are noncompensating. Any failure gives `NO_GO` or `INCONCLUSIVE`, never a rescued PASS.

## Frozen controls

- **identity-tail control:** confirms exact stabilization when only source identity strands are appended;
- **shuffled-sign control:** apply one fixed non-Hadamard permutation of each spatial sign row chosen in the endpoint witness before focal access; it must lose rank three or stabilization for source specificity;
- **matched non-Braid control:** preserve dimension, projector ranks, seed norms and nonzero commutator rank while replacing the actual Braid transport by the frozen coordinate-swap rival from the endpoint witness; it must fail at least one word-independence or compatibility endpoint;
- **single-direction control:** retain only `a=1`; it must have rank exactly one and must not be misreported as a three-plane.

## Stop rule and claim ceiling

No focal evaluator may run until a revision-matched independent E0 record passes the exact endpoint, controls, retention and no-outcome-access audit. DPA cannot issue that E0.

A later PASS may establish only three source-selected compatible closable unbounded derivations on the declared refinement carrier. It cannot by itself establish cotangent moment maps, clock-spatial first-class closure, diffeomorphism gravity, empirical gravity, RPD adoption or Official SIEL adoption.
