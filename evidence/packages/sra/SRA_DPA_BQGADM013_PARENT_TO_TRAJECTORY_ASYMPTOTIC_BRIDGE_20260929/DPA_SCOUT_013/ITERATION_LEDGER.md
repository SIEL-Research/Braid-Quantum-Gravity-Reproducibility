# DPA-SCOUT-BQGADM-013 iteration ledger

## Attempt 001 — frozen exact source audit

- Date: 2026-09-29
- Pinned commit: `b93a2a5dad11476be7e7b0203a8c8c30e0f851db`
- Hypothesis: exact finite parent/flow identity, with asymptotic BKM-local-shadow fallback declared before execution.
- Inputs: `SOURCE_MATRIX.json` only, read through `git show` from the pinned commit.
- Endpoint changes after outcome access: none.
- Decision rule: the literal identity fails on any exact-versus-asymptotic constraint-preservation mismatch; the fallback passes only if all carrier, target, BKM uniqueness, residual and trajectory gates pass.
- Status: `FAILED_IMPLEMENTATION`; `REPO=HERE.parents[3]` selected the parent
  directory above the Git worktree, so the first `git show` could not resolve
  the pinned path. No scientific output was produced or inspected.
- Preserved script:
  `evaluate_bridge_attempt1_FAILED_REPO_ROOT.py.txt`.

## Attempt 002 — repo-root-only correction

- Change from attempt 001: `REPO=HERE.parents[2]`; no source, hypothesis,
  endpoint, gate or decision-rule change.
- Status: `COMPLETE`.
- All fourteen pinned source hashes: `PASS`.
- Scientific decision:
  `SCOPED_PASS_ASYMPTOTIC_ON_SHELL_PARENT_TO_TRAJECTORY_BRIDGE__NO_GO_LITERAL_EXACT_FINITE_FLOW_IDENTITY__OPEN_EXPLICIT_PHYSICAL_PROJECTOR`.
- Evaluator SHA-256:
  `2ebabb8a55f0958f5c251378e9894336e8b891a14f7a237e83e77dc27667ad36`.
