# Iteration ledger

## Attempt 001 — COMPLETE

- The plan, endpoints, falsifier, source matrix and claim ceiling were frozen
  before execution.
- Command: `python3 audits/SRA_DPA_BQGADM015_MOVING_PROJECTOR_ALL_SOURCE_MOMENTA_20260929/DPA_SCOUT_015/evaluate_moving_projector.py`
- The pinned three-axis constraint symbols and BQGADM-014 projectors were first
  reproduced exactly.
- All noncompensating gates passed on all 124 nonzero `C5^3` momenta.
- Five exact rational moving-frame witnesses passed every moving-projector
  identity.
- `RAW_OUTPUT.json` SHA-256:
  `760dc37b191c0199d01be8fbcdb2a1dc16b34f9d6748c5fce361ab5d5964fded`
- `RESULT.json` SHA-256:
  `045bef41d3731ee7fa79d3f9d1eda3eb03e4f18fb7c95f4cb0a37d3b2f2f612e`
- Evaluator SHA-256:
  `73cd38c28ea87aca957e383629fb54d2a4c2cdd2e806b94f0e4a9c12a1009a59`
- A second execution reproduced both result hashes byte-for-byte.
- No outcome-aware repair or endpoint change occurred.
