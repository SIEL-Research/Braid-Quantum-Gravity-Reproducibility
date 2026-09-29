# PUBLIC-RUN-BGCE458-001 iteration ledger

## Attempt 0001

- State: `FROZEN_NOT_EXECUTED`
- Source commit: `abd5261df92d1639c4a16d6e2309b542d176fe14`
- Allowed computation: one exact 125-history replay plus identity, ordinary-flip, and fixed Yang-Baxter-broken controls
- Outcome-aware repair: none
- Raw output: not yet created
- Scientific decision: not yet made

### Attempt 0001 execution

- State: `IMPLEMENTATION_PROVENANCE_FAILURE`
- Outcome accessed: `false`
- Failure: frozen evaluator resolved the repository root one directory above the worktree and stopped with `FileNotFoundError` before source access.
- Scientific decision: none
- Containment: retain the failed evaluator unchanged and freeze a path-only Attempt 0002 wrapper.

## Attempt 0002

- State: `FROZEN_NOT_EXECUTED`
- Scientific code: frozen Attempt 0001 evaluator, unchanged
- Permitted change: repo-root and source-path resolution only
- Endpoint, controls, thresholds, source rows, and claim ceiling: unchanged
- Freeze: `SCOUT_FREEZE_R2.json`

### Attempt 0002 execution

- State: `IMPLEMENTATION_PROVENANCE_FAILURE`
- Failure: ordinary flip has 40 three-cycles and exact `P` rank `80`; the frozen assertion incorrectly expected `120`.
- Outcome accessed: only the failing comparator expectation; no complete raw output
- Scientific decision: none
- Containment: retain Attempt 0002 unchanged and freeze an Attempt 0003 runner with the analytic comparator correction only.

## Attempt 0003

- State: `FROZEN_NOT_EXECUTED`
- Focal source endpoint and expected actual-source values: unchanged
- Result-informed change: ordinary-flip comparator expected rank corrected from `120` to `80`
- Claim ceiling: unchanged
- Freeze: `SCOUT_FREEZE_R3.json`

### Attempt 0003 execution

- State: `COMPLETE`
- Executed once after freeze
- Raw SHA-256: `0db4d8cb8cb92cc5defadda23b84a1e1f59c5b66cdf1b8c971e57e60103a5c5a`
- Decision: `SCOPED PASS / BQG-G0-R01.1 CLOSED_SCOPED`
- Actual reconstructed complex dimension: `36`
- Identity / ordinary-flip complex dimensions: `0 / 40`
- Born rule: `OPEN`
- Pointed-Braid specificity: `NOT_ESTABLISHED`
