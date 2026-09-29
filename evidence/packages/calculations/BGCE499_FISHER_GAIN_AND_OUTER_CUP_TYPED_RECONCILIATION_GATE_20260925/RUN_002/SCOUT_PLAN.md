# PUBLIC-RUN-BGCE499-002 — repair-only rerun

The parent hypothesis, exact endpoint, falsifier, stopping condition, pinned
commit, input hashes, execution boundary and claim ceiling are unchanged from
`PUBLIC-RUN-BGCE499-001/SCOUT_PLAN.md`.

The only repairs are:

1. repository root: `Path(__file__).resolve().parents[3]`;
2. BGCE371 unit stationary gain: read
   `variational_closure.unique_stationary_translation` and
   `variational_closure.free_actuation_coefficient`.

No result-informed scientific change is permitted.
